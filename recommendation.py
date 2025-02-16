# routes/recommendation.py
from flask import Blueprint, request, jsonify
from ml_model.diet_recommendation import recommend_diet

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/api/recommend", methods=["POST"])
def get_diet_recommendation():
    data = request.get_json()

    # Validate required fields
    if "age" not in data or "gender" not in data:
        return jsonify({"error": "Missing required fields: age and gender are mandatory"}), 400

    gender_map = {"male": 0, "female": 1}
    numeric_gender = gender_map.get(data["gender"].lower())
    if numeric_gender is None:
        return jsonify({"error": "Invalid gender. Use 'male' or 'female'"}), 400

    user_data = {"age": data["age"], "gender": numeric_gender}
    optional_fields = ["weight", "low_bp", "high_bp", "sugar", "diabetes", "heart_disease", "menstrual_health"]
    for field in optional_fields:
        if field in data:
            user_data[field] = data[field]

    diet_plan = recommend_diet(user_data)
    return jsonify({"recommended_30_day_diet": list(diet_plan.values())})
