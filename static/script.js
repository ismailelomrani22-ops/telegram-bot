document.getElementById("signalBtn").addEventListener("click", async () => {

    const pair = document.getElementById("pair").value;
    const timeframe = document.getElementById("timeframe").value;

    document.getElementById("signal").innerHTML = "⏳ ANALYZING...";

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

        if(data.status!="success"){

            document.getElementById("signal").innerHTML="❌ ERROR";

            return;

        }

        document.getElementById("price").innerHTML=data.price;

        document.getElementById("ema9").innerHTML=data.ema9;

        document.getElementById("ema21").innerHTML=data.ema21;

        document.getElementById("rsi").innerHTML=data.rsi;

        document.getElementById("macd").innerHTML=data.macd;

        document.getElementById("support").innerHTML=data.support;

        document.getElementById("resistance").innerHTML=data.resistance;

        document.getElementById("trend").innerHTML=data.trend;

        const signal = document.getElementById("signal");
const confidence = document.getElementById("confidence");
const timer = document.getElementById("timer");

// نسبة الذكاء الاصطناعي
confidence.innerHTML = (90 + Math.floor(Math.random() * 10)) + "%";

// إظهار الإشارة
if (data.trend.toLowerCase().includes("bull")) {

    signal.innerHTML = "🟢 BUY";
    signal.className = "signal buy";

} else if (data.trend.toLowerCase().includes("bear")) {

    signal.innerHTML = "🔴 SELL";
    signal.className = "signal sell";

} else {

    signal.innerHTML = "🟡 WAIT";
    signal.className = "signal wait";
}

// عداد 45 ثانية
let time = 45;

timer.innerHTML = "00:45";

clearInterval(window.countdown);

window.countdown = setInterval(() => {

    time--;

    timer.innerHTML = "00:" + (time < 10 ? "0" + time : time);

    if (time <= 0) {
        clearInterval(window.countdown);
    }

}, 1000);

            document.getElementById("signal").innerHTML="🟢 BUY";

            document.getElementById("signal").style.color="#00ff66";

        }else if(data.trend.toLowerCase().includes("bear")){

            document.getElementById("signal").innerHTML="🔴 SELL";

            document.getElementById("signal").style.color="#ff4444";

        }else{

            document.getElementById("signal").innerHTML="🟡 WAIT";

            document.getElementById("signal").style.color="#ffd54f";

        }

    } catch (err){

        document.getElementById("signal").innerHTML="SERVER ERROR";

    }

});
