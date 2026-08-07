import os
import requests
import pandas as pd

API_KEY = os.getenv("TWELVEDATA_API_KEY")

TIMEFRAME_MAP = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "H1": "1h",
    "H4": "4h",
    "D1": "1day"
}

SYMBOLS = {
    "EUR/USD": "EUR/USD",
    "GBP/USD": "GBP/USD",
    "AUD/USD": "AUD/USD",
    "NZD/USD": "NZD/USD",
    "USD/JPY": "USD/JPY",
    "USD/CAD": "USD/CAD",
    "USD/CHF": "USD/CHF",
    "XAU/USD": "XAU/USD",
}


def get_market_data(symbol, timeframe):
    interval = TIMEFRAME_MAP.get(timeframe, "1min")

    symbol = SYMBOLS.get(symbol, symbol)

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=250"
        f"&apikey={API_KEY}"
    )

    try:
        r = requests.get(url, timeout=15)
        data = r.json()

        print(data)

        if "values" not in data:
            return None

        df = pd.DataFrame(data["values"])
        df = df.iloc[::-1].reset_index(drop=True)

        for c in ["open", "high", "low", "close"]:
            df[c] = df[c].astype(float)

        return df

    except Exception as e:
        print("DATA ERROR:", e)
        return None
