from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000")
    page.wait_for_timeout(1000)
    
    # 3. Proposal Tab
    tabs = page.query_selector_all(".tab-btn")
    if len(tabs) >= 4:
        tabs[3].click()
    page.wait_for_timeout(1000)
    
    # Screenshot
    page.screenshot(path="local_preview_proposal.png", full_page=True)

    browser.close()
