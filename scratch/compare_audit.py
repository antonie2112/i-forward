
import json

excel_file = 'scratch/brute_force_mappings.json'
json_file = 'public/dmap_data.json'

with open(excel_file, 'r', encoding='utf-8') as f:
    excel_data = json.load(f)

with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Normalize functions
def norm(s):
    return str(s).lower().strip().replace('  ', ' ')

# Map Diversey Name -> Ecolab Name from Excel
excel_map = {}
for m in excel_data:
    excel_map[norm(m['diversey'])] = m['ecolab']

# Map Diversey Name -> Ecolab Name from JSON
json_map = {}
for j in json_data:
    json_map[norm(j['DiverseyShort'])] = j['Ecolab']

# Findings
mismatches = []
missing_in_json = []

for div_name, eco_name in excel_map.items():
    if div_name in json_map:
        if norm(json_map[div_name]) != norm(eco_name):
            mismatches.append({
                "product": div_name,
                "excel": eco_name,
                "json": json_map[div_name]
            })
    else:
        missing_in_json.append({
            "product": div_name,
            "excel": eco_name
        })

print(f"--- Mismatches ({len(mismatches)}) ---")
for m in mismatches:
    print(f"{m['product']}: JSON={m['json']} != EXCEL={m['excel']}")

print(f"\n--- Missing in JSON ({len(missing_in_json)}) ---")
for m in missing_in_json:
    print(f"{m['product']} -> {m['excel']}")
