import time

from config import (
    SYMBOLS,
    CHECK_INTERVAL_SECONDS,
    ALERT_THRESHOLD_PERCENT,
    COOLDOWN_SECONDS,
    LOOKBACK_SECONDS,
    CHAT_ID
)

from datetime import datetime
from binance_client import get_prices
from telegram_bot import send_telegram_message, get_updates
from discord_bot import send_discord_message


def calculate_percentage_change(old_price, new_price):
    return ((new_price - old_price) / old_price) * 100


def format_price(price):
    return f"${price:,.4f}"


def format_alert(symbol, percentage_change, old_price, new_price):
    if percentage_change > 0:
        direction_emoji = "🚀"
        direction_text = "UP"
    else:
        direction_emoji = "🔻"
        direction_text = "DOWN"

    current_time = datetime.now().strftime("%H:%M:%S")

    return (
        f"{direction_emoji} <b>CRYPTO MOVEMENT ALERT</b>\n\n"
        f"<b>Symbol:</b> {symbol}\n"
        f"<b>Direction:</b> {direction_text}\n"
        f"<b>Move:</b> {percentage_change:.2f}% in {LOOKBACK_SECONDS // 60} min\n"
        f"<b>Old Price:</b> {format_price(old_price)}\n"
        f"<b>New Price:</b> {format_price(new_price)}\n"
        f"<b>Time:</b> {current_time}\n\n"
        f"<i>Automated alert by Simset Bot. Not financial advice.</i>"
    )


def format_discord_alert(symbol, percentage_change, old_price, new_price):
    direction_emoji = "🚀" if percentage_change > 0 else "🔻"
    direction_text = "UP" if percentage_change > 0 else "DOWN"
    current_time = datetime.now().strftime("%H:%M:%S")

    return (
        f"{direction_emoji} **CRYPTO MOVEMENT ALERT**\n\n"
        f"**Symbol:** {symbol}\n"
        f"**Direction:** {direction_text}\n"
        f"**Move:** {percentage_change:.2f}% in {LOOKBACK_SECONDS // 60} min\n"
        f"**Old Price:** {format_price(old_price)}\n"
        f"**New Price:** {format_price(new_price)}\n"
        f"**Time:** {current_time}\n\n"
        f"*Automated alert by Simset Bot. Not financial advice.*"
    )


def should_send_alert(symbol, percentage_change, last_alert_times):
    current_time = time.time()

    if abs(percentage_change) < ALERT_THRESHOLD_PERCENT:
        return False

    if symbol not in last_alert_times:
        last_alert_times[symbol] = current_time
        return True

    if current_time - last_alert_times[symbol] >= COOLDOWN_SECONDS:
        last_alert_times[symbol] = current_time
        return True

    return False


def get_old_price_from_history(history, target_time):
    old_price = None

    for timestamp, price in history:
        if timestamp <= target_time:
            old_price = price
        else:
            break

    return old_price


def format_status(alerts_paused):
    status = "⏸️ Paused" if alerts_paused else "✅ Running"

    symbols_text = ", ".join(SYMBOLS)

    return (
        f"<b>Bot Status</b>\n\n"
        f"<b>Status:</b> {status}\n"
        f"<b>Monitoring:</b> {symbols_text}\n"
        f"<b>Lookback:</b> {LOOKBACK_SECONDS // 60} min\n"
        f"<b>Threshold:</b> {ALERT_THRESHOLD_PERCENT}%\n"
        f"<b>Cooldown:</b> {COOLDOWN_SECONDS}s"
    )


def format_help():
    return (
        f"<b>Available Commands</b>\n\n"
        f"/status - Show current bot status\n"
        f"/pause - Pause alerts\n"
        f"/resume - Resume alerts\n"
        f"/help - Show this help message"
    )


def handle_command(command, alerts_paused):
    command = command.lower().strip()

    if command == "/pause":
        alerts_paused = True
        send_telegram_message("⏸️ <b>Alerts paused.</b>")

    elif command == "/resume":
        alerts_paused = False
        send_telegram_message("▶️ <b>Alerts resumed.</b>")

    elif command == "/status":
        send_telegram_message(format_status(alerts_paused))

    elif command == "/help":
        send_telegram_message(format_help())

    return alerts_paused


def check_telegram_commands(last_update_id, alerts_paused):
    updates = get_updates(offset=last_update_id)

    for update in updates:
        last_update_id = update["update_id"] + 1

        message = update.get("message", {})
        chat = message.get("chat", {})
        text = message.get("text", "")

        if str(chat.get("id")) != str(CHAT_ID):
            continue

        if text.startswith("/"):
            alerts_paused = handle_command(text, alerts_paused)

    return last_update_id, alerts_paused


def main():
    print("Starting crypto Telegram alert bot...")
    send_telegram_message(
        "✅ <b>Crypto Alert Bot Started</b>\n\n"
        "Monitoring Binance price movements..."
    )

    send_discord_message(
        "✅ **Crypto Alert Bot Started**\n\n"
        "Monitoring Binance price movements..."
    )

    print(f"Symbols: {SYMBOLS}")
    print(f"Check interval: {CHECK_INTERVAL_SECONDS}s")
    print(f"Lookback: {LOOKBACK_SECONDS}s")
    print(f"Alert threshold: {ALERT_THRESHOLD_PERCENT}%")
    print(f"Cooldown: {COOLDOWN_SECONDS}s")

    price_history = {symbol: [] for symbol in SYMBOLS}
    last_alert_times = {}

    alerts_paused = False
    last_update_id = None

    while True:
        last_update_id, alerts_paused = check_telegram_commands(
            last_update_id,
            alerts_paused
        )
        
        current_time = time.time()
        current_prices = get_prices(SYMBOLS)

        for symbol, current_price in current_prices.items():
            price_history[symbol].append((current_time, current_price))

            cutoff_time = current_time - LOOKBACK_SECONDS - 60
            price_history[symbol] = [
                item for item in price_history[symbol]
                if item[0] >= cutoff_time
            ]

            target_time = current_time - LOOKBACK_SECONDS
            old_price = get_old_price_from_history(
                price_history[symbol],
                target_time
            )

            if old_price is None:
                print(f"{symbol}: collecting history...")
                continue

            percentage_change = calculate_percentage_change(old_price, current_price)

            print(f"{symbol}: {percentage_change:.4f}% in {LOOKBACK_SECONDS // 60} min")

            if not alerts_paused and should_send_alert(symbol, percentage_change, last_alert_times):
                telegram_message = format_alert(
                    symbol,
                    percentage_change,
                    old_price,
                    current_price
                )

                discord_message = format_discord_alert(
                    symbol,
                    percentage_change,
                    old_price,
                    current_price
                )

                send_telegram_message(telegram_message)
                send_discord_message(discord_message)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()