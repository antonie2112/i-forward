
import pandas as pd
import json
import os

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def extract_all_mappings(sheet_names):
    all_data = []
    for sheet in sheet_names:
        try:
            df = pd.read_excel(file_path, sheet_name=sheet)
            # Find the header row (contains both DIVERSEY and ECOLAB or similar)
            header_idx = -1
            div_col = -1
            eco_col = -1
            
            for idx, row in df.iterrows():
                row_list = [str(x).upper() for x in row.tolist()]
                if 'DIVERSEY' in row_list and any('ECOLAB' in x for x in row_list):
                    header_idx = idx
                    div_col = row_list.index('DIVERSEY')
                    # Find Ecolab column (there might be multiple, we want the product name)
                    for i, val in enumerate(row_list):
                        if 'ECOLAB' in val and i > div_col:
                            # Usually the product name is the column right after a header or identified as Product Name
                            # Let's look for 'PRODUCT NAME' in the row
                            if 'PRODUCT NAME' in row_list:
                                eco_col = row_list.index('PRODUCT NAME')
                            else:
                                eco_col = i
                            break
                    if div_col != -1 and eco_col != -1:
                        break
            
            if header_idx != -1:
                # Process subsequent rows
                for idx, row in df.iloc[header_idx+1:].iterrows():
                    row_list = row.tolist()
                    div_val = str(row_list[div_col]).strip()
                    eco_val = str(row_list[eco_col]).strip()
                    if div_val != 'nan' and div_val != '' and 'TOTAL' not in div_val.upper():
                        all_data.append({
                            "diversey": div_val,
                            "ecolab": eco_val,
                            "sheet": sheet,
                            "row": idx + 2
                        })
        except Exception as e:
            print(f"Error in sheet {sheet}: {e}")
    return all_data

sheets = ['Kitchen', 'Housekeeping_tương đương', 'Houseskeeping_sustainability']
mappings = extract_all_mappings(sheets)

with open('scratch/full_audit_excel.json', 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=2)

print(f"Successfully extracted {len(mappings)} mappings.")
# Print a few to check
for m in mappings[:10]:
    print(f"{m['diversey']} -> {m['ecolab']}")
