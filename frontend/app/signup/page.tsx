/**
 * Signup Page
 *
 * User registration page with SignupForm and AuthLayout
 */

import SignupForm from '@/components/auth/SignupForm';
import AuthLayout from '@/components/auth/AuthLayout';

export default function SignupPage() {
  return (
    <AuthLayout
      title="Create Account"
      subtitle="Sign up to start managing your tasks"
    >
      <SignupForm />
    </AuthLayout>
  );
}
