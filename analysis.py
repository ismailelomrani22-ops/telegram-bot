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
    elif result["ema9"] < result["ema21"]:
        score_sell += 2

    # RSI
    if result["rsi"] < 35:
        score_buy += 2
    elif result["rsi"] > 65:
        score_sell += 2
    elif 45 <= result["rsi"] <= 55:
        score_buy += 1
        score_sell += 1

    # MACD
    if result["macd"] > result["signal"]:
        score_buy += 2
    elif result["macd"] < result["signal"]:
        score_sell += 2

    # ADX
    if result["adx"] > 25:
        if score_buy > score_sell:
            score_buy += 1
        elif score_sell > score_buy:
            score_sell += 1

    # STOCHASTIC
    if result["stoch_k"] > result["stoch_d"]:
        score_buy += 1
    else:
        score_sell += 1

    # PRICE
    if result["price"] > result["ema9"]:
        score_buy += 1
    else:
        score_sell += 1

    # SUPPORT / RESISTANCE
    if result["price"] <= result["support"] * 1.001:
        score_buy += 1

    if result["price"] >= result["resistance"] * 0.999:
        score_sell += 1

    if score_buy >= 7:
        trend = "Bullish"
        trade = "BUY"
        confidence = min(99, 70 + score_buy * 3)

    elif score_sell >= 7:
        trend = "Bearish"
        trade = "SELL"
        confidence = min(99, 70 + score_sell * 3)

    else:
        trend = "Neutral"
        trade = "WAIT"
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

        "trade": trade,

        "confidence": confidence

    }
