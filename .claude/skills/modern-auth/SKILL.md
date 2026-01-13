## Modern Auth Components

---
name: modern-auth
description: Create stunning authentication forms with login, signup, and password reset. Modern glassmorphism design with social auth integration. Use when building auth interfaces.
---

### Instructions
Create authentication components with these features:

#### **Visual Design**
- Glassmorphism effect with backdrop blur
- Gradient backgrounds and accents
- Smooth transitions and animations
- Form field animations (focus, error states)
- Password strength indicators
- Social auth buttons (Google, GitHub, Apple)
- Split-screen layouts (form + image)

#### **Form Features**
- Login form with email/password
- Signup form with validation
- Password reset/forgot password
- Email verification screens
- Two-factor authentication (2FA)
- Remember me checkbox
- Show/hide password toggle
- Auto-focus on first field
- Enter key submission

#### **User Experience**
- Real-time validation feedback
- Loading states during submission
- Success/error animations
- Smooth form transitions
- Accessibility (ARIA labels, keyboard nav)
- Mobile-responsive design
- Touch-friendly inputs (min 44px)

#### **Security Indicators**
- Password strength meter
- CAPTCHA integration
- Rate limiting messages
- Secure connection badge
- Privacy policy links

### Example Code

#### Login Form Component

```typescript
// components/auth/LoginForm.tsx
import { useState } from 'react';
import { Eye, EyeOff, Mail, Lock, Chrome, Github, Apple } from 'lucide-react';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise;
  onSocialLogin?: (provider: 'google' | 'github' | 'apple') => void;
  onForgotPassword?: () => void;
  isLoading?: boolean;
}

export function LoginForm({ onSubmit, onSocialLogin, onForgotPassword, isLoading }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    const newErrors: { email?: string; password?: string } = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    await onSubmit(email, password);
  };

  return (
    
      
        {/* Header */}
        
          Welcome Back
          Sign in to your account
        

        {/* Social Login */}
        
          <button 
            type="button"
            onClick={() => onSocialLogin?.('google')}
            className="social-button"
          >
            
            Continue with Google
          
          <button 
            type="button"
            onClick={() => onSocialLogin?.('github')}
            className="social-button"
          >
            
            Continue with GitHub
          
        

        {/* Divider */}
        
          or
        

        {/* Login Form */}
        
          {/* Email Field */}
          
            
              Email Address
            
            
              
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={`form-input ${errors.email ? 'input-error' : ''}`}
                placeholder="you@example.com"
                autoComplete="email"
                autoFocus
              />
            
            {errors.email && (
              {errors.email}
            )}
          

          {/* Password Field */}
          
            
              Password
            
            
              
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={`form-input ${errors.password ? 'input-error' : ''}`}
                placeholder="••••••••"
                autoComplete="current-password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="password-toggle"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ?  : }
              
            
            {errors.password && (
              {errors.password}
            )}
          

          {/* Remember Me & Forgot Password */}
          
            
              
              Remember me
            
            
              Forgot password?
            
          

          {/* Submit Button */}
          
            {isLoading ? (
              
            ) : (
              'Sign In'
            )}
          
        

        {/* Sign Up Link */}
        
          
            Don't have an account?{' '}
            Sign up
          
        
      
    
  );
}
```

#### Signup Form Component

```typescript
// components/auth/SignupForm.tsx
import { useState } from 'react';
import { User, Mail, Lock, Eye, EyeOff } from 'lucide-react';

interface SignupFormProps {
  onSubmit: (data: SignupData) => Promise;
  isLoading?: boolean;
}

interface SignupData {
  name: string;
  email: string;
  password: string;
}

export function SignupForm({ onSubmit, isLoading }: SignupFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState(0);
  const [errors, setErrors] = useState<Record>({});

  const calculatePasswordStrength = (password: string): number => {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    return strength;
  };

  const handlePasswordChange = (password: string) => {
    setFormData({ ...formData, password });
    setPasswordStrength(calculatePasswordStrength(password));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    const newErrors: Record = {};
    if (!formData.name) newErrors.name = 'Name is required';
    if (!formData.email) newErrors.email = 'Email is required';
    if (!formData.password) newErrors.password = 'Password is required';
    if (formData.password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    if (passwordStrength < 2) {
      newErrors.password = 'Password is too weak';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    await onSubmit(formData);
  };

  const strengthColors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500'];
  const strengthLabels = ['Weak', 'Fair', 'Good', 'Strong'];

  return (
    
      
        
          Create Account
          Start your journey with us
        

        
          {/* Name Field */}
          
            Full Name
            
              
              <input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className={`form-input ${errors.name ? 'input-error' : ''}`}
                placeholder="John Doe"
                autoComplete="name"
                autoFocus
              />
            
            {errors.name && {errors.name}}
          

          {/* Email Field */}
          
            Email Address
            
              
              <input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className={`form-input ${errors.email ? 'input-error' : ''}`}
                placeholder="you@example.com"
                autoComplete="email"
              />
            
            {errors.email && {errors.email}}
          

          {/* Password Field */}
          
            Password
            
              
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => handlePasswordChange(e.target.value)}
                className={`form-input ${errors.password ? 'input-error' : ''}`}
                placeholder="••••••••"
                autoComplete="new-password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="password-toggle"
              >
                {showPassword ?  : }
              
            
            
            {/* Password Strength Indicator */}
            {formData.password && (
              
                
                  {[...Array(4)].map((_, i) => (
                    
                  ))}
                
                
                  {passwordStrength > 0 ? strengthLabels[passwordStrength - 1] : 'Enter password'}
                
              
            )}
            
            {errors.password && {errors.password}}
          

          {/* Confirm Password Field */}
          
            Confirm Password
            
              
              <input
                id="confirmPassword"
                type={showPassword ? 'text' : 'password'}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className={`form-input ${errors.confirmPassword ? 'input-error' : ''}`}
                placeholder="••••••••"
                autoComplete="new-password"
              />
            
            {errors.confirmPassword && {errors.confirmPassword}}
          

          {/* Terms & Conditions */}
          
            
              
              
                I agree to the{' '}
                Terms of Service
                {' '}and{' '}
                Privacy Policy
              
            
          

          {/* Submit Button */}
          
            {isLoading ?  : 'Create Account'}
          
        

        
          
            Already have an account?{' '}
            Sign in
          
        
      
    
  );
}
```

#### CSS Styles (Tailwind)

```css
/* Add to your global styles or component CSS */

.auth-container {
  @apply min-h-screen flex items-center justify-center p-4 relative overflow-hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-container::before {
  content: '';
  @apply absolute inset-0;
  background: radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  animation: pulse 8s ease-in-out infinite;
}

.auth-card {
  @apply relative w-full max-w-md p-8 rounded-3xl;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.auth-header {
  @apply text-center mb-8;
}

.auth-title {
  @apply text-3xl font-bold text-white mb-2;
}

.auth-subtitle {
  @apply text-white/80;
}

.social-auth {
  @apply space-y-3 mb-6;
}

.social-button {
  @apply w-full flex items-center justify-center gap-3 px-4 py-3 rounded-xl;
  @apply bg-white/10 border border-white/20 text-white font-medium;
  @apply transition-all duration-300 hover:bg-white/20 hover:scale-105;
  backdrop-filter: blur(10px);
}

.auth-divider {
  @apply relative text-center my-6;
}

.auth-divider::before {
  content: '';
  @apply absolute left-0 top-1/2 w-full h-px bg-white/20;
}

.auth-divider span {
  @apply relative bg-transparent px-4 text-white/60 text-sm;
}

.auth-form {
  @apply space-y-5;
}

.form-field {
  @apply space-y-2;
}

.form-label {
  @apply block text-sm font-medium text-white/90;
}

.input-wrapper {
  @apply relative;
}

.input-icon {
  @apply absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50;
}

.form-input {
  @apply w-full pl-12 pr-4 py-3 rounded-xl;
  @apply bg-white/10 border border-white/20 text-white placeholder:text-white/40;
  @apply transition-all duration-300 focus:outline-none focus:border-white/40 focus:bg-white/15;
  backdrop-filter: blur(10px);
}

.form-input.input-error {
  @apply border-red-400 focus:border-red-400;
}

.password-toggle {
  @apply absolute right-4 top-1/2 -translate-y-1/2 text-white/50;
  @apply hover:text-white/80 transition-colors;
}

.error-message {
  @apply text-sm text-red-300 mt-1;
}

.form-options {
  @apply flex items-center justify-between;
}

.checkbox-label {
  @apply flex items-center gap-2 text-sm text-white/80 cursor-pointer;
}

.checkbox {
  @apply w-4 h-4 rounded border-white/20 bg-white/10;
  @apply checked:bg-gradient-to-br checked:from-purple-500 checked:to-pink-500;
}

.link-button {
  @apply text-sm text-white/80 hover:text-white transition-colors;
}

.submit-button {
  @apply w-full py-3 px-4 rounded-xl font-semibold;
  @apply bg-white text-purple-600 hover:bg-white/90;
  @apply transition-all duration-300 hover:scale-105 hover:shadow-xl;
  @apply disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100;
}

.loading-spinner {
  @apply inline-block w-5 h-5 border-2 border-purple-600 border-t-transparent rounded-full;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.auth-footer {
  @apply text-center mt-6 text-sm text-white/80;
}

.link {
  @apply text-white font-medium hover:underline;
}

.password-strength {
  @apply mt-2 space-y-1;
}

.strength-bars {
  @apply flex gap-1;
}

.strength-bar {
  @apply h-1 flex-1 rounded-full transition-all duration-300;
}

.strength-label {
  @apply text-xs text-white/70;
}
```

#### Alternative Split-Screen Layout

```typescript
// components/auth/SplitAuthLayout.tsx
export function SplitAuthLayout({ children }: { children: React.ReactNode }) {
  return (
    
      {/* Left Side - Form */}
      
        {children}
      
      
      {/* Right Side - Image/Branding */}
      
        
          
            
          
          
            Welcome to Our Platform
            
              Join thousands of users building amazing things
            
            
              
                10K+
                Users
              
              
                50+
                Countries
              
              
                99%
                Satisfaction
              
            
          
        
      
    
  );
}
```
