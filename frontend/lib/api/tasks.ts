/**
 * Task API Functions
 *
 * API functions for task CRUD operations
 */

import apiClient from './client';
import { Task, TaskCreate, TaskUpdate } from '@/types/task';

/**
 * Get all tasks for a user
 */
export async function getTasks(userId: number): Promise<Task[]> {
  try {
    console.log('[getTasks] Fetching tasks for user:', userId);
    const response = await apiClient.get(`/api/${userId}/tasks`);
    console.log('[getTasks] Response:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('[getTasks] Error:', error);
    console.error('[getTasks] Error response:', error.response);
    const errorMessage = error.response?.data?.detail || 'Failed to fetch tasks';
    throw new Error(errorMessage);
  }
}

/**
 * Create a new task
 */
export async function createTask(userId: number, data: TaskCreate): Promise<Task> {
  try {
    console.log('[createTask] Creating task for user:', userId, 'data:', data);
    const response = await apiClient.post(`/api/${userId}/tasks`, data);
    console.log('[createTask] Response:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('[createTask] Error:', error);
    console.error('[createTask] Error response:', error.response);
    const errorMessage = error.response?.data?.detail || 'Failed to create task';
    throw new Error(errorMessage);
  }
}

/**
 * Update an existing task
 */
export async function updateTask(userId: number, taskId: number, data: TaskUpdate): Promise<Task> {
  try {
    const response = await apiClient.put(`/api/${userId}/tasks/${taskId}`, data);
    return response.data;
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Failed to update task';
    throw new Error(errorMessage);
  }
}

/**
 * Toggle task completion status
 */
export async function toggleTaskComplete(userId: number, taskId: number): Promise<Task> {
  try {
    const response = await apiClient.patch(`/api/${userId}/tasks/${taskId}/toggle`);
    return response.data;
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Failed to toggle task completion';
    throw new Error(errorMessage);
  }
}

/**
 * Delete a task
 */
export async function deleteTask(userId: number, taskId: number): Promise<void> {
  try {
    await apiClient.delete(`/api/${userId}/tasks/${taskId}`);
  } catch (error: any) {
    const errorMessage = error.response?.data?.detail || 'Failed to delete task';
    throw new Error(errorMessage);
  }
}
