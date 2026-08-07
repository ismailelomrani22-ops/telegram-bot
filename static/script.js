async function analyze() {

    let pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;

    const displayPair = pair;

    // تحويل OTC إلى الزوج العادي قبل الإرسال
    pair = pair.replace(" OTC", "").replace("_OTC", "");

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
            button.disabled = false;
            button.innerHTML = "⚡ Analyze";
            return;
        }

        document.getElementById("pairName").innerText =
            displayPair + " | " + timeframe;

        document.getElementById("price").innerText = Number(data.price).toFixed(5);
        document.getElementById("ema").innerText = Number(data.ema50).toFixed(5);
        document.getElementById("rsi").innerText = Number(data.rsi).toFixed(2);
        document.getElementById("macd").innerText = Number(data.macd).toFixed(5);
        document.getElementById("adx").innerText = Number(data.adx).toFixed(2);
        document.getElementById("cci").innerText = Number(data.cci).toFixed(2);
        document.getElementById("support").innerText = Number(data.support).toFixed(5);
        document.getElementById("resistance").innerText = Number(data.resistance).toFixed(5);
        document.getElementById("trend").innerText = data.trend;

        animateConfidence(data.confidence);
        updateSignal(data.trade);
        updateChart(pair, timeframe);

    } catch (e) {

        console.log(e);
        alert("Server Error");

    }

    button.disabled = false;
    button.innerHTML = "⚡ Analyze";
}

function updateSignal(signal) {

    const box = document.getElementById("signal");

    box.innerHTML = signal;

    box.className = "";

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

    clearInterval(window.confTimer);

    window.confTimer = setInterval(() => {

        value++;

        label.innerHTML = value + "%";

        if (value >= target) {

            clearInterval(window.confTimer);

        }

    }, 15);
}

function updateChart(pair, timeframe) {

    pair = pair.replace(" OTC", "");

    const map = {

        "EUR/USD":"FX:EURUSD",
        "GBP/USD":"FX:GBPUSD",
        "USD/JPY":"FX:USDJPY",
        "EUR/JPY":"FX:EURJPY",
        "AUD/USD":"FX:AUDUSD",
        "USD/CAD":"FX:USDCAD",
        "USD/CHF":"FX:USDCHF",
        "NZD/USD":"FX:NZDUSD",
        "AUD/JPY":"FX:AUDJPY",
        "GBP/JPY":"FX:GBPJPY",
        "BTC/USD":"BINANCE:BTCUSDT",
        "ETH/USD":"BINANCE:ETHUSDT",
        "XAU/USD":"OANDA:XAUUSD"

    };

    const intervals = {

        "M1":"1",
        "M5":"5",
        "M15":"15",
        "M30":"30",
        "H1":"60",
        "H4":"240",
        "D1":"D"

    };

    const symbol = map[pair] || "FX:EURUSD";
    const interval = intervals[timeframe] || "1";

    document.querySelector(".chart-box iframe").src =
        `https://s.tradingview.com/widgetembed/?symbol=${symbol}&interval=${interval}&theme=dark&style=1&hide_top_toolbar=1&hide_side_toolbar=0`;
}

setInterval(analyze, 60000);
