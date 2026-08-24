
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

try:
    xl = pd.ExcelFile(file_path)
    sheets = xl.sheet_names
    print(f"Sheets: {sheets}")
    
    mapping = []
    
    # Process 'Housekeeping_tương đương' and 'Kitchen' sheets as they usually contain mappings
    target_sheets = ['Kitchen', 'Housekeeping_tương đương']
    
    for sheet in target_sheets:
        if sheet in sheets:
            df = pd.read_excel(file_path, sheet_name=sheet)
            # We need to find columns that look like Diversey and Ecolab names
            # Usually Diversey is on the left, Ecolab on the right in comparison sheets
            
            # Print columns to see the structure
            print(f"\n--- Sheet: {sheet} ---")
            print(df.columns.tolist())
            
            # Store raw data for analysis
            rows = df.values.tolist()
            mapping.append({"sheet": sheet, "headers": df.columns.tolist(), "rows": rows[:20]}) # Sample 20 rows

    with open('scratch/excel_audit_raw.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
        
except Exception as e:
    print(f"Error: {e}")
