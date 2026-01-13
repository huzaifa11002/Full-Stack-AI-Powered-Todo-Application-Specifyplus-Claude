# Task Breakdown: Better Auth JWT Authentication Integration

**Feature**: 003-better-auth-jwt
**Branch**: `003-better-auth-jwt`
**Created**: 2026-01-10
**Total Tasks**: 85

## Overview

This task breakdown implements JWT-based authentication using Better Auth (Next.js) and PyJWT (FastAPI). Tasks are organized by user story to enable independent implementation and testing.

**User Stories**:
- **US1 (P1)**: User Registration with Better Auth
- **US2 (P1)**: User Login with JWT Token Generation
- **US3 (P1)**: Protected API Access with JWT Verification
- **US4 (P2)**: User Isolation Enforcement

**Implementation Strategy**: MVP-first approach. Complete US1-US3 (P1 stories) for basic authentication, then add US4 (P2) for user isolation.

---

## Phase 1: Setup & Configuration (8 tasks)

**Goal**: Initialize project dependencies and environment configuration for both frontend and backend.

**Tasks**:

- [X] T001 [P] Install Better Auth package in frontend: `cd frontend && npm install better-auth`
- [X] T002 [P] Install PyJWT and bcrypt in backend: `cd backend && pip install pyjwt bcrypt passlib`
- [X] T003 [P] Generate cryptographically secure BETTER_AUTH_SECRET (32+ chars) using Python: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [X] T004 [P] Create frontend/.env.local.example with BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
- [X] T005 [P] Create backend/.env.example with BETTER_AUTH_SECRET, DATABASE_URL, FRONTEND_URL
- [X] T006 [P] Update frontend/.gitignore to exclude .env.local
- [X] T007 [P] Update backend/.gitignore to exclude .env
- [X] T008 Update backend/requirements.txt to add pyjwt, bcrypt, passlib[bcrypt]

**Completion Criteria**: All dependencies installed, environment variables configured, secrets generated and documented.

---

## Phase 2: Foundational Components (13 tasks)

**Goal**: Create foundational database models, schemas, and utilities that all user stories depend on.

**Tasks**:

- [X] T009 Create backend/app/models/user.py with User SQLModel (id, email, hashed_password, username, is_active, created_at, updated_at)
- [X] T010 Create backend/app/schemas/user.py with UserCreate, UserLogin, UserResponse, TokenResponse Pydantic schemas
- [X] T011 Create backend/app/utils/jwt.py with create_access_token() and verify_token() functions using PyJWT
- [X] T012 Create backend/app/utils/password.py with hash_password() and verify_password() functions using bcrypt
- [X] T013 Create Alembic migration in backend/alembic/versions/ to add users table with indexes on id and email
- [X] T014 [P] Update backend/app/models/__init__.py to export User model
- [X] T015 [P] Update backend/app/schemas/__init__.py to export user schemas
- [X] T016 [P] Create frontend/types/auth.ts with User, AuthState, LoginCredentials, SignupData, AuthContextValue interfaces
- [X] T017 [P] Create frontend/lib/auth.ts with signUp(), signIn(), signOut(), getSession() functions (direct API calls, not Better Auth client)
- [X] T018 Run Alembic migration to create users table: `cd backend && alembic upgrade head`
- [X] T019 Verify users table created in database with correct schema and indexes
- [X] T020 Update backend/app/models/task.py to add user_id foreign key field (String, foreign_key="users.id")
- [X] T021 Create Alembic migration to add user_id column to tasks table with foreign key constraint

**Completion Criteria**: User model, schemas, JWT utilities, password utilities created. Database migrations applied. Task model updated with user_id foreign key.

---

## Phase 3: User Story 1 - User Registration (14 tasks)

**Goal**: Implement user signup with email/password, bcrypt hashing, and JWT token generation.

**Independent Test**: Submit signup form with valid email/password → User created in database → JWT token returned with 7-day expiration.

**Tasks**:

### Backend Implementation

- [X] T022 [US1] Create backend/app/routers/auth.py with FastAPI router (prefix="/api/auth", tags=["Authentication"])
- [X] T023 [US1] Implement POST /api/auth/signup endpoint in backend/app/routers/auth.py
- [X] T024 [US1] Add email uniqueness validation in signup endpoint (query User by email, return 400 if exists)
- [X] T025 [US1] Add password validation in signup endpoint (min 8 chars, at least one number and letter)
- [X] T026 [US1] Hash password with bcrypt in signup endpoint using password.hash_password()
- [X] T027 [US1] Create User record in database in signup endpoint
- [X] T028 [US1] Generate JWT token in signup endpoint using jwt.create_access_token() with 7-day expiration
- [X] T029 [US1] Return TokenResponse with access_token, token_type="bearer", and user data in signup endpoint
- [X] T030 [US1] Add error handling in signup endpoint for duplicate email (400), validation errors (400), database errors (500)

### Frontend Implementation

- [X] T031 [P] [US1] Update frontend/app/signup/page.tsx to add email, password, username state and form handlers
- [X] T032 [US1] Implement handleSignup function in signup page to call auth.signUp() with form data
- [X] T033 [US1] Store JWT token in localStorage on successful signup: `localStorage.setItem('token', data.access_token)`
- [X] T034 [US1] Redirect to /dashboard after successful signup using useRouter().push('/dashboard')
- [X] T035 [US1] Display error messages in signup form for validation failures and API errors

**Completion Criteria**: Users can sign up with email/password. Password hashed with bcrypt. JWT token generated and returned. Token stored in localStorage. User redirected to dashboard.

**Acceptance Test**:
```bash
# Test signup
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "username": "Test User"}'

# Expected: 201 Created with JWT token and user data
```

---

## Phase 4: User Story 2 - User Login (12 tasks)

**Goal**: Implement user signin with credential verification and JWT token generation.

**Independent Test**: Submit login form with valid credentials → Password verified → JWT token returned with 7-day expiration.

**Tasks**:

### Backend Implementation

- [X] T036 [US2] Implement POST /api/auth/signin endpoint in backend/app/routers/auth.py
- [X] T037 [US2] Query User by email in signin endpoint (normalize email to lowercase)
- [X] T038 [US2] Verify password in signin endpoint using password.verify_password() against hashed_password
- [X] T039 [US2] Return 401 "Invalid credentials" if user not found or password incorrect (don't reveal which)
- [X] T040 [US2] Check user.is_active in signin endpoint, return 401 if inactive
- [X] T041 [US2] Generate JWT token in signin endpoint using jwt.create_access_token() with 7-day expiration
- [X] T042 [US2] Return TokenResponse with access_token, token_type="bearer", and user data in signin endpoint
- [X] T043 [US2] Add error handling in signin endpoint for authentication failures (401), database errors (500)

### Frontend Implementation

- [X] T044 [P] [US2] Update frontend/app/login/page.tsx to add email, password state and form handlers
- [X] T045 [US2] Implement handleLogin function in login page to call auth.signIn() with credentials
- [X] T046 [US2] Store JWT token in localStorage on successful login: `localStorage.setItem('token', data.access_token)`
- [X] T047 [US2] Redirect to /dashboard after successful login using useRouter().push('/dashboard')

**Completion Criteria**: Users can sign in with email/password. Password verified against bcrypt hash. JWT token generated and returned. Token stored in localStorage. User redirected to dashboard.

**Acceptance Test**:
```bash
# Test signin
curl -X POST http://localhost:8001/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Expected: 200 OK with JWT token and user data
```

---

## Phase 5: User Story 3 - Protected API Access (18 tasks)

**Goal**: Implement JWT verification middleware and protect all API endpoints.

**Independent Test**: Make API request with valid token → Middleware verifies token → Request succeeds. Make request with invalid/missing token → 401 error.

**Tasks**:

### Backend Middleware Implementation

- [X] T048 [US3] Create backend/app/middleware/auth.py with JWTAuthMiddleware class extending BaseHTTPMiddleware
- [X] T049 [US3] Implement dispatch() method in JWTAuthMiddleware to intercept all requests
- [X] T050 [US3] Add path exclusions in middleware for public endpoints: /health, /ready, /docs, /openapi.json, /api/auth/*
- [X] T051 [US3] Extract JWT token from Authorization header in middleware (format: "Bearer <token>")
- [X] T052 [US3] Return 401 "Authentication required" if Authorization header missing or malformed
- [X] T053 [US3] Verify JWT token signature in middleware using jwt.verify_token() with BETTER_AUTH_SECRET
- [X] T054 [US3] Return 401 "Token has expired" if token expiration (exp claim) has passed
- [X] T055 [US3] Return 401 "Invalid token" if token signature verification fails or token malformed
- [X] T056 [US3] Attach decoded token payload to request.state.user in middleware after successful verification
- [X] T057 [US3] Register JWTAuthMiddleware in backend/app/main.py using app.add_middleware()
- [X] T058 [US3] Register auth router in backend/app/main.py using app.include_router(auth.router)

### Backend Dependencies Implementation

- [X] T059 [P] [US3] Create backend/app/dependencies/auth.py with get_current_user() dependency function
- [X] T060 [US3] Implement get_current_user() to extract user from request.state.user (set by middleware)
- [X] T061 [US3] Raise 401 "Authentication required" in get_current_user() if request.state.user not set

### Frontend API Client Implementation

- [X] T062 [P] [US3] Update frontend/lib/api/client.ts to add request interceptor for JWT token injection
- [X] T063 [US3] Add Authorization header in request interceptor: `Authorization: Bearer ${localStorage.getItem('token')}`
- [X] T064 [US3] Add response interceptor in API client to handle 401 errors (clear token, redirect to /login)
- [X] T065 [US3] Update frontend/contexts/AuthContext.tsx to check for existing token on mount using getSession()

**Completion Criteria**: Middleware verifies JWT tokens on all /api/* requests. Valid tokens allow access. Invalid/missing tokens return 401. Frontend includes token in all API requests. 401 errors clear token and redirect to login.

**Acceptance Test**:
```bash
# Test protected endpoint with valid token
curl -X GET http://localhost:8001/api/users/USER_ID/tasks \
  -H "Authorization: Bearer VALID_TOKEN"
# Expected: 200 OK with tasks

# Test protected endpoint without token
curl -X GET http://localhost:8001/api/users/USER_ID/tasks
# Expected: 401 Unauthorized

# Test protected endpoint with invalid token
curl -X GET http://localhost:8001/api/users/USER_ID/tasks \
  -H "Authorization: Bearer INVALID_TOKEN"
# Expected: 401 Unauthorized
```

---

## Phase 6: User Story 4 - User Isolation (12 tasks)

**Goal**: Enforce user isolation by validating JWT user_id matches URL user_id parameter.

**Independent Test**: User A with valid token requests User A's resources → Success. User A requests User B's resources → 403 Forbidden.

**Tasks**:

### Backend User Isolation Implementation

- [X] T066 [US4] Add validate_user_access() function to backend/app/dependencies/auth.py
- [X] T067 [US4] Implement validate_user_access() to compare current_user["user_id"] with url_user_id parameter
- [X] T068 [US4] Raise 403 "Access denied: cannot access other users' resources" if user_id mismatch
- [X] T069 [US4] Update GET /api/users/{user_id}/tasks in backend/app/routers/tasks.py to add get_current_user dependency
- [X] T070 [US4] Add validate_user_access(current_user, user_id) call in GET /api/users/{user_id}/tasks
- [X] T071 [US4] Update POST /api/users/{user_id}/tasks in backend/app/routers/tasks.py to add user isolation validation
- [X] T072 [US4] Update PUT /api/users/{user_id}/tasks/{task_id} in backend/app/routers/tasks.py to add user isolation validation
- [X] T073 [US4] Update DELETE /api/users/{user_id}/tasks/{task_id} in backend/app/routers/tasks.py to add user isolation validation
- [X] T074 [US4] Update PATCH /api/users/{user_id}/tasks/{task_id} in backend/app/routers/tasks.py to add user isolation validation
- [X] T075 [US4] Ensure all task queries filter by user_id from JWT token (not URL parameter)
- [X] T076 [US4] Add error handling for 403 Forbidden responses in all task endpoints
- [X] T077 [US4] Update frontend error handling to display "Access denied" message for 403 responses

**Completion Criteria**: All task endpoints validate JWT user_id matches URL user_id. Users can only access their own tasks. Cross-user access attempts return 403 Forbidden.

**Acceptance Test**:
```bash
# Test user accessing own resources (should succeed)
curl -X GET http://localhost:8001/api/users/USER_A_ID/tasks \
  -H "Authorization: Bearer USER_A_TOKEN"
# Expected: 200 OK with User A's tasks

# Test user accessing another user's resources (should fail)
curl -X GET http://localhost:8001/api/users/USER_B_ID/tasks \
  -H "Authorization: Bearer USER_A_TOKEN"
# Expected: 403 Forbidden
```

---

## Phase 7: Polish & Cross-Cutting Concerns (8 tasks)

**Goal**: Add documentation, error handling improvements, and production readiness features.

**Tasks**:

- [X] T078 [P] Create backend/.env.example with all required environment variables and comments
- [X] T079 [P] Create frontend/.env.local.example with all required environment variables and comments
- [X] T080 [P] Update backend/README.md with authentication setup instructions and API documentation
- [X] T081 [P] Update frontend/README.md with authentication flow documentation and token storage notes
- [X] T082 [P] Add rate limiting to authentication endpoints in backend/app/routers/auth.py (prevent brute force)
- [X] T083 [P] Add CORS configuration in backend/app/main.py to whitelist frontend origin
- [X] T084 Document security considerations in README: token storage, secret management, known limitations
- [X] T085 Create end-to-end authentication flow test: signup → signin → protected access → logout

**Completion Criteria**: Documentation complete. Environment variables documented. Rate limiting configured. CORS configured. Security considerations documented.

---

## Dependencies & Execution Order

### User Story Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 (US4) → Phase 7 (Polish)
                                              ↓              ↓              ↓              ↓
                                           Independent   Independent   Independent   Depends on US3
```

**Dependency Rules**:
- **Phase 1 & 2**: Must complete before any user stories (foundational)
- **US1 (Registration)**: Independent, can be implemented first
- **US2 (Login)**: Independent, can be implemented in parallel with US1 (different endpoints)
- **US3 (JWT Verification)**: Independent, can be implemented in parallel with US1/US2 (middleware layer)
- **US4 (User Isolation)**: Depends on US3 (requires middleware to extract user_id from token)
- **Phase 7 (Polish)**: Can be done in parallel with user stories (documentation, configuration)

### Parallel Execution Opportunities

**Phase 1 (Setup)**: All 8 tasks can run in parallel (different files, no dependencies)

**Phase 2 (Foundational)**:
- Parallel Group 1: T009, T010, T011, T012 (different files)
- Sequential: T013 → T018 → T019 (database migrations)
- Parallel Group 2: T014, T015, T016, T017 (different files)
- Sequential: T020 → T021 (task model update)

**Phase 3 (US1)**:
- Backend tasks (T022-T030) must be sequential (same file)
- Frontend tasks (T031-T035): T031 can be parallel, T032-T035 sequential
- Backend and Frontend can run in parallel (different services)

**Phase 4 (US2)**:
- Backend tasks (T036-T043) must be sequential (same file)
- Frontend tasks (T044-T047): T044 can be parallel, T045-T047 sequential
- Backend and Frontend can run in parallel (different services)
- **US2 can run in parallel with US1** (different endpoints)

**Phase 5 (US3)**:
- Middleware tasks (T048-T058) must be sequential (same file)
- Dependencies tasks (T059-T061) can be parallel with middleware
- Frontend tasks (T062-T065) can be parallel with backend
- **US3 can run in parallel with US1/US2** (different layer)

**Phase 6 (US4)**:
- All tasks (T066-T077) must be sequential (modifying existing endpoints)
- **US4 depends on US3** (requires middleware)

**Phase 7 (Polish)**: All 8 tasks can run in parallel (different files, documentation)

---

## MVP Scope Recommendation

**Minimum Viable Product (MVP)**: Complete Phase 1, Phase 2, and Phase 3 (US1 only)

**MVP Delivers**:
- User registration with email/password
- Password hashing with bcrypt
- JWT token generation with 7-day expiration
- Token storage in localStorage
- Basic authentication flow

**MVP Test**:
```bash
# 1. User signs up
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# 2. Verify JWT token returned
# 3. Verify user created in database
# 4. Verify password hashed with bcrypt
```

**Next Increments**:
- **Increment 2**: Add Phase 4 (US2 - Login)
- **Increment 3**: Add Phase 5 (US3 - JWT Verification)
- **Increment 4**: Add Phase 6 (US4 - User Isolation)
- **Increment 5**: Add Phase 7 (Polish)

---

## Task Summary

**Total Tasks**: 85
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 13 tasks
- Phase 3 (US1 - Registration): 14 tasks
- Phase 4 (US2 - Login): 12 tasks
- Phase 5 (US3 - JWT Verification): 18 tasks
- Phase 6 (US4 - User Isolation): 12 tasks
- Phase 7 (Polish): 8 tasks

**Parallelizable Tasks**: 28 tasks marked with [P]

**User Story Distribution**:
- US1: 14 tasks
- US2: 12 tasks
- US3: 18 tasks
- US4: 12 tasks
- Setup/Foundational/Polish: 29 tasks

**Estimated Completion**: 3-4 days (per spec constraint)
- Day 1: Phase 1, Phase 2 (Setup & Foundational)
- Day 2: Phase 3, Phase 4 (US1 Registration, US2 Login)
- Day 3: Phase 5 (US3 JWT Verification)
- Day 4: Phase 6, Phase 7 (US4 User Isolation, Polish)

---

## Format Validation

✓ All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✓ Task IDs sequential (T001-T085)
✓ [P] markers for parallelizable tasks (28 tasks)
✓ [Story] labels for user story tasks (US1, US2, US3, US4)
✓ File paths included in all implementation tasks
✓ Independent test criteria for each user story
✓ Dependencies documented
✓ Parallel execution opportunities identified

**Ready for execution**: Run `/sp.implement` to begin task execution.
