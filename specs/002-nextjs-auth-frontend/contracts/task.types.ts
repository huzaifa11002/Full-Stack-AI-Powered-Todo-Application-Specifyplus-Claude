/**
 * Task Type Definitions
 *
 * TypeScript types for todo tasks, including CRUD operations
 * and data transfer objects.
 */

/**
 * Task entity representing a todo item
 */
export interface Task {
  /** Unique identifier (UUID) */
  id: string;

  /** ID of the user who owns this task (UUID) */
  user_id: string;

  /** Task title/summary (1-200 characters) */
  title: string;

  /** Detailed task description (max 2000 characters, nullable) */
  description: string | null;

  /** Whether the task is completed */
  is_completed: boolean;

  /** ISO 8601 timestamp when task was created */
  created_at: string;

  /** ISO 8601 timestamp when task was last updated */
  updated_at: string;
}

/**
 * Data transfer object for creating a new task
 */
export interface TaskCreate {
  /** Task title (required, 1-200 characters) */
  title: string;

  /** Task description (optional, max 2000 characters) */
  description?: string;
}

/**
 * Data transfer object for updating an existing task
 */
export interface TaskUpdate {
  /** Updated task title (optional, 1-200 characters) */
  title?: string;

  /** Updated task description (optional, max 2000 characters) */
  description?: string;

  /** Updated completion status (optional) */
  is_completed?: boolean;
}

/**
 * Task form data (used in TaskForm component)
 * Similar to TaskCreate but with explicit optional description
 */
export interface TaskFormData {
  /** Task title */
  title: string;

  /** Task description */
  description: string;
}

/**
 * Task validation errors
 */
export interface TaskValidationErrors {
  /** Title validation error message */
  title?: string;

  /** Description validation error message */
  description?: string;
}
