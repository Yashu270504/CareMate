"use client";

import Image from "next/image";
import { useState } from "react";

export default function ChatbotButton() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-14 h-14 rounded-full shadow-lg bg-white flex items-center justify-center hover:scale-110 transition"
        >
          <Image
            src="/chatbox_icon.png"   // 👈 Place icon in public/
            alt="Chatbot"
            width={40}
            height={40}
            className="rounded-full"
          />
        </button>
      </div>

      {/* Chatbot Popup */}
      {isOpen && (
        <div className="fixed bottom-20 right-6 w-80 h-96 bg-white shadow-xl rounded-xl p-4 z-50">
          <h3 className="font-bold text-blue-800">💬 CareMate Chatbot</h3>
          <div className="mt-2 flex flex-col h-[85%]">
            <div className="flex-1 overflow-y-auto border p-2 mb-2 rounded-lg text-sm">
              {/* Messages will go here (connect to backend later) */}
              <p className="text-gray-500">👋 Hello! How can I help you today?</p>
            </div>
            <input
              type="text"
              placeholder="Type a message..."
              className="border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      )}
    </>
  );
}
