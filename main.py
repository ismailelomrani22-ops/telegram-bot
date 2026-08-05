import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "أرسل مثلاً:\nEUR/USD M1"
    )

@bot.message_handler(func=lambda m: True)
def analyze(message):
    text = message.text.upper().strip()

    # هنا تضيف:
    # 1. قراءة الزوج والفريم.
    # 2. جلب البيانات من Twelve Data.
    # 3. حساب EMA وRSI وMACD.
    # 4. إرسال النتائج للمستخدم.

    report = (
        "📊 التحليل الفني\n\n"
        "EMA(9): ...\n"
        "EMA(21): ...\n"
        "RSI(14): ...\n"
        "MACD: ...\n"
        "MACD Signal: ..."
    )

    bot.reply_to(message, report)

bot.infinity_polling()
