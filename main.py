import os
import telebot
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def analyze(symbol, interval):
    ticker = symbol.replace("/", "") + "=X"

    intervals = {
        "M1": "1m",
        "M5": "5m",
        "M15": "15m",
        "H1": "1h"
    }

    data = yf.download(
        ticker,
        period="1d",
        interval=intervals.get(interval, "5m"),
        progress=False
    )

    if data.empty:
        return "❌ لا توجد بيانات."

    close = data["Close"]

    ema9 = EMAIndicator(close, 9).ema_indicator().iloc[-1]
    ema21 = EMAIndicator(close, 21).ema_indicator().iloc[-1]
    rsi = RSIIndicator(close, 14).rsi().iloc[-1]

    macd = MACD(close)
    macd_line = macd.macd().iloc[-1]
    signal = macd.macd_signal().iloc[-1]

    price = close.iloc[-1]

    if ema9 > ema21 and macd_line > signal and rsi < 70:
        trade = "🟢 BUY"
        confidence = "85%"
    elif ema9 < ema21 and macd_line < signal and rsi > 30:
        trade = "🔴 SELL"
        confidence = "85%"
    else:
        trade = "⚪ WAIT"
        confidence = "50%"

    return f"""
📊 التحليل الفني

💱 الزوج: {symbol}
⏱ الفريم: {interval}

💰 السعر: {price:.5f}

📈 EMA(9): {ema9:.5f}
📉 EMA(21): {ema21:.5f}

📊 RSI: {rsi:.2f}

📉 MACD: {macd_line:.5f}
📍 Signal: {signal:.5f}

🎯 الإشارة: {trade}
📊 الثقة: {confidence}
"""

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "😉 أرسل الزوج والفريم.\n\nمثال:\nEUR/USD M1"
    )

@bot.message_handler(func=lambda m: True)
def signal(message):
    try:
        pair, tf = message.text.upper().split()
        bot.reply_to(message, analyze(pair, tf))
    except:
        bot.reply_to(message, "❌ أرسل بالشكل:\nEUR/USD M1")

print("Bot Started...")
bot.infinity_polling()
