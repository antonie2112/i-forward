
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def get_sku_map():
    xl = pd.ExcelFile(file_path)
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    sku_map = {}
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        div_prod_col = -1
        sku_col = -1
        
        for r_idx, row in enumerate(rows):
            row_str = [str(x).upper() for x in row]
            if 'DIVERSEY' in row_str and 'PROPOSED' in "".join(row_str):
                div_prod_col = row_str.index('DIVERSEY')
                # Find SKU column (usually index 3)
                for i, col_val in enumerate(row_str):
                    if 'PROPOSED' in col_val:
                        sku_col = i
                        break
                
                if div_prod_col != -1 and sku_col != -1:
                    for data_row in rows[r_idx+1:]:
                        div_val = str(data_row[div_prod_col]).strip()
                        sku_val = str(data_row[sku_col]).strip().replace('.0', '')
                        
                        if div_val != 'nan' and div_val != '' and 'TOTAL' not in div_val.upper() and sku_val != 'nan' and sku_val != '':
                            key = div_val.lower().replace('  ', ' ')
                            sku_map[key] = sku_val
                    break
    return sku_map

try:
    mapping = get_sku_map()
    with open('scratch/sku_audit.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"Extracted {len(mapping)} SKUs.")
    for k, v in list(mapping.items())[:10]:
        print(f"{k} -> {v}")
except Exception as e:
    print(f"Error: {e}")
