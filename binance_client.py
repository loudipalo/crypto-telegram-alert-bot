import requests


def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    return float(data["price"])


def get_prices(symbols):
    prices = {}

    for symbol in symbols:
        try:
            prices[symbol] = get_price(symbol)
        except Exception as error:
            print(f"Error getting {symbol}: {error}")

    return prices