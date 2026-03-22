from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        def handle_request(route):
            if route.request.resource_type in ["xhr", "fetch"]:
                print(f"--- Intercepted Request to {route.request.url} ---")
                print(f"Post Data: {route.request.post_data}")
            route.continue_()
            
        page.route("**/*", handle_request)
        
        print("Navigating...")
        page.goto("https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3")
        page.wait_for_selector("input[placeholder='Search by product name']", timeout=15000)
        
        print("Searching...")
        page.fill("input[placeholder='Search by product name']", "Miraglo")
        page.click("button:has-text('Search')")
        
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    run()
