import requests

URL = "https://ecolabwallchart.azurewebsites.net/ecolab/show_result.php"
BASE_URL = "https://ecolabwallchart.azurewebsites.net/ecolab/"

payloads = [
    {"q": "Miraglo", "lang": "3", "table": "3", "page": "1"},
    {"q": "Miraglo", "s[]": "", "lang": "3", "table": "3", "page": "1"},
    {"q": "Miraglo", "s": "", "lang": "3", "table": "3", "page": "1"},
    "q=Miraglo&lang=3&table=3&page=1"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Origin": "https://ecolabwallchart.azurewebsites.net",
    "Referer": "https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3",
    "Content-Type": "application/x-www-form-urlencoded"
}

for i, p in enumerate(payloads):
    try:
        if isinstance(p, dict):
            r = requests.post(URL, data=p, headers=headers, timeout=10)
        else:
            r = requests.post(URL, data=p, headers=headers, timeout=10)
        print(f"Payload {i} response length: {len(r.text)}")
    except Exception as e:
        print(f"Payload {i} Error: {e}")

