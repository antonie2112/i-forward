
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def extract_dilution_data(sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    rows = df.values.tolist()
    
    # Heuristic for columns based on previous inspection
    # Kitchen: Div Product=2, Div Dilution=11 (or 10-12), Eco Product=20, Eco Dilution=29 (or 28-30)
    
    div_prod_col = -1
    eco_prod_col = -1
    div_dil_col = -1
    eco_dil_col = -1
    
    for r_idx, row in enumerate(rows):
        row_str = [str(x).upper() for x in row]
        if 'DIVERSEY' in row_str and any('ECOLAB' in x for x in row_str):
            div_prod_col = row_str.index('DIVERSEY')
            # eco_prod_col is usually near 'PRODUCT NAME' or 'PRODUCT' index
            for i, val in enumerate(row_str):
                if 'PRODUCT NAME' in val: eco_prod_col = i
                if eco_prod_col == -1 and 'ECOLAB' in val and i > div_prod_col: eco_prod_col = i
            
            # Find Dilution columns
            # For Diversey
            for i in range(div_prod_col, eco_prod_col):
                if 'DILUTION %' in row_str[i]: 
                    div_dil_col = i - 1 # Usually the 1 : X is before Dilution %
                    break
            # For Ecolab
            for i in range(eco_prod_col, len(row_str)):
                if 'DILUTION %' in row_str[i]:
                    eco_dil_col = i - 1
                    break
            
            if div_prod_col != -1 and eco_prod_col != -1:
                results = []
                for data_row in rows[r_idx+1:]:
                    div_val = str(data_row[div_prod_col]).strip()
                    eco_val = str(data_row[eco_prod_col]).strip()
                    
                    if div_val != 'nan' and div_val != '' and 'TOTAL' not in div_val.upper():
                        # Extract Dilution ratios
                        div_dil = ""
                        if div_dil_col != -1:
                            ratio_parts = data_row[div_dil_col-1:div_dil_col+2]
                            div_dil = "".join([str(x) for x in ratio_parts if str(x) != 'nan']).replace('.0', '')
                        
                        eco_dil = ""
                        if eco_dil_col != -1:
                            ratio_parts = data_row[eco_dil_col-1:eco_dil_col+2]
                            eco_dil = "".join([str(x) for x in ratio_parts if str(x) != 'nan']).replace('.0', '')
                            
                        results.append({
                            "diversey": div_val,
                            "ecolab": eco_val,
                            "div_dilution": div_dil,
                            "eco_dilution": eco_dil
                        })
                return results
    return []

try:
    all_data = []
    all_data.extend(extract_dilution_data('Kitchen'))
    all_data.extend(extract_dilution_data('Housekeeping_tương đương'))
    
    with open('scratch/dilution_audit.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {len(all_data)} products.")
    for d in all_data[:10]:
        print(f"{d['diversey']} ({d['div_dilution']}) -> {d['ecolab']} ({d['eco_dilution']})")
except Exception as e:
    print(f"Error: {e}")
