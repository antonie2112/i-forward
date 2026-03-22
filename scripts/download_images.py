import requests
from bs4 import BeautifulSoup
import urllib.parse
import json
import os
import re
import time

URL = "https://ecolabwallchart.azurewebsites.net/ecolab/show_result.php"
BASE_URL = "https://ecolabwallchart.azurewebsites.net/ecolab/"
IMAGE_DIR = "Product images"

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def sanitize_filename(name):
    # Remove chars invalid in macOS/Windows filenames
    return re.sub(r'[\\/*?:\"<>|]', "", name).strip()

def search_api(term):
    payload = {
        "q": term,
        "s": "0",
        "lang": "vn|",
        "table": "3",
        "page": "1"
    }
    try:
        r = requests.post(URL, data=payload, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = soup.find_all('img', class_='product-image')
        
        for img in imgs:
            src = img.get('src', '')
            clean_src = src.split('?')[0] if '?' in src else src
            if clean_src:
                return urllib.parse.urljoin(BASE_URL, clean_src)
    except Exception as e:
        pass
    return None

def download_image(url, filepath):
    try:
        # Check if already downloaded
        if os.path.exists(filepath):
            return True
            
        r = requests.get(url, stream=True, timeout=10)
        if r.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def run():
    try:
        with open('products.json', 'r') as f:
            products = json.load(f)
    except FileNotFoundError:
        print("products.json not found")
        return
        
    print(f"Loaded {len(products)} products to check/download.")
    
    success_count = 0
    not_found = []
    
    for prod in products:
        code = prod['code']
        name = prod['name']
        print(f"\nProcessing: {code} - {name}")
        
        safe_name = sanitize_filename(name)
        safe_code = sanitize_filename(code)
        filename = f"{safe_code} - {safe_name}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)
        
        if os.path.exists(filepath):
            print(f"  Already exists locally: {filename}")
            success_count += 1
            continue
            
        img_url = search_api(name)
        
        # Strategies for name variations
        if not img_url:
            # 1. Without spaces (e.g. Lemon Eze -> LemonEze)
            no_spaces = name.replace(" ", "")
            if no_spaces != name:
                img_url = search_api(no_spaces)
                
        if not img_url:
            # 2. Insert spaces before uppercase if it doesn't have spaces (EcoKlene -> Eco Klene)
            if " " not in name:
                split_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', name).strip()
                if split_name != name:
                    img_url = search_api(split_name)
                    
        if not img_url:
            # 3. Simple transformations or common typos
            if "Floordress" in name:
                img_url = search_api(name.replace("Floordress", "").strip())
        
        if img_url:
            print(f"  Found URL: {img_url}")
            if download_image(img_url, filepath):
                print(f"  Downloaded: {filename}")
                success_count += 1
            else:
                print("  Download failed.")
        else:
            print("  Image completely not found.")
            not_found.append(name)
            
        time.sleep(0.5) # Gentle rate limiting
        
    print(f"\nOverall Processed: {success_count}/{len(products)} found and downloaded.")
    if not_found:
        print(f"Missing images for: {', '.join(not_found)}")

if __name__ == "__main__":
    run()
