/**
 * Authentication API Functions
 *
 * Direct API calls for JWT authentication with the FastAPI backend
 */

/**
 * Sign up a new user
 */
export async function signUp(email: string, password: string, username: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, username }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Signup failed');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

/**
 * Sign in an existing user
 */
export async function signIn(email: string, password: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

/**
 * Sign out the current user
 */
export async function signOut() {
  // Clear local storage token
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
}

/**
 * Get current session
 */
export async function getSession() {
  try {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    if (!token) {
      return null;
    }

    // Verify token with backend
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      return null;
    }

    const user = await response.json();
    return { user, token };
  } catch (error) {
    return null;
  }
}
