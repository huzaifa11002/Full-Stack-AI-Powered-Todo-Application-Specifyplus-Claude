/**
 * useTasks Hook
 *
 * Custom hook for task state management with optimistic updates
 */

'use client';

import { useState, useEffect } from 'react';
import { Task, TaskCreate, TaskUpdate } from '@/types/task';
import { getTasks, createTask, updateTask, toggleTaskComplete, deleteTask } from '@/lib/api/tasks';
import { useAuth } from '@/contexts/AuthContext';
import toast from 'react-hot-toast';

export function useTasks() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks on mount
  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user]);

  // Load tasks from API
  const loadTasks = async () => {
    if (!user) {
      console.log('[useTasks] No user, skipping task load');
      return;
    }

    console.log('[useTasks] Loading tasks for user:', user.id);

    try {
      setIsLoading(true);
      setError(null);
      const fetchedTasks = await getTasks(user.id);
      console.log('[useTasks] Tasks loaded successfully:', fetchedTasks.length);
      setTasks(fetchedTasks);
    } catch (err: any) {
      console.error('[useTasks] Failed to load tasks:', err);
      const errorMessage = err.message || 'Failed to load tasks';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Add task with optimistic update
  const addTask = async (data: TaskCreate) => {
    if (!user) {
      console.error('[useTasks] Cannot add task: No user');
      toast.error('Please log in to add tasks');
      return;
    }

    console.log('[useTasks] Adding task for user:', user.id, 'data:', data);

    // Create optimistic task with negative ID (will be replaced by real ID from backend)
    const optimisticTask: Task = {
      id: -Date.now(),
      user_id: user.id,
      title: data.title,
      description: data.description || null,
      is_completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };

    // Optimistic update
    setTasks((prev) => [optimisticTask, ...prev]);

    try {
      const newTask = await createTask(user.id, data);
      console.log('[useTasks] Task created successfully:', newTask);
      // Replace optimistic task with real task
      setTasks((prev) => prev.map((t) => (t.id === optimisticTask.id ? newTask : t)));
      toast.success('Task created successfully');
    } catch (err: any) {
      console.error('[useTasks] Failed to create task:', err);
      // Rollback on error
      setTasks((prev) => prev.filter((t) => t.id !== optimisticTask.id));
      toast.error(err.message || 'Failed to create task');
      throw err;
    }
  };

  // Update task with optimistic update
  const updateTaskData = async (taskId: number, data: TaskUpdate) => {
    if (!user) return;

    // Store original task for rollback
    const originalTask = tasks.find((t) => t.id === taskId);
    if (!originalTask) return;

    // Optimistic update
    setTasks((prev) =>
      prev.map((t) =>
        t.id === taskId
          ? { ...t, ...data, updated_at: new Date().toISOString() }
          : t
      )
    );

    try {
      const updatedTask = await updateTask(user.id, taskId, data);
      // Replace with real updated task
      setTasks((prev) => prev.map((t) => (t.id === taskId ? updatedTask : t)));
      toast.success('Task updated successfully');
    } catch (err: any) {
      // Rollback on error
      setTasks((prev) => prev.map((t) => (t.id === taskId ? originalTask : t)));
      toast.error(err.message || 'Failed to update task');
      throw err;
    }
  };

  // Toggle task completion with optimistic update
  const toggleComplete = async (taskId: number) => {
    if (!user) return;

    // Store original task for rollback
    const originalTask = tasks.find((t) => t.id === taskId);
    if (!originalTask) return;

    // Optimistic update
    setTasks((prev) =>
      prev.map((t) =>
        t.id === taskId
          ? { ...t, is_completed: !t.is_completed, updated_at: new Date().toISOString() }
          : t
      )
    );

    try {
      const updatedTask = await toggleTaskComplete(user.id, taskId);
      // Replace with real updated task
      setTasks((prev) => prev.map((t) => (t.id === taskId ? updatedTask : t)));
      toast.success(updatedTask.is_completed ? 'Task completed' : 'Task marked incomplete');
    } catch (err: any) {
      // Rollback on error
      setTasks((prev) => prev.map((t) => (t.id === taskId ? originalTask : t)));
      toast.error(err.message || 'Failed to toggle task completion');
      throw err;
    }
  };

  // Remove task with optimistic update
  const removeTask = async (taskId: number) => {
    if (!user) return;

    // Store original task for rollback
    const originalTask = tasks.find((t) => t.id === taskId);
    if (!originalTask) return;

    // Optimistic update
    setTasks((prev) => prev.filter((t) => t.id !== taskId));

    try {
      await deleteTask(user.id, taskId);
      toast.success('Task deleted successfully');
    } catch (err: any) {
      // Rollback on error
      setTasks((prev) => [...prev, originalTask]);
      toast.error(err.message || 'Failed to delete task');
      throw err;
    }
  };

  return {
    tasks,
    isLoading,
    error,
    loadTasks,
    addTask,
    updateTask: updateTaskData,
    toggleComplete,
    removeTask,
  };
}
