import time
from data import get_market_data
from indicators import calculate_indicators


def analyze_market(symbol, timeframe):

    # محاكاة تحليل احترافي
    time.sleep(3)

    df = get_market_data(symbol, timeframe)

    if df is None or len(df) < 60:
        return {
            "status": "error",
            "message": "Market data unavailable"
        }

    r = calculate_indicators(df)

    buy = 0
    sell = 0

    # EMA
    if r["ema9"] > r["ema21"]:
        buy += 2
    else:
        sell += 2

    if r["ema21"] > r["ema50"]:
        buy += 2
    else:
        sell += 2

    # RSI
    if 45 <= r["rsi"] <= 65:
        buy += 1

    if r["rsi"] < 30:
        buy += 2

    if r["rsi"] > 70:
        sell += 2

    # MACD
    if r["macd"] > r["signal"]:
        buy += 2
    else:
        sell += 2

    # ADX
    if r["adx"] > 25:
        buy += 1
        sell += 1

    # CCI
    if r["cci"] > 100:
        buy += 1

    if r["cci"] < -100:
        sell += 1

    # Williams
    if r["williams"] < -80:
        buy += 1

    if r["williams"] > -20:
        sell += 1

    # SAR
    if r["price"] > r["psar"]:
        buy += 2
    else:
        sell += 2

    # Bollinger
    if r["price"] <= r["lower"]:
        buy += 1

    if r["price"] >= r["upper"]:
        sell += 1

    # Stochastic
    if r["stoch_k"] > r["stoch_d"]:
        buy += 1
    else:
        sell += 1

    # Support / Resistance
    if r["price"] <= r["support"] * 1.001:
        buy += 1

    if r["price"] >= r["resistance"] * 0.999:
        sell += 1

    # Price Action
    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last["close"] > last["open"] and prev["close"] > prev["open"]:
        buy += 2

    if last["close"] < last["open"] and prev["close"] < prev["open"]:
        sell += 2

    # القرار
    if buy >= sell + 3:
        signal = "BUY"
        trend = "Bullish"
        confidence = min(99, 60 + buy * 3)

    elif sell >= buy + 3:
        signal = "SELL"
        trend = "Bearish"
        confidence = min(99, 60 + sell * 3)

    else:
        signal = "WAIT"
        trend = "Neutral"
        confidence = 50

    return {
        "status": "success",
        "pair": symbol,
        "timeframe": timeframe,
        "price": r["price"],
        "ema9": r["ema9"],
        "ema21": r["ema21"],
        "ema50": r["ema50"],
        "rsi": r["rsi"],
        "macd": r["macd"],
        "signal": r["signal"],
        "adx": r["adx"],
        "cci": r["cci"],
        "williams": r["williams"],
        "psar": r["psar"],
        "support": r["support"],
        "resistance": r["resistance"],
        "trend": trend,
        "trade": signal,
        "confidence": confidence
    }
