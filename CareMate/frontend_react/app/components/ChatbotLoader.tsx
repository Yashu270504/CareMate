"use client";
import { useEffect } from "react";

declare global {
  interface Window {
    watsonAssistantChatOptions: any;
    watsonInstance?: any;
  }
}

export default function ChatbotLoader() {
  useEffect(() => {
    window.watsonAssistantChatOptions = {
      integrationID: "17528a45-ee62-41ec-90c4-d42745945410", // ✅ yours
      region: "au-syd", // ✅ must stay au-syd
      serviceInstanceID: "646058b4-559c-4a73-8eee-83ff935f5a47",
      onLoad: async (instance: any) => {
        window.watsonInstance = instance;
        await instance.render();
      },
    };

    const script = document.createElement("script");
    // ✅ keep global (CDN handles it)
    script.src =
      "https://web-chat.global.assistant.watson.appdomain.cloud/versions/latest/WatsonAssistantChatEntry.js";
    script.async = true;
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return null;
}
