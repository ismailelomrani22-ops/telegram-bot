async function analyze() {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;

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
        data.price;

    document.getElementById("trend").innerText =
        data.trend;

    document.getElementById("confidence").innerText =
        data.confidence + "%";

    document.getElementById("signal").innerText =
        data.trade;

    const signal = document.getElementById("signal");

    signal.classList.remove("buy", "sell", "wait");

    if (data.trade === "BUY") {

        signal.classList.add("buy");

    } else if (data.trade === "SELL") {

        signal.classList.add("sell");

    } else {

        signal.classList.add("wait");

    }

    document.getElementById("ema").innerText =
        data.ema50.toFixed(5);

    document.getElementById("rsi").innerText =
        data.rsi.toFixed(2);

    document.getElementById("macd").innerText =
        data.macd.toFixed(5);

    document.getElementById("adx").innerText =
        data.adx.toFixed(2);

    document.getElementById("cci").innerText =
        data.cci.toFixed(2);

    document.getElementById("support").innerText =
        data.support.toFixed(5);

    document.getElementById("resistance").innerText =
        data.resistance.toFixed(5);

}
