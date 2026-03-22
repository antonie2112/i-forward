import openpyxl
import re
import json

excel_file = "Price_2026_tier_E.xlsx"
js_file = "main.js"

# 1. Load Prices from Excel
try:
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    ws = wb.active
except Exception as e:
    print(f"Error loading Excel: {e}")
    exit(1)

price_map = {}
for row in ws.iter_rows(min_row=1, values_only=True):
    # Depending on the exact columns, we know Name/Code/Price.
    # Let's check typical rows: ('KITCHEN', 'READYDOSE', 6102666, 'SPCLTY BVRG...', '1x100', 723100)
    # The code is index 2, price is index 5
    if len(row) > 5:
        code_val = row[2]
        price_val = row[5]
        
        if code_val and isinstance(price_val, (int, float)):
            # Normalize code to string
            code_str = str(code_val).strip()
            price_map[code_str] = float(price_val)

print(f"Loaded {len(price_map)} prices from {excel_file}")

# 2. Update main.js
try:
    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()
except FileNotFoundError:
    print(f"{js_file} not found.")
    exit(1)

# We want to find product blocks cleanly.
# A regex to match a whole block inside common/premium/custom arrays:
# Example: "code": "7106040", \n "name": "Neo", \n "specs": "...", \n "unit": "...", \n "price": 972708.0,
# We can find blocks separated by braces '{...}' or simply use a regex function to replace the price immediately following a specific code.

updated_count = 0
not_found_in_excel = []

# Parse out the JSON-like structures in main.js by iterating over the blocks
# Actually, it's easier to find the codes first, then update the price field inside the same object.
def replace_price_in_block(match):
    global updated_count
    block = match.group(0)
    
    # Extract code
    code_match = re.search(r'"code":\s*"([^"]+)"', block)
    if not code_match:
        return block
        
    code = code_match.group(1).strip()
    
    if code in price_map:
        new_price = price_map[code]
        # Replace the price in this block
        new_block = re.sub(r'"price":\s*[\d.]+,', f'"price": {new_price},', block)
        if new_block != block:
            updated_count += 1
        return new_block
    else:
        not_found_in_excel.append(code)
        return block

# The regex matches a whole JS object block starting with { and ending with }
# Warning: Since JS blocks might contain nested {}, this regex must be careful.
# But looking at main.js, the product objects are flat.
# Let's match from { up to }, non-greedy
new_js_content = re.sub(r'\{[^{}]*"code"[^{}]*"price"[^{}]*\}', replace_price_in_block, js_content, flags=re.DOTALL)

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(new_js_content)

print(f"Updated {updated_count} product prices in {js_file}.")
if not_found_in_excel:
    print(len(not_found_in_excel), "product codes in main.js were not found in the Excel file.")
    print("Sample missing codes:", not_found_in_excel[:10])
