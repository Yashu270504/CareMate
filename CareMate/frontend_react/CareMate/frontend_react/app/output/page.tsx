"use client";

import { useState, useEffect } from "react";

export default function ResultsPage() {
  // ✅ These will later come from backend API
  const [results, setResults] = useState<{ food: string; status: string }[]>([]);
  const [alternatives, setAlternatives] = useState<{ food: string }[]>([]);

  // Mock backend fetch (replace with actual API call)
  useEffect(() => {
    // Example: replace this with your backend fetch
    const mockResults = [
      { food: "Chicken Curry", status: "Safe ✅" },
      { food: "Peanut Sauce", status: "Dangerous ⚠️" },
    ];
    const mockAlternatives = [
      { food: "Grilled Chicken" },
      { food: "Vegetable Soup" },
    ];

    setResults(mockResults);
    setAlternatives(mockAlternatives);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center animate-gradient px-6">
      <div className="bg-white/95 p-10 rounded-2xl shadow-2xl w-full max-w-4xl space-y-8">
        <h1 className="text-3xl font-bold text-blue-800 text-center">
          Results 📊
        </h1>

        {/* Box 1 - Results */}
        <div className="bg-red-50 p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Food Status</h2>
          <div className="bg-white rounded-lg p-4 h-52 overflow-y-auto shadow-inner border">
            {results.length > 0 ? (
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                {results.map((res, index) => (
                  <li key={index}>
                    {res.food}: <span className={res.status.includes("Safe") ? "text-green-600" : "text-red-600"}>{res.status}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No results yet.</p>
            )}
          </div>
        </div>

        {/* Box 2 - Alternatives */}
        <div className="bg-green-50 p-6 rounded-xl shadow-md">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Suggested Alternatives</h2>
          <div className="bg-white rounded-lg p-4 h-52 overflow-y-auto shadow-inner border">
            {alternatives.length > 0 ? (
              <ul className="list-disc list-inside text-gray-700 space-y-1">
                {alternatives.map((alt, index) => (
                  <li key={index}>{alt.food}</li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 italic">No alternatives suggested yet.</p>
            )}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-between">
          <button
            type="button"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
            onClick={() => alert("Back to Home (Implement routing)")}
          >
            Back to Home
          </button>
          <button
            type="button"
            className="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700 transition"
            onClick={() => alert("Edit Entries (Implement routing)")}
          >
            Edit Entries
          </button>
        </div>
      </div>
    </div>
  );
}
