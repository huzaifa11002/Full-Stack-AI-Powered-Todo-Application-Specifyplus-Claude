/**
 * API Client Configuration
 *
 * Axios instance with request/response interceptors for JWT authentication
 */

import axios from 'axios';
import { ApiError } from '@/types/api';

// Create Axios instance
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add JWT token to all requests
apiClient.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    console.log('[apiClient] Request:', config.method?.toUpperCase(), config.url);
    console.log('[apiClient] Token:', token ? 'Present' : 'Missing');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
apiClient.interceptors.response.use(
  (response) => {
    console.log('[apiClient] Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('[apiClient] Error:', error.response?.status, error.config?.url);
    console.error('[apiClient] Error detail:', error.response?.data);

    // Handle 401 Unauthorized - Token expired or invalid
    if (error.response?.status === 401) {
      console.error('[apiClient] Unauthorized - clearing token and redirecting to login');
      // Clear token and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }

    // Handle 403 Forbidden - Access denied
    if (error.response?.status === 403) {
      console.error('Access denied:', error.response.data);
    }

    // Handle 404 Not Found
    if (error.response?.status === 404) {
      console.error('Resource not found:', error.response.data);
    }

    // Handle network errors
    if (!error.response) {
      console.error('Network error:', error.message);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
