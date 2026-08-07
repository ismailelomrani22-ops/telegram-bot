from flask import Flask, request, jsonify, render_template
from analysis import analyze_market
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "No data"
            })

        pair = data.get("pair")
        timeframe = data.get("timeframe")

        result = analyze_market(pair, timeframe)

        return jsonify(result)

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
