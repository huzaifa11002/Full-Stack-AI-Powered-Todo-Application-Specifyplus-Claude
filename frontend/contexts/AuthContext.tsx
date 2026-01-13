/**
 * Authentication Context
 *
 * Provides authentication state and methods throughout the application
 */

'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { AuthContextValue, User, LoginCredentials, SignupData } from '@/types/auth';
import { signIn, signUp, signOut, getSession } from '@/lib/auth';
import toast from 'react-hot-toast';

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check for existing session on mount
  useEffect(() => {
    const checkSession = async () => {
      console.log('[AuthContext] Checking session...');
      try {
        // Try to get token from localStorage first, then from cookies
        let storedToken = localStorage.getItem('token');
        console.log('[AuthContext] Token from localStorage:', storedToken ? 'Found' : 'Not found');
        
        if (!storedToken) {
          // Check cookies as fallback
          const cookies = document.cookie.split(';');
          const tokenCookie = cookies.find(c => c.trim().startsWith('token='));
          if (tokenCookie) {
            storedToken = tokenCookie.split('=')[1];
            console.log('[AuthContext] Token from cookie:', 'Found');
            // Sync to localStorage
            localStorage.setItem('token', storedToken);
          }
        }

        if (storedToken) {
          console.log('[AuthContext] Fetching session from API...');
          const session = await getSession();
          if (session) {
            console.log('[AuthContext] Session restored:', session.user);
            setUser(session.user);
            setToken(session.token);
            setIsAuthenticated(true);
          } else {
            console.log('[AuthContext] Session fetch returned null');
          }
        } else {
          console.log('[AuthContext] No token found');
        }
      } catch (error) {
        console.error('[AuthContext] Session check failed:', error);
      } finally {
        setIsLoading(false);
        console.log('[AuthContext] Session check complete');
      }
    };

    checkSession();
  }, []);

  // Login function
  const login = async (credentials: LoginCredentials) => {
    try {
      setIsLoading(true);
      const response = await signIn(credentials.email, credentials.password);

      // Store token in localStorage
      const accessToken = response.access_token;
      localStorage.setItem('token', accessToken);

      // Also store token in cookie for middleware
      document.cookie = `token=${accessToken}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`;

      // Update state
      setToken(accessToken);
      setUser(response.user);
      setIsAuthenticated(true);

      toast.success('Login successful!');
      
      // Use window.location for hard navigation to ensure middleware sees the cookie
      window.location.href = '/dashboard';
    } catch (error: any) {
      toast.error(error.message || 'Login failed');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Signup function
  const signup = async (data: SignupData) => {
    try {
      setIsLoading(true);

      // Validate password match
      if (data.password !== data.confirmPassword) {
        throw new Error('Passwords do not match');
      }

      const response = await signUp(data.email, data.password, data.username);

      // Auto-login after signup
      const accessToken = response.access_token;
      localStorage.setItem('token', accessToken);

      // Also store token in cookie for middleware
      document.cookie = `token=${accessToken}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`;

      // Update state
      setToken(accessToken);
      setUser(response.user);
      setIsAuthenticated(true);

      toast.success('Account created successfully!');
      
      // Use window.location for hard navigation to ensure middleware sees the cookie
      window.location.href = '/dashboard';
    } catch (error: any) {
      toast.error(error.message || 'Signup failed');
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await signOut();

      // Clear state
      setUser(null);
      setToken(null);
      setIsAuthenticated(false);

      // Clear cookie
      document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';

      toast.success('Logged out successfully');
      router.push('/login');
    } catch (error: any) {
      toast.error('Logout failed');
      console.error('Logout error:', error);
    }
  };

  const value: AuthContextValue = {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
