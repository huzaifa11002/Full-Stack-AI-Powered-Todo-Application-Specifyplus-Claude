/**
 * AuthLayout Component
 *
 * Shared layout for authentication pages (login, signup)
 */

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
}

export default function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Logo/Header Area */}
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Todo App</h1>
          <h2 className="text-2xl font-semibold text-gray-700">{title}</h2>
          {subtitle && <p className="mt-2 text-sm text-gray-600">{subtitle}</p>}
        </div>

        {/* Card Container */}
        <div className="bg-white rounded-lg shadow-md p-8">
          {children}
        </div>
      </div>
    </div>
  );
}
