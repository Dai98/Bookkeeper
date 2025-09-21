import re
import os
from pypdf import PdfReader
from datetime import datetime, timedelta


def _parse_chase_bank_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    data = []
    for page in reader.pages:
        page_text = page.extract_text()
        if "TRANSACTION DETAIL" in page_text:
            for line in page_text.split("\n"):
                if re.match(r"^\d{2}/\d{2}\b.*\-.*$", line):
                    delimiter_index = line.rfind("-")
                    amount_balance = line[delimiter_index+2:]
                    date_name = line[:delimiter_index]
                    amount = float(amount_balance.strip().split(" ")[0].replace(",", ""))
                    date = date_name[:5]
                    name = date_name[6:].strip()
                    row = [date, name, amount, "", owner, card_name, "", ""]
                    data.append(row)
    return data


def _parse_chase_freedom_flex_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    data = []
    for page in reader.pages:
        page_text = page.extract_text()
        if "ACCOUNT ACTIVITY" in page_text:
            for line in page_text.split("\n"):
                if re.match(r"^\d{2}/\d{2}", line):
                    date = line[:5]
                    amount_delimiter = line.rfind(" ")
                    amount = line[amount_delimiter+1:]
                    name = line[6:amount_delimiter].strip()
                    row = [date, name, amount, "", owner, card_name, "", ""]
                    if not amount.startswith("-"):
                        data.append(row)
    return data


def _parse_citi_costco_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    data = []
    for page in reader.pages:
        page_text = page.extract_text()
        if "Standard Purchases" in page_text:
            for line in page_text.split("\n"):
                if re.match(r"^\d{2}/\d{2} \d{2}/\d{2}", line):
                    date = line[:5]
                    amount_delimiter = line.rfind(" ")
                    amount = line[amount_delimiter+2:]  # Skip $ character
                    name = line[12:amount_delimiter].strip()
                    row = [date, name, amount, "", owner, card_name, "", ""]
                    data.append(row)
    return data


def _parse_citi_strata_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    data = []
    for page in reader.pages:
        page_text = page.extract_text()
        if "Standard Purchases" in page_text:
            for line in page_text.split("\n"):
                print(f"line =={line}==")
                if re.match(r"^\d{2}/\d{2} \d{2}/\d{2}", line):
                    date = line[:5]
                    amount_delimiter = line.rfind(" ")
                    amount = line[amount_delimiter+2:]  # Skip $ character
                    name = line[12:amount_delimiter].strip()
                    row = [date, name, amount, "", owner, card_name, "", ""]
                    data.append(row)
    return data


def _parse_amex_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    data = []
    statement_text = "".join(page.extract_text() for page in reader.pages)
    lines = statement_text.split("\n")
    record_line = False
    temp_line = []
    for line in lines:
        line = line.strip()
        if "New Charges Details" == line:
            record_line = True
        if "Fees" == line:
            record_line = False
        if record_line:
            if re.match(r"^\d{2}/\d{2}/\d{2}", line):
                date = line[:5]
                name = line[9:]
                temp_line = [date, name]
            if re.match(r"\$\d+\.\d{2}", line):
                amount = re.findall(r"\$\d+\.\d{2}", line)[0][1:]
                temp_line.append(amount)
                temp_line = temp_line + ["", owner, card_name, "", ""]
                data.append(temp_line)
    return data


def _parse_discover_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    """
        Discover's text is embedded in image
    """
    data = []
    return data


def _parse_bilt_statement(reader: PdfReader, owner: str, card_name: str) -> list:
    data = []
    for page in reader.pages:
        page_text = page.extract_text()
        if "Transaction Summary" in page_text:
            for line in page_text.split("\n"):
                if re.match(r"^\d{2}/\d{2}", line) and not line.endswith("-"):
                    tokens = line.split(" ")
                    date = tokens[1]
                    amount = tokens[-1][1:]  # Skip $ character
                    name = " ".join(tokens[4:len(tokens)-2]).strip()
                    row = [date, name, amount, "", owner, card_name, "", ""]
                    data.append(row)
    return data


class StatementParser:
    @staticmethod
    def parse(reader: PdfReader, owner: str, card_name: str) -> list:
        if card_name == "Chase":
            return _parse_chase_bank_statement(reader, owner, card_name)
        elif card_name in ["Chase Freedom Flex", "Chase Ritz Carlton", "Chase Southwest", "Chase Amazon"]:
            return _parse_chase_freedom_flex_statement(reader, owner, card_name)
        elif card_name == "Citi Costco":
            return _parse_citi_costco_statement(reader, owner, card_name)
        elif card_name == "Citi Strata":
            return _parse_citi_strata_statement(reader, owner, card_name)
        elif card_name in ["Amex", "Amex 8000"]:
            return _parse_amex_statement(reader, owner, card_name)
        elif card_name == "Discover":
            return _parse_discover_statement(reader, owner, card_name)
        elif card_name == "Bilt":
            return _parse_bilt_statement(reader, owner, card_name)
        else:
            print(f"{card_name} is not implemented yet")
            return []


class WorkbookGenerator:
    @staticmethod
    def generate(date: str):
        current_month_dir = date.replace("/", "-")
        
        date_obj = datetime.strptime(current_month_dir, "%m-%Y")
        previous_month = date_obj.replace(day=1) - timedelta(days=1)
        prev_month_dir = previous_month.strftime("%m-%Y")

        dir_name = "statements"
        file_paths = [f"{dir_name}/{prev_month_dir}/{filename}" for filename in os.listdir(f"{dir_name}/{prev_month_dir}")] \
            + [f"{dir_name}/{current_month_dir}/{filename}" for filename in os.listdir(f"{dir_name}/{current_month_dir}")]
        workbook = []
        for file_path in file_paths:
            card_name = file_path.split("/")[-1].split("-")[0]
            owner = file_path.split("-")[2][0]
            reader = PdfReader(file_path)
            data = StatementParser.parse(reader, owner, card_name)
            workbook.extend(data)
        workbook.sort(key=lambda row: row[0])
        return workbook
