import os
import threading
from flask import Flask
import telebot
from analysis import analyze_market

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
      <head><title>Telegram Trading Bot</title></head>
      <body style="font-family:Arial;text-align:center;margin-top:80px;">
        <h1>🤖 Telegram Trading Bot</h1>
        <h2 style="color:green;">Online ✅</h2>
      </body>
    </html>
    """

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ضع هنا جميع @bot.message_handler الموجودة عندك بدون تغيير

def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
