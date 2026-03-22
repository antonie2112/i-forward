from playwright.sync_api import sync_playwright
import os

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        abs_path = os.path.abspath('index.html')
        page.goto(f"file://{abs_path}")
        
        # Click the 'Common Items' card or call function
        page.evaluate("selectQuoteType('common')")
        page.wait_for_timeout(2000)
        
        # Take screenshot
        page.screenshot(path="local_preview_table.png", full_page=True)
        print("Screenshot saved to local_preview_table.png")
        
        browser.close()

if __name__ == "__main__":
    take_screenshot()
