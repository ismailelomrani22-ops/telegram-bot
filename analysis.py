from data import get_market_data
from indicators import calculate_indicators

def analyze_market(symbol, timeframe):

    df = get_market_data(symbol, timeframe)

    if df is None:
        return {
            "status": "error",
            "message": "تعذر جلب بيانات السوق."
        }

    result = calculate_indicators(df)

    trend = "محايد"

    if result["ema9"] > result["ema21"]:
        trend = "صاعد"
    elif result["ema9"] < result["ema21"]:
        trend = "هابط"

    summary = []

    summary.append(f"الاتجاه قصير الأجل: {trend}")

    if result["rsi"] < 30:
        summary.append("RSI في منطقة منخفضة.")
    elif result["rsi"] > 70:
        summary.append("RSI في منطقة مرتفعة.")
    else:
        summary.append("RSI في النطاق المتوسط.")

    if result["macd"] > result["signal"]:
        summary.append("MACD أعلى من خط الإشارة.")
    else:
        summary.append("MACD أسفل خط الإشارة.")

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
        "summary": summary
    }
