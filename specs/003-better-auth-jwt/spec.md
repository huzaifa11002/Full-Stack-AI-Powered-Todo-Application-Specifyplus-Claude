# Feature Specification: Better Auth JWT Authentication Integration

**Feature Branch**: `003-better-auth-jwt`
**Created**: 2026-01-10
**Status**: Draft
**Input**: User description: "Better Auth authentication with JWT-secured FastAPI backend integration"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration with Better Auth (Priority: P1)

A new user visits the application and creates an account using email and password. Better Auth handles password hashing with bcrypt and stores the user credentials securely. Upon successful registration, the user receives a JWT token that can be used to access protected resources.

**Why this priority**: This is the foundation of the authentication system. Without user registration, no other authentication features can function. This is the entry point for all users.

**Independent Test**: Can be fully tested by submitting a signup form with valid email/password, verifying the user is created in the database, and confirming a valid JWT token is returned. Delivers immediate value by allowing users to create accounts.

**Acceptance Scenarios**:

1. **Given** a new user visits the signup page, **When** they submit valid email and password (min 8 chars), **Then** Better Auth creates the user with bcrypt-hashed password and returns a JWT token with user_id, email, and 7-day expiration
2. **Given** a user tries to register with an existing email, **When** they submit the signup form, **Then** the system returns a 400 error with message "Email already registered"
3. **Given** a user submits invalid data (weak password, invalid email format), **When** they attempt registration, **Then** Better Auth validation rejects the request with specific error messages

---

### User Story 2 - User Login with JWT Token Generation (Priority: P1)

An existing user returns to the application and logs in with their email and password. Better Auth verifies the credentials against the bcrypt-hashed password in the database. Upon successful authentication, the system generates a JWT token containing the user's ID, email, and expiration timestamp, which the frontend stores for subsequent API requests.

**Why this priority**: Login is equally critical as registration. Users need to authenticate to access their data. This completes the basic authentication flow.

**Independent Test**: Can be fully tested by submitting login credentials for an existing user, verifying password validation, and confirming a valid JWT token is returned. Delivers value by allowing returning users to access their accounts.

**Acceptance Scenarios**:

1. **Given** an existing user with valid credentials, **When** they submit email and password to the login endpoint, **Then** Better Auth validates the password and returns a JWT token signed with BETTER_AUTH_SECRET
2. **Given** a user submits incorrect password, **When** they attempt login, **Then** the system returns 401 Unauthorized with message "Invalid credentials"
3. **Given** a user submits email for non-existent account, **When** they attempt login, **Then** the system returns 401 Unauthorized without revealing whether the email exists (security best practice)
4. **Given** a successful login, **When** the JWT token is generated, **Then** it includes claims: user_id, email, iat (issued at), exp (expiration = 7 days from now)

---

### User Story 3 - Protected API Access with JWT Verification (Priority: P1)

A logged-in user makes requests to protected API endpoints (e.g., /api/tasks). The FastAPI middleware intercepts all /api/* requests, extracts the JWT token from the Authorization header, verifies the token signature using PyJWT and the shared BETTER_AUTH_SECRET, and validates the token hasn't expired. If valid, the middleware extracts user information and allows the request to proceed. If invalid or missing, the middleware returns 401 Unauthorized.

**Why this priority**: This is the core security mechanism. Without JWT verification, the authentication system provides no actual protection. This must work for the system to be secure.

**Independent Test**: Can be fully tested by making API requests with valid tokens (should succeed), invalid tokens (should return 401), expired tokens (should return 401), and no tokens (should return 401). Delivers value by securing all protected resources.

**Acceptance Scenarios**:

1. **Given** a user has a valid JWT token, **When** they make a request to /api/tasks with Authorization: Bearer <token>, **Then** the FastAPI middleware verifies the token and allows the request to proceed
2. **Given** a user has an expired JWT token, **When** they make a request to a protected endpoint, **Then** the middleware returns 401 with message "Token has expired"
3. **Given** a user has an invalid/malformed token, **When** they make a request to a protected endpoint, **Then** the middleware returns 401 with message "Invalid token"
4. **Given** a user makes a request without an Authorization header, **When** they attempt to access a protected endpoint, **Then** the middleware returns 401 with message "Authorization header missing"
5. **Given** a user provides a token signed with wrong secret, **When** they make a request, **Then** PyJWT signature verification fails and returns 401 with message "Invalid token signature"

---

### User Story 4 - User Isolation Enforcement (Priority: P2)

When a user accesses their own resources (e.g., GET /api/users/{user_id}/tasks), the FastAPI middleware extracts the user_id from the verified JWT token and compares it to the user_id in the URL path parameter. If they match, the request proceeds. If they don't match (user trying to access another user's data), the middleware returns 403 Forbidden. This ensures users can only access their own data.

**Why this priority**: While critical for security, this builds on top of the JWT verification (P1). The system can function with basic authentication before adding user isolation, making this P2. However, it's essential for production deployment.

**Independent Test**: Can be fully tested by having User A attempt to access User B's resources using User A's valid token. Should return 403 Forbidden. Delivers value by enforcing data privacy and preventing unauthorized access to other users' data.

**Acceptance Scenarios**:

1. **Given** User A is authenticated with a valid JWT token (user_id=123), **When** they request GET /api/users/123/tasks, **Then** the middleware verifies user_id from token matches URL parameter and allows access
2. **Given** User A is authenticated with a valid JWT token (user_id=123), **When** they request GET /api/users/456/tasks, **Then** the middleware detects mismatch and returns 403 Forbidden with message "Access denied: cannot access other users' resources"
3. **Given** User A attempts to create a task for User B, **When** they POST to /api/users/456/tasks with User A's token, **Then** the middleware returns 403 Forbidden
4. **Given** User A attempts to update User B's task, **When** they PUT to /api/users/456/tasks/789 with User A's token, **Then** the middleware returns 403 Forbidden

---

### Edge Cases

- What happens when a user's token expires mid-session while they're actively using the app?
- How does the system handle concurrent login attempts from the same user account?
- What happens if the BETTER_AUTH_SECRET is changed/rotated while users have active tokens?
- How does the system handle malformed JWT tokens (missing claims, wrong structure)?
- What happens when a user tries to register with an email that was previously deleted?
- How does the system handle requests with multiple Authorization headers?
- What happens if the JWT token contains extra/unexpected claims?
- How does the system handle timezone differences in token expiration (iat/exp claims)?
- What happens when a user makes a request with a token that's valid but for a deleted user account?
- How does the system handle very long JWT tokens (potential DoS via header size)?

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Token Management
- **FR-001**: System MUST install and configure Better Auth library in the Next.js frontend with JWT plugin enabled
- **FR-002**: System MUST provide a signup endpoint that accepts email and password, validates input, hashes password with bcrypt, and returns a JWT token
- **FR-003**: System MUST provide a login endpoint that accepts email and password, verifies credentials against bcrypt hash, and returns a JWT token on success
- **FR-004**: System MUST generate JWT tokens with HS256 algorithm signed with BETTER_AUTH_SECRET environment variable
- **FR-005**: JWT tokens MUST include claims: user_id (string), email (string), iat (issued at timestamp), exp (expiration timestamp = 7 days from iat)
- **FR-006**: System MUST store BETTER_AUTH_SECRET in environment variables (.env files) and NEVER hardcode secrets in source code
- **FR-007**: System MUST use the same BETTER_AUTH_SECRET value in both Next.js (Better Auth) and FastAPI (PyJWT) for token signing and verification

#### FastAPI Middleware & Verification
- **FR-008**: System MUST implement FastAPI middleware that intercepts all requests to /api/* endpoints before they reach route handlers
- **FR-009**: Middleware MUST extract JWT token from Authorization header in format "Bearer <token>"
- **FR-010**: Middleware MUST verify JWT token signature using PyJWT library and BETTER_AUTH_SECRET
- **FR-011**: Middleware MUST validate token expiration (exp claim) and reject expired tokens with 401 status
- **FR-012**: Middleware MUST extract user_id and email from verified token claims and make them available to route handlers
- **FR-013**: Middleware MUST return 401 Unauthorized with clear error message for: missing token, invalid token, expired token, invalid signature
- **FR-014**: Middleware MUST allow requests to proceed to route handlers only after successful token verification

#### User Isolation & Authorization
- **FR-015**: System MUST enforce user isolation by comparing user_id from JWT token to user_id in URL path parameters
- **FR-016**: System MUST return 403 Forbidden when authenticated user attempts to access another user's resources
- **FR-017**: System MUST validate user_id match for all user-specific endpoints: GET/POST/PUT/DELETE /api/users/{user_id}/*
- **FR-018**: System MUST ensure users can only create, read, update, and delete their own tasks

#### Error Handling & Security
- **FR-019**: System MUST return 401 Unauthorized (not 403) when token is missing or invalid to avoid leaking information about resource existence
- **FR-020**: System MUST return 403 Forbidden only when token is valid but user lacks permission (user isolation violation)
- **FR-021**: System MUST NOT reveal whether an email exists during login failures (return generic "Invalid credentials" message)
- **FR-022**: System MUST validate email format during registration (valid email structure)
- **FR-023**: System MUST enforce minimum password length of 8 characters during registration
- **FR-024**: System MUST return specific validation error messages for registration failures (weak password, invalid email, duplicate email)

#### Token Storage & Transmission
- **FR-025**: Frontend MUST store JWT tokens in localStorage or httpOnly cookies (implementation choice to be documented)
- **FR-026**: Frontend MUST include JWT token in Authorization header for all API requests to protected endpoints
- **FR-027**: Frontend MUST use format "Authorization: Bearer <token>" for all authenticated requests
- **FR-028**: Frontend MUST handle 401 responses by clearing stored token and redirecting to login page

#### Configuration & Environment
- **FR-029**: System MUST load BETTER_AUTH_SECRET from environment variables in both Next.js and FastAPI
- **FR-030**: System MUST provide clear documentation on setting up .env files for both services
- **FR-031**: System MUST use different .env files for development and production environments
- **FR-032**: System MUST validate that BETTER_AUTH_SECRET is set on application startup and fail fast if missing
- **FR-033**: System MUST configure JWT token expiration to 7 days (604800 seconds) by default

### Key Entities

- **User**: Represents an authenticated user account with email (unique identifier), password (bcrypt-hashed), user_id (UUID), created_at timestamp, and updated_at timestamp
- **JWT Token**: Represents an authentication token containing claims (user_id, email, iat, exp), signed with HS256 algorithm using BETTER_AUTH_SECRET, transmitted via Authorization header
- **Task**: Represents a user's todo item with task_id, user_id (foreign key to User), title, description, is_completed status, created_at, and updated_at timestamps

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Better Auth is successfully installed and configured in Next.js with JWT plugin, verified by successful npm install and import statements
- **SC-002**: Users can successfully sign up with email and password, verified by user record created in database and valid JWT token returned
- **SC-003**: Users can successfully sign in with correct credentials, verified by JWT token returned with correct claims (user_id, email, exp)
- **SC-004**: JWT tokens include all required claims (user_id, email, iat, exp) with 7-day expiration, verified by decoding token and inspecting claims
- **SC-005**: FastAPI middleware successfully intercepts all /api/* requests and verifies JWT tokens, verified by 401 responses for invalid tokens and successful requests for valid tokens
- **SC-006**: Middleware correctly extracts user information from valid tokens, verified by route handlers receiving user_id and email from middleware
- **SC-007**: User isolation is enforced with user_id from JWT matching user_id in URL parameters, verified by 403 responses when user_id mismatch detected
- **SC-008**: Unauthorized requests (no token, invalid token, expired token) return 401 with clear error messages, verified by test suite covering all unauthorized scenarios
- **SC-009**: Token expiration is properly configured to 7 days, verified by checking exp claim is iat + 604800 seconds
- **SC-010**: Shared BETTER_AUTH_SECRET environment variable is used in both Next.js and FastAPI, verified by tokens generated in Next.js being successfully verified in FastAPI

## Assumptions *(mandatory)*

1. **Database**: PostgreSQL database is already set up and accessible from both Next.js and FastAPI (from feature 001-fastapi-todo-api)
2. **User Model**: User table/model already exists in the database with id, email, and password fields
3. **Task Model**: Task table/model already exists with user_id foreign key relationship
4. **Environment**: Both Next.js and FastAPI services can access shared environment variables (same .env file or synchronized secrets)
5. **Network**: Next.js frontend can make HTTP requests to FastAPI backend (CORS configured, network accessible)
6. **Dependencies**: npm/pip package managers are available and can install Better Auth and PyJWT libraries
7. **Python Version**: Python 3.11+ is installed (required for FastAPI and PyJWT)
8. **Node Version**: Node.js 18+ is installed (required for Next.js 16)
9. **Existing Auth**: No conflicting authentication system is currently implemented (or will be replaced)
10. **Token Format**: Standard JWT format (header.payload.signature) is acceptable for all use cases
11. **Secret Management**: Development environment can use .env files for secrets (production will use proper secret management)
12. **Single Secret**: One shared secret (BETTER_AUTH_SECRET) is sufficient for both signing and verification (no key rotation required initially)
13. **Timezone**: Server times are synchronized or UTC is used consistently for token timestamps
14. **Session Management**: Stateless JWT authentication is acceptable (no server-side session storage required)
15. **Token Revocation**: Immediate token revocation is not required (tokens remain valid until expiration even if user logs out)

## Out of Scope *(mandatory)*

The following items are explicitly excluded from this feature:

1. **OAuth Providers**: No integration with Google, GitHub, Facebook, or other OAuth providers
2. **Password Reset**: No "forgot password" or password reset functionality
3. **Email Verification**: No email verification workflow or confirmation emails
4. **Two-Factor Authentication (2FA)**: No TOTP, SMS, or other 2FA mechanisms
5. **Role-Based Access Control (RBAC)**: No roles, permissions, or fine-grained authorization beyond user isolation
6. **User Profile Management**: No endpoints for updating user profile, changing email, or managing account settings
7. **Admin Dashboard**: No admin interface for managing users or viewing system-wide data
8. **Refresh Token Rotation**: No refresh token mechanism (only access tokens with 7-day expiration)
9. **Account Deletion**: No user account deletion or deactivation functionality
10. **Multi-Device Session Management**: No tracking or management of sessions across multiple devices
11. **"Remember Me" Functionality**: No extended session duration or persistent login option
12. **Password Strength Meter**: No UI component for real-time password strength feedback
13. **Account Lockout**: No automatic account locking after failed login attempts
14. **Login History**: No tracking or display of user login history
15. **Social Login**: No "Sign in with Apple", "Sign in with Twitter", etc.
16. **Magic Links**: No passwordless authentication via email magic links
17. **Biometric Authentication**: No fingerprint, Face ID, or other biometric login
18. **API Key Authentication**: No alternative authentication method for API clients
19. **JWT Blacklisting**: No mechanism to invalidate tokens before expiration
20. **Token Refresh Endpoint**: No endpoint to refresh or renew tokens (users must re-login after 7 days)

## Dependencies *(mandatory)*

### External Dependencies
- **Better Auth**: JWT authentication library for Next.js (npm package)
- **PyJWT**: JWT encoding/decoding library for Python (pip package)
- **bcrypt**: Password hashing (included with Better Auth)
- **PostgreSQL**: Database for storing user credentials (already set up)

### Internal Dependencies
- **Feature 001-fastapi-todo-api**: Requires existing FastAPI backend with user and task models
- **Feature 002-nextjs-auth-frontend**: Requires existing Next.js frontend with authentication UI components

### Service Dependencies
- **Next.js Frontend**: Must be running to generate JWT tokens via Better Auth
- **FastAPI Backend**: Must be running to verify JWT tokens and serve protected API endpoints
- **Database Connection**: Both services must have access to the same PostgreSQL database

## Constraints *(mandatory)*

### Technical Constraints
- **Technology Stack**: Must use Better Auth (Next.js) + PyJWT (FastAPI) - no alternative libraries
- **Authentication Method**: JWT tokens only - no session-based authentication or cookies for auth state
- **Token Transmission**: Authorization: Bearer <token> header exclusively - no query parameters or cookies for token transmission
- **Secret Management**: Environment variables (.env files) only - no hardcoded secrets in source code
- **Password Hashing**: Better Auth's built-in bcrypt - no custom hashing implementation
- **Token Algorithm**: HS256 (HMAC with SHA-256) - no asymmetric algorithms (RS256, ES256)
- **Token Storage**: localStorage or httpOnly cookies - must document choice and security implications

### Timeline Constraints
- **Completion Deadline**: Must be completed within 3-4 days from specification approval
- **Phased Delivery**: Must deliver in phases (P1 stories first, then P2) to enable early testing

### Security Constraints
- **Secret Sharing**: Same BETTER_AUTH_SECRET must be used in both services - no separate signing/verification keys
- **Token Expiration**: Fixed 7-day expiration - no configurable expiration per user or request
- **HTTPS Requirement**: Production deployment must use HTTPS for all API requests (development can use HTTP)
- **Password Requirements**: Minimum 8 characters - no maximum length or complexity requirements specified

### Operational Constraints
- **No Token Revocation**: Tokens remain valid until expiration - cannot be invalidated early
- **No Session Tracking**: Stateless authentication - no server-side session storage or tracking
- **Single Secret**: One shared secret for all tokens - no per-user or per-session secrets

## Risks *(mandatory)*

### Technical Risks
- **Risk**: Better Auth library may have compatibility issues with Next.js 16 (as seen in feature 002)
  - **Mitigation**: Test Better Auth installation early; have fallback plan to implement custom JWT generation if needed
  - **Impact**: High - could block entire feature

- **Risk**: JWT token size may grow too large if additional claims are added later
  - **Mitigation**: Keep initial claims minimal (user_id, email, iat, exp); document token size limits
  - **Impact**: Medium - could affect performance with large headers

- **Risk**: Clock skew between Next.js and FastAPI servers could cause token validation failures
  - **Mitigation**: Use UTC timestamps; allow small clock skew tolerance in PyJWT verification (leeway parameter)
  - **Impact**: Medium - could cause intermittent authentication failures

### Security Risks
- **Risk**: Shared secret (BETTER_AUTH_SECRET) could be compromised if exposed in logs, error messages, or version control
  - **Mitigation**: Never log secret; use .gitignore for .env files; implement secret rotation plan for production
  - **Impact**: Critical - would compromise all tokens

- **Risk**: localStorage storage of JWT tokens is vulnerable to XSS attacks
  - **Mitigation**: Document security tradeoff; consider httpOnly cookies as alternative; implement CSP headers
  - **Impact**: High - could lead to token theft

- **Risk**: 7-day token expiration is long and increases window for token theft/misuse
  - **Mitigation**: Document tradeoff between security and UX; plan for refresh token mechanism in future
  - **Impact**: Medium - acceptable for MVP but should be addressed later

### Operational Risks
- **Risk**: No token revocation means compromised tokens remain valid until expiration
  - **Mitigation**: Document limitation; plan for token blacklist or shorter expiration in future
  - **Impact**: High - limits ability to respond to security incidents

- **Risk**: Secret rotation requires coordinated deployment of both Next.js and FastAPI services
  - **Mitigation**: Document deployment procedure; plan for zero-downtime secret rotation strategy
  - **Impact**: Medium - could cause service disruption if not coordinated

- **Risk**: Users must re-login every 7 days, which may impact user experience
  - **Mitigation**: Provide clear messaging when token expires; plan for refresh token mechanism in future
  - **Impact**: Low - acceptable for MVP

## Notes *(optional)*

### Implementation Approach
- Start with P1 user stories (Registration, Login, Protected API Access) to establish core authentication flow
- Implement FastAPI middleware as a separate module for testability and reusability
- Create comprehensive test suite covering all authentication scenarios (valid, invalid, expired, missing tokens)
- Document token storage decision (localStorage vs httpOnly cookies) with security implications

### Future Enhancements
- Implement refresh token rotation for better security and UX
- Add token blacklist for immediate revocation capability
- Implement password reset and email verification workflows
- Add OAuth provider integration for social login
- Implement RBAC for fine-grained permissions
- Add 2FA for enhanced security

### Testing Strategy
- Unit tests for Better Auth configuration and JWT generation
- Unit tests for PyJWT verification and middleware logic
- Integration tests for end-to-end authentication flow (signup → login → protected API access)
- Security tests for token validation edge cases (expired, invalid, malformed, wrong signature)
- User isolation tests to verify 403 responses for cross-user access attempts

### Documentation Requirements
- README with setup instructions for both Next.js and FastAPI
- Environment variable configuration guide (.env.example files)
- API documentation for authentication endpoints (signup, login)
- Security considerations document (token storage, secret management, known limitations)
- Troubleshooting guide for common authentication issues
