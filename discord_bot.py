import requests
from config import DISCORD_WEBHOOK_URL


def send_discord_message(message):
    if not DISCORD_WEBHOOK_URL:
        return False

    payload = {
        "content": message
    }

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload,
        timeout=10
    )

    if response.status_code not in [200, 204]:
        print("Discord error:", response.text)
        return False

    return True