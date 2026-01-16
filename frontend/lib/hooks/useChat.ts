/**
 * useChat Hook
 *
 * Custom hook for chat state management with optimistic updates and conversation persistence
 */

"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Message,
  ChatRequest,
  ChatResponse,
  UseChatReturn,
  CONVERSATION_ID_KEY,
  generateTempMessageId,
  validateMessage,
} from "@/types/chat";
import { sendMessage as sendMessageAPI } from "@/lib/api/chat";
import { useAuth } from "@/contexts/AuthContext";
import toast from "react-hot-toast";

export function useChat(): UseChatReturn {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      const savedConversationId = localStorage.getItem(CONVERSATION_ID_KEY);
      if (savedConversationId) {
        const id = parseInt(savedConversationId, 10);
        if (!isNaN(id)) {
          console.log(
            "[useChat] Loaded conversation ID from localStorage:",
            id,
          );
          setConversationId(id);
        }
      }
    }
  }, []);

  // Save conversation ID to localStorage whenever it changes
  useEffect(() => {
    if (typeof window !== "undefined") {
      if (conversationId !== null) {
        console.log(
          "[useChat] Saving conversation ID to localStorage:",
          conversationId,
        );
        localStorage.setItem(CONVERSATION_ID_KEY, conversationId.toString());
      } else {
        console.log("[useChat] Clearing conversation ID from localStorage");
        localStorage.removeItem(CONVERSATION_ID_KEY);
      }
    }
  }, [conversationId]);

  /**
   * Send a message to the AI assistant
   */
  const sendMessage = useCallback(
    async (content: string): Promise<void> => {
      if (!user) {
        console.error("[useChat] Cannot send message: No user");
        toast.error("Please log in to send messages");
        return;
      }

      // Prevent duplicate requests if already loading
      if (isLoading) {
        console.warn("[useChat] Request already in progress, ignoring duplicate");
        return;
      }

      // Validate message
      const validation = validateMessage(content);
      if (!validation.valid) {
        console.error("[useChat] Message validation failed:", validation.error);
        toast.error(validation.error || "Invalid message");
        return;
      }

      console.log("[useChat] Sending message for user:", user.id);

      // Create optimistic user message
      const optimisticMessage: Message = {
        id: generateTempMessageId(),
        role: "user",
        content: content.trim(),
        created_at: new Date().toISOString(),
      };

      // Optimistic update - add user message immediately
      setMessages((prev) => [...prev, optimisticMessage]);
      setIsLoading(true);
      setError(null);

      try {
        // Prepare request
        const request: ChatRequest = {
          message: content.trim(),
        };

        // Include conversation ID if exists
        if (conversationId !== null) {
          request.conversation_id = conversationId;
        }

        // Send message to backend
        const response: ChatResponse = await sendMessageAPI(user.id, request);
        console.log("[useChat] Message sent successfully:", response);

        // Update conversation ID if this is a new conversation
        if (conversationId === null && response.conversation_id) {
          console.log(
            "[useChat] New conversation created:",
            response.conversation_id,
          );
          setConversationId(response.conversation_id);
        }

        // Create assistant message from response
        const assistantMessage: Message = {
          role: "assistant",
          content: response.response,
          tool_calls: response.tool_calls,
          created_at: new Date().toISOString(),
        };

        // Add assistant message to state
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err: unknown) {
        console.error("[useChat] Failed to send message:", err);

        // Rollback optimistic update - remove user message
        setMessages((prev) =>
          prev.filter((m) => m.id !== optimisticMessage.id),
        );

        // Set error state with better messaging for rate limits
        const error = err as { message?: string };
        let errorMessage = error.message || "Failed to send message";
        
        // Check if it's a rate limit error
        if (errorMessage.includes("429") || errorMessage.includes("quota") || errorMessage.includes("rate limit")) {
          errorMessage = "⏱️ API rate limit reached. Please wait a moment and try again, or check your API quota.";
        }
        
        setError(errorMessage);
        toast.error(errorMessage);

        throw err;
      } finally {
        setIsLoading(false);
      }
    },
    [user, conversationId, isLoading],
  );

  /**
   * Start a new conversation
   */
  const startNewConversation = useCallback(() => {
    console.log("[useChat] Starting new conversation");
    setMessages([]);
    setConversationId(null);
    setError(null);
    setIsLoading(false);
  }, []);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    console.log("[useChat] Clearing error");
    setError(null);
  }, []);

  return {
    messages,
    conversationId,
    isLoading,
    error,
    sendMessage,
    startNewConversation,
    clearError,
  };
}
