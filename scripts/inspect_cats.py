import openpyxl
import json

excel_file = "Price_2026_tier_E.xlsx"
wb = openpyxl.load_workbook(excel_file, data_only=True)
ws = wb.active

categories = set()
map_code_to_cat = {}

for row in ws.iter_rows(min_row=2, values_only=True): # skip header
    if len(row) > 5:
        cat1 = row[0]
        cat2 = row[1]
        code = row[2]
        
        if code and cat1:
            code_str = str(code).strip()
            # Let's see what cat1 looks like
            categories.add(str(cat1))
            map_code_to_cat[code_str] = {"c1": str(cat1).strip(), "c2": str(cat2).strip() if cat2 else ""}

print(f"Loaded {len(map_code_to_cat)} product categories.")
print("Unique Categories (Col 0):", categories)

# Check some codes from main.js to see what they map to
test_codes = ["7106040", "7106063", "7106043", "7101070", "7106121"]
for tc in test_codes:
    if tc in map_code_to_cat:
        print(f"Code {tc} -> {map_code_to_cat[tc]}")
    else:
        print(f"Code {tc} -> NOT FOUND")
