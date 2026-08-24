
import json

excel_file = 'scratch/brute_force_mappings.json'
json_file = 'public/dmap_data.json'

with open(excel_file, 'r', encoding='utf-8') as f:
    excel_data = json.load(f)

with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

def norm(s): return str(s).lower().strip().replace('  ', ' ')

json_shorts = {norm(j['DiverseyShort']) for j in json_data}
json_longs = {norm(j['Diversey']) for j in json_data}

missing = []
for ex in excel_data:
    div = norm(ex['diversey'])
    if div not in json_shorts and div not in json_longs:
        missing.append(ex)

print(f"--- Missing Products ({len(missing)}) ---")
for m in missing:
    print(f"{m['diversey']} -> {m['ecolab']} ({m['sheet']})")
