from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000")
    page.wait_for_timeout(2000)
    
    # Click Catsheets tab
    tabs = page.query_selector_all(".tab-btn")
    if len(tabs) >= 2:
        tabs[1].click()
        
    page.wait_for_timeout(500)
    
    # Type Oasis
    page.fill("#librarySearchInput", "Oasis")
    page.wait_for_timeout(1000)
    
    page.screenshot(path="local_preview_lib.png", full_page=True)
    browser.close()
