import pandas as pd

from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange


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

    adx = ADXIndicator(high, low, close).adx().iloc[-1]

    stoch = StochasticOscillator(high, low, close)
    stoch_k = stoch.stoch().iloc[-1]
    stoch_d = stoch.stoch_signal().iloc[-1]

    atr = AverageTrueRange(high, low, close).average_true_range().iloc[-1]

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

        "adx": adx,

        "stoch_k": stoch_k,
        "stoch_d": stoch_d,

        "atr": atr,

        "support": support,
        "resistance": resistance

    }
