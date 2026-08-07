from data import get_market_data
from indicators import calculate_indicators


def analyze_market(symbol, timeframe):

    df = get_market_data(symbol, timeframe)

    if df is None:
        return {
            "status": "error",
            "message": "Market data unavailable"
        }

    result = calculate_indicators(df)

    score_buy = 0
    score_sell = 0

    # EMA
    if result["ema9"] > result["ema21"]:
        score_buy += 2
    else:
        score_sell += 2

    # RSI
    if result["rsi"] < 35:
        score_buy += 1
    elif result["rsi"] > 65:
        score_sell += 1

    # MACD
    if result["macd"] > result["signal"]:
        score_buy += 2
    else:
        score_sell += 2

    # السعر فوق EMA9
    if result["price"] > result["ema9"]:
        score_buy += 1
    else:
        score_sell += 1

    # قرب الدعم والمقاومة
    if result["price"] <= result["support"] * 1.001:
        score_buy += 1

    if result["price"] >= result["resistance"] * 0.999:
        score_sell += 1

    if score_buy > score_sell:
        trend = "Bullish"
        signal = "BUY"
        confidence = min(98, 60 + score_buy * 6)
    elif score_sell > score_buy:
        trend = "Bearish"
        signal = "SELL"
        confidence = min(98, 60 + score_sell * 6)
    else:
        trend = "Neutral"
        signal = "WAIT"
        confidence = 50

    return {
        "status": "success",
        "pair": symbol,
        "timeframe": timeframe,
        "price": result["price"],
        "ema9": result["ema9"],
        "ema21": result["ema21"],
        "rsi": result["rsi"],
        "macd": result["macd"],
        "signal": result["signal"],
        "support": result["support"],
        "resistance": result["resistance"],
        "trend": trend,
        "trade": signal,
        "confidence": confidence
    }
