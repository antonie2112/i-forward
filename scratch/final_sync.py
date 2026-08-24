
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def get_definitive_mappings():
    xl = pd.ExcelFile(file_path)
    # Priority sheets
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    mappings = {}
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        div_col = -1
        eco_col = -1
        
        # Find headers in the sheet
        for r_idx, row in enumerate(rows):
            row_str = [str(x).upper() for x in row]
            if 'DIVERSEY' in row_str and any('ECOLAB' in x for x in row_str):
                div_col = row_str.index('DIVERSEY')
                # Find appropriate Ecolab product name column
                # In Kitchen: It's index 19
                # In HK: It's index 20
                if 'PRODUCT NAME' in row_str:
                    eco_col = row_str.index('PRODUCT NAME')
                else:
                    # Look for the first column after Div that contains 'Product' or similar
                    for c_idx in range(div_col + 1, len(row_str)):
                        if 'PRODUCT' in row_str[c_idx] or 'ECOLAB' in row_str[c_idx]:
                            eco_col = c_idx
                            break
                
                if div_col != -1 and eco_col != -1:
                    # Extract from rows below
                    for data_row in rows[r_idx+1:]:
                        div_val = str(data_row[div_col]).strip()
                        eco_val = str(data_row[eco_col]).strip()
                        
                        if div_val != 'nan' and div_val != '' and 'TOTAL' not in div_val.upper() \
                           and eco_val != 'nan' and eco_val != '':
                            # Normalize Diversey name for keying
                            key = div_val.lower().replace('  ', ' ')
                            mappings[key] = eco_val
                    break
    return mappings

# Load existing JSON
json_path = 'public/dmap_data.json'
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

definitive = get_definitive_mappings()

# Update
updated = 0
for entry in json_data:
    div_short = entry['DiverseyShort'].lower().replace('  ', ' ')
    div_long = entry['Diversey'].lower().replace('  ', ' ')
    
    # Priority: exact short name match
    if div_short in definitive:
        if entry['Ecolab'] != definitive[div_short]:
            print(f"Update {entry['DiverseyShort']}: {entry['Ecolab']} -> {definitive[div_short]}")
            entry['Ecolab'] = definitive[div_short]
            updated += 1
    # Secondary: match by long name (Diversey field)
    elif div_long in definitive:
         if entry['Ecolab'] != definitive[div_long]:
            print(f"Update {entry['Diversey']}: {entry['Ecolab']} -> {definitive[div_long]}")
            entry['Ecolab'] = definitive[div_long]
            updated += 1

# Specific fixes for common items to ensure perfect sync
overrides = {
    "Glance 101": "Miraglo",
    "Suma J512": "22 Multi Quat Sanitizer",
    "Forward DC": "Future DC",
    "Taski R5": "Oasis Pro Garden Sunshine / Zephair"
}
for entry in json_data:
    if entry['DiverseyShort'] in overrides:
        if entry['Ecolab'] != overrides[entry['DiverseyShort']]:
            print(f"Override {entry['DiverseyShort']}: {entry['Ecolab']} -> {overrides[entry['DiverseyShort']]}")
            entry['Ecolab'] = overrides[entry['DiverseyShort']]
            updated += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"Synchronized {updated} product mappings with Excel definitive list.")
