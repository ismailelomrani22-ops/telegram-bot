from data import get_market_data
from indicators import calculate_indicators


def analyze_market(symbol, timeframe):

    symbol = symbol.replace(" OTC", "").replace("_OTC", "").strip()

    df = get_market_data(symbol, timeframe)

    if df is None:
        return {
            "status": "error",
            "message": "Market data unavailable"
        }

    result = calculate_indicators(df)

    score_buy = 0
    score_sell = 0

    if result["ema9"] > result["ema21"]:
        score_buy += 2
    else:
        score_sell += 2

    if result["rsi"] < 35:
        score_buy += 1
    elif result["rsi"] > 65:
        score_sell += 1

    if result["macd"] > result["signal"]:
        score_buy += 2
    else:
        score_sell += 2

    if result["price"] > result["ema9"]:
        score_buy += 1
    else:
        score_sell += 1

    if result["price"] <= result["support"] * 1.001:
        score_buy += 1

    if result["price"] >= result["resistance"] * 0.999:
        score_sell += 1

    if score_buy > score_sell:
        trend = "Bullish"
        trade = "BUY"
        confidence = min(98, 60 + score_buy * 6)
    elif score_sell > score_buy:
        trend = "Bearish"
        trade = "SELL"
        confidence = min(98, 60 + score_sell * 6)
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
