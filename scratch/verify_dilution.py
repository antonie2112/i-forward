
import json

excel_audit_file = 'scratch/dilution_audit.json' # This was from previous extraction attempts
json_file = 'public/dmap_data.json'

with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Re-extract definitive dilution map for verification
# (Using the logic from the successful sync script)
import pandas as pd
file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'
xl = pd.ExcelFile(file_path)
sheets = ['Kitchen', 'Housekeeping_tương đương']
audit_map = {}
for sheet in sheets:
    df = pd.read_excel(file_path, sheet_name=sheet, header=None)
    rows = df.values.tolist()
    for r_idx, row in enumerate(rows):
        if 'DIVERSEY' in [str(x).upper() for x in row]:
            for data_row in rows[r_idx+1:]:
                div_name = str(data_row[2]).strip()
                div_dil = str(data_row[14]).strip().replace('nan', '-').replace('.0', '')
                eco_dil = str(data_row[32]).strip().replace('nan', '-').replace('.0', '')
                if div_name != 'nan' and div_name != '':
                    audit_map[div_name.lower().replace('  ', ' ')] = (div_dil, eco_dil)
            break

failures = 0
for entry in json_data:
    key = entry['DiverseyShort'].lower().replace('  ', ' ')
    if key in audit_map:
        expected_div, expected_eco = audit_map[key]
        actual_div = entry['Technical']['Dilution']
        actual_eco = entry['Cost']['dilution_eco']
        if actual_div != expected_div or actual_eco != expected_eco:
            print(f"Mismatch for {entry['DiverseyShort']}:")
            print(f"  Expected: Div={expected_div}, Eco={expected_eco}")
            print(f"  Actual:   Div={actual_div}, Eco={actual_eco}")
            failures += 1

if failures == 0:
    print("Verification Successful: All product dilutions match the Excel proposal.")
else:
    print(f"Verification Failed: Found {failures} mismatches.")
