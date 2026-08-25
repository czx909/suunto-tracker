import requests
from bs4 import BeautifulSoup

URL = "https://www.suunto.com/en-ca/Products/sports-watches/suunto-core-2/suunto-core-2-all-black/"
NTFY_TOPIC = "suunto_core_2"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

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

try:
    response = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Target button elements specifically instead of searching global text
    buttons = soup.find_all(["button", "a"])
    
    # Filter for buttons directly associated with purchasing this item
    buy_buttons = [
        btn for btn in buttons 
        if "add to cart" in btn.get_text().lower() or "buy now" in btn.get_text().lower()
    ]
    
    # Check if a buy button exists AND is not disabled/hidden
    in_stock = False
    for btn in buy_buttons:
        is_disabled = btn.has_attr("disabled") or "disabled" in btn.get("class", [])
        if not is_disabled:
            in_stock = True
            break

    # Alternative check: explicit "out of stock" notice in the buy area
    page_text = soup.get_text().lower()
    if "notify me when available" in page_text or "out of stock" in page_text:
        in_stock = False

    if in_stock:
        send_push("Suunto Core 2 IN STOCK!", "The Suunto Core 2 All Black is available now! Tap to purchase.", priority="5")
        print("Stock detected! Alert sent.")
    else:
        print("Still out of stock. Staying silent.")

except Exception as e:
    print(f"Error checking page: {e}")
