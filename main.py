
import telebot

TOKEN = "8632983518:AAGtdmb-vRqTOMCxo0PGkdxy33872Uqimok"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "السلام عليكم! البوت خدام ✅")

bot.infinity_polling()
