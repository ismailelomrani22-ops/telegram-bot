# ==========================
# فلتر الاتجاه العام
# ==========================

if r["ema50"] > r["ema100"] > r["ema200"]:
    buy += 3

elif r["ema50"] < r["ema100"] < r["ema200"]:
    sell += 3

else:
    return {
        "status": "success",
        "pair": symbol,
        "timeframe": timeframe,
        "price": r["price"],
        "ema9": r["ema9"],
        "ema21": r["ema21"],
        "ema50": r["ema50"],
        "ema100": r["ema100"],
        "ema200": r["ema200"],
        "rsi": r["rsi"],
        "macd": r["macd"],
        "signal": r["signal"],
        "adx": r["adx"],
        "cci": r["cci"],
        "williams": r["williams"],
        "psar": r["psar"],
        "support": r["support"],
        "resistance": r["resistance"],
        "trend": "Sideways",
        "trade": "WAIT",
        "confidence": 40
    }

# ==========================
# القرار النهائي
# ==========================

if buy >= 14 and buy >= sell + 4:
    signal = "BUY"
    trend = "Bullish"
    confidence = min(95, 55 + buy * 2)

elif sell >= 14 and sell >= buy + 4:
    signal = "SELL"
    trend = "Bearish"
    confidence = min(95, 55 + sell * 2)

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
    "ema100": r["ema100"],
    "ema200": r["ema200"],
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
