/**
 * ChatMessage Component
 *
 * Individual message display with user/assistant styling, word wrapping, timestamp formatting, and tool call display
 */

"use client";

import { memo } from "react";
import { ChatMessageProps } from "@/types/chat";
import { isUserMessage, isAssistantMessage, hasToolCalls } from "@/types/chat";
import { formatDistanceToNow, format, isToday, isYesterday } from "date-fns";
import ToolCallDisplay from "./ToolCallDisplay";

function ChatMessage({ message }: ChatMessageProps) {
  const isUser = isUserMessage(message);
  const isAssistant = isAssistantMessage(message);

  // Format timestamp with date-fns
  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = (now.getTime() - date.getTime()) / (1000 * 60);

    // Use relative time for recent messages (less than 1 hour)
    if (diffInMinutes < 60) {
      return formatDistanceToNow(date, { addSuffix: true });
    }

    // Use absolute time for older messages
    if (isToday(date)) {
      return format(date, "h:mm a"); // "2:30 PM"
    } else if (isYesterday(date)) {
      return `Yesterday ${format(date, "h:mm a")}`; // "Yesterday 2:30 PM"
    } else {
      return format(date, "MMM d, h:mm a"); // "Jan 14, 2:30 PM"
    }
  };

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"}`}
      role="article"
      aria-label={`${isUser ? "User" : "Assistant"} message`}
    >
      <div
        className={`max-w-full sm:max-w-[85%] md:max-w-[75%] lg:max-w-[70%] rounded-lg px-4 py-3 ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white text-gray-900 border border-gray-200"
        }`}
      >
        {/* Message Content */}
        <div className="whitespace-pre-wrap break-words">{message.content}</div>

        {/* Tool Calls Display (for assistant messages only) */}
        {isAssistant && hasToolCalls(message) && (
          <ToolCallDisplay toolCalls={message.tool_calls} />
        )}

        {/* Timestamp (if available) */}
        {message.created_at && (
          <div
            className={`text-xs mt-2 ${
              isUser ? "text-blue-100" : "text-gray-500"
            }`}
          >
            {formatTimestamp(message.created_at)}
          </div>
        )}
      </div>
    </div>
  );
}

export default memo(ChatMessage);
