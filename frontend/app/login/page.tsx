/**
 * Login Page
 *
 * User login page with LoginForm and AuthLayout
 */

import LoginForm from '@/components/auth/LoginForm';
import AuthLayout from '@/components/auth/AuthLayout';

export default function LoginPage() {
  return (
    <AuthLayout
      title="Welcome Back"
      subtitle="Log in to access your tasks"
    >
      <LoginForm />
    </AuthLayout>
  );
}
