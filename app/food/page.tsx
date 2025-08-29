"use client";

import { useState } from "react";

export default function FoodEntryPage() {
  const [dish, setDish] = useState("");
  const [ingredient, setIngredient] = useState("");
  const [ingredients, setIngredients] = useState<string[]>([]);

  const handleAddIngredient = () => {
    if (ingredient.trim() !== "") {
      setIngredients([...ingredients, ingredient.trim()]);
      setIngredient("");
    }
  };

  const handleClear = () => {
    setDish("");
    setIngredients([]);
    setIngredient("");
  };

  const handleSubmit = () => {
    alert(`Dish: ${dish}\nIngredients: ${ingredients.join(", ")}`);
    // ✅ Later: Send this data to backend via API call
  };

  return (
    <div className="min-h-screen flex items-center justify-center animate-gradient px-6">
      <div className="bg-white/95 p-10 rounded-2xl shadow-2xl w-full max-w-4xl space-y-8">
        <h1 className="text-3xl font-bold text-blue-800 text-center">
          Food Entry 🍲
        </h1>

        {/* Box 1 - Dish Name */}
        <div className="bg-blue-50 p-6 rounded-xl shadow-md">
          <label className="block font-semibold text-gray-700 mb-2">
            Dish Name
          </label>
          <input
            type="text"
            value={dish}
            onChange={(e) => setDish(e.target.value)}
            placeholder="e.g. Chicken Curry"
            className="w-full border rounded-lg px-4 py-3 shadow-sm focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Box 2 - Ingredients */}
        <div className="bg-green-50 p-6 rounded-xl shadow-md">
          <label className="block font-semibold text-gray-700 mb-2">
            Ingredients
          </label>

          {/* Input + Add button */}
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              value={ingredient}
              onChange={(e) => setIngredient(e.target.value)}
              placeholder="e.g. Onion"
              className="flex-1 border rounded-lg px-4 py-3 shadow-sm focus:ring-2 focus:ring-green-500"
            />
            <button
              type="button"
              onClick={handleAddIngredient}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition"
            >
              Add
            </button>
          </div>

          {/* Ingredient List */}
          <div className="bg-white rounded-lg p-4 h-52 overflow-y-auto shadow-inner border">
            {ingredients.length > 0 ? (
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                {ingredients.map((ing, index) => (
                  <li key={index}>{ing}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No ingredients added yet.</p>
            )}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-between">
          <button
            type="button"
            onClick={handleSubmit}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Submit
          </button>
          <button
            type="button"
            onClick={handleClear}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}
