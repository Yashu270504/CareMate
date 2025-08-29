"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-white/80 backdrop-blur-md shadow-md fixed top-0 w-full z-50">
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        
        {/* Logo / App Name */}
        <h1 className="text-2xl font-bold text-blue-700">CareMate</h1>
        
        {/* Links */}
        <div className="space-x-6">
          <Link href="/" className="text-gray-800 hover:text-blue-600 transition">Home</Link>
          <Link href="/profile" className="text-gray-800 hover:text-blue-600 transition">Profile</Link>
          <Link href="/food" className="text-gray-800 hover:text-blue-600 transition">Food Entry</Link>
          <Link href="/medicines" className="text-gray-800 hover:text-blue-600 transition">Medicines</Link>
          <Link href="/output" className="text-gray-800 hover:text-blue-600 transition">Results</Link>
        </div>
      </div>
    </nav>
  );
}
