# Crypto Telegram & Discord Alert Bot

A Python alert bot that monitors Binance crypto price movements and sends alerts to Telegram and Discord when a symbol moves beyond a configured percentage threshold.

This project was built as a reusable automation template: data source → Python logic → alert condition → Telegram notification.

## Features

* Monitors selected crypto pairs from Binance
* Calculates percentage movement over a configurable lookback window
* Sends Telegram alerts when movement passes the threshold
* Uses cooldown logic to avoid spam
* Stores private credentials safely with `.env`
* Simple modular structure for learning and future expansion
* Sends alerts to Telegram
* Sends alerts to Discord using webhooks
* Supports Telegram commands: `/status`, `/pause`, `/resume`, and `/help`

## Tech Stack

* Python
* Telegram Bot API
* Binance API
* Requests
* python-dotenv
* Git / GitHub
* Discord Webhooks

## Project Structure

```text
crypto-telegram-alert-bot/
├── main.py
├── config.py
├── telegram_bot.py
├── discord_bot.py
├── binance_client.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How It Works

The bot follows this flow:

```text
Binance API
    ↓
Python price checker
    ↓
Percentage movement calculation
    ↓
Alert condition
    ↓
Telegram message
```

`main.py` coordinates the program.

`config.py` stores settings like symbols, interval, threshold, cooldown, and environment variables.

`binance_client.py` gets crypto prices from Binance.

`telegram_bot.py` sends formatted messages to Telegram.

## Setup

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/crypto-telegram-alert-bot.git
cd crypto-telegram-alert-bot
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create a `.env` file:

```bash
touch .env
```

Add your Telegram credentials:

```env
BOT_TOKEN=your_telegram_bot_token_here
CHAT_ID=your_telegram_chat_id_here
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

Run the bot:

```bash
python3 main.py
```

## Configuration

You can change the bot behavior in `config.py`.

Example testing settings:

```python
CHECK_INTERVAL_SECONDS = 10
LOOKBACK_SECONDS = 60
ALERT_THRESHOLD_PERCENT = 0.03
COOLDOWN_SECONDS = 30
```

Example more realistic settings:

```python
CHECK_INTERVAL_SECONDS = 30
LOOKBACK_SECONDS = 300
ALERT_THRESHOLD_PERCENT = 0.50
COOLDOWN_SECONDS = 300
```

## Example Alert

```text
🚀 CRYPTO MOVEMENT ALERT

Symbol: SOLUSDT
Direction: UP
Move: 0.52% in 5 min
Old Price: $145.2000
New Price: $145.9550
Time: 14:32:10

Automated alert by Kalu Bot. Not financial advice.
```

## Future Improvements

## Future Improvements

- Add full Discord bot commands
- Add Telegram commands like `/settings`, `/add`, and `/remove`
- Support custom symbols per user or community
- Add volume spike alerts
- Deploy the bot to run 24/7
- Add logging for alerts and errors
- Add database support for saved settings
- Add multiple alert types
- Add web dashboard for configuration

## Disclaimer

This bot is for educational and automation practice purposes only. It is not financial advice and should not be used as the only basis for trading decisions.
