import requests

NTFY_TOPIC = "YOUR_NTFY_TOPIC_HERE"

requests.post(
    f"https://ntfy.sh/{NTFY_TOPIC}",
    data="Test ping from GitHub Actions!".encode('utf-8'),
    headers={"Title": "Test Notification", "Priority": "3", "Tags": "bell"}
)
