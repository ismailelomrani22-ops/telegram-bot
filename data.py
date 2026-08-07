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

    # إزالة كلمة OTC إذا كانت موجودة
    symbol = symbol.replace(" OTC", "").replace("_OTC", "").strip()

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=250"
        f"&apikey={API_KEY}"
    )

    try:

        response = requests.get(url, timeout=15)
        data = response.json()

        if "values" not in data:
            print("API ERROR:", data)
            return None

        df = pd.DataFrame(data["values"])

        df = df.iloc[::-1].reset_index(drop=True)

        numeric_columns = [
            "open",
            "high",
            "low",
            "close"
        ]

        for col in numeric_columns:
            df[col] = df[col].astype(float)

        return df

    except Exception as e:
        print("DATA ERROR:", e)
        return None
