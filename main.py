import os
import threading
from flask import Flask
import telebot
from analysis import analyze_market

app = Flask(__name__)

@app.route("/")
def home():
    return """... HTML ..."""
    <html>
      <head>
        <title>Telegram Trading Bot</title>
      </head>
      <body style="font-family:Arial;text-align:center;margin-top:80px;">
        <h1>🤖 Telegram Trading Bot</h1>
        <h2 style="color:green;">Online ✅</h2>
        <p>Hosted on Railway</p>
      </body>
    </html>
    """

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 مرحباً بك\n\n"
        "أرسل الزوج والفريم.\n\n"
        "مثال:\n"
        "EUR/USD M1"
    )

@bot.message_handler(func=lambda m: True)
def analyze(message):
    try:
        text = message.text.upper().strip()
        pair, timeframe = text.split()

        result = analyze_market(pair, timeframe)

        if result["status"] != "success":
            bot.reply_to(message, result["message"])
            return

        reply = f"""
📊 التحليل الفني

💱 الزوج: {result['pair']}
⏱️ الفريم: {result['timeframe']}

━━━━━━━━━━━━━━

💰 السعر:
{result['price']:.5f}

📈 EMA9:
{result['ema9']:.5f}

📈 EMA21:
{result['ema21']:.5f}

📉 RSI:
{result['rsi']:.2f}

📊 MACD:
{result['macd']:.5f}

📊 Signal:
{result['signal']:.5f}

━━━━━━━━━━━━━━

🟢 الدعم:
{result['support']:.5f}

🔴 المقاومة:
{result['resistance']:.5f}

━━━━━━━━━━━━━━

📈 الاتجاه:
{result['trend']}

📝 الملخص:
"""

        for item in result["summary"]:
            reply += f"• {item}\n"

        bot.reply_to(message, reply)

    except Exception:
        bot.reply_to(message, "❌ الصيغة الصحيحة:\n\nEUR/USD M1")

def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
