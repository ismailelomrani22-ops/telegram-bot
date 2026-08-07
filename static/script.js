document.getElementById("signalBtn").addEventListener("click", async () => {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;
    const market = document.getElementById("market").value;

    document.getElementById("signal").innerHTML = "Loading...";

    try {

        const response = await fetch("/signal", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                pair: pair,
                timeframe: timeframe,
                market: market
            })
        });

        const data = await response.json();

        document.getElementById("signal").innerHTML = data.signal;
        document.getElementById("ema9").innerHTML = data.ema9;
        document.getElementById("ema21").innerHTML = data.ema21;
        document.getElementById("rsi").innerHTML = data.rsi;
        document.getElementById("macd").innerHTML = data.macd;
        document.getElementById("support").innerHTML = data.support;
        document.getElementById("resistance").innerHTML = data.resistance;

    } catch (e) {

        document.getElementById("signal").innerHTML = "Server Error";

    }

});
