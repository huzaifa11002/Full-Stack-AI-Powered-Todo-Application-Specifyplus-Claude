/**
 * ChatInterface Component
 *
 * Main chat container with header, message list, input area, and smart auto-scroll
 */

"use client";

import { useChat } from "@/lib/hooks/useChat";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useRef, useEffect, useState } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";
import EmptyChat from "./EmptyChat";

export default function ChatInterface() {
  const {
    messages,
    conversationId,
    isLoading,
    error,
    sendMessage,
    startNewConversation,
    clearError,
  } = useChat();

  const { logout } = useAuth();
  const router = useRouter();

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);

  // Detect user scroll position
  const handleScroll = () => {
    if (!messagesContainerRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } =
      messagesContainerRef.current;
    const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;

    setShouldAutoScroll(isNearBottom);
  };

  // Smart auto-scroll: scroll to bottom only when user is near bottom
  useEffect(() => {
    if (shouldAutoScroll) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, shouldAutoScroll]);

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <header
        className="bg-white border-b border-gray-200 px-4 py-3 sm:px-6"
        role="banner"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">
              AI Assistant
            </h1>
            <p
              className="text-sm text-gray-500"
              role="status"
              aria-live="polite"
            >
              {conversationId
                ? `Conversation #${conversationId}`
                : "New conversation"}
            </p>
          </div>
          <nav className="flex items-center gap-3" aria-label="Chat navigation">
            <button
              onClick={() => router.push("/dashboard")}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              aria-label="Switch to list view"
            >
              📋 List View
            </button>
            <button
              onClick={startNewConversation}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              aria-label="Start new conversation"
            >
              New Chat
            </button>
            <button
              onClick={logout}
              className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Logout"
            >
              Logout
            </button>
          </nav>
        </div>
      </header>

      {/* Messages Area */}
      <div
        ref={messagesContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto px-4 py-6 sm:px-6"
        role="main"
        aria-label="Chat messages"
      >
        {messages.length === 0 ? (
          <EmptyChat onSendMessage={sendMessage} />
        ) : (
          <div
            className="space-y-4"
            role="log"
            aria-live="polite"
            aria-atomic="false"
          >
            {messages.map((message, index) => (
              <ChatMessage key={message.id || index} message={message} />
            ))}
            {isLoading && <TypingIndicator />}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div
          className="px-4 py-3 bg-red-50 border-t border-red-200 sm:px-6"
          role="alert"
          aria-live="assertive"
        >
          <div className="flex items-center justify-between">
            <p className="text-sm text-red-800">{error}</p>
            <button
              onClick={clearError}
              className="text-sm font-medium text-red-600 hover:text-red-500"
              aria-label="Dismiss error message"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 px-4 py-4 sm:px-6">
        <ChatInput onSendMessage={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
