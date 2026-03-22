import re
import json

def round_presets_discount():
    js_path = 'main.js'

    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the PRESETS block
    match = re.search(r'const PRESETS = (\{[\s\S]*?\n\});', content)
    if not match:
        print("Error: Could not find PRESETS object block in main.js")
        return

    json_str = match.group(1)
    
    # Preprocess to valid JSON
    json_str_fixed = re.sub(r'(?<!")\b(\w+)\s*:', r'"\1":', json_str)
    
    try:
        presets = json.loads(json_str_fixed)
    except json.JSONDecodeError as e:
        print(f"Error parsing PRESETS JSON from main.js: {e}")
        return

    updated_count = 0

    # Round discountPrice in all arrays
    for key, items in presets.items():
        for item in items:
            if 'discountPrice' in item:
                original = item['discountPrice']
                rounded = round(float(original))
                if original != rounded:
                    item['discountPrice'] = rounded
                    updated_count += 1

    if updated_count == 0:
        print("No preset discount prices needed rounding.")
    else:
        # Reconstruct JSON with indent 4
        new_json_str = json.dumps(presets, ensure_ascii=False, indent=4)
        # Remove quotes from keys to match JS style
        new_json_str = re.sub(r'"(\w+)":', r'\1:', new_json_str)
        
        new_content = content[:match.start(1)] + new_json_str + content[match.end(1):]
        
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\nSuccessfully rounded {updated_count} discount prices in PRESETS.")


if __name__ == "__main__":
    round_presets_discount()
