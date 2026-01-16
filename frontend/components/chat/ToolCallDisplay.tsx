/**
 * ToolCallDisplay Component
 *
 * Displays tool call information inline with AI responses
 */

"use client";

import {
  ToolCallDisplayProps,
  formatToolName,
  getToolIcon,
} from "@/types/chat";

export default function ToolCallDisplay({ toolCalls }: ToolCallDisplayProps) {
  if (!toolCalls || toolCalls.length === 0) {
    return null;
  }

  return (
    <div className="mt-3 pt-3 border-t border-gray-200">
      <div className="text-xs font-medium text-gray-600 uppercase mb-2">
        Actions Performed
      </div>

      <div className="space-y-2">
        {toolCalls.map((toolCall, index) => (
          <div
            key={index}
            className="bg-gray-50 rounded-md p-3 border border-gray-200"
          >
            {/* Tool Name with Icon */}
            <div className="flex items-center gap-2 mb-2">
              <span className="text-lg" role="img" aria-label={toolCall.tool}>
                {getToolIcon(toolCall.tool)}
              </span>
              <span className="text-sm font-medium text-gray-900">
                {formatToolName(toolCall.tool)}
              </span>
            </div>

            {/* Parameters Display */}
            {toolCall.params && Object.keys(toolCall.params).length > 0 && (
              <div className="mb-2">
                <div className="text-xs font-medium text-gray-600 mb-1">
                  Parameters:
                </div>
                <div className="text-xs text-gray-700 bg-white rounded px-2 py-1 border border-gray-200">
                  {Object.entries(toolCall.params)
                    .filter(([key]) => key !== "user_id") // Hide user_id
                    .map(([key, value]) => (
                      <div key={key} className="flex gap-2">
                        <span className="font-medium">{key}:</span>
                        <span>{JSON.stringify(value)}</span>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* Result Summary */}
            {toolCall.result && Object.keys(toolCall.result).length > 0 && (
              <div>
                <div className="text-xs font-medium text-gray-600 mb-1">
                  Result:
                </div>
                <div className="text-xs text-gray-700 bg-white rounded px-2 py-1 border border-gray-200">
                  {formatToolResult(toolCall.result)}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * Format tool result for display
 */
function formatToolResult(result: Record<string, unknown>): string {
  // Handle common result patterns
  if (result.title) {
    return `Task: "${result.title}"`;
  }

  if (result.tasks && Array.isArray(result.tasks)) {
    return `Found ${result.tasks.length} task(s)`;
  }

  if (result.count !== undefined) {
    return `Count: ${result.count}`;
  }

  if (result.status) {
    return `Status: ${result.status}`;
  }

  if (result.id) {
    return `ID: ${result.id}`;
  }

  // Fallback: show all key-value pairs
  return Object.entries(result)
    .map(([key, value]) => `${key}: ${JSON.stringify(value)}`)
    .join(", ");
}
