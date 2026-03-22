import openpyxl
import json
import sys

filename = "Ecolab application Quote 2025.xlsx"

try:
    wb = openpyxl.load_workbook(filename, data_only=True)
    ws = wb.active
except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)

items = []
current_section_id = 0
section_idx = 1
item_idx = 101

# Assume data starts after some header rows. Let's inspect first few rows to find patterns.
# Based on typical Excel quotes: Blue background indicates Section.
# Data columns mapping (approximate based on `main.js`):
# A: No/STT (skip)
# B: Product Code
# C: Item Name
# D: Specs
# E: Image (skip)
# F: Unit
# G: Price 2025
# H: Discount Price
# I: Dilution

# Helper to get cell color
def is_blue_bg(cell):
    if not cell.fill or not cell.fill.start_color:
        return False
    # Check for blue-ish color. Theme colors can be tricky.
    # Often '00CCFF' (cyan) or similar.
    # Let's check if it's NOT standard white/none.
    color = cell.fill.start_color.index
    # If it's a theme index, it might be tough without theme map, but let's try assuming explicit colors first.
    # Or just check if column C has text but B is empty?
    # Actually, the user said "Blue rows are sections". The header row itself is likely row 1 or similar.
    return str(color) != '00000000' and str(color) != 'FFFFFFFF'

# Iterate rows
start_row = 1
found_header = False

for row in ws.iter_rows(min_row=1, values_only=False):
    # Try to find the header row first ("STT", "MÃ SẢN PHẨM" etc)
    row_values = [cell.value for cell in row]
    
    if not found_header:
        # Check if this looks like the header
        # Column 1 (B) is usually Code. Column 2 (C) Name.
        # Let's look for "STT" or "NO" in first col
        if row_values[0] and "STT" in str(row_values[0]).upper():
            found_header = True
            # print("DEBUG: Found header at row", row[0].row)
            continue
        continue

    # Process data rows
    cell_stt = row[0]
    cell_code = row[1]
    cell_name = row[2]
    
    # Check for empty rows to stop?
    if not cell_name.value and not cell_code.value:
        continue

    # Identify Section vs Product
    # Section: Blue background in Name column? Or merged cells?
    # User said: "Blue header rows".
    # Let's check cell_name background color.
    
    is_section = False
    if cell_name.fill and cell_name.fill.start_color:
        # Check if color is not default. Simple heuristic.
        # print("DEBUG: Color:", cell_name.fill.start_color.index) 
        if cell_name.fill.start_color.type == 'rgb' and cell_name.fill.start_color.rgb:
             # Just assume any non-white/transparent is section for now or check specifically for blue if we knew hex
             # The user said "Blue".
             rgb = cell_name.fill.start_color.rgb
             # print("DEBUG: RGB", rgb) 
             if rgb.startswith("FF"): # Alpha FF
                 # Check for blue component dominating? Or just "not white"
                 if rgb != "FFFFFFFF":
                     is_section = True
        elif cell_name.fill.start_color.type == 'theme':
             # Theme color. 
             is_section = True # Assume styled rows are sections in this context

    # Override: If Code is empty but Name is present, likely a section or sub-header
    if not cell_code.value and cell_name.value:
        is_section = True

    if is_section:
        current_section = {
            "id": f"s{section_idx}",
            "type": "section",
            "name": str(cell_name.value).strip()
        }
        items.append(current_section)
        section_idx += 1
    else:
        # Product
        # code: B, name: C, specs: D, unit: F, price: G, discount: H, dilution: I
        price = row[6].value
        discount = row[7].value
        
        # Handle N/A or strings in price
        try:
            price = float(price) if price else 0
        except:
            price = 0
            
        try:
            discount = float(discount) if discount else 0
        except:
            discount = 0

        item = {
            "id": item_idx,
            "code": str(cell_code.value).strip() if cell_code.value else "",
            "name": str(cell_name.value).strip() if cell_name.value else "",
            "specs": str(row[3].value).strip() if row[3].value else "",
            "unit": str(row[5].value).strip() if row[5].value else "",
            "price": price,
            "discountPrice": discount,
            "dilution": str(row[8].value).strip() if row[8].value else ""
        }
        items.append(item)
        item_idx += 1

print(json.dumps(items, indent=2))
