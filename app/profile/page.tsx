"use client";

import { useState } from "react";

export default function ProfilePage() {
  const [name, setName] = useState("");
  const [dob, setDob] = useState("");
  const [age, setAge] = useState("");
  const [conditions, setConditions] = useState("");
  const [allergies, setAllergies] = useState("");

  const handleSave = () => {
    alert("Profile Saved ✅ (Later this will be sent to backend/cloud)");
  };

  const handleDelete = () => {
    setName("");
    setDob("");
    setAge("");
    setConditions("");
    setAllergies("");
    alert("Profile Deleted ❌");
  };

  return (
    <div className="min-h-screen flex items-center justify-center animate-gradient px-6">
      <div className="bg-white/95 p-8 rounded-2xl shadow-xl w-full max-w-2xl">
        <h1 className="text-3xl font-bold text-blue-800 mb-6">User Profile</h1>

        <form className="space-y-5">
          {/* Name */}
          <div>
            <label className="block font-medium text-gray-700">Full Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 block w-full border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500"
              placeholder="Enter your name"
            />
          </div>

          {/* Date of Birth */}
          <div>
            <label className="block font-medium text-gray-700">Date of Birth</label>
            <input
              type="date"
              value={dob}
              onChange={(e) => setDob(e.target.value)}
              className="mt-1 block w-full border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Age */}
          <div>
            <label className="block font-medium text-gray-700">Age</label>
            <input
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="mt-1 block w-full border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500"
              placeholder="Enter age"
            />
          </div>

          {/* Medical Conditions */}
          <div>
            <label className="block font-medium text-gray-700">Medical Conditions</label>
            <textarea
              value={conditions}
              onChange={(e) => setConditions(e.target.value)}
              className="mt-1 block w-full border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500"
              placeholder="e.g. Diabetes, Hypertension"
              rows={3}
            />
          </div>

          {/* Allergies */}
          <div>
            <label className="block font-medium text-gray-700">Known Sensitivities</label>
            <textarea
              value={allergies}
              onChange={(e) => setAllergies(e.target.value)}
              className="mt-1 block w-full border rounded-lg px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500"
              placeholder="e.g. Peanuts, Penicillin"
              rows={3}
            />
          </div>

          {/* Buttons */}
          <div className="flex justify-between mt-6">
            <button
              type="button"
              onClick={handleSave}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              Save Profile
            </button>

            <button
              type="button"
              onClick={handleDelete}
              className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition"
            >
              Delete Profile
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
