import os
import requests

NTFY_TOPIC = os.getenv("NTFY_TOPIC")
URL = "https://www.suunto.com/en-ca/Products/sports-watches/suunto-core-2/suunto-core-2-all-black/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def check_stock():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        page_text = response.text

        # Triggers ONLY when "Out of stock" is removed from the product page
        if "Out of stock" not in page_text:
            requests.post(
                f"https://ntfy.sh/{NTFY_TOPIC}",
                data="Suunto Core 2 All Black is back IN STOCK!".encode("utf-8"),
                headers={
                    "Title": "STOCK ALERT: Suunto Core 2",
                    "Priority": "high",
                    "Tags": "watch,tada"
                }
            )
            print("Stock detected! Notification sent via ntfy.")
        else:
            print("Item is still out of stock.")

    except Exception as e:
        print(f"Error checking stock: {e}")

if __name__ == "__main__":
    check_stock()
