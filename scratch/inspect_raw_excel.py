
import pandas as pd

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

try:
    xl = pd.ExcelFile(file_path)
    df = pd.read_excel(file_path, sheet_name='Housekeeping_tương đương', header=None, nrows=20)
    print("--- Housekeeping_tương đương Raw Top 20 ---")
    # Print with column indices to help identify positions
    print(df.to_string(index=False))
except Exception as e:
    print(f"Error: {e}")
