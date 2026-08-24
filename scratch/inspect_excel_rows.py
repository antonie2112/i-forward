
import pandas as pd

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

try:
    xl = pd.ExcelFile(file_path)
    df = pd.read_excel(file_path, sheet_name='Housekeeping_tương đương', nrows=10)
    print("--- Housekeeping_tương đương Top 10 ---")
    print(df.to_string())
    
    df_kitchen = pd.read_excel(file_path, sheet_name='Kitchen', nrows=10)
    print("\n--- Kitchen Top 10 ---")
    print(df_kitchen.to_string())
    
except Exception as e:
    print(f"Error: {e}")
