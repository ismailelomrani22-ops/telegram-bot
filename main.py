import os
import re
import requests
import pandas as pd
import telebot

from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.volatility import BollingerBands, AverageTrueRange

# ==========================
# Environment Variables
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

TIMEFRAME_MAP = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "H1": "1h",
    "H4": "4h",
    "D1": "1day"
}

# ==========================
# Download Market Data
# ==========================

def get_market_data(symbol, timeframe):

    interval = TIMEFRAME_MAP.get(timeframe)

    if interval is None:
        return None

    url = (
        "https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        "&outputsize=300"
        f"&apikey={TWELVEDATA_API_KEY}"
    )

    response = requests.get(url, timeout=20)

    data = response.json()

    if "values" not in data:
        return None

    df = pd.DataFrame(data["values"])

    df = df.iloc[::-1].reset_index(drop=True)

    for col in ["open", "high", "low", "close"]:
        df[col] = df[col].astype(float)

    return df


# ==========================
# Start Command
# ==========================

@bot.message_handler(commands=["start"])
def start(message):

    bot.reply_to(
        message,
        "📊 مرحباً بك\n\n"
        "أرسل الزوج والفريم.\n\n"
        "مثال:\n"
        "EUR/USD M1"
    )# ==========================
# Technical Indicators
# ==========================

def calculate_indicators(df):

    close = df["close"]
    high = df["high"]
    low = df["low"]

    ema9 = EMAIndicator(close, window=9).ema_indicator().iloc[-1]
    ema21 = EMAIndicator(close, window=21).ema_indicator().iloc[-1]
    ema50 = EMAIndicator(close, window=50).ema_indicator().iloc[-1]
    ema200 = EMAIndicator(close, window=200).ema_indicator().iloc[-1]

    rsi = RSIIndicator(close, window=14).rsi().iloc[-1]

    macd = MACD(close)
    macd_line = macd.macd().iloc[-1]
    macd_signal = macd.macd_signal().iloc[-1]

    bb = BollingerBands(close)
    upper = bb.bollinger_hband().iloc[-1]
    middle = bb.bollinger_mavg().iloc[-1]
    lower = bb.bollinger_lband().iloc[-1]

    atr = AverageTrueRange(high, low, close).average_true_range().iloc[-1]

    adx = ADXIndicator(high, low, close).adx().iloc[-1]

    stoch = StochRSIIndicator(close)
    stoch_value = stoch.stochrsi().iloc[-1]

    resistance = high.tail(20).max()
    support = low.tail(20).min()

    if ema9 > ema21:
        trend = "📈 الميل قصير الأجل صاعد"
    elif ema9 < ema21:
        trend = "📉 الميل قصير الأجل هابط"
    else:
        trend = "➖ الميل قصير الأجل محايد"

    if rsi < 30:
        rsi_state = "RSI في منطقة منخفضة"
    elif rsi > 70:
        rsi_state = "RSI في منطقة مرتفعة"
    else:
        rsi_state = "RSI في النطاق المتوسط"

    if macd_line > macd_signal:
        macd_state = "MACD أعلى من خط الإشارة"
    else:
        macd_state = "MACD أسفل خط الإشارة"

    return {
        "price": close.iloc[-1],
        "ema9": ema9,
        "ema21": ema21,
        "ema50": ema50,
        "ema200": ema200,
        "rsi": rsi,
        "macd": macd_line,
        "macd_signal": macd_signal,
        "upper": upper,
        "middle": middle,
        "lower": lower,
        "atr": atr,
        "adx": adx,
        "stoch": stoch_value,
        "support": support,
        "resistance": resistance,
        "trend": trend,
        "rsi_state": rsi_state,
        "macd_state": macd_state
    }# ==========================
# Message Handler
# ==========================

@bot.message_handler(func=lambda m: True)
def analyze(message):

    text = message.text.upper().strip()

    match = re.match(
        r"^([A-Z]{3})/([A-Z]{3})\s+(M1|M5|M15|M30|H1|H4|D1)$",
        text
    )

    if not match:
        bot.reply_to(
            message,
            "❌ الصيغة الصحيحة:\n\nEUR/USD M1"
        )
        return

    symbol = f"{match.group(1)}/{match.group(2)}"
    timeframe = match.group(3)

    bot.send_chat_action(message.chat.id, "typing")

    df = get_market_data(symbol, timeframe)

    if df is None:
        bot.reply_to(
            message,
            "❌ تعذر جلب البيانات من Twelve Data."
        )
        return

    result = calculate_indicators(df)

    report = f"""
📊 التحليل الفني

💱 الزوج: {symbol}
⏱ الفريم: {timeframe}

━━━━━━━━━━━━━━━━

💰 السعر الحالي
{result['price']:.5f}

📈 EMA 9
{result['ema9']:.5f}

📈 EMA 21
{result['ema21']:.5f}

📈 EMA 50
{result['ema50']:.5f}

📈 EMA 200
{result['ema200']:.5f}

━━━━━━━━━━━━━━━━

📉 RSI
{result['rsi']:.2f}

📊 MACD
{result['macd']:.5f}

📊 Signal
{result['macd_signal']:.5f}

━━━━━━━━━━━━━━━━

📦 Bollinger Upper
{result['upper']:.5f}

📦 Bollinger Middle
{result['middle']:.5f}

📦 Bollinger Lower
{result['lower']:.5f}

━━━━━━━━━━━━━━━━

📏 ATR
{result['atr']:.5f}

📐 ADX
{result['adx']:.2f}

📍 Stoch RSI
{result['stoch']:.2f}

━━━━━━━━━━━━━━━━

🟢 الدعم
{result['support']:.5f}

🔴 المقاومة
{result['resistance']:.5f}

━━━━━━━━━━━━━━━━

📈 الاتجاه
{result['trend']}

📉 RSI
{result['rsi_state']}

📊 MACD
{result['macd_state']}
"""

    bot.reply_to(message, report)
    # ==========================
# Run Bot
# ==========================

def run_bot():
    print("🤖 Bot Started...")

    while True:
        try:
            bot.infinity_polling(
                timeout=30,
                long_polling_timeout=30,
                skip_pending=True
            )

        except Exception as e:
            print("Bot Error:", e)


if __name__ == "__main__":
    run_bot()
