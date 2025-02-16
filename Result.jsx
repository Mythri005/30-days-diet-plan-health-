import React from "react";

const Result = ({ data }) => {
  if (!data) return <p>No diet plan available. Please submit the form.</p>;

  return (
    <div>
      <h2>Recommended 30-Day Diet Plan</h2>
      <ul>
        {Object.entries(data).map(([day, meals]) => (
          <li key={day}>
            <strong>Day {day}:</strong>
            <p>🍽️ Breakfast: {meals.breakfast}</p>
            <p>🥗 Lunch: {meals.lunch}</p>
            <p>🌙 Dinner: {meals.dinner}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Result;
