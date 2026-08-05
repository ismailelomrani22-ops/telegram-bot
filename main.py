import telebot
import random
import re

TOKEN = "8632983518:AAEdhcYLq0MfvN6Uw1_BVpLDLlCzxmyNKMI"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ أرسل زوج العملات مع الفريم.\nمثال:\nEUR/USD M1")

@bot.message_handler(func=lambda m: True)
def signal(message):
    text = message.text.upper().strip()

    pattern = r"^[A-Z]{3}/[A-Z]{3}\s+(M1|M5|M15|M30|H1)$"

    if re.match(pattern, text):
        signal = random.choice(["📈 BUY", "📉 SELL"])
        bot.reply_to(message, f"{text}\n\n{signal}")
    else:
        bot.reply_to(message, "❌ مثال صحيح:\nEUR/USD M1")

bot.infinity_polling()
