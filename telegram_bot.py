import requests
from config import BOT_TOKEN, CHAT_ID


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload, timeout=10)

    if response.status_code != 200:
        print("Telegram error:", response.text)
        return False

    return True


def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    payload = {
        "timeout": 1
    }

    if offset is not None:
        payload["offset"] = offset

    response = requests.get(url, params=payload, timeout=5)

    if response.status_code != 200:
        print("Telegram getUpdates error:", response.text)
        return []

    data = response.json()
    return data.get("result", [])