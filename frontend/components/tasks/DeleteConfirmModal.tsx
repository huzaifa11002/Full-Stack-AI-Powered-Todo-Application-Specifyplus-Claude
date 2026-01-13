/**
 * DeleteConfirmModal Component
 *
 * Confirmation modal for deleting tasks
 */

'use client';

import { Task } from '@/types/task';
import Button from '@/components/ui/Button';

interface DeleteConfirmModalProps {
  task: Task | null;
  isOpen: boolean;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
}

export default function DeleteConfirmModal({ task, isOpen, onConfirm, onCancel }: DeleteConfirmModalProps) {
  const [isDeleting, setIsDeleting] = React.useState(false);

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
    } finally {
      setIsDeleting(false);
    }
  };

  if (!isOpen || !task) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onCancel}
        aria-hidden="true"
      />

      {/* Modal container */}
      <div className="flex min-h-full items-center justify-center p-4">
        {/* Modal card */}
        <div
          className="relative bg-white rounded-lg shadow-xl max-w-md w-full p-6 transform transition-all"
          onClick={(e) => e.stopPropagation()}
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-modal-title"
        >
          {/* Icon */}
          <div className="flex items-center justify-center w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full">
            <svg
              className="w-6 h-6 text-red-600"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>

          {/* Content */}
          <h3 id="delete-modal-title" className="text-lg font-semibold text-gray-900 text-center mb-2">
            Delete Task
          </h3>
          <p className="text-sm text-gray-600 text-center mb-6">
            Are you sure you want to delete "<span className="font-medium">{task.title}</span>"? This action cannot be undone.
          </p>

          {/* Actions */}
          <div className="flex gap-3">
            <Button
              variant="secondary"
              fullWidth
              onClick={onCancel}
              disabled={isDeleting}
            >
              Cancel
            </Button>
            <Button
              variant="danger"
              fullWidth
              onClick={handleConfirm}
              isLoading={isDeleting}
            >
              Delete
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

// Import React at the top
import React from 'react';
