
import pandas as pd

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'

def find_product_mapping(sheet_name, search_terms):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # Find rows containing search terms
        results = []
        for idx, row in df.iterrows():
            row_str = " ".join([str(x) for x in row.tolist()]).upper()
            if any(term.upper() in row_str for term in search_terms):
                results.append(row.tolist())
        return results
    except Exception as e:
        return str(e)

print("--- Searching for Glance in Housekeeping_tương đương ---")
glance_rows = find_product_mapping('Housekeeping_tương đương', ['Glance', 'Miraglo', 'Oasis 197'])
for r in glance_rows:
    print(r)

print("\n--- Searching for Forward in Housekeeping_tương đương ---")
forward_rows = find_product_mapping('Housekeeping_tương đương', ['Forward'])
for r in forward_rows:
    print(r)
