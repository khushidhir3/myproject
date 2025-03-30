import os
from flask import Flask, request, jsonify, session
import yfinance as yf

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Investment recommendations logic
def get_recommendations(goal):
    """Returns investment options based on goal"""
    investment_options = {
        "short-term": ["Stock A", "Stock B", "ETF C"],
        "long-term": ["Mutual Fund X", "Gold Y", "Index Fund Z"],
        "retirement": ["Pension Fund A", "Government Bonds B"],
        "high-risk": ["Crypto A", "Tech Startup B"]
    }
    return investment_options.get(goal, ["General Investment Fund"])

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Returns investment recommendations based on user goals."""
    
    # Ensure user is logged in
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    data = request.json
    goal = data.get("goal", "default")

    # Get recommendations
    recommendations = get_recommendations(goal)
    
    return jsonify({"goal": goal, "suggested_investments": recommendations})

# Stock analysis function
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
