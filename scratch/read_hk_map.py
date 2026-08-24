
import pandas as pd

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

try:
    df = pd.read_excel(file_path, sheet_name='Housekeeping_tương đương')
    # Filter for Forward DC
    # The columns might be Unnamed: X. Let's look for rows containing 'Forward DC'
    for index, row in df.iterrows():
        row_str = row.astype(str).str.cat(sep=' | ')
        if 'Forward DC' in row_str:
            print(f"Row {index}: {row_str}")
except Exception as e:
    print(f"Error: {e}")
