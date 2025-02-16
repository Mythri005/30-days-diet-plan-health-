import React, { useState } from "react";
import "./styles.css"; // ✅ Import your CSS file

const App = () => {
  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    weight: "",
    health_conditions: [],
    sugar: "",
  });

  const [dietPlan, setDietPlan] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setFormData((prev) => ({
        ...prev,
        health_conditions: checked
          ? [...prev.health_conditions, value]
          : prev.health_conditions.filter((item) => item !== value),
      }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const requestData = {
      ...formData,
      age: Number(formData.age),
      weight: Number(formData.weight),
      sugar: Number(formData.sugar) || 0,
    };

    console.log("Sending data to backend:", requestData);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Received diet plan:", data);

      if (data.recommended_30_day_diet) {
        setDietPlan(data.recommended_30_day_diet);
      } else {
        setError("No diet plan available.");
      }
    } catch (err) {
      console.error("Error fetching diet plan:", err);
      setError("Failed to fetch diet plan. Please try again.");
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Diet Recommendation</h1>
        <p>Get a 30-day meal plan based on your health profile</p>
      </header>

      {/* Form Container for Centering */}
      <div className="form-container">
        <form onSubmit={handleSubmit} className="form-content">
          <div>
            <label>Age:</label>
            <input type="number" name="age" value={formData.age} onChange={handleChange} required />
          </div>
          <div>
            <label>Gender:</label>
            <select name="gender" value={formData.gender} onChange={handleChange} required>
              <option value="">Select</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div>
            <label>Weight (kg):</label>
            <input type="number" name="weight" value={formData.weight} onChange={handleChange} required />
          </div>
          <div>
            <label>Health Conditions (optional):</label>
            <div className="checkbox-group">
              <label><input type="checkbox" value="low bp" onChange={handleChange} /> Low BP</label>
              <label><input type="checkbox" value="high bp" onChange={handleChange} /> High BP</label>
              <label><input type="checkbox" value="sugar" onChange={handleChange} /> Sugar</label>
              <label><input type="checkbox" value="diabetes" onChange={handleChange} /> Diabetes</label>
              <label><input type="checkbox" value="heart disease" onChange={handleChange} /> Heart Disease</label>
            </div>
          </div>
          <button type="submit">Get Diet Plan</button>
        </form>
      </div>

      {/* Display diet plan */}
      {error && <p className="text-red-500 mt-4">{error}</p>}
      {dietPlan && (
        <div className="meal-plan-container">
          {Object.entries(dietPlan).map(([day, meals]) => (
            <div key={day} className="meal-day">
              <h4>Day {day}</h4>
              <p><strong>Breakfast:</strong> {meals.breakfast}</p>
              <p><strong>Lunch:</strong> {meals.lunch}</p>
              <p><strong>Dinner:</strong> {meals.dinner}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
