from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8000/test_iframe.html")
    page.wait_for_timeout(3000)
    page.screenshot(path="test_iframe.png")
    browser.close()
