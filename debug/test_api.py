import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

URL = "https://ecolabwallchart.azurewebsites.net/ecolab/show_result.php"
BASE_URL = "https://ecolabwallchart.azurewebsites.net/ecolab/"

payload = {
    "q": "Miraglo",
    "s": "0",
    "lang": "vn|",
    "table": "3",
    "page": "1"
}

print(f"Testing API with q={payload['q']} lang={payload['lang']}")
try:
    r = requests.post(URL, data=payload, timeout=10)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    soup = BeautifulSoup(r.text, 'html.parser')
    imgs = soup.find_all('img', class_='product-image')
    
    for img in imgs:
        src = img.get('src', '')
        # Remove cache buster ?xxxx
        clean_src = src.split('?')[0] if '?' in src else src
        full_url = urllib.parse.urljoin(BASE_URL, clean_src)
        print("Found image:", full_url)
        
except Exception as e:
    print("Error:", e)
