import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing. Check your .env file.")

if not CHAT_ID:
    raise ValueError("CHAT_ID is missing. Check your .env file.")

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "DOGEUSDT",
    "ADAUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "BNBUSDT"
]

CHECK_INTERVAL_SECONDS = 10
LOOKBACK_SECONDS = 60
ALERT_THRESHOLD_PERCENT = 0.03
COOLDOWN_SECONDS = 30