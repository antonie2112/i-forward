import openpyxl
import json

def build_database():
    excel_file = "Price_2026_tier_E.xlsx"
    common_data_file = "common_data.json"
    output_file = "products_2026.json"

    # Load common data to get specs and dilution
    common_map = {}
    try:
        with open(common_data_file, 'r', encoding='utf-8') as f:
            common_data = json.load(f)
            for item in common_data:
                code = str(item.get("code", "")).strip()
                if code:
                    common_map[code] = {
                        "specs": item.get("specs", ""),
                        "dilution": item.get("dilution", "")
                    }
    except Exception as e:
        print(f"Error loading common_data.json: {e}")

    # Load 2026 Prices
    wb = openpyxl.load_workbook(excel_file, data_only=True)
    ws = wb.active

    products = []
    
    # Headers are on row 1: Category, PH L2/ INNOVATION, Code, Item, Packing, Unit Price
    for row in ws.iter_rows(min_row=2, values_only=True):
        code = str(row[2]).strip() if row[2] else ""
        item_name = str(row[3]).strip() if row[3] else ""
        packing = str(row[4]).strip() if row[4] else ""
        price_val = row[5]

        if code and code != "None":
            try:
                price = float(price_val)
            except:
                price = 0

            specs = ""
            dilution = ""
            if code in common_map:
                specs = common_map[code]["specs"]
                dilution = common_map[code]["dilution"]

            product = {
                "code": code,
                "name": item_name,
                "specs": specs,
                "unit": packing,
                "price": price,
                "dilution": dilution
            }
            products.append(product)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {output_file} with {len(products)} products.")

if __name__ == "__main__":
    build_database()
