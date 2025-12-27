from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "strategies.json"


def load_strategies():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_strategies(strats):
    with open(DATA_FILE, "w") as f:
        json.dump(strats, f)


strategies = load_strategies()


@app.route("/")
def home():
    return "<h1>TradeShare Chain 🚀</h1><p>Your trading bot network LIVE!</p>"


@app.route("/upload_strategy", methods=["POST"])
def upload():
    data = request.json
    strategy = {
        "id": len(strategies),
        "strategy": data["strategy"],
        "author": data["wallet"][:10] + "...",
        "votes": 0,
    }
    strategies.append(strategy)
    save_strategies(strategies)
    return jsonify({"success": True, "strategy": strategy})


@app.route("/strategies")
def strategies_list():
    top = sorted(strategies, key=lambda x: x["votes"], reverse=True)
    return jsonify({"top_strategies": top})


if __name__ == "__main__":
    print("🚀 TradeShare starting at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)
