import csv
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
ws = wb.active
ws.title = "Books"

with open("books.csv", encoding="utf-8") as f:
    for row in csv.reader(f):
        ws.append(row)

for cell in ws[1]:
    cell.font = Font(bold=True)

ws.column_dimensions["A"].width = 60
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 10
ws.freeze_panes = "A2"

wb.save("books.xlsx")
print("books.xlsx তৈরি হয়েছে")
