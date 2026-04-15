import json
import os
import re

def categorize(name, content_en="", content_vi=""):
    name = name.lower()
    content = (content_en + " " + content_vi).lower()
    
    # Laundry Keywords
    laundry_keywords = [
        r"\blaundry\b", r"\bgiặt\b", r"\bvải\b", r"\blinen\b", r"\bbleach\b", r"\bsoftener\b", r"\bstarch\b", 
        r"\boxybrite\b", r"\bsour\b", r"\bbuilder\b", r"\bdet plus\b", r"\beco-star\b", r"\becostar\b", 
        r"\bsericol\b", r"\bturbo\b", r"\beco-brite\b"
    ]
    
    # Kitchen Keywords
    kitchen_keywords = [
        r"\bkitchen\b", r"\bbếp\b", r"\bdish\b", r"\brửa chén\b", r"\brửa bát\b", r"\bpot\b", r"\bpan\b", 
        r"\bdegreaser\b", r"\boven\b", r"\bfryer\b", r"\bgreasecutter\b", r"\btopax\b", r"\bxy-12\b", 
        r"\bvegi\b", r"\bfruit\b", r"\bvegetable\b", r"\bdip it\b", r"\blime away\b", r"\brinse dry\b", 
        r"\bsuper trump\b", r"\bsmartpower\b", r"\bsolid power\b"
    ]
    
    # Housekeeping Keywords
    housekeeping_keywords = [
        r"\bbathroom\b", r"\btoilet\b", r"\bfloor\b", r"\bglass\b", r"\bcarpet\b", r"\bsàn\b", r"\bkính\b", 
        r"\bthảm\b", r"\bair freshener\b", r"\broom\b", r"\bphòng\b", r"\bfurniture\b", r"\bmarble\b", 
        r"\bpolish\b", r"\bstripper\b", r"\bacid bathroom\b", r"\bmiraglo\b", r"\bfuture dc\b", 
        r"\bsanigard\b", r"\bmop dressing\b", r"\bdeep gloss\b", r"\bcarestrip\b", r"\blemon-eze\b",
        r"\blemon eze\b", r"\bstainless steel\b", r"\bhand fresh plus\b"
    ]
    
    def matches(keywords, text):
        return any(re.search(k, text) for k in keywords)
    
    combined_text = name + " " + content
    
    # Priority matching
    if matches(laundry_keywords, combined_text):
        return "Laundry"
    if matches(kitchen_keywords, combined_text):
        return "Kitchen"
    if matches(housekeeping_keywords, combined_text):
        return "Housekeeping"
        
    return "Housekeeping" # Default to Housekeeping

def process_file(filepath, is_list=False):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if is_list:
        for item in data:
            name = item.get("name", "")
            specs = item.get("specs", "")
            item["sector"] = categorize(name, specs)
    else:
        for key in data:
            item_data = data[key]
            en = item_data.get("en", {})
            vi = item_data.get("vi", {})
            en_text = en.get("properties", "") + " " + en.get("usage", "")
            vi_text = vi.get("properties", "") + " " + vi.get("usage", "")
            item_data["sector"] = categorize(key, en_text, vi_text)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Processed {filepath}")

categories_base = {
    "public/catsheets.json": False,
    "public/guidex_data.json": False,
    "public/products_2026.json": True
}

for path, is_list in categories_base.items():
    working_path = os.path.join("/Users/nguyenphong/Desktop/Inst.sale", path)
    process_file(working_path, is_list)
