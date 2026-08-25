import sys
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.suunto.com/en-ca/Products/sports-watches/suunto-core-2/suunto-core-2-all-black/"
NTFY_TOPIC = "suunto_core_2"

def send_push(title, message, priority="5"):
    try:
        headers = {
            "Title": title,
            "Priority": priority,
            "Click": URL,
            "Tags": "watch,shopping_cart"
        }
        response = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers=headers,
            timeout=10
        )
        print(f"Push sent! Response status: {response.status_code}")
    except Exception as e:
        print(f"Push error: {e}")

def check_stock():
    with sync_playwright() as p:
        # Launch headless browser with standard desktop user agent
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("Loading page in headless browser...")
            page.goto(URL, wait_until="networkidle", timeout=30000)
            
            # Wait 3 seconds for client-side JS to fully render button states
            page.wait_for_timeout(3000)
            
            page_text = page.content().lower()
            
            # Look for active buy buttons rendered in the DOM
            buy_button = page.query_selector("button:has-text('Add to cart'), button:has-text('Buy now')")
            
            # Strict out of stock text check across rendered page
            is_out_of_stock = "out of stock" in page_text or "sold out" in page_text or "notify me" in page_text
            
            in_stock = False
            if buy_button and not is_out_of_stock:
                # Check if the rendered button is actually clickable and not disabled
                if buy_button.is_enabled() and buy_button.is_visible():
                    in_stock = True

            if in_stock:
                send_push("Suunto Core 2 IN STOCK!", "The Suunto Core 2 All Black is available now! Tap to purchase.", priority="5")
                print("Stock detected! Alert sent.")
            else:
                print("Still out of stock. Staying silent.")

        except Exception as e:
            print(f"Error checking page: {e}")
            
        browser.close()

if __name__ == "__main__":
    check_stock()
