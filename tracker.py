import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.suunto.com/en-ca/Products/sports-watches/suunto-core-2/suunto-core-2-all-black/"
NTFY_TOPIC = "suunto_core_2"  # Put your exact ntfy topic name here

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_push(title, message, priority="default"):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode('utf-8'),
            headers={"Title": title, "Priority": priority, "Click": URL, "Tags": "watch,shopping_cart"},
            timeout=10
        )
    except Exception as e:
        print(f"Push error: {e}")

try:
    response = requests.get(URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text().lower()

    if "buy now" in page_text and "out of stock" not in page_text:
        send_push("🚨 Suunto Core 2 IN STOCK!", "The Suunto Core 2 All Black is available now! Tap to purchase.", priority="5")
    else:
        print("Still out of stock.")
except Exception as e:
    print(f"Error checking page: {e}")
