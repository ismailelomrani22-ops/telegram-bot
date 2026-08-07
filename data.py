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


def get_market_data(symbol, timeframe):

    interval = TIMEFRAME_MAP.get(timeframe)

    if interval is None:
        return None

    symbol = symbol.replace(" OTC", "").replace("_OTC", "").strip()

    url = (
        "https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        "&outputsize=350"
        f"&apikey={API_KEY}"
    )

    try:

        response = requests.get(url, timeout=20)
        data = response.json()

        if "values" not in data:
            print(data)
            return None

        df = pd.DataFrame(data["values"])

        df = df.iloc[::-1].reset_index(drop=True)

        for col in ["open", "high", "low", "close"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        if len(df) < 250:
            print("Not enough candles")
            return None

        return df

    except Exception as e:
        print(e)
        return None
