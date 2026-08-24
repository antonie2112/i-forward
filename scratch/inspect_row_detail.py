
import pandas as pd

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def inspect_product_row(sheet_name, prod_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    rows = df.values.tolist()
    for row in rows:
        if prod_name.upper() in str(row[2]).upper(): # Typically Product is column 2
            print(f"--- {sheet_name}: {prod_name} ---")
            for i, val in enumerate(row):
                print(f"Col {i}: {val}")
            break

inspect_product_row('Housekeeping_tương đương', 'Glance 101')
inspect_product_row('Kitchen', 'SUMA J512')
