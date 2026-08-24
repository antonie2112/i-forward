
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def extract_from_sheet(sheet_name):
    xl = pd.ExcelFile(file_path)
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Identify Diversey and Ecolab columns
    # Based on previous output: Diversey is likely column 2 and Ecolab is column 20 for HK
    # Let's find columns by header name or position
    
    div_col = -1
    eco_col = -1
    
    # Search for headers
    for i, col in enumerate(df.columns):
        if str(col).lower() == 'diversey':
            div_col = i
        elif str(col).lower() == 'ecolab':
            eco_col = i
            
    # If not found by header, use positions (heuristical)
    if div_col == -1:
        # Check rows for headers if they are not in the column list
        for idx, row in df.iterrows():
            row_list = row.tolist()
            if 'DIVERSEY' in [str(x).upper() for x in row_list]:
                div_col = [str(x).upper() for x in row_list].index('DIVERSEY')
                eco_col = [str(x).upper() for x in row_list].index('ECOLAB')
                break
                
    if div_col == -1:
        return []
        
    results = []
    found_header = False
    for idx, row in df.iterrows():
        row_list = row.tolist()
        div_val = str(row_list[div_col]).strip()
        eco_val = str(row_list[eco_col]).strip()
        
        if div_val.upper() == 'DIVERSEY':
            found_header = True
            continue
            
        if found_header and div_val != 'nan' and div_val != '':
            results.append({
                "diversey": div_val,
                "ecolab": eco_val,
                "sheet": sheet_name,
                "row": idx + 2 # 1-indexed + header row
            })
            
    return results

try:
    all_mappings = []
    all_mappings.extend(extract_from_sheet('Kitchen'))
    all_mappings.extend(extract_from_sheet('Housekeeping_tương đương'))
    
    with open('scratch/excel_mappings_audit.json', 'w', encoding='utf-8') as f:
        json.dump(all_mappings, f, ensure_ascii=False, indent=2)
        
    print(f"Extracted {len(all_mappings)} mappings.")
    for m in all_mappings[:10]:
        print(f"{m['diversey']} -> {m['ecolab']}")
        
except Exception as e:
    print(f"Error: {e}")
