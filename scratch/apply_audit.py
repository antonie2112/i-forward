
import json
import os

excel_file = 'scratch/brute_force_mappings.json'
json_file = 'public/dmap_data.json'

with open(excel_file, 'r', encoding='utf-8') as f:
    excel_data = json.load(f)

with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Normalize names for matching
def norm(s):
    return str(s).lower().strip().replace('  ', ' ')

# Map Diversey Name -> Ecolab Name from Excel
excel_map = {}
for m in excel_data:
    excel_map[norm(m['diversey'])] = m['ecolab']

# Map Diversey Name -> Sheet name from Excel
excel_sheet_map = {}
for m in excel_data:
    excel_sheet_map[norm(m['diversey'])] = m['sheet']

# Update JSON data
updated_count = 0
for entry in json_data:
    short_name = norm(entry['DiverseyShort'])
    long_name = norm(entry['Diversey'])
    
    # Try matching by short name
    if short_name in excel_map:
        new_eco = excel_map[short_name]
        if entry['Ecolab'] != new_eco:
            print(f"Updating {entry['DiverseyShort']}: {entry['Ecolab']} -> {new_eco}")
            entry['Ecolab'] = new_eco
            updated_count += 1
    # Try matching by long name (if short name didn't match or long name has a direct entry)
    elif long_name in excel_map:
        new_eco = excel_map[long_name]
        if entry['Ecolab'] != new_eco:
            print(f"Updating {entry['Diversey']}: {entry['Ecolab']} -> {new_eco}")
            entry['Ecolab'] = new_eco
            updated_count += 1

# Write back
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

print(f"\nAudit Complete. Updated {updated_count} products.")
