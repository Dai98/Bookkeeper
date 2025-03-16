

class WorkbookProcessor:

    @staticmethod
    def process(workbook: list, date: str) -> list:
        # Because statement periods do not include exact month, filter out rows that don't belong in current month
        month = date[:2]
        processed_workbook = [row for row in workbook if row[0].startswith(month)]
        
        # Append header
        processed_workbook = WorkbookProcessor._append_header(processed_workbook)
        return processed_workbook
    
    @staticmethod
    def _append_header(workbook: list) -> list:
        header = ["时间", "商家", "消费金额", "备注", "卡holder", "卡", "charge", "类别"]
        workbook.insert(0, header)
        return workbook