async function analyze() {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;

    document.getElementById("result").innerHTML =
        "⏳ جاري تحليل السوق...";

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                pair: pair,
                timeframe: timeframe
            })

        });

        const data = await response.json();

        if (data.status !== "success") {

            document.getElementById("result").innerHTML =
                "❌ " + data.message;

            return;
        }

        let text = `
📊 التحليل الفني

💱 الزوج: ${data.pair}
⏱️ الفريم: ${data.timeframe}

━━━━━━━━━━━━━━

💰 السعر:
${Number(data.price).toFixed(5)}

📈 EMA9:
${Number(data.ema9).toFixed(5)}

📈 EMA21:
${Number(data.ema21).toFixed(5)}

📉 RSI:
${Number(data.rsi).toFixed(2)}

📊 MACD:
${Number(data.macd).toFixed(5)}

📊 Signal:
${Number(data.signal).toFixed(5)}

━━━━━━━━━━━━━━

🟢 الدعم:
${Number(data.support).toFixed(5)}

🔴 المقاومة:
${Number(data.resistance).toFixed(5)}

━━━━━━━━━━━━━━

📈 الاتجاه:
${data.trend}

📝 الملخص:

`;

        data.summary.forEach(item => {
            text += "• " + item + "\n";
        });

        document.getElementById("result").innerHTML = text;

    } catch (error) {

        document.getElementById("result").innerHTML =
            "❌ حدث خطأ أثناء الاتصال بالخادم.";

    }

}
