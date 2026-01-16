/**
 * TypingIndicator Component
 *
 * Loading indicator with animated dots
 */

"use client";

import { TypingIndicatorProps } from "@/types/chat";

export default function TypingIndicator({
  text = "AI is typing...",
}: TypingIndicatorProps) {
  return (
    <div className="flex justify-start">
      <div className="max-w-full sm:max-w-[85%] md:max-w-[75%] lg:max-w-[70%] bg-white border border-gray-200 rounded-lg px-4 py-3">
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-600">{text}</span>
          <div className="flex space-x-1">
            <div
              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
              style={{ animationDelay: "0ms" }}
            ></div>
            <div
              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
              style={{ animationDelay: "150ms" }}
            ></div>
            <div
              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
              style={{ animationDelay: "300ms" }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
}
