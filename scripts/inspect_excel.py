import openpyxl
import json

filename = "Price_2026_tier_E.xlsx"
wb = openpyxl.load_workbook(filename, data_only=True)
ws = wb.active

for i, row in enumerate(ws.iter_rows(min_row=1, max_row=20, values_only=True)):
    print(f"Row {i+1}: {row}")
