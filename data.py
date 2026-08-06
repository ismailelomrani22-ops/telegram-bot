import requests
import pandas as pd
import os

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

    url = (
        "https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        "&outputsize=200"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url, timeout=20)
    data = response.json()

    if "values" not in data:
        return None

    df = pd.DataFrame(data["values"])

    df = df.iloc[::-1].reset_index(drop=True)

    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)

    return df
