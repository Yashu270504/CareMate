"use client";

import { useState } from "react";

export default function MedicinesEntryPage() {
  const [medicine, setMedicine] = useState("");
  const [medicines, setMedicines] = useState<string[]>([]);

  const handleAddMedicine = () => {
    if (medicine.trim() !== "") {
      setMedicines([...medicines, medicine.trim()]);
      setMedicine("");
    }
  };

  const handleClear = () => {
    setMedicine("");
    setMedicines([]);
  };

  const handleSubmit = () => {
    alert(
      `Medicines:\n${medicines
        .map((med, index) => `${index + 1}. ${med}`)
        .join("\n")}`
    );
    // ✅ Later: Send this data to backend via API call
  };

  return (
    <div className="min-h-screen flex items-center justify-center animate-gradient px-6">
      <div className="bg-white/95 p-10 rounded-2xl shadow-2xl w-full max-w-4xl space-y-8">
        <h1 className="text-3xl font-bold text-blue-800 text-center">
          Medicines Entry 💊
        </h1>

        {/* Box 1 - Medicine Name */}
        <div className="bg-yellow-50 p-6 rounded-xl shadow-md">
          <label className="block font-semibold text-gray-700 mb-2">
            Medicine Name
          </label>
          <input
            type="text"
            value={medicine}
            onChange={(e) => setMedicine(e.target.value)}
            placeholder="e.g. Paracetamol"
            className="w-full border rounded-lg px-4 py-3 shadow-sm focus:ring-2 focus:ring-yellow-500"
          />

          <button
            type="button"
            onClick={handleAddMedicine}
            className="mt-4 bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700 transition"
          >
            Add
          </button>
        </div>

        {/* Medicine List */}
        <div className="bg-white rounded-xl p-4 h-52 overflow-y-auto shadow-inner border">
          {medicines.length > 0 ? (
            <ul className="list-decimal list-inside text-gray-700 space-y-1">
              {medicines.map((med, index) => (
                <li key={index}>{med}</li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 italic">No medicines added yet.</p>
          )}
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
