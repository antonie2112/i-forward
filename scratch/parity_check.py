
import pandas as pd
import json

excel_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'
json_path = 'public/dmap_data.json'

def get_excel_mappings():
    xl = pd.ExcelFile(excel_path)
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    mappings = []
    
    for sheet in sheets:
        df = pd.read_excel(excel_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        div_col, eco_col = -1, -1
        
        for r_idx, row in enumerate(rows):
            row_str = [str(x).upper() for x in row]
            if 'DIVERSEY' in row_str and 'ECOLAB' in row_str:
                div_col = row_str.index('DIVERSEY')
                eco_col = row_str.index('ECOLAB')
                
                for data_row in rows[r_idx+1:]:
                    eco_name = str(data_row[eco_col]).strip()
                    div_name = str(data_row[div_col]).strip()
                    
                    if eco_name != 'nan' and eco_name != '' and div_name != 'nan' and div_name != '':
                        if 'TOTAL' not in eco_name.upper() and 'TOTAL' not in div_name.upper():
                            # Extract first lines in case of multiline
                            eco_clean = eco_name.split('\n')[0].strip()
                            div_clean = div_name.split('\n')[0].strip()
                            mappings.append({'Ecolab': eco_clean, 'Diversey': div_clean, 'Sheet': sheet})
                break
    return mappings

try:
    excel_mappings = get_excel_mappings()
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        
    json_eco_div = {}
    for entry in json_data:
        eco_key = entry['Ecolab'].lower().replace('  ', ' ')
        json_eco_div[eco_key] = entry
        
    missing = []
    mismatch = []
    
    for m in excel_mappings:
        e_key = m['Ecolab'].lower().replace('  ', ' ')
        d_key = m['Diversey'].lower().replace('  ', ' ')
        
        if e_key not in json_eco_div:
            # Maybe slight name diff? Let's check substrings
            found = False
            for k in json_eco_div:
                if k in e_key or e_key in k:
                    found = True
                    # check if diversey matches
                    j_div = json_eco_div[k]['Diversey'].lower().replace('  ', ' ')
                    j_div_short = json_eco_div[k]['DiverseyShort'].lower().replace('  ', ' ')
                    if d_key not in j_div and d_key not in j_div_short and j_div_short not in d_key:
                        mismatch.append(f"Mismatch: Excel ({m['Ecolab']} -> {m['Diversey']}) vs JSON ({json_eco_div[k]['Ecolab']} -> {json_eco_div[k]['DiverseyShort']})")
                    break
            
            if not found:
                missing.append(f"Missing Ecolab Product in JSON: {m['Ecolab']} (vs {m['Diversey']} in Excel)")
        else:
            j_div = json_eco_div[e_key]['Diversey'].lower().replace('  ', ' ')
            j_div_short = json_eco_div[e_key]['DiverseyShort'].lower().replace('  ', ' ')
            if d_key not in j_div and d_key not in j_div_short and j_div_short not in d_key:
                 mismatch.append(f"Mismatch: Excel ({m['Ecolab']} -> {m['Diversey']}) vs JSON ({json_eco_div[e_key]['Ecolab']} -> {json_eco_div[e_key]['DiverseyShort']})")

    print(f"Total mappings in Excel: {len(excel_mappings)}")
    print(f"Total entries in JSON: {len(json_data)}")
    print(f"\nMissing products ({len(missing)}):")
    for msg in missing:
        print("  " + msg)
        
    print(f"\nMismatches ({len(mismatch)}):")
    for msg in mismatch:
        print("  " + msg)
        
except Exception as e:
    print(f"Error: {e}")
