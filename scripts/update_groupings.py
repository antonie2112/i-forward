import openpyxl
import re
import json

excel_file = "Price_2026_tier_E.xlsx"
js_file = "main.js"

# 1. Load Categories from Excel
wb = openpyxl.load_workbook(excel_file, data_only=True)
ws = wb.active

map_code_to_cat = {}
for row in ws.iter_rows(min_row=2, values_only=True):
    if len(row) > 5:
        cat1 = row[0]
        code = row[2]
        if code and cat1:
            code_str = str(code).strip()
            # FSR - FOOD SERVICE RESTAURANT is too long, maybe just FSR? We can keep the string as is.
            cat_str = str(cat1).strip()
            map_code_to_cat[code_str] = cat_str

# Manual overrides for legacy products not in Excel
manual_overrides = {
    "6113094": "HOUSEKEEPING",
    "7106864": "HOUSEKEEPING",
    "7106578": "LAUNDRY",
    "7106090": "LAUNDRY"
}
map_code_to_cat.update(manual_overrides)

with open(js_file, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Helper to process an array string
def process_array_content(array_str):
    # Extract all objects {}
    items = re.findall(r'\{([^{}]+)\}', array_str)
    
    products = []
    # Parse items
    for item in items:
        # Check if type is section
        if '"type":' in item and '"section"' in item:
            continue # Drop old sections
            
        c_match = re.search(r'"code":\s*"([^"]+)"', item)
        n_match = re.search(r'"name":\s*"([^"]+)"', item)
        if c_match:
            code = c_match.group(1).strip()
            cat = map_code_to_cat.get(code, "OTHER")
            # We want to keep the original raw item text to rebuild exactly
            products.append((cat, "{" + item + "}"))
            
    # Group by category
    grouped = {}
    for cat, raw_item in products:
        grouped.setdefault(cat, []).append(raw_item)
        
    # Rebuild the final array string
    new_items_strs = []
    section_id = 900 # start at some high id for sections to avoid collision
    
    # Sort categories alphabetically or keep as is? Let's sort to be consistent
    for cat in sorted(grouped.keys()):
        # add section header
        new_items_strs.append(f'        {{\n            "id": {section_id},\n            "type": "section",\n            "name": "{cat}"\n        }}')
        section_id += 1
        
        # add products
        for raw_item in grouped[cat]:
            new_items_strs.append(f"        {raw_item}")
            
    return "[\n" + ",\n".join(new_items_strs) + "\n    ]"

# Replace common
def replacer_common(m):
    return "common: " + process_array_content(m.group(1))
js_content = re.sub(r'common:\s*\[(.*?)\]\s*(?=,|premium)', replacer_common, js_content, flags=re.DOTALL)

# Replace premium
def replacer_premium(m):
    return "premium: " + process_array_content(m.group(1))
js_content = re.sub(r'premium:\s*\[(.*?)\]\s*(?=,|custom)', replacer_premium, js_content, flags=re.DOTALL)

# Replace custom
def replacer_custom(m):
    return "custom: " + process_array_content(m.group(1))
js_content = re.sub(r'custom:\s*\[(.*?)\]\s*(?=,|})', replacer_custom, js_content, flags=re.DOTALL)

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Updated grouping successfully.")
