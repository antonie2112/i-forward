import urllib.request
import json

url = "https://www.ecolab.com/sds-search?query=Oasis&countryCode=Vietnam"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        print(f"Fetched HTML of length: {len(html)}")
        # Check if there's a JSON blob
        if 'window.SDS_DATA' in html or 'results' in html:
            print("Found potential data")
        
        with open('debug_sds.html', 'w') as f:
            f.write(html)
except Exception as e:
    print("Error:", e)
