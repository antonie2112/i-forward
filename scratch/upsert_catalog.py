
import pandas as pd
import json

file_path = '/Users/nguyenphong/Desktop/data_raw/Premier Village Phu Quoc- Bảng so sánh giá Ecolab_ Diversey.xlsx'
json_path = 'public/dmap_data.json'

def get_full_excel_data():
    xl = pd.ExcelFile(file_path)
    sheets = ['Kitchen', 'Housekeeping_tương đương']
    full_list = []
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=None)
        rows = df.values.tolist()
        
        div_col, eco_col, app_col, cat_col = -1, -1, -1, -1
        
        for r_idx, row in enumerate(rows):
            row_str = [str(x).upper() for x in row]
            if 'DIVERSEY' in row_str and any('ECOLAB' in x for x in row_str):
                div_col = row_str.index('DIVERSEY')
                if 'APPLICATION' in row_str: app_col = row_str.index('APPLICATION')
                if 'DEPARTMENT' in row_str: cat_col = row_str.index('DEPARTMENT')
                
                if 'PRODUCT NAME' in row_str:
                    eco_col = row_str.index('PRODUCT NAME')
                else:
                    for c_idx in range(div_col + 1, len(row_str)):
                        if 'PRODUCT' in row_str[c_idx] or 'ECOLAB' in row_str[c_idx]:
                            eco_col = c_idx
                            break
                
                if div_col != -1 and eco_col != -1:
                    for data_row in rows[r_idx+1:]:
                        div_val = str(data_row[div_col]).strip()
                        eco_val = str(data_row[eco_col]).strip()
                        app_val = str(data_row[app_col]).strip() if app_col != -1 else ""
                        cat_val = str(data_row[cat_col]).strip() if cat_col != -1 else sheet
                        
                        if div_val != 'nan' and div_val != '' and 'TOTAL' not in div_val.upper() \
                           and eco_val != 'nan' and eco_val != '':
                            full_list.append({
                                "Category": "Kitchen" if "KITCHEN" in cat_val.upper() or "KH" in cat_val.upper() else "Housekeeping",
                                "Diversey": div_val,
                                "DiverseyShort": div_val.split(' ')[0] + (' ' + div_val.split(' ')[1] if len(div_val.split(' ')) > 1 else ''),
                                "Ecolab": eco_val,
                                "Description": app_val.replace('\n', ' '),
                                "Features": "Đang cập nhật...",
                                "Technical": { "pH": "-", "Appearance": "-", "Dilution": "-" },
                                "Safety": { "Signal": "Lưu ý", "Hazards": "-" },
                                "Cost": { "dilution_eco": "-", "dilution_div": "-", "cost_per_task_eco": "-", "cost_per_task_div": "-", "unit_price": "-" }
                            })
                    break
    return full_list

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        existing_json = json.load(f)
    
    excel_data = get_full_excel_data()
    
    # Normalize helper
    def norm(s): return str(s).lower().strip().replace('  ', ' ')
    
    existing_map = {norm(j['DiverseyShort']): j for j in existing_json}
    
    added = 0
    updated = 0
    
    for ex in excel_data:
        ex_short = norm(ex['DiverseyShort'])
        if ex_short in existing_map:
            # Update mapping
            target = existing_map[ex_short]
            if target['Ecolab'] != ex['Ecolab']:
                target['Ecolab'] = ex['Ecolab']
                updated += 1
        else:
            # Add new entry
            existing_json.append(ex)
            existing_map[ex_short] = ex
            added += 1
            
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(existing_json, f, ensure_ascii=False, indent=2)
        
    print(f"Upsert Complete. Added {added}, Updated {updated}.")
except Exception as e:
    print(f"Error: {e}")
