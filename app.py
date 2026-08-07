from flask import Flask, request, jsonify
from analysis import analyze_market
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Telegram Bot API is running"
    })

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data received"}), 400

    pair = data.get("pair")
    timeframe = data.get("timeframe")

    if not pair or not timeframe:
        return jsonify({"error": "pair and timeframe are required"}), 400

    result = analyze_market(pair, timeframe)

    print(result)

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
