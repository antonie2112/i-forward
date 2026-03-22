from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.ecolab.com/sds-search?countryCode=Vietnam")
    page.wait_for_timeout(3000)
    
    # Fill search input and click
    try:
        # Assuming there is an input like input[type='text']
        inputs = page.query_selector_all("input[type='text']")
        if inputs:
            for inp in inputs:
                if inp.is_visible():
                    inp.fill("Oasis")
                    page.keyboard.press("Enter")
                    time.sleep(3)
                    print("Current URL after search:", page.url)
                    break
        else:
            print("No visible text input found.")
    except Exception as e:
        print("Error:", e)
        
    browser.close()
