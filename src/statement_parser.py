import re
import os
from pypdf import PdfReader


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


def _parse_citi_statement(reader: PdfReader, owner: str, card_name: str) -> list:
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


class StatementParser:
    @staticmethod
    def parse(reader: PdfReader, owner: str, card_name: str) -> list:
        if card_name == "Chase":
            return _parse_chase_bank_statement(reader, owner, card_name)
        elif card_name == "Chase Freedom Flex":
            return _parse_chase_freedom_flex_statement(reader, owner, card_name)
        elif card_name == "Citi":
            return _parse_citi_statement(reader, owner, card_name)


class WorkbookGenerator:
    @staticmethod
    def generate():
        dir_name = "statements"
        file_names = os.listdir(dir_name)
        workbook = []
        for file_name in file_names:
            card_name = file_name.split("-")[0]
            owner = file_name.split("-")[1][0]
            file_path = os.path.join(dir_name, file_name)
            reader = PdfReader(file_path)
            data = StatementParser.parse(reader, owner, card_name)
            workbook.extend(data)
        workbook.sort(key=lambda row: row[0])
        return workbook
