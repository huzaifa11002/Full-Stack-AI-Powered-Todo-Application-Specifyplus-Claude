/**
 * Dashboard Page
 *
 * Protected route showing user's tasks with loading and error states
 */

'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useTasks } from '@/lib/hooks/useTasks';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import TaskList from '@/components/tasks/TaskList';
import EmptyState from '@/components/tasks/EmptyState';
import Modal from '@/components/ui/Modal';
import TaskForm from '@/components/tasks/TaskForm';
import DeleteConfirmModal from '@/components/tasks/DeleteConfirmModal';
import Button from '@/components/ui/Button';
import { Task } from '@/types/task';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading: authLoading, logout } = useAuth();
  const { tasks, isLoading: tasksLoading, error, toggleComplete, addTask, updateTask, removeTask } = useTasks();
  const router = useRouter();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading state while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Don't render if not authenticated
  if (!isAuthenticated || !user) {
    return null;
  }

  // Handle create task
  const handleCreateTask = async (data: { title: string; description?: string }) => {
    await addTask(data);
    setIsCreateModalOpen(false);
  };

  // Handle edit task
  const handleEditTask = async (data: { title: string; description?: string }) => {
    if (!editingTask) return;
    await updateTask(editingTask.id, data);
    setEditingTask(null);
  };

  // Handle delete task
  const handleDeleteTask = async () => {
    if (!deletingTask) return;
    await removeTask(deletingTask.id);
    setDeletingTask(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Todo App</h1>
              <p className="text-sm text-gray-600">{user.email}</p>
            </div>
            <div className="flex items-center gap-3">
              <Button onClick={() => setIsCreateModalOpen(true)}>
                Add Task
              </Button>
              <button
                onClick={logout}
                className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error State */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {tasksLoading && (
          <div className="flex justify-center py-12">
            <LoadingSpinner size="lg" />
          </div>
        )}

        {/* Empty State */}
        {!tasksLoading && tasks.length === 0 && (
          <EmptyState onAddTask={() => setIsCreateModalOpen(true)} />
        )}

        {/* Task List */}
        {!tasksLoading && tasks.length > 0 && (
          <TaskList
            tasks={tasks}
            onToggleComplete={toggleComplete}
            onEdit={setEditingTask}
            onDelete={setDeletingTask}
          />
        )}
      </main>

      {/* Create Task Modal */}
      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Task"
      >
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setIsCreateModalOpen(false)}
        />
      </Modal>

      {/* Edit Task Modal */}
      <Modal
        isOpen={!!editingTask}
        onClose={() => setEditingTask(null)}
        title="Edit Task"
      >
        <TaskForm
          initialData={editingTask || undefined}
          onSubmit={handleEditTask}
          onCancel={() => setEditingTask(null)}
          isEditMode
        />
      </Modal>

      {/* Delete Confirmation Modal */}
      <DeleteConfirmModal
        task={deletingTask}
        isOpen={!!deletingTask}
        onConfirm={handleDeleteTask}
        onCancel={() => setDeletingTask(null)}
      />
    </div>
  );
}
