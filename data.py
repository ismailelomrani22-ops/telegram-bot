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
        print(f"❌ Invalid timeframe: {timeframe}")
        return None

    if not API_KEY:
        print("❌ TWELVEDATA_API_KEY is missing.")
        return None

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": 200,
        "apikey": API_KEY
    }

    try:

        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()

        data = response.json()

        print("API Response:", data)

        if "values" not in data:
            print("❌ API Error:", data)
            return None

        df = pd.DataFrame(data["values"])

        df = df.iloc[::-1].reset_index(drop=True)

        numeric_columns = ["open", "high", "low", "close"]

        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df.dropna(inplace=True)

        if df.empty:
            print("❌ No valid market data.")
            return None

        return df

    except requests.exceptions.RequestException as e:
        print("❌ Network Error:", e)
        return None

    except Exception as e:
        print("❌ Unexpected Error:", e)
        return None
