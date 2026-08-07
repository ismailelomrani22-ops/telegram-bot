import os
import threading
from flask import Flask
import telebot
from analysis import analyze_market

# -------------------------
# Flask Website
# -------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Trading Bot Dashboard</title>

<style>
body{
margin:0;
font-family:Arial;
background:#0f172a;
color:white;
text-align:center;
}

header{
padding:40px;
background:#111827;
}

h1{
font-size:42px;
margin:0;
}

.green{
color:#22c55e;
}

.container{
max-width:1100px;
margin:auto;
padding:40px;
}

.card{
display:inline-block;
width:260px;
margin:15px;
padding:25px;
border-radius:18px;
background:#1e293b;
box-shadow:0 0 15px rgba(0,0,0,.4);
}

.card h2{
margin:10px 0;
}

.btn{
display:inline-block;
padding:15px 35px;
margin-top:25px;
background:#22c55e;
color:white;
text-decoration:none;
border-radius:10px;
font-size:18px;
}

footer{
margin-top:60px;
padding:25px;
background:#111827;
}
</style>

</head>

<body>

<header>
<h1>🤖 Telegram Trading Bot</h1>
<h2 class="green">ONLINE ✅</h2>
<p>Powered by Railway</p>
</header>

<div class="container">

<div class="card">
<h2>📊 Analysis</h2>
<p>EMA 9</p>
<p>EMA 21</p>
<p>RSI</p>
<p>MACD</p>
</div>

<div class="card">
<h2>⚡ Status</h2>
<p style="color:#22c55e;">Bot Online</p>
<p>API Connected</p>
<p>Railway Running</p>
</div>

<div class="card">
<h2>🚀 Features</h2>
<p>Forex Analysis</p>
<p>Telegram Bot</p>
<p>Technical Indicators</p>
</div>

<a class="btn" href="https://t.me/YOUR_BOT_USERNAME">
Open Telegram Bot
</a>

</div>

<footer>
© 2026 Telegram Trading Bot
</footer>

</body>
</html>
"""

# -------------------------
# Telegram Bot
# -------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🤖 مرحباً بك\n\nأرسل الزوج والفريم\n\nمثال:\nEUR/USD M1"
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
📈 EMA9: {result['ema9']:.5f}
📈 EMA21: {result['ema21']:.5f}
📉 RSI: {result['rsi']:.2f}

📊 MACD: {result['macd']:.5f}
📊 Signal: {result['signal']:.5f}

🟢 الدعم: {result['support']:.5f}
🔴 المقاومة: {result['resistance']:.5f}

📈 الاتجاه:
{result['trend']}
"""

        bot.reply_to(message, text)

    except Exception:
        bot.reply_to(message, "❌ الصيغة الصحيحة:\nEUR/USD M1")

def run_bot():
    bot.infinity_polling(skip_pending=True)

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
