import openpyxl
import json
import os

filename = "Price_2026_tier_E.xlsx"

if not os.path.exists(filename):
    print(f"File {filename} not found.")
    exit(1)

wb = openpyxl.load_workbook(filename, data_only=True)
ws = wb.active

products = []

# Assuming row 1 or 2 is header. Let's just iterate and find where "code" or "price" is.
# Usually standard format. Let's print out the first few rows to understand the structure.
for i, row in enumerate(ws.iter_rows(min_row=1, max_row=10, values_only=True)):
    print(f"Row {i+1}: {row}")

