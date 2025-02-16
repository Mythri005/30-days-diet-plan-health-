import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ✅ Sample dataset for training (dummy data)
data = {
    "age": np.random.randint(20, 70, 100),
    "gender": np.random.randint(0, 2, 100),  # 0: Female, 1: Male
    "weight": np.random.randint(50, 100, 100),
    "low_bp": np.random.randint(0, 2, 100),
    "high_bp": np.random.randint(0, 2, 100),
    "sugar": np.random.randint(70, 200, 100),
    "diabetes": np.random.randint(0, 2, 100),
    "heart_disease": np.random.randint(0, 2, 100),
    "menstrual_health": np.random.randint(0, 2, 100),  
}

df = pd.DataFrame(data)

# ✅ Define labels (health conditions that require specific diets)
df["condition"] = np.select(
    [
        (df["diabetes"] == 1),
        (df["heart_disease"] == 1),
        (df["high_bp"] == 1),
        (df["low_bp"] == 1),
        (df["menstrual_health"] == 1),
    ],
    ["Diabetes", "Heart Disease", "High BP", "Low BP", "Menstrual Health"],
    default="General"
)

# ✅ Split data
X = df.drop(columns=["condition"])
y = df["condition"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ✅ Save the trained model
with open("ml_model/model.pkl", "wb") as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as model.pkl")
