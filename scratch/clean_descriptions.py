
import json

json_path = 'public/dmap_data.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

phrases_to_remove = [
    " theo đề xuất danh mục Phu Quoc",
    " theo đề xuất danh mục Phu Quốc",
    " theo đề xuất danh mục Phu Quốc.",
    " theo đề xuất danh mục Phu Quoc.",
    "theo đề xuất danh mục Phu Quoc",
    "theo đề xuất danh mục Phu Quốc"
]

for entry in data:
    if 'Description' in entry:
        for phrase in phrases_to_remove:
            entry['Description'] = entry['Description'].replace(phrase, "")
        entry['Description'] = entry['Description'].strip()
        # Clean up double periods if they exist after removal
        entry['Description'] = entry['Description'].replace('..', '.').strip()
        
    if 'Features' in entry:
        for phrase in phrases_to_remove:
            entry['Features'] = entry['Features'].replace(phrase, "")
        entry['Features'] = entry['Features'].strip()

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Successfully cleaned descriptions.")
