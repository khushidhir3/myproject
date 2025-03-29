def get_recommendations(goal):
    investment_options = {
        "short-term": ["Stock A", "Stock B", "ETF C"],
        "long-term": ["Mutual Fund X", "Gold Y", "Index Fund Z"],
        "retirement": ["Pension Fund A", "Government Bonds B"],
        "high-risk": ["Crypto A", "Tech Startup B"]
    }
    return investment_options.get(goal, ["General Investment Fund"])
