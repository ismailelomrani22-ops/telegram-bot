async function analyze() {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;

    const button = document.querySelector(".controls button");
    button.disabled = true;
    button.innerHTML = "⏳ Analyzing...";

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
            alert(data.message);
            return;
        }

        document.getElementById("pairName").innerText =
            data.pair + " | " + data.timeframe;

        document.getElementById("price").innerText =
            Number(data.price).toFixed(5);

        document.getElementById("ema").innerText =
            Number(data.ema50).toFixed(5);

        document.getElementById("rsi").innerText =
            Number(data.rsi).toFixed(2);

        document.getElementById("macd").innerText =
            Number(data.macd).toFixed(5);

        document.getElementById("adx").innerText =
            Number(data.adx).toFixed(2);

        document.getElementById("cci").innerText =
            Number(data.cci).toFixed(2);

        document.getElementById("support").innerText =
            Number(data.support).toFixed(5);

        document.getElementById("resistance").innerText =
            Number(data.resistance).toFixed(5);

        document.getElementById("trend").innerText =
            data.trend;

        animateConfidence(data.confidence);

        updateSignal(data.trade);

        updateChart(pair, timeframe);

    } catch (e) {

        alert("Server Error");

        console.log(e);

    }

    button.disabled = false;
    button.innerHTML = "⚡ Analyze";

}

function updateSignal(signal) {

    const box = document.getElementById("signal");

    box.innerHTML = signal;

    box.classList.remove("buy");
    box.classList.remove("sell");
    box.classList.remove("wait");

    if (signal === "BUY") {

        box.classList.add("buy");

    } else if (signal === "SELL") {

        box.classList.add("sell");

    } else {

        box.classList.add("wait");

    }

}

function animateConfidence(target) {

    let value = 0;

    const label = document.getElementById("confidence");

    const timer = setInterval(() => {

        value++;

        label.innerHTML = value + "%";

        if (value >= target) {

            clearInterval(timer);

        }

    }, 20);

}

function updateChart(pair, timeframe) {

    const map = {

        "EUR/USD":"FX:EURUSD",
        "GBP/USD":"FX:GBPUSD",
        "USD/JPY":"FX:USDJPY",
        "EUR/JPY":"FX:EURJPY",
        "AUD/USD":"FX:AUDUSD",
        "USD/CAD":"FX:USDCAD",
        "USD/CHF":"FX:USDCHF",
        "BTC/USD":"BINANCE:BTCUSDT",
        "ETH/USD":"BINANCE:ETHUSDT",
        "XAU/USD":"OANDA:XAUUSD"

    };

    const symbol = map[pair] || "FX:EURUSD";

    document.querySelector(".chart-box iframe").src =
        `https://s.tradingview.com/widgetembed/?symbol=${symbol}&interval=1&theme=dark&style=1`;

}

setInterval(() => {

    analyze();

}, 60000);
