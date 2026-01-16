/**
 * TypeScript Type Definitions for OpenAI ChatKit Frontend
 *
 * Feature: 002-chatkit-frontend
 * Date: 2026-01-14
 *
 * These types define the shape of data flowing through the chat interface.
 * All types are exported for use in components, hooks, and API clients.
 */

/**
 * Message entity representing a single message in a conversation
 */
export interface Message {
  /** Optional client-generated ID for optimistic updates */
  id?: string;

  /** Message sender role */
  role: "user" | "assistant";

  /** Message text content (1-2000 characters) */
  content: string;

  /** Optional tool invocations (assistant messages only) */
  tool_calls?: ToolCall[];

  /** ISO 8601 timestamp (e.g., "2026-01-14T19:30:00Z") */
  created_at?: string;
}

/**
 * Tool call entity representing an AI agent tool invocation
 */
export interface ToolCall {
  /** Tool name (e.g., "add_task", "list_tasks") */
  tool: string;

  /** Tool parameters as key-value pairs */
  params: Record<string, unknown>;

  /** Tool execution result as key-value pairs */
  result: Record<string, unknown>;
}

/**
 * Conversation entity representing a chat session
 */
export interface Conversation {
  /** Backend-generated conversation ID */
  id: number;

  /** ISO 8601 timestamp when conversation was created */
  created_at: string;

  /** ISO 8601 timestamp when conversation was last updated */
  updated_at: string;

  /** Optional preview text for conversation list */
  preview?: string;
}

/**
 * Chat state managed by useChat hook
 */
export interface ChatState {
  /** Current conversation messages in chronological order */
  messages: Message[];

  /** Active conversation ID (null for new conversation) */
  currentConversationId: number | null;

  /** True when API request is in progress */
  isLoading: boolean;

  /** Error message if request failed, null otherwise */
  error: string | null;
}

/**
 * Request payload for sending a message to the backend API
 */
export interface ChatRequest {
  /** Optional conversation ID to continue existing conversation */
  conversation_id?: number;

  /** User message (1-2000 characters, non-whitespace) */
  message: string;
}

/**
 * Response payload from backend API after sending a message
 */
export interface ChatResponse {
  /** Conversation ID (newly created or existing) */
  conversation_id: number;

  /** AI assistant's response message */
  response: string;

  /** Tools invoked by AI (empty array if none) */
  tool_calls: ToolCall[];
}

/**
 * Props for ChatInterface component
 */
export interface ChatInterfaceProps {
  /** Optional initial conversation ID to load */
  initialConversationId?: number;
}

/**
 * Props for ChatMessage component
 */
export interface ChatMessageProps {
  /** Message to display */
  message: Message;
}

/**
 * Props for ChatInput component
 */
export interface ChatInputProps {
  /** Callback when user sends a message */
  onSendMessage: (message: string) => void;

  /** Whether input is disabled (e.g., while loading) */
  disabled?: boolean;
}

/**
 * Props for ToolCallDisplay component
 */
export interface ToolCallDisplayProps {
  /** Array of tool calls to display */
  toolCalls: ToolCall[];
}

/**
 * Props for EmptyChat component
 */
export interface EmptyChatProps {
  /** Callback when user clicks a suggestion */
  onSendMessage: (message: string) => void;
}

/**
 * Props for ConversationList component (optional enhancement)
 */
export interface ConversationListProps {
  /** Callback when user selects a conversation */
  onSelectConversation: (id: number) => void;

  /** Currently active conversation ID */
  currentConversationId: number | null;
}

/**
 * Props for TypingIndicator component
 */
export interface TypingIndicatorProps {
  /** Optional custom text (defaults to "AI is typing...") */
  text?: string;
}

/**
 * Return type for useChat hook
 */
export interface UseChatReturn {
  /** Current conversation messages */
  messages: Message[];

  /** Active conversation ID */
  conversationId: number | null;

  /** Loading state */
  isLoading: boolean;

  /** Error message if any */
  error: string | null;

  /** Send a message */
  sendMessage: (content: string) => Promise<void>;

  /** Start a new conversation */
  startNewConversation: () => void;

  /** Clear error message */
  clearError: () => void;
}

/**
 * Return type for useConversations hook (optional enhancement)
 */
export interface UseConversationsReturn {
  /** List of user conversations */
  conversations: Conversation[];

  /** Loading state */
  isLoading: boolean;

  /** Error message if any */
  error: string | null;

  /** Refresh conversation list */
  refresh: () => Promise<void>;
}

/**
 * API client error type
 */
export interface ApiError {
  /** Error message */
  message: string;

  /** HTTP status code */
  status?: number;

  /** Error code for debugging */
  code?: string;
}

/**
 * Tool icon mapping type
 */
export type ToolIconMap = Record<string, string>;

/**
 * Tool label mapping type
 */
export type ToolLabelMap = Record<string, string>;

/**
 * Validation result type
 */
export interface ValidationResult {
  /** Whether validation passed */
  valid: boolean;

  /** Error message if validation failed */
  error?: string;
}

/**
 * Message validation function type
 */
export type MessageValidator = (message: string) => ValidationResult;

/**
 * Conversation ID storage key
 */
export const CONVERSATION_ID_KEY = "chatkit_conversation_id";

/**
 * Maximum message length
 */
export const MAX_MESSAGE_LENGTH = 2000;

/**
 * Tool names enum
 */
export enum ToolName {
  ADD_TASK = "add_task",
  LIST_TASKS = "list_tasks",
  COMPLETE_TASK = "complete_task",
  DELETE_TASK = "delete_task",
  UPDATE_TASK = "update_task",
}

/**
 * Message role enum
 */
export enum MessageRole {
  USER = "user",
  ASSISTANT = "assistant",
}

/**
 * Type guard to check if a message is from the user
 */
export function isUserMessage(message: Message): boolean {
  return message.role === MessageRole.USER;
}

/**
 * Type guard to check if a message is from the assistant
 */
export function isAssistantMessage(message: Message): boolean {
  return message.role === MessageRole.ASSISTANT;
}

/**
 * Type guard to check if a message has tool calls
 */
export function hasToolCalls(
  message: Message,
): message is Message & { tool_calls: ToolCall[] } {
  return message.tool_calls !== undefined && message.tool_calls.length > 0;
}

/**
 * Validate message content
 */
export function validateMessage(message: string): ValidationResult {
  if (!message || !message.trim()) {
    return {
      valid: false,
      error: "Message cannot be empty or whitespace-only",
    };
  }

  if (message.length > MAX_MESSAGE_LENGTH) {
    return {
      valid: false,
      error: `Message cannot exceed ${MAX_MESSAGE_LENGTH} characters`,
    };
  }

  return { valid: true };
}

/**
 * Generate a temporary message ID for optimistic updates
 */
export function generateTempMessageId(): string {
  return `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Format tool name for display
 */
export function formatToolName(toolName: string): string {
  const labels: ToolLabelMap = {
    [ToolName.ADD_TASK]: "Added Task",
    [ToolName.LIST_TASKS]: "Listed Tasks",
    [ToolName.COMPLETE_TASK]: "Completed Task",
    [ToolName.DELETE_TASK]: "Deleted Task",
    [ToolName.UPDATE_TASK]: "Updated Task",
  };

  return labels[toolName] || toolName;
}

/**
 * Get tool icon for display
 */
export function getToolIcon(toolName: string): string {
  const icons: ToolIconMap = {
    [ToolName.ADD_TASK]: "➕",
    [ToolName.LIST_TASKS]: "📋",
    [ToolName.COMPLETE_TASK]: "✅",
    [ToolName.DELETE_TASK]: "🗑️",
    [ToolName.UPDATE_TASK]: "✏️",
  };

  return icons[toolName] || "🔧";
}
