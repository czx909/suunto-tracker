import os
import requests
from playwright.sync_api import sync_playwright

NTFY_TOPIC = os.getenv("NTFY_TOPIC")
URL = "https://www.suunto.com/en-ca/Products/sports-watches/suunto-core-2/suunto-core-2-all-black/"

def check_stock():
    with sync_playwright() as p:
        # Launch a real, headless Chromium browser instance
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the product page and wait for network activity to settle
        page.goto(URL, wait_until="networkidle")
        
        # Extract full page body text after JavaScript has fully rendered
        content = page.content()
        browser.close()

        # Check if 'Out of stock' is absent or 'In stock' / 'Add to cart' appears
        if "Out of stock" not in content:
            # Send alert via ntfy
            requests.post(
                f"https://ntfy.sh/{NTFY_TOPIC}",
                data="Suunto Core 2 All Black is back IN STOCK!".encode("utf-8"),
                headers={
                    "Title": "STOCK ALERT: Suunto Core 2",
                    "Priority": "high",
                    "Tags": "watch,tada"
                }
            )

if __name__ == "__main__":
    check_stock()
