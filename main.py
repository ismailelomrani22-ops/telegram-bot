import telebot

TOKEN = "8632983518:AAGtdmb-vRqTOMCxo0PGkdxy33872Uqimok"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ السلام عليكم! البوت خدام")

@bot.message_handler(func=lambda message: True)
def signals(message):
    text = message.text.upper()

    if text == "EUR/USD M1":
        bot.reply_to(message, "📈 BUY")

    elif text == "EUR/USD 5S":
        bot.reply_to(message, "📉 SELL")

    else:
        bot.reply_to(message, "❌ الأمر غير معروف")

bot.infinity_polling()
