
from flask import Flask, render_template, request, jsonify
from analysis import analyze_market

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    pair = data.get("pair")
    timeframe = data.get("timeframe")

    result = analyze_market(pair, timeframe)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
