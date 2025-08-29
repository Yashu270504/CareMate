"use client";

import Image from "next/image";

export default function Home() {
  return (
    <div className="relative min-h-screen flex">
      
      {/* Left Side with gradient */}
      <div className="w-3/5 flex items-center justify-center px-12 animate-gradient">
        <div className="max-w-xl">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-6">
            Welcome to <span className="text-blue-800">CareMate</span>
          </h1>
          <p className="text-2xl font-medium text-gray-700 mb-8">
            Your personalized wellness companion 🌿💊
          </p>

          <div className="bg-white/90 p-6 rounded-2xl shadow-lg">
            <h3 className="text-xl font-semibold text-blue-900 mb-3">
              About This Platform
            </h3>
            <p className="text-gray-800 leading-relaxed">
              CareMate is designed to support patients and caregivers by
              identifying possible risks between prescribed medicines,
              dietary choices, and existing health conditions.
              <br />
              <br />
              It provides clear warnings where interactions might be harmful
              and suggests safer alternatives — helping you make informed
              decisions for better health and wellness.
            </p>
          </div>
        </div>
      </div>

      {/* Right Side Image */}
      <div className="w-2/5 h-screen relative">
        <Image
          src="/intro_page_bg.jpg"
          alt="Healthcare illustration"
          fill
          className="object-cover"
        />
      </div>
    </div>
  );
}
