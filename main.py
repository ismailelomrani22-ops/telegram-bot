import os
import re
import requests
import pandas as pd
import telebot

from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("TWELVEDATA_API_KEY")

bot = telebot.TeleBot(TOKEN)

TIMEFRAME_MAP = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
    "M30": "30min",
    "H1": "1h",
    "H4": "4h"
}


def get_indicators(symbol, tf):
    interval = TIMEFRAME_MAP.get(tf)

    if interval is None:
        return None

    url = (
        f"https://api.twelvedata.com/time_series"
        f"?symbol={symbol}"
        f"&interval={interval}"
        f"&outputsize=100"
        f"&apikey={API_KEY}"
    )

    response = requests.get(url, timeout=15)
    data = response.json()

    if "values" not in data:
        return None

    df = pd.DataFrame(data["values"])
    df["close"] = df["close"].astype(float)
    df = df.iloc[::-1]

    price = df["close"].iloc[-1]

    ema9 = EMAIndicator(df["close"], window=9).ema_indicator().iloc[-1]
    ema21 = EMAIndicator(df["close"], window=21).ema_indicator().iloc[-1]

    rsi = RSIIndicator(df["close"], window=14).rsi().iloc[-1]

    macd = MACD(df["close"])
    macd_line = macd.macd().iloc[-1]
    macd_signal = macd.macd_signal().iloc[-1]

    return {
        "price": price,
        "ema9": ema9,
        "ema21": ema21,
        "rsi": rsi,
        "macd": macd_line,
        "signal": macd_signal,
    }


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "📊 أرسل الزوج والفريم.\n\n"
        "مثال:\n"
        "EUR/USD M1"
    )


@bot.message_handler(func=lambda m: True)
def analyze(message):
    text = message.text.upper().strip()

    match = re.match(
        r"^([A-Z]{3})/([A-Z]{3})\s+(M1|M5|M15|M30|H1|H4)$",
        text
    )

    if not match:
        bot.reply_to(
            message,
            "❌ الصيغة الصحيحة:\nEUR/USD M1"
        )
        return

    symbol = f"{match.group(1)}/{match.group(2)}"
    tf = match.group(3)

    result = get_indicators(symbol, tf)

    if result is None:
        bot.reply_to(message, "❌ تعذر جلب البيانات.")
        return

    if result["ema9"] > result["ema21"]:
        ema_state = "📈 EMA9 أعلى من EMA21 (ميل صاعد)"
    elif result["ema9"] < result["ema21"]:
        ema_state = "📉 EMA9 أسفل EMA21 (ميل هابط)"
    else:
        ema_state = "➖ EMA9 يساوي EMA21"

    if result["rsi"] < 30:
        rsi_state = "RSI منخفض"
    elif result["rsi"] > 70:
        rsi_state = "RSI مرتفع"
    else:
        rsi_state = "RSI متوسط"

    if result["macd"] > result["signal"]:
        macd_state = "MACD أعلى من خط الإشارة"
    else:
        macd_state = "MACD أسفل خط الإشارة"

    report = f"""
📊 التحليل الفني

💱 الزوج: {symbol}
⏱ الفريم: {tf}

💰 السعر:
{result['price']:.5f}

📈 EMA(9):
{result['ema9']:.5f}

📈 EMA(21):
{result['ema21']:.5f}

📉 RSI:
{result['rsi']:.2f}

📊 MACD:
{result['macd']:.5f}

📊 Signal:
{result['signal']:.5f}

━━━━━━━━━━━━━━

{ema_state}
{rsi_state}
{macd_state}
"""

    bot.reply_to(message, report)


print("Bot Started...")
bot.infinity_polling()
