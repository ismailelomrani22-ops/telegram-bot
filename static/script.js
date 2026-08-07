document.getElementById("signalBtn").addEventListener("click", async () => {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;

    document.getElementById("pairName").innerHTML = pair;

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
                pair,
                timeframe
            })
        });

        const data = await response.json();

        if (data.status !== "success") {
            signal.innerHTML = "❌ ERROR";
            return;
        }

        document.getElementById("price").innerHTML = Number(data.price).toFixed(5);
        document.getElementById("ema9").innerHTML = Number(data.ema9).toFixed(5);
        document.getElementById("ema21").innerHTML = Number(data.ema21).toFixed(5);
        document.getElementById("rsi").innerHTML = Number(data.rsi).toFixed(2);
        document.getElementById("macd").innerHTML = Number(data.macd).toFixed(5);
        document.getElementById("support").innerHTML = Number(data.support).toFixed(5);
        document.getElementById("resistance").innerHTML = Number(data.resistance).toFixed(5);
        document.getElementById("trend").innerHTML = data.trend;

        confidence.innerHTML = data.confidence + "%";

        if (data.trade === "BUY") {
            signal.innerHTML = "🟢 BUY";
            signal.className = "signal buy";
        } else if (data.trade === "SELL") {
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

            timer.innerHTML =
                "00:" + (time < 10 ? "0" + time : time);

            if (time <= 0) {

                clearInterval(window.countdown);

            }

        }, 1000);

    } catch (err) {

        console.log(err);

        signal.innerHTML = "❌ SERVER ERROR";

    }

});
const marketSelect = document.getElementById("market");
const pairSelect = document.getElementById("pair");

const forexPairs = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "USD/CAD",
    "AUD/USD",
    "NZD/USD",
    "EUR/JPY",
    "EUR/GBP",
    "GBP/JPY",
    "XAU/USD"
];

const otcPairs = [
    "EUR/USD OTC",
    "GBP/USD OTC",
    "USD/JPY OTC",
    "USD/CAD OTC",
    "AUD/USD OTC",
    "NZD/USD OTC",
    "EUR/JPY OTC",
    "EUR/GBP OTC",
    "GBP/JPY OTC",
    "XAU/USD OTC"
];

function loadPairs() {

    pairSelect.innerHTML = "";

    const list = marketSelect.value === "OTC"
        ? otcPairs
        : forexPairs;

    list.forEach(pair => {

        const option = document.createElement("option");
        option.value = pair;
        option.textContent = pair;

        pairSelect.appendChild(option);

    });

}

marketSelect.addEventListener("change", loadPairs);

loadPairs();
