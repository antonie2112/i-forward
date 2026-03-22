import re
import json
import os

def load_products_from_js():
    with open('main.js', 'r') as f:
        content = f.read()
    
    # Extract common PRESETS
    match = re.search(r'common:\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        print("Could not find common presets in main.js")
        return []
    
    json_str = match.group(1)
    
    products = []
    items = re.findall(r'\{(.*?)\}', json_str, re.DOTALL)
    for item in items:
        # Match code: "..." or "code": "..."
        c_match = re.search(r'(?:["\'])?code(?:["\'])?:\s*["\']([^"\']+)["\']', item)
        n_match = re.search(r'(?:["\'])?name(?:["\'])?:\s*["\']([^"\']+)["\']', item)
        
        if c_match and n_match:
            products.append({
                "code": c_match.group(1),
                "name": n_match.group(1)
            })
            
    return products

products = load_products_from_js()
print(f"Found {len(products)} products.")

with open('products.json', 'w') as f:
    json.dump(products, f, indent=2)
    
print("Saved to products.json")
