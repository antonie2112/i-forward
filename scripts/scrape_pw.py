from playwright.sync_api import sync_playwright
import json

def run():
    products_to_search = [
        "Miraglo", "Hand Fresh Plus", "Lemon Eze", "Mop Dressing A", "First Impression", 
        "Deep Gloss", "Floordress T500", "Floordress T510", "Floordress R600", "Pinnacle Marble Polishing Paste",
        "Wash n Walk", "Solitaire", "Trump", "Solid Sense", "Pantastic", 
        "Apex Power", "Apex Presoak", "Solid Brilliance", "Absorbit",
        "EcoKlene HD 20L", "Rinse Dry 20L", "Neo", "22 Multi Quat sanitizer", "Dip It Plus"
    ]
    
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36"
        )
        page = context.new_page()

        search_input_sel = "input[placeholder='Search by product name']"

        for prod in products_to_search:
            print(f"Searching for: {prod}")
            try:
                page.goto("https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3")
                page.wait_for_selector(search_input_sel, state="visible", timeout=15000)
                
                page.fill(search_input_sel, prod)
                page.press(search_input_sel, "Enter")
                
                # Wait for loading state
                page.wait_for_timeout(4000)
                
                images = page.locator(".product-image").all()
                found_url = None
                if images:
                    for img in images:
                        src = img.get_attribute("src")
                        if src:
                            clean_src = src.split('?')[0] if '?' in src else src
                            found_url = "https://ecolabwallchart.azurewebsites.net/ecolab/" + clean_src
                            break
                
                print(f"  -> Result: {found_url}")
                if found_url:
                    results.append({"name": prod, "image_url": found_url})
                else:
                    import re
                    split_name = re.sub(r'(?<!^)(?=[A-Z])', ' ', prod).strip()
                    if split_name != prod:
                        print(f"  Retrying as: {split_name}")
                        page.goto("https://ecolabwallchart.azurewebsites.net/ecolab/home.php?l=3")
                        page.wait_for_selector(search_input_sel, state="visible", timeout=15000)
                        
                        page.fill(search_input_sel, split_name)
                        page.press(search_input_sel, "Enter")
                        page.wait_for_timeout(4000)
                        
                        images = page.locator(".product-image").all()
                        if images:
                            for img in images:
                                src = img.get_attribute("src")
                                if src:
                                    clean_src = src.split('?')[0] if '?' in src else src
                                    found_url = "https://ecolabwallchart.azurewebsites.net/ecolab/" + clean_src
                                    break
                        print(f"  -> Retry Result: {found_url}")
                        if found_url:
                            results.append({"name": prod, "image_url": found_url})
            except Exception as e:
                print(f"  Error on {prod}: {e}")

        browser.close()
        
    print(f"Total crawled this session: {len(results)}")
    
    filename = 'image_urls_playwright.json'
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
