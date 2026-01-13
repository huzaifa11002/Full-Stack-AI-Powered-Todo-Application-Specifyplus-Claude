/**
 * Authentication Type Definitions
 *
 * TypeScript types for user authentication, session management,
 * and auth-related data structures.
 */

/**
 * User entity representing an authenticated user
 */
export interface User {
  /** Unique identifier (UUID) */
  id: string;

  /** User's email address (used for login) */
  email: string;

  /** Optional display name */
  username?: string;
}

/**
 * Authentication session state
 * Managed by AuthContext
 */
export interface AuthState {
  /** Currently authenticated user (null if not authenticated) */
  user: User | null;

  /** JWT access token (null if not authenticated) */
  token: string | null;

  /** Whether user is currently authenticated */
  isAuthenticated: boolean;

  /** Whether auth state is being loaded/checked */
  isLoading: boolean;
}

/**
 * Login credentials for user authentication
 */
export interface LoginCredentials {
  /** User's email address */
  email: string;

  /** User's password (min 8 characters) */
  password: string;
}

/**
 * Signup data for user registration
 */
export interface SignupData {
  /** User's email address */
  email: string;

  /** User's password (min 8 characters, must contain letter + number) */
  password: string;

  /** Password confirmation (must match password) */
  confirmPassword: string;
}

/**
 * Auth context value provided by AuthProvider
 */
export interface AuthContextValue extends AuthState {
  /** Login function */
  login: (credentials: LoginCredentials) => Promise<void>;

  /** Signup function */
  signup: (data: SignupData) => Promise<void>;

  /** Logout function */
  logout: () => Promise<void>;
}
