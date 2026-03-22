from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000")
    page.wait_for_timeout(1000)
    
    # Take screenshot of builder selection page
    page.screenshot(path="local_preview_brand.png")
    
    # Enter first category to show buttons 
    cards = page.query_selector_all(".selection-card")
    if cards:
        cards[0].click()
        
    page.wait_for_timeout(1000)
    # Scroll slightly down
    page.evaluate("window.scrollBy(0, 300)")
    page.wait_for_timeout(500)
    
    page.screenshot(path="local_preview_brand_table.png")
    
    browser.close()
