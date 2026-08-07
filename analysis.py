from data import get_market_data
from indicators import calculate_indicators
import pandas as pd
import math


def safe(v, default=0):
    if v is None:
        return default

    try:
        if math.isnan(float(v)):
            return default
    except:
        pass

    return float(v)


def analyze_market(symbol, timeframe):

    df = get_market_data(symbol, timeframe)

    if df is None or len(df) < 220:

        return {
            "status": "error",
            "message": "Market data unavailable"
        }

    r = calculate_indicators(df)

    buy = 0
    sell = 0

    price = safe(r["price"])

    ema9 = safe(r["ema9"])
    ema21 = safe(r["ema21"])
    ema50 = safe(r["ema50"])
    ema100 = safe(r["ema100"])
    ema200 = safe(r["ema200"])

    rsi = safe(r["rsi"], 50)

    macd = safe(r["macd"])
    signal = safe(r["signal"])

    adx = safe(r["adx"], 20)

    atr = safe(r["atr"])

    cci = safe(r["cci"])

    stoch_k = safe(r["stoch_k"], 50)
    stoch_d = safe(r["stoch_d"], 50)

    upper = safe(r["upper"])
    lower = safe(r["lower"])

    support = safe(r["support"], price)
    resistance = safe(r["resistance"], price)
        # ==========================
    # EMA
    # ==========================

    if price > ema9:
        buy += 2
    else:
        sell += 2

    if ema9 > ema21:
        buy += 3
    else:
        sell += 3

    if ema21 > ema50:
        buy += 2
    else:
        sell += 2

    if ema50 > ema100:
        buy += 2
    else:
        sell += 2

    if ema100 > ema200:
        buy += 2
    else:
        sell += 2

    # ==========================
    # RSI
    # ==========================

    if rsi < 30:
        buy += 4

    elif rsi > 70:
        sell += 4

    elif rsi > 50:
        buy += 2

    else:
        sell += 2

    # ==========================
    # MACD
    # ==========================

    if macd > signal:
        buy += 4
    else:
        sell += 4

    # ==========================
    # ADX
    # ==========================

    if adx > 25:

        if buy > sell:
            buy += 3

        else:
            sell += 3

    # ==========================
    # CCI
    # ==========================

    if cci < -100:
        buy += 2

    elif cci > 100:
        sell += 2

    # ==========================
    # STOCHASTIC
    # ==========================

    if stoch_k > stoch_d and stoch_k < 80:
        buy += 3

    elif stoch_k < stoch_d and stoch_k > 20:
        sell += 3

    # ==========================
    # BOLLINGER
    # ==========================

    if lower != 0 and price <= lower:
        buy += 2

    if upper != 0 and price >= upper:
        sell += 2

    # ==========================
    # SUPPORT / RESISTANCE
    # ==========================

    if support != 0 and price <= support * 1.001:
        buy += 3

    if resistance != 0 and price >= resistance * 0.999:
        sell += 3

    # ==========================
    # PRICE ACTION
    # ==========================

    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last["close"] > last["open"] and prev["close"] > prev["open"]:
        buy += 4

    elif last["close"] < last["open"] and prev["close"] < prev["open"]:
        sell += 4
        # ==========================
    # FINAL DECISION
    # ==========================

    score = buy + sell

    if buy >= 20 and buy >= sell + 5:
        trade = "BUY"
        trend = "STRONG BULLISH"
        confidence = min(99, 60 + buy * 2)

    elif sell >= 20 and sell >= buy + 5:
        trade = "SELL"
        trend = "STRONG BEARISH"
        confidence = min(99, 60 + sell * 2)

    else:
        trade = "WAIT"
        trend = "NEUTRAL"
        confidence = 50

    return {

        "status": "success",

        "pair": symbol,
        "timeframe": timeframe,

        "price": round(price, 5),

        "ema9": round(ema9, 5),
        "ema21": round(ema21, 5),
        "ema50": round(ema50, 5),
        "ema100": round(ema100, 5),
        "ema200": round(ema200, 5),

        "rsi": round(rsi, 2),

        "macd": round(macd, 5),
        "signal": round(signal, 5),

        "adx": round(adx, 2),
        "atr": round(atr, 5),

        "cci": round(cci, 2),

        "stoch_k": round(stoch_k, 2),
        "stoch_d": round(stoch_d, 2),

        "support": round(support, 5),
        "resistance": round(resistance, 5),

        "trend": trend,
        "trade": trade,
        "confidence": confidence,

        "buy_score": buy,
        "sell_score": sell,
        "score": score

    }
