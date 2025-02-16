import sys
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 🔥 Add CORS

# Add 'ml_model' directory to system path
sys.path.append(os.path.abspath("ml_model"))

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
CORS(app)  # 🔥 Enable CORS for all routes

# Import your recommendation function
try:
    from diet_recommendation import recommend_diet  # ✅ Ensure correct import
except ModuleNotFoundError:
    raise ModuleNotFoundError("Ensure 'diet_recommendation.py' is inside 'ml_model' and accessible.")

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    print("Received data:", data)  # Debugging log

    # Ensure required fields are present
    if not all(key in data for key in ['age', 'gender', 'weight']):
        return jsonify({"error": "Age, gender, and weight are required"}), 400

    try:
        # Get diet recommendations
        recommendations = recommend_diet(data)
        print("Sending response:", recommendations)  # Debugging log
        return jsonify({"recommended_30_day_diet": recommendations})
    except Exception as e:
        print("Error:", str(e))  # Debugging log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
