/**
 * Chat API Client
 *
 * API functions for chat interface communication with backend
 */

import apiClient from "./client";
import { ChatRequest, ChatResponse, ApiError } from "@/types/chat";

/**
 * Send a message to the AI chat assistant
 *
 * @param userId - ID of the authenticated user
 * @param request - Chat request payload (message and optional conversation_id)
 * @returns Promise resolving to chat response with conversation_id, response text, and tool_calls
 * @throws ApiError if request fails
 */
export async function sendMessage(
  userId: number,
  request: ChatRequest,
): Promise<ChatResponse> {
  try {
    const response = await apiClient.post<ChatResponse>(
      `/api/${userId}/chat`,
      request,
    );

    return response.data;
  } catch (error: unknown) {
    // Transform axios error to ApiError
    const err = error as {
      response?: { data?: { detail?: string }; status?: number };
      message?: string;
      code?: string;
    };
    const apiError: ApiError = {
      message:
        err.response?.data?.detail || err.message || "Failed to send message",
      status: err.response?.status,
      code: err.code,
    };

    throw apiError;
  }
}

/**
 * Get conversation history (optional - backend may not support this yet)
 *
 * @param userId - ID of the authenticated user
 * @param conversationId - ID of the conversation to fetch
 * @returns Promise resolving to array of messages
 * @throws ApiError if request fails
 */
export async function getConversationHistory(
  userId: number,
  conversationId: number,
): Promise<unknown> {
  try {
    const response = await apiClient.get(
      `/api/${userId}/conversations/${conversationId}`,
    );

    return response.data;
  } catch (error: unknown) {
    const err = error as {
      response?: { data?: { detail?: string }; status?: number };
      message?: string;
      code?: string;
    };
    const apiError: ApiError = {
      message:
        err.response?.data?.detail ||
        err.message ||
        "Failed to fetch conversation history",
      status: err.response?.status,
      code: err.code,
    };

    throw apiError;
  }
}

/**
 * List all conversations for a user (optional - backend may not support this yet)
 *
 * @param userId - ID of the authenticated user
 * @returns Promise resolving to array of conversations
 * @throws ApiError if request fails
 */
export async function listConversations(userId: number): Promise<unknown> {
  try {
    const response = await apiClient.get(`/api/${userId}/conversations`);

    return response.data;
  } catch (error: unknown) {
    const err = error as {
      response?: { data?: { detail?: string }; status?: number };
      message?: string;
      code?: string;
    };
    const apiError: ApiError = {
      message:
        err.response?.data?.detail ||
        err.message ||
        "Failed to fetch conversations",
      status: err.response?.status,
      code: err.code,
    };

    throw apiError;
  }
}
