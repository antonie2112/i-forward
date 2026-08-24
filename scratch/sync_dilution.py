
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def get_dilution_map():
    xl = pd.ExcelFile(file_path)
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    dilution_map = {}
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        for r_idx, row in enumerate(rows):
            # Check for header row
            if 'DIVERSEY' in [str(x).upper() for x in row]:
                # In both sheets, Div Product=2, Div Dilution=14, Eco Product=20, Eco Dilution=32
                for data_row in rows[r_idx+1:]:
                    div_name = str(data_row[2]).strip()
                    eco_name = str(data_row[20]).strip()
                    div_dil = str(data_row[14]).strip()
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

dmap = get_dilution_map()
updated = 0

for entry in json_data:
    short_name = entry['DiverseyShort'].lower().replace('  ', ' ')
    long_name = entry['Diversey'].lower().replace('  ', ' ')
    
    # Priority matching
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
        if entry['Cost']['dilution_eco'] != ratios['eco']:
            entry['Cost']['dilution_eco'] = ratios['eco']
            changed = True
        
        if changed:
            print(f"Sync {entry['DiverseyShort']}: Div={ratios['div']}, Eco={ratios['eco']}")
            updated += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"Successfully synchronized dilution ratios for {updated} products.")
