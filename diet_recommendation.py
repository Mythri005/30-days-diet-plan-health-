import pickle
import numpy as np
import random

# Load the model only once at the top of the file
model = None

def load_model():
    global model
    if model is None:
        with open("ml_model/model.pkl", "rb") as file:
            model = pickle.load(file)
    return model

# Load the model at the start
load_model()

# Meal plans for different health conditions
diet_plans = {
    "Diabetes": [
        {"breakfast": "Ragi dosa", "lunch": "Bajra khichdi", "dinner": "Foxtail millet soup"},
        {"breakfast": "Jowar roti", "lunch": "Quinoa salad", "dinner": "Brown rice & dal"},
        {"breakfast": "Millet porridge", "lunch": "Sprouts salad", "dinner": "Grilled tofu"}
    ],
    "Heart Disease": [
        {"breakfast": "Oats upma", "lunch": "Vegetable millet pulao", "dinner": "Dal khichdi"},
        {"breakfast": "Cornflakes with millet milk", "lunch": "Sprout salad", "dinner": "Grilled vegetables"},
        {"breakfast": "Ragi idli", "lunch": "Foxtail millet curry", "dinner": "Millet dosa"}
    ],
    "High BP": [
        {"breakfast": "Fruit salad", "lunch": "Millet chapati with curry", "dinner": "Vegetable stew"},
        {"breakfast": "Egg omelet", "lunch": "Rice and dal", "dinner": "Sautéed greens"},
        {"breakfast": "Smoothie bowl", "lunch": "Chickpea salad", "dinner": "Grilled tofu"}
    ],
    "Low BP": [
        {"breakfast": "Banana smoothie", "lunch": "Coconut rice", "dinner": "Pumpkin soup"},
        {"breakfast": "Peanut butter toast", "lunch": "Rajma rice", "dinner": "Vegetable soup"},
        {"breakfast": "Chia seed pudding", "lunch": "Spinach dal", "dinner": "Sweet potato stir-fry"}
    ],
    "Menstrual Health": [
        {"breakfast": "Ragi malt", "lunch": "Paneer paratha", "dinner": "Palak dal"},
        {"breakfast": "Sprouted moong salad", "lunch": "Pumpkin soup", "dinner": "Mixed millet roti"},
        {"breakfast": "Sesame seed smoothie", "lunch": "Chickpea curry", "dinner": "Dal tadka"}
    ]
}

# Function to generate a 30-day meal plan based on predicted category
def generate_30_day_plan(predicted_category):
    if predicted_category not in diet_plans:
        predicted_category = "Diabetes"  # Default fallback
    
    selected_meals = diet_plans[predicted_category]

    # If there are fewer than 30 unique meals, cycle through and mix them better
    if len(selected_meals) < 30:
        selected_meals = selected_meals * (30 // len(selected_meals)) + selected_meals[:(30 % len(selected_meals))]

    # Create the meal plan for 30 days, ensuring meals are distributed well
    full_plan = {}
    for day in range(1, 31):
        full_plan[day] = selected_meals[day - 1]  # Keep meals in order (no shuffling)

    # Sort the dictionary by the key (day)
    full_plan = dict(sorted(full_plan.items()))

    return full_plan




# Function to recommend diet based on user data
def recommend_diet(user_data):
    gender_map = {'male': 0, 'female': 1, 'other': 2}
    user_data['gender'] = gender_map.get(user_data.get('gender', '').lower(), -1)

    # Get health conditions and map them to binary features
    has_low_bp = 1 if 'low bp' in user_data.get('health_conditions', []) else 0
    has_high_bp = 1 if 'high bp' in user_data.get('health_conditions', []) else 0
    has_diabetes = 1 if 'diabetes' in user_data.get('health_conditions', []) else 0
    has_heart_disease = 1 if 'heart disease' in user_data.get('health_conditions', []) else 0
    has_menstrual_health = 1 if 'menstrual health' in user_data.get('health_conditions', []) else 0
    
    # Default value for 'sugar' if not provided
    sugar = user_data.get('sugar', 0)  # Assuming 0 if sugar is not provided

    # Create feature vector for prediction
    input_data = np.array([[user_data.get('age', 0),
                            user_data.get('gender', 0),
                            user_data.get('weight', 0),
                            has_diabetes,
                            has_low_bp,
                            has_high_bp,
                            has_heart_disease,
                            has_menstrual_health,
                            sugar]])  # Adding 'sugar' as the 9th feature

    # Make prediction
    predicted_category = model.predict(input_data)[0]

    # Generate and return 30-day meal plan based on predicted category
    return generate_30_day_plan(predicted_category)
