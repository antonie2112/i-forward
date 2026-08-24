
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'
json_path = 'public/dmap_data.json'

def get_sku_map():
    xl = pd.ExcelFile(file_path)
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    sku_map = {}
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        # Start from row 2 (data row)
        for data_row in rows[2:]:
            div_name = str(data_row[2]).strip()
            sku_val = str(data_row[3]).strip().replace('.0', '')
            
            if div_name != 'nan' and div_name != '' and sku_val != 'nan' and sku_val != '':
                key = div_name.lower().replace('  ', ' ')
                sku_map[key] = sku_val
                
    return sku_map

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    skus = get_sku_map()
    updated = 0
    
    for entry in json_data:
        short = entry['DiverseyShort'].lower().replace('  ', ' ')
        long = entry['Diversey'].lower().replace('  ', ' ')
        
        # Exact match or substring match for "Diversey" names
        found_sku = None
        if short in skus: found_sku = skus[short]
        elif long in skus: found_sku = skus[long]
        else:
            # Fallback: check if the key is a substring of the Excel name
            for k, v in skus.items():
                if short in k or k in short:
                    found_sku = v
                    break
        
        if found_sku:
            entry['SKU'] = found_sku
            updated += 1
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        
    print(f"Database updated with {updated} SKUs.")
except Exception as e:
    print(f"Error: {e}")
