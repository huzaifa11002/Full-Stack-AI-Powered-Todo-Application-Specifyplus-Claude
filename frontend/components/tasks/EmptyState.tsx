/**
 * EmptyState Component
 *
 * Placeholder shown when user has no tasks
 */

interface EmptyStateProps {
  onAddTask?: () => void;
}

export default function EmptyState({ onAddTask }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <svg
        className="w-24 h-24 text-gray-300 mb-4"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
      <h3 className="text-xl font-semibold text-gray-700 mb-2">No tasks yet</h3>
      <p className="text-gray-500 mb-6 max-w-sm">
        Get started by creating your first task. Stay organized and track your progress!
      </p>
      {onAddTask && (
        <button
          onClick={onAddTask}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Create Your First Task
        </button>
      )}
    </div>
  );
}
