/**
 * Input Component
 *
 * Reusable input field with label, error display, and character count
 */

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement> {
  /** Input label */
  label: string;
  /** Error message to display */
  error?: string;
  /** Maximum character count (shows counter if provided) */
  maxLength?: number;
  /** Current value length (for character counter) */
  valueLength?: number;
  /** Use textarea instead of input */
  multiline?: boolean;
  /** Number of rows for textarea */
  rows?: number;
}

export default function Input({
  label,
  error,
  maxLength,
  valueLength,
  multiline = false,
  rows = 3,
  className = '',
  id,
  ...props
}: InputProps) {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-');

  const baseClasses = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors';
  const stateClasses = error
    ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
    : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500';

  const InputElement = multiline ? 'textarea' : 'input';

  return (
    <div className="w-full">
      <label htmlFor={inputId} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <InputElement
        id={inputId}
        className={`${baseClasses} ${stateClasses} ${className}`}
        maxLength={maxLength}
        rows={multiline ? rows : undefined}
        {...(props as any)}
      />
      <div className="flex justify-between items-center mt-1">
        {error && (
          <p className="text-sm text-red-600" role="alert">
            {error}
          </p>
        )}
        {maxLength && valueLength !== undefined && (
          <p className={`text-sm ml-auto ${valueLength > maxLength ? 'text-red-600' : 'text-gray-500'}`}>
            {valueLength}/{maxLength}
          </p>
        )}
      </div>
    </div>
  );
}
