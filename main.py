import os
import threading

from flask import Flask, render_template, request, jsonify

import telebot

from analysis import analyze_market

app = Flask(__name__)


# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")


# API للموقع
@app.route("/analyze", methods=["POST"])
def analyze_api():

    data = request.get_json()

    pair = data.get("pair")
    timeframe = data.get("timeframe")

    result = analyze_market(pair, timeframe)

    return jsonify(result)


# Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):

    bot.reply_to(
        message,
        "🤖 مرحباً بك\n\n"
        "أرسل الزوج والفريم\n\n"
        "مثال:\n"
        "EUR/USD M1"
    )


@bot.message_handler(func=lambda m: True)
def analyze(message):

    try:

        pair, timeframe = message.text.upper().split()

        result = analyze_market(pair, timeframe)

        if result["status"] != "success":

            bot.reply_to(message, result["message"])

            return

        text = f"""
📊 التحليل الفني

💱 الزوج: {result['pair']}
⏱️ الفريم: {result['timeframe']}

💰 السعر: {result['price']:.5f}

📈 EMA9 : {result['ema9']:.5f}

📈 EMA21 : {result['ema21']:.5f}

📉 RSI : {result['rsi']:.2f}

📊 MACD : {result['macd']:.5f}

📊 Signal : {result['signal']:.5f}

🟢 Support : {result['support']:.5f}

🔴 Resistance : {result['resistance']:.5f}

📈 Trend

{result['trend']}
"""

        bot.reply_to(message, text)

    except Exception:

        bot.reply_to(message, "❌ الصيغة الصحيحة\n\nEUR/USD M1")


def run_bot():
    bot.remove_webhook()
    bot.infinity_polling(
        skip_pending=True,
        timeout=30,
        long_polling_timeout=30
    )


threading.Thread(target=run_bot).start()


if __name__ == "__main__":

    port = int(os.getenv("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
