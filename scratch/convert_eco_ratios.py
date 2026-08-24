
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def get_dilution_map_ratio():
    xl = pd.ExcelFile(file_path)
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    dilution_map = {}
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        for r_idx, row in enumerate(rows):
            if 'DIVERSEY' in [str(x).upper() for x in row]:
                for data_row in rows[r_idx+1:]:
                    div_name = str(data_row[2]).strip()
                    # Diversey Dilution is in Col 14
                    div_dil = str(data_row[14]).strip()
                    
                    # Ecolab Dilution: User wants 1:X format
                    # Columns 28, 29, 30 usually contain 1 , : , X
                    e1 = str(data_row[28]).strip()
                    e2 = str(data_row[29]).strip()
                    e3 = str(data_row[30]).strip().replace('.0', '')
                    
                    # Fallback to Col 32 if 1:X is not found
                    eco_dil = f"{e1}{e2}{e3}"
                    if 'nan' in eco_dil or eco_dil == "":
                        eco_dil = str(data_row[32]).strip()
                    
                    if div_name != 'nan' and div_name != '' and 'TOTAL' not in div_name.upper():
                        key = div_name.lower().replace('  ', ' ')
                        dilution_map[key] = {
                            "div": div_dil.replace('nan', '-').replace('.0', ''),
                            "eco": eco_dil.replace('nan', '-').replace('.0', '')
                        }
                break
    return dilution_map

json_path = 'public/dmap_data.json'
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

dmap = get_dilution_map_ratio()
updated = 0

for entry in json_data:
    short_name = entry['DiverseyShort'].lower().replace('  ', ' ')
    long_name = entry['Diversey'].lower().replace('  ', ' ')
    
    match_key = None
    if short_name in dmap: match_key = short_name
    elif long_name in dmap: match_key = long_name
    
    if match_key:
        ratios = dmap[match_key]
        changed = False
        if entry['Technical']['Dilution'] != ratios['div']:
            entry['Technical']['Dilution'] = ratios['div']
            changed = True
        if entry['Cost']['dilution_div'] != ratios['div']:
            entry['Cost']['dilution_div'] = ratios['div']
            changed = True
        # NEW: Force Ecolab to ratio format
        if entry['Cost']['dilution_eco'] != ratios['eco']:
            entry['Cost']['dilution_eco'] = ratios['eco']
            changed = True
        
        if changed:
            print(f"Update {entry['DiverseyShort']}: Div={ratios['div']}, Eco={ratios['eco']}")
            updated += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json_data = json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"Successfully converted Ecolab dilutions to ratios for {updated} products.")
