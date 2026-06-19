import time

from config import (
    SYMBOLS,
    CHECK_INTERVAL_SECONDS,
    ALERT_THRESHOLD_PERCENT,
    COOLDOWN_SECONDS,
    LOOKBACK_SECONDS
)

from datetime import datetime
from binance_client import get_prices
from telegram_bot import send_telegram_message


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


def main():
    print("Starting crypto Telegram alert bot...")
    send_telegram_message("✅ <b>Crypto Alert Bot Started</b>\n\n""Monitoring Binance price movements...")

    print(f"Symbols: {SYMBOLS}")
    print(f"Check interval: {CHECK_INTERVAL_SECONDS}s")
    print(f"Lookback: {LOOKBACK_SECONDS}s")
    print(f"Alert threshold: {ALERT_THRESHOLD_PERCENT}%")
    print(f"Cooldown: {COOLDOWN_SECONDS}s")

    price_history = {symbol: [] for symbol in SYMBOLS}
    last_alert_times = {}

    while True:
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

            if should_send_alert(symbol, percentage_change, last_alert_times):
                message = format_alert(
                    symbol,
                    percentage_change,
                    old_price,
                    current_price
                )

                send_telegram_message(message)

        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()