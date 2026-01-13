/**
 * TaskList Component
 *
 * Responsive grid of tasks with sorting (incomplete first, then completed)
 */

'use client';

import { Task } from '@/types/task';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (taskId: string) => void;
  onEdit?: (task: Task) => void;
  onDelete?: (task: Task) => void;
}

export default function TaskList({ tasks, onToggleComplete, onEdit, onDelete }: TaskListProps) {
  // Sort tasks: incomplete first, then completed
  const sortedTasks = [...tasks].sort((a, b) => {
    if (a.is_completed === b.is_completed) {
      // If same completion status, sort by created date (newest first)
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    }
    // Incomplete tasks first
    return a.is_completed ? 1 : -1;
  });

  // Calculate task counts
  const completedCount = tasks.filter((t) => t.is_completed).length;
  const totalCount = tasks.length;

  return (
    <div>
      {/* Task count */}
      <div className="mb-4 text-sm text-gray-600">
        <span className="font-medium">
          {completedCount} of {totalCount}
        </span>{' '}
        completed
      </div>

      {/* Responsive grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sortedTasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggleComplete={onToggleComplete}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
}
