import os
from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

def analyze_stock(symbol):
    """Fetch stock data using Yahoo Finance API"""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")

    if data.empty:
        return {"error": "Invalid stock symbol or no data available."}

    # Extract stock details
    current_price = round(data["Close"].iloc[-1], 2)
    price_change = round(current_price - data["Open"].iloc[-1], 2)
    volume = int(data["Volume"].iloc[-1])

    # Simple Buy/Sell/Hold Recommendation
    recommendation = "BUY" if price_change > 0 else "SELL" if price_change < 0 else "HOLD"

    return {
        "symbol": symbol,
        "current_price": current_price,
        "price_change": price_change,
        "trading_volume": volume,
        "recommendation": recommendation
    }

@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    """API route to fetch stock insights"""
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    stock_info = analyze_stock(symbol)
    return jsonify(stock_info)

@app.route("/api/stock/history")
def get_stock_history():
    """Fetch historical stock data for the past 5 days"""
    symbol = request.args.get("symbol", "").upper()

    stock = yf.Ticker(symbol)
    history = stock.history(period="5d")

    if history.empty:
        return jsonify({"error": "No historical data available."})

    dates = history.index.strftime("%Y-%m-%d").tolist()
    prices = history["Close"].tolist()

    return jsonify({"symbol": symbol, "dates": dates, "prices": prices})

if __name__ == '__main__':
    app.run(debug=True)