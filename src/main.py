import re
from statement_parser import WorkbookGenerator
from workbook_processor import WorkbookProcessor
from excel_writer import ExcelWriter

if __name__ == "__main__":
    date = input("Please enter the month of the workbook in MM/YYYY format: ")
    if not re.match("^[0-9]{2}/[0-9]{4}$", date):
        raise ValueError(f"Invalid date input string: {date}")
    
    workbook = WorkbookGenerator.generate()
    workbook = WorkbookProcessor.process(workbook, date)
    for row in workbook:
        print(row)
    
    ExcelWriter.write(workbook, date)
