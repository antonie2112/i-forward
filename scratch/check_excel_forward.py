
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

try:
    xl = pd.ExcelFile(file_path)
    print(f"Sheets: {xl.sheet_names}")
    
    for sheet in xl.sheet_names:
        print(f"\n--- Checking Sheet: {sheet} ---")
        df = pd.read_excel(file_path, sheet_name=sheet)
        
        # Search for Forward DC
        matches = df[df.apply(lambda row: row.astype(str).str.contains('Forward DC', case=False).any(), axis=1)]
        if not matches.empty:
            print(f"Found matches for 'Forward DC' in {sheet}:")
            # print first 5 columns and the one with 'Forward DC'
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_colwidth', None)
            print(matches)
            
except Exception as e:
    print(f"Error: {e}")
