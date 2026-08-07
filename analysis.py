import time
from data import get_market_data
from indicators import calculate_indicators


def analyze_market(symbol, timeframe):

    time.sleep(2)

    df = get_market_data(symbol, timeframe)

    if df is None or len(df) < 200:
        return {
            "status": "error",
            "message": "Market data unavailable"
        }

    r = calculate_indicators(df)
        print("INDICATORS:", r)

    buy = 0
    sell = 0

    # ==========================
    # TREND FILTER
    # ==========================

    if r["ema50"] > r["ema100"] > r["ema200"]:
        buy += 5

    elif r["ema50"] < r["ema100"] < r["ema200"]:
        sell += 5

    else:
        return {
            "status": "success",
            "pair": symbol,
            "timeframe": timeframe,
            "price": r["price"],
            "trend": "SIDEWAYS",
            "trade": "WAIT",
            "confidence": 40
        }

    # ==========================
    # ADX FILTER
    # ==========================

    if r["adx"] < 25:
        return {
            "status": "success",
            "pair": symbol,
            "timeframe": timeframe,
            "price": r["price"],
            "trend": "WEAK TREND",
            "trade": "WAIT",
            "confidence": 45
        }

    # ==========================
    # EMA
    # ==========================

    if r["ema9"] > r["ema21"]:
        buy += 3
    else:
        sell += 3

    # ==========================
    # MACD
    # ==========================

    if r["macd"] > r["signal"]:
        buy += 3
    else:
        sell += 3

    # ==========================
    # RSI
    # ==========================

    if 50 <= r["rsi"] <= 68:
        buy += 2

    elif 32 <= r["rsi"] <= 50:
        sell += 2
        # ==========================
    # CCI
    # ==========================

    if r["cci"] > 100:
        buy += 2
    elif r["cci"] < -100:
        sell += 2

    # ==========================
    # Williams %R
    # ==========================

    if r["williams"] < -80:
        buy += 2
    elif r["williams"] > -20:
        sell += 2

    # ==========================
    # Parabolic SAR
    # ==========================

    if r["price"] > r["psar"]:
        buy += 2
    else:
        sell += 2

    # ==========================
    # Bollinger Bands
    # ==========================

    if r["price"] <= r["lower"]:
        buy += 1

    if r["price"] >= r["upper"]:
        sell += 1

    # ==========================
    # ATR FILTER
    # ==========================

    if r["atr"] < 0.0002:
        return {
            "status": "success",
            "pair": symbol,
            "timeframe": timeframe,
            "price": r["price"],
            "trend": "LOW VOLATILITY",
            "trade": "WAIT",
            "confidence": 40
        }

    # ==========================
    # STOCHASTIC
    # ==========================

    if r["stoch_k"] > r["stoch_d"] and r["stoch_k"] < 80:
        buy += 2

    elif r["stoch_k"] < r["stoch_d"] and r["stoch_k"] > 20:
        sell += 2

    # ==========================
    # SUPPORT / RESISTANCE
    # ==========================

    if r["price"] <= r["support"] * 1.001:
        buy += 2

    if r["price"] >= r["resistance"] * 0.999:
        sell += 2

    # ==========================
    # PRICE ACTION
    # ==========================

    last = df.iloc[-1]
    prev = df.iloc[-2]

    if last["close"] > last["open"] and prev["close"] > prev["open"]:
        buy += 3

    elif last["close"] < last["open"] and prev["close"] < prev["open"]:
        sell += 3
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

        "price": round(r["price"], 5),

        "ema9": round(r["ema9"], 5),
        "ema21": round(r["ema21"], 5),
        "ema50": round(r["ema50"], 5),
        "ema100": round(r["ema100"], 5),
        "ema200": round(r["ema200"], 5),

        "rsi": round(r["rsi"], 2),

        "macd": round(r["macd"], 5),
        "signal": round(r["signal"], 5),

        "adx": round(r["adx"], 2),
        "atr": round(r["atr"], 5),

        "cci": round(r["cci"], 2),
        "williams": round(r["williams"], 2),

        "psar": round(r["psar"], 5),

        "stoch_k": round(r["stoch_k"], 2),
        "stoch_d": round(r["stoch_d"], 2),

        "support": round(r["support"], 5),
        "resistance": round(r["resistance"], 5),

        "trend": trend,
        "trade": trade,
        "confidence": confidence,
        "buy_score": buy,
        "sell_score": sell,
        "score": score
    }
