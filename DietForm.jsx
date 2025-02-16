import React, { useState } from "react";

const DietForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    age: "",
    gender: "",
    weight: "",
    health_conditions: [],
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === "checkbox") {
      setFormData((prev) => ({
        ...prev,
        health_conditions: checked
          ? [...prev.health_conditions, value]
          : prev.health_conditions.filter((c) => c !== value),
      }));
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.age || !formData.gender || !formData.weight) {
      alert("Please fill in all required fields.");
      return;
    }

    console.log("Submitting form data:", formData); // Debugging log
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Age:</label>
      <input type="number" name="age" value={formData.age} onChange={handleChange} required />

      <label>Gender:</label>
      <select name="gender" value={formData.gender} onChange={handleChange} required>
        <option value="">Select</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
      </select>

      <label>Weight (kg):</label>
      <input type="number" name="weight" value={formData.weight} onChange={handleChange} required />

      <label>Health Conditions (optional):</label>
      {["low bp", "high bp", "sugar", "diabetes", "heart disease"].map((condition) => (
        <label key={condition}>
          <input type="checkbox" name="health_conditions" value={condition} onChange={handleChange} />
          {condition}
        </label>
      ))}

      <button type="submit">Get Diet Plan</button>
    </form>
  );
};

export default DietForm;
