from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000")
    page.wait_for_timeout(1000)
    
    # Enable Dark Mode
    theme_btn = page.query_selector("#themeToggle")
    if theme_btn:
        theme_btn.click()
    page.wait_for_timeout(500)
    
    # 1. Catsheets Library
    tabs = page.query_selector_all(".tab-btn")
    if len(tabs) >= 2:
        tabs[1].click()
    page.wait_for_timeout(500)
    page.fill("#librarySearchInput", "Oasis")
    page.wait_for_timeout(1000)
    page.screenshot(path="local_preview_dark_lib.png", full_page=True)

    # 2. SDS Viewer
    if len(tabs) >= 3:
        tabs[2].click()
    page.wait_for_timeout(500)
    page.screenshot(path="local_preview_dark_sds.png")

    browser.close()
