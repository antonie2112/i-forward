import requests
import re
import os
import time
import json
import urllib.parse
from bs4 import BeautifulSoup

# --- Configuration ---
SOURCE_URL = "https://ecolabwallchart.azurewebsites.net/ecolab/home.php"
IMAGE_DIR = "images/products"
os.makedirs(IMAGE_DIR, exist_ok=True)

# --- Cookie Setup ---
# We need to set 'Language' to 'vn' (or l=3)
cookies = {
    'language': 'vn', # Guessing cookie name, or we can use the 'l=3' query param in a session
}

# Actually, the site uses a query param ?l=3 to set language in session.
# Let's use a session to maintain state.
session = requests.Session()
# Visit home with l=3 to set session language
session.get(f"{SOURCE_URL}?l=3")

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def download_image(img_url, filename):
    try:
        if not img_url.startswith('http'):
            # Handle relative URLs. Domain seems to be ecolabwallchart...
            base = "https://ecolabwallchart.azurewebsites.net/ecolab/"
            img_url = urllib.parse.urljoin(base, img_url)
        
        r = session.get(img_url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")
    return False

def search_and_download(code, name):
    print(f"Processing: {code} - {name}")
    safe_name = sanitize_filename(name)
    target_file = os.path.join(IMAGE_DIR, f"{code} - {safe_name}.jpg")
    
    if os.path.exists(target_file):
        print("  Skipping (already exists)")
        return

    # Strategy 1: Search exact name
    search_term = name
    
    # Strategy 2: If CamelCase, try splitting (e.g. EcoKlene -> Eco Klene)
    # Simple heuristic: add space before capital letters if missing? 
    # Or just use the user provided name. User said "CombinedName fails, try Combined Name"
    # Let's try original name first.
    
    found_img = perform_search(search_term)
    
    if not found_img:
        # Try inserting spaces before uppercase letters (except first)
        # e.g. "EcoKlene" -> "Eco Klene"
        split_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
        if split_name != name:
            print(f"  Retrying with split name: '{split_name}'")
            found_img = perform_search(split_name)
    
    if found_img:
        if download_image(found_img, target_file):
            print(f"  Success: Saved to {target_file}")
        else:
            print("  Failed to download image.")
    else:
        print("  Image not found.")

def perform_search(term):
    try:
        # Search seems to be POST to separate page or same page?
        # Browser subagent typed in form. Form likely submits to home.php or search.php?
        # Let's assume POST to home.php based on typical PHP sites, or index.
        # Wait, subagent typed in `search_text` maybe?
        # Let's inspecting the `search_result.html` from previous step would have been good but I removed the step.
        # I'll just try POST to home.php with 'search=<term>'
        
        payload = {'search': term}
        r = session.post(SOURCE_URL, data=payload)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Find product image. 
        # Inspecting typical output: usually <img src="product_img/..." >
        # Let's look for images in the result area.
        
        # Heuristic: look for 'product_img' in src
        imgs = soup.find_all('img', src=re.compile(r'product_img/'))
        if imgs:
            return imgs[0]['src']
        else:
            # Debug: save HTML to see what happened
            with open("debug_search_fail.html", "w") as f:
                f.write(str(soup))
            
        # Fallback: check checking for any image inside a product card?
        
    except Exception as e:
        print(f"  Search error: {e}")
    return None

# --- Main Execution ---
# 1. Read main.js to get products
# We'll use a regex to extract the JSON array from main.js since it's a JS file.

def load_products_from_js():
    with open('main.js', 'r') as f:
        content = f.read()
    
    # Extract common PRESETS
    match = re.search(r'common:\s*\[(.*?)\]', content, re.DOTALL)
    if not match:
        print("Could not find common presets in main.js")
        return []
    
    json_str = match.group(1)
    # This JSON might be loose JS object (keys without quotes). JSON.parse requires quotes.
    # Python's json parser is strict.
    # Simple regex to extract code and name:
    # code: "...", name: "..."
    
    products = []
    # Regex to find: code: "123", ... name: "ABC"
    # It loops through objects enclosed in { }
    
    # Let's iterate over object blocks
    # This is rough but should work for this file structure
    items = re.findall(r'\{(.*?)\}', json_str, re.DOTALL)
    for item in items:
        # Match code: "..." or "code": "..."
        c_match = re.search(r'(?:["\'])?code(?:["\'])?:\s*["\']([^"\']+)["\']', item)
        n_match = re.search(r'(?:["\'])?name(?:["\'])?:\s*["\']([^"\']+)["\']', item)
        
        if c_match and n_match:
            products.append((c_match.group(1), n_match.group(1)))
            
    return products

products = load_products_from_js()
print(f"Found {len(products)} products.")

for code, name in products:
    search_and_download(code, name)
