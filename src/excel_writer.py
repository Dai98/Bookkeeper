import xlsxwriter


class ExcelWriter:

    @staticmethod
    def write(workbook_data: list, date: str) -> None:
        date = "".join(date.split("/")[::-1])
        workbook_name = f"output/workbook_{date}.xlsx"
        workbook = xlsxwriter.Workbook(workbook_name)
        worksheet = workbook.add_worksheet()

        for row_index, row in enumerate(workbook_data):
            for col_index, col in enumerate(row):
                worksheet.write(row_index, col_index, col)

        # Write summary section
        # Deprecated for now, formula won't be copied to Lark spreadsheet
        # worksheet.write(1, 9, "F开销")
        # worksheet.write(2, 9, "F实付")
        # worksheet.write(3, 9, "F实际开销")
        # worksheet.write(5, 9, "类别")

        # worksheet.write(1, 10, '=SUMIF(G:G, "F", C:C) + SUMIF(G:G, "DF", C:C)/2 + SUMIF(G:G, "DL", C:C)/2 + SUMIF(G:G, "DFL", C:C)/3')
        # worksheet.write(2, 10, '=SUMIF($E:$E, "F", $C:$C)')
        # worksheet.write(3, 10, '=K2-SUMIFS($C:$C, $G:$G, "F", $H:$H, "H")-SUMIFS($C:$C, $G:$G, "DF", $H:$H, "H")/2-SUMIFS($C:$C, $G:$G, "DL", $H:$H, "H")/2-SUMIFS($C:$C, $G:$G, "DFL", $H:$H, "H")/3')
        # worksheet.write(5, 10, 'Grocery (G)')
        # worksheet.write(6, 10, 'Extra (E)')
        # worksheet.write(7, 10, 'Extra F (EF)')
        # worksheet.write(8, 10, 'Extra D (ED)')
        # worksheet.write(9, 10, 'Recurring (R)')
        # worksheet.write(10, 10, 'Recurring F (RF)')
        # worksheet.write(11, 10, 'Recurring D (RD)')
        # worksheet.write(12, 10, 'Travel (T)')
        # worksheet.write(14, 10, 'EatOut (O)')
        # worksheet.write(15, 10, 'Helper (H)')
        # worksheet.write(16, 10, '总花销')

        # worksheet.write(1, 11, 'D开销')
        # worksheet.write(2, 11, 'D实付')
        # worksheet.write(3, 11, 'D实际开销')
        # worksheet.write(4, 11, 'D应转账')
        # worksheet.write(5, 11, '=SUMIF(H:H, "G", C:C)')
        # worksheet.write(6, 11, '=SUMIF(H:H, "E", C:C)')
        # worksheet.write(7, 11, '=SUMIF(H:H, "EF", C:C)')
        # worksheet.write(8, 11, '=SUMIF(H:H, "ED", C:C)')
        # worksheet.write(9, 11, '=SUMIF(H:H, "R", C:C)')
        # worksheet.write(10, 11, '=SUMIF(H:H, "RF", C:C)')
        # worksheet.write(11, 11, '=SUMIF(H:H, "RD", C:C)')
        # worksheet.write(12, 11, '=SUMIF(H:H, "T", C:C)')
        # worksheet.write(14, 11, '=SUMIF(H:H, "O", C:C)')
        # worksheet.write(15, 11, '=SUMIF(H:H, "H", C:C)')
        # worksheet.write(16, 11, '=SUM(L6:L15)')

        # worksheet.write(1, 12, '=SUMIF(G:G, "D", C:C) + SUMIF(G:G, "DF", C:C)/2 + SUMIF(G:G, "DL", C:C)/2 + SUMIF(G:G, "DFL", C:C)/3')
        # worksheet.write(2, 12, '=SUMIF($E:$E, "D", $C:$C)')
        # worksheet.write(3, 12, '=M2-SUMIFS($C:$C, $G:$G, "D", $H:$H, "H")-SUMIFS($C:$C, $G:$G, "DF", $H:$H, "H")/2 - SUMIFS($C:$C, $G:$G, "DL", $H:$H, "H")/2 - SUMIFS($C:$C, $G:$G, "DFL", $H:$H, "H")/2')
        # worksheet.write(2, 12, '=M2-M3')

        workbook.close()