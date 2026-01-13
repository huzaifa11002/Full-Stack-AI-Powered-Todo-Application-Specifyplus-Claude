/**
 * API Type Definitions
 *
 * TypeScript types for API responses, errors, and HTTP client configuration.
 */

/**
 * Standard API error response
 */
export interface ApiError {
  /** Human-readable error message */
  detail: string;

  /** HTTP status code */
  status_code: number;
}

/**
 * Generic API response wrapper
 * Used for consistent response handling
 */
export interface ApiResponse<T> {
  /** Response data of type T */
  data?: T;

  /** Error object if request failed */
  error?: ApiError;
}

/**
 * Axios error response structure
 * Extended from AxiosError
 */
export interface ApiErrorResponse {
  /** Error response data */
  response?: {
    /** Response data containing error details */
    data: ApiError;

    /** HTTP status code */
    status: number;

    /** Response headers */
    headers: Record<string, string>;
  };

  /** Error message */
  message: string;
}

/**
 * API client configuration
 */
export interface ApiClientConfig {
  /** Base URL for API requests */
  baseURL: string;

  /** Request timeout in milliseconds */
  timeout?: number;

  /** Default headers */
  headers?: Record<string, string>;
}

/**
 * Pagination metadata (for future use)
 * Currently not implemented per spec
 */
export interface PaginationMeta {
  /** Current page number */
  page: number;

  /** Items per page */
  per_page: number;

  /** Total number of items */
  total: number;

  /** Total number of pages */
  total_pages: number;
}

/**
 * Paginated response (for future use)
 * Currently not implemented per spec
 */
export interface PaginatedResponse<T> {
  /** Array of items */
  items: T[];

  /** Pagination metadata */
  meta: PaginationMeta;
}
