import sys
import random

# 25% chance to run every 5 minutes (averages out to running roughly every 20 mins randomly)
if random.random() > 0.25:
    print("Randomly skipping this run to randomize check intervals.")
    sys.exit(0)

import requests
from bs4 import BeautifulSoup

# Target product URL and your ntfy channel
URL = "https://www.suunto.com/en-ca/Products/sports-watches/suunto-core-2/suunto-core-2-all-black/"
NTFY_TOPIC = "suunto_core_2"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_push(title, message, priority="5"):
    try:
        # Pass headers with strict ASCII characters to avoid latin-1 encoding errors
        headers = {
            "Title": title.encode("utf-8").decode("latin-1"),
            "Priority": priority,
            "Click": URL,
            "Tags": "watch,shopping_cart"
        }
        
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers=headers,
            timeout=10
        )
    except Exception as e:
        print(f"Push error: {e}")

try:
    response = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text().lower()

    # Checks for active purchase options while ensuring it isn't listed as out of stock
    if "add to cart" in page_text or ("buy now" in page_text and "out of stock" not in page_text):
        send_push("Suunto Core 2 IN STOCK!", "The Suunto Core 2 All Black is available now! Tap to purchase.", priority="5")
        print("Stock detected! Alert sent.")
    else:
        print("Still out of stock. Staying silent.")
except Exception as e:
    print(f"Error checking page: {e}")
