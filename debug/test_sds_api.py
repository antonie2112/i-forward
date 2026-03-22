from playwright.sync_api import sync_playwright
import time

def handle_response(response):
    try:
        url = response.url.lower()
        if "sds" in url and response.request.resource_type in ["fetch", "xhr"]:
            print(f"URL: {response.url}")
            print(f"Status: {response.status}")
            try:
                print("Headers:")
                for k, v in response.headers.items():
                    if k.lower() in ['access-control-allow-origin', 'content-type']:
                        print(f"  {k}: {v}")
                text = response.text()
                print(f"Response length: {len(text)}")
                if len(text) > 0:
                    print(f"Preview: {text[:200]}")
            except Exception as e:
                pass
            print("-" * 40)
    except Exception as e:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on("response", handle_response)
    
    print("Navigating...")
    page.goto("https://www.ecolab.com/sds-search?query=Oasis&countryCode=Vietnam")
    
    page.wait_for_timeout(5000)
    browser.close()
