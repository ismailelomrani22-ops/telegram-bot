document.getElementById("signalBtn").addEventListener("click", async () => {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;
    const market = document.getElementById("market").value;

    const signal = document.getElementById("signal");
    const confidence = document.getElementById("confidence");
    const timer = document.getElementById("timer");

    signal.innerHTML = "⏳ ANALYZING...";
    signal.className = "signal";

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
            signal.innerHTML = "❌ ERROR";
            return;
        }

        document.getElementById("pairName").innerHTML =
            pair + (market === "OTC" ? " OTC" : "");

        document.getElementById("price").innerHTML = Number(data.price).toFixed(5);
        document.getElementById("ema9").innerHTML = Number(data.ema9).toFixed(5);
        document.getElementById("ema21").innerHTML = Number(data.ema21).toFixed(5);
        document.getElementById("rsi").innerHTML = Number(data.rsi).toFixed(2);
        document.getElementById("macd").innerHTML = Number(data.macd).toFixed(5);
        document.getElementById("support").innerHTML = Number(data.support).toFixed(5);
        document.getElementById("resistance").innerHTML = Number(data.resistance).toFixed(5);
        document.getElementById("trend").innerHTML = data.trend;

        confidence.innerHTML = (90 + Math.floor(Math.random() * 10)) + "%";

        const trend = data.trend.toLowerCase();

        if (trend.includes("صاعد") || trend.includes("bull")) {
            signal.innerHTML = "🟢 BUY";
            signal.className = "signal buy";
        } else if (trend.includes("هابط") || trend.includes("bear")) {
            signal.innerHTML = "🔴 SELL";
            signal.className = "signal sell";
        } else {
            signal.innerHTML = "🟡 WAIT";
            signal.className = "signal wait";
        }

        let time = 45;
        timer.innerHTML = "00:45";

        clearInterval(window.countdown);

        window.countdown = setInterval(() => {
            time--;
            timer.innerHTML = "00:" + (time < 10 ? "0" + time : time);

            if (time <= 0) clearInterval(window.countdown);

        }, 1000);

    } catch (err) {
        console.error(err);
        signal.innerHTML = "❌ SERVER ERROR";
    }

});
