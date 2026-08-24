
import pandas as pd

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def inspect_dilution_columns(sheet_name):
    xl = pd.ExcelFile(file_path)
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=5)
    print(f"--- {sheet_name} Headers ---")
    print(df.to_string())

inspect_dilution_columns('Kitchen')
inspect_dilution_columns('Housekeeping_tương đương')
