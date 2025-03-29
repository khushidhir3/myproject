from flask import Blueprint, request, jsonify
from api.investment_logic import get_recommendations

investment_blueprint = Blueprint('investment', __name__)

@investment_blueprint.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    goal = data.get("goal", "default")
    recommendations = get_recommendations(goal)
    return jsonify({"goal": goal, "suggested_investments": recommendations})
