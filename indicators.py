import pandas as pd

from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

def calculate_indicators(df):

    close = df["close"]
    high = df["high"]
    low = df["low"]

    ema9 = EMAIndicator(close, window=9).ema_indicator().iloc[-1]
    ema21 = EMAIndicator(close, window=21).ema_indicator().iloc[-1]

    rsi = RSIIndicator(close, window=14).rsi().iloc[-1]

    macd = MACD(close)

    macd_line = macd.macd().iloc[-1]
    signal = macd.macd_signal().iloc[-1]

    bb = BollingerBands(close)

    upper = bb.bollinger_hband().iloc[-1]
    lower = bb.bollinger_lband().iloc[-1]

    support = low.tail(20).min()
    resistance = high.tail(20).max()

    return {
        "price": close.iloc[-1],
        "ema9": ema9,
        "ema21": ema21,
        "rsi": rsi,
        "macd": macd_line,
        "signal": signal,
        "upper": upper,
        "lower": lower,
        "support": support,
        "resistance": resistance
    }
