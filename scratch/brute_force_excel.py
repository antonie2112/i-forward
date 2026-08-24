
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def brute_force_extract():
    xl = pd.ExcelFile(file_path)
    all_mappings = []
    
    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        # Find columns that might contain Diversey and Ecolab
        div_cols = []
        eco_cols = []
        
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row):
                val = str(cell).upper()
                if 'DIVERSEY' in val:
                    div_cols.append(c_idx)
                if 'ECOLAB' in val:
                    eco_cols.append(c_idx)
        
        if not div_cols or not eco_cols:
            continue
            
        # Try to find a row where we have both a Diversey column and an Ecolab column
        # and then extract data from below that row
        for div_c in set(div_cols):
            for eco_c in set(eco_cols):
                if div_c == eco_c: continue
                # Look for data row by row below the likely header
                found_any = False
                for r_idx in range(0, len(rows)):
                    div_val = str(rows[r_idx][div_c]).strip()
                    eco_val = str(rows[r_idx][eco_c]).strip()
                    
                    if div_val != 'nan' and div_val != '' and eco_val != 'nan' and eco_val != '' \
                       and 'DIVERSEY' not in div_val.upper() and 'ECOLAB' not in div_val.upper() \
                       and 'TOTAL' not in div_val.upper():
                        all_mappings.append({
                            "diversey": div_val,
                            "ecolab": eco_val,
                            "sheet": sheet,
                            "row": r_idx + 1
                        })
                        found_any = True
                if found_any:
                    break
    
    # Deduplicate
    unique_mappings = []
    seen = set()
    for m in all_mappings:
        key = (m['diversey'].lower(), m['ecolab'].lower())
        if key not in seen:
            unique_mappings.append(m)
            seen.add(key)
            
    return unique_mappings

try:
    data = brute_force_extract()
    with open('scratch/brute_force_mappings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(data)} unique mappings.")
    for d in data[:20]:
        print(f"{d['diversey']} -> {d['ecolab']} ({d['sheet']})")
except Exception as e:
    print(f"Error: {e}")
