/**
 * TaskItem Component
 *
 * Individual task card with checkbox, title, description, and action buttons
 */

'use client';

import { Task } from '@/types/task';
import { memo } from 'react';

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: number) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (task: Task) => void;
}

function TaskItem({ task, onToggleComplete, onEdit, onDelete }: TaskItemProps) {
  return (
    <div
      className={`bg-white rounded-lg shadow-sm border p-4 hover:shadow-md transition-shadow ${
        task.is_completed ? 'opacity-75' : ''
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={() => onToggleComplete(task.id)}
          className="mt-1 w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500 cursor-pointer"
          aria-label={`Mark "${task.title}" as ${task.is_completed ? 'incomplete' : 'complete'}`}
        />

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium text-gray-900 mb-1 ${
              task.is_completed ? 'line-through text-gray-500' : ''
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`text-sm text-gray-600 mb-2 ${
                task.is_completed ? 'line-through text-gray-400' : ''
              }`}
            >
              {task.description}
            </p>
          )}
          <p className="text-xs text-gray-400">
            {new Date(task.created_at).toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              year: 'numeric',
            })}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          {onEdit && (
            <button
              onClick={() => onEdit(task)}
              className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors"
              aria-label={`Edit "${task.title}"`}
            >
              <svg
                className="w-5 h-5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(task)}
              className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
              aria-label={`Delete "${task.title}"`}
            >
              <svg
                className="w-5 h-5"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// Memoize component to prevent unnecessary re-renders
export default memo(TaskItem, (prevProps, nextProps) => {
  // Only re-render if task data or callbacks change
  return (
    prevProps.task.id === nextProps.task.id &&
    prevProps.task.title === nextProps.task.title &&
    prevProps.task.description === nextProps.task.description &&
    prevProps.task.is_completed === nextProps.task.is_completed &&
    prevProps.task.updated_at === nextProps.task.updated_at
  );
});
