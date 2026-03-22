from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Navigating...")
        page.goto("https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3")
        page.wait_for_load_state("networkidle")
        
        print("Executing get_result('Miraglo', 1)...")
        # Initialize variables needed by get_result if any
        page.evaluate("lang = '3'; s = []; get_result('Miraglo', 1)")
        
        page.wait_for_timeout(3000)
        
        images = page.locator(".product-image").all()
        for img in images:
            print("Found image:", img.get_attribute("src"))
            
        browser.close()

if __name__ == "__main__":
    run()
