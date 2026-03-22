from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000")
    page.wait_for_timeout(2000)
    
    # Click SDS Viewer tab
    tabs = page.query_selector_all(".tab-btn")
    if len(tabs) >= 3:
        tabs[2].click()
        
    page.wait_for_timeout(1000)
    page.screenshot(path="local_preview_sds.png", full_page=True)
    browser.close()
