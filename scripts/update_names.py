import openpyxl
import re
import json

def update_product_names():
    excel_path = 'Price_2026_tier_E.xlsx'
    js_path = 'main.js'

    # Load Excel Data
    print(f"Loading '{excel_path}'...")
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet = wb.active

    # Create mapping: Code -> Name
    code_to_name = {}
    for row in sheet.iter_rows(min_row=5, values_only=True):
        item_code = str(row[2]).strip() if row[2] else None
        item_desc = str(row[3]).strip() if row[3] else None
        
        if item_code and item_desc and item_code != 'None':
            code_to_name[item_code] = item_desc

    print(f"Found {len(code_to_name)} mapping pairs in Excel.")

    # Load main.js content
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract PRESETS block
    match = re.search(r'const PRESETS = (\{[\s\S]*?\n\});', content)
    if not match:
        print("Error: Could not find PRESETS object block in main.js")
        return

    json_str = match.group(1)
    
    # Fix unquoted keys for JSON validation (e.g., common: -> "common":)
    # Be careful not to replace inside string values
    json_str_fixed = re.sub(r'(?<!")\b(\w+)\s*:', r'"\1":', json_str)
    
    try:
        presets = json.loads(json_str_fixed)
    except json.JSONDecodeError as e:
        print(f"Error parsing PRESETS JSON from main.js: {e}\nString was:\n{json_str_fixed[:200]}")
        return

    updated_count = 0
    not_found = set()

    # Update item names in 'common' array
    for item in presets.get('common', []):
        if item.get('type') == 'section':
            continue
            
        code = str(item.get('code', '')).strip()
        if code in code_to_name:
            old_name = item.get('name', '')
            new_name = code_to_name[code]
            if old_name != new_name:
                item['name'] = new_name
                updated_count += 1
                print(f"Updated {code}: '{old_name}' -> '{new_name}'")
        elif code:
            not_found.add(code)

    if updated_count == 0:
        print("No product names needed updating.")
    else:
        # Reconstruct JSON with indent 4
        new_json_str = json.dumps(presets, ensure_ascii=False, indent=4)
        # Remove quotes from keys to match JS style
        new_json_str = re.sub(r'"(\w+)":', r'\1:', new_json_str)
        
        new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\nSuccessfully updated {updated_count} product names in {js_path}")

    if not_found:
        print(f"\nWarning: The following codes in main.js were not found in Excel:")
        print(", ".join(not_found))

if __name__ == "__main__":
    update_product_names()
