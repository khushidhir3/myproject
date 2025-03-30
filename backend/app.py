import os
from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import random

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def analyze_stock(symbol):
    """ Fetch stock data and extract key insights """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    response = requests.get(url).json()

    # Extract time series data
    time_series = response.get("Time Series (5min)", {})
    if not time_series:
        return {"error": "No stock data found"}

    # Get latest two timestamps
    sorted_timestamps = sorted(time_series.keys(), reverse=True)
    latest_timestamp = sorted_timestamps[0]
    previous_timestamp = sorted_timestamps[1] if len(sorted_timestamps) > 1 else None

    # Extract stock prices
    latest_data = time_series[latest_timestamp]
    current_price = float(latest_data["4. close"])
    volume = int(latest_data["5. volume"])

    # Calculate price change
    if previous_timestamp:
        previous_price = float(time_series[previous_timestamp]["4. close"])
        price_change = round(current_price - previous_price, 2)
    else:
        price_change = 0

    # Generate simple investment insight
    if price_change > 0:
        recommendation = "BUY"
    elif price_change < 0:
        recommendation = "SELL"
    else:
        recommendation = "HOLD"

    return {
        "symbol": symbol,
        "current_price": current_price,
        "price_change": price_change,
        "trading_volume": volume,
        "recommendation": recommendation
    }

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    """ API route to fetch stock insights """
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    stock_info = analyze_stock(symbol)
    return jsonify(stock_info)

@app.route("/api/stock/history")
def get_stock_history():
    symbol = request.args.get("symbol", "").upper()

    # Simulated stock price history (replace with real API calls)
    dates = ["2025-03-25", "2025-03-26", "2025-03-27", "2025-03-28", "2025-03-29"]
    prices = [random.uniform(100, 300) for _ in range(5)]  # Random prices

    return jsonify({"symbol": symbol, "dates": dates, "prices": prices})

if __name__ == '__main__':
    app.run(debug=True)
