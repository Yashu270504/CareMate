"use client";

export default function ChatbotButton() {
  const handleClick = () => {
    if (window.watsonInstance) {
      window.watsonInstance.openWindow(); // ✅ safely open
    } else {
      alert("Chat is still loading, please try again in a moment.");
    }
  };

  return (
    <button
      onClick={handleClick}
      className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-lg hover:bg-blue-700 transition"
    >
      💬
    </button>
  );
}
