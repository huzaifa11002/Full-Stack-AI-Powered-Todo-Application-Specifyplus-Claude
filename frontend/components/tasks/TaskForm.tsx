/**
 * TaskForm Component
 *
 * Form for creating and editing tasks with validation
 */

'use client';

import { useState, useEffect } from 'react';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import { TaskFormData, TaskValidationErrors, Task } from '@/types/task';

interface TaskFormProps {
  /** Initial data for edit mode */
  initialData?: Task;
  /** Form submission handler */
  onSubmit: (data: { title: string; description?: string }) => Promise<void>;
  /** Cancel handler */
  onCancel?: () => void;
  /** Whether form is in edit mode */
  isEditMode?: boolean;
}

export default function TaskForm({ initialData, onSubmit, onCancel, isEditMode = false }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskFormData>({
    title: initialData?.title || '',
    description: initialData?.description || '',
  });
  const [errors, setErrors] = useState<TaskValidationErrors>({});
  const [isLoading, setIsLoading] = useState(false);

  // Update form data when initialData changes (for edit mode)
  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title,
        description: initialData.description || '',
      });
    }
  }, [initialData]);

  // Handle input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    setErrors((prev) => ({ ...prev, [name]: '' }));
  };

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: TaskValidationErrors = {};

    // Title validation
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 200) {
      newErrors.title = 'Title must be under 200 characters';
    }

    // Description validation
    if (formData.description && formData.description.length > 2000) {
      newErrors.description = 'Description must be under 2000 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      await onSubmit({
        title: formData.title.trim(),
        description: formData.description.trim() || undefined,
      });

      // Reset form on successful submission (only for create mode)
      if (!isEditMode) {
        setFormData({ title: '', description: '' });
      }
    } catch (error) {
      // Error is handled by parent component with toast
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Title"
        name="title"
        value={formData.title}
        onChange={handleChange}
        error={errors.title}
        maxLength={200}
        valueLength={formData.title.length}
        placeholder="Enter task title"
        required
      />

      <Input
        label="Description (optional)"
        name="description"
        value={formData.description}
        onChange={handleChange}
        error={errors.description}
        maxLength={2000}
        valueLength={formData.description.length}
        placeholder="Enter task description"
        multiline
        rows={4}
      />

      <div className="flex justify-end gap-2 pt-2">
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" isLoading={isLoading}>
          {isEditMode ? 'Update Task' : 'Create Task'}
        </Button>
      </div>
    </form>
  );
}
