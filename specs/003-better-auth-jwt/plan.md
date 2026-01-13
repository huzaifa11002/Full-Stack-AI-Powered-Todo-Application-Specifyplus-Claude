# Implementation Plan: Better Auth JWT Authentication Integration

**Branch**: `003-better-auth-jwt` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-better-auth-jwt/spec.md`

## Summary

Implement JWT-based authentication using Better Auth (Next.js frontend) and PyJWT (FastAPI backend) with shared secret key for token signing/verification. Users will sign up and sign in through Better Auth, receiving JWT tokens that are verified by FastAPI middleware on all protected API endpoints. User isolation is enforced by comparing JWT user_id claims with URL path parameters.

**Primary Requirements**:
- Better Auth installation and configuration with JWT plugin in Next.js
- User signup/signin with email and password (bcrypt hashing)
- JWT token generation with 7-day expiration
- FastAPI middleware for token verification and user isolation
- Shared BETTER_AUTH_SECRET environment variable across services

**Technical Approach**:
- Frontend: Better Auth handles authentication, generates JWT tokens
- Backend: PyJWT verifies tokens, FastAPI middleware enforces authorization
- Token transmission: Authorization: Bearer <token> header
- Token storage: localStorage (development) or httpOnly cookies (production)
- User isolation: Middleware validates JWT user_id matches URL user_id parameter

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.0+, Node.js 18+
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Better Auth (npm), Next.js 16+, React 18+
- Backend: PyJWT (pip), FastAPI (latest stable), SQLModel, Pydantic v2

**Storage**:
- PostgreSQL (Neon DB) for user credentials and tasks
- JWT tokens in localStorage (dev) or httpOnly cookies (prod)

**Testing**:
- Frontend: Jest, React Testing Library (60% coverage target)
- Backend: pytest (70% coverage target)
- Integration: End-to-end authentication flow tests

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge)
- Backend: Linux server (containerized with Docker)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- JWT verification: <10ms per request
- Authentication endpoints: <200ms p95 latency
- Token generation: <100ms

**Constraints**:
- Must use Better Auth + PyJWT (no alternative libraries)
- JWT-only authentication (no session-based auth)
- Bearer token transmission only (no query parameters)
- 7-day token expiration (fixed, not configurable per user)
- Shared secret between services (no asymmetric keys)
- 3-4 day implementation timeline

**Scale/Scope**:
- Initial: 10-100 concurrent users
- JWT token size: <1KB
- 4 user stories (3 P1, 1 P2)
- 33 functional requirements
- 2 services (Next.js frontend, FastAPI backend)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

**I. Production-Ready Code Quality** ✓ PASS
- TypeScript strict mode enabled (100% typed code)
- Python type hints for all function signatures
- Testing coverage targets: 70% backend, 60% frontend
- ESLint (frontend) and Ruff (backend) with zero warnings
- Architectural decisions documented in code comments

**II. Cloud-Native Architecture** ✓ PASS
- Services containerized with Docker (existing infrastructure)
- Health check endpoints required (`/health`, `/ready`)
- Graceful shutdown handling (SIGTERM)
- Configuration externalized (environment variables)
- Stateless JWT authentication (no server-side sessions)

**III. AI Integration Excellence** ⚠️ NOT APPLICABLE
- This feature does not integrate AI capabilities
- No AI API calls, streaming, or context management required

**IV. Security-First Approach** ✓ PASS
- All secrets in environment variables (BETTER_AUTH_SECRET)
- JWT-based authentication with 7-day expiration
- API rate limiting enforced on authentication endpoints
- Input sanitization via Pydantic models
- CORS properly configured
- Parameterized database queries (SQLModel)
- Password hashing with bcrypt (cost factor 12+)

**V. Developer Experience** ✓ PASS
- README with setup instructions for both services
- Local development with docker-compose
- Environment-specific configurations documented (.env.example files)
- Consistent code patterns across codebase
- OpenAPI/Swagger documentation for authentication endpoints

### Technology Stack Compliance

**Fixed Technologies** ✓ PASS
- Frontend: Next.js 16+, React 18+, TypeScript 5+, Tailwind CSS ✓
- Backend: FastAPI, Python 3.11+, SQLModel, Pydantic v2 ✓
- Database: Neon DB (PostgreSQL-compatible) ✓
- Additional: Better Auth (npm), PyJWT (pip) ✓

### Security Requirements Compliance

**Authentication & Authorization** ⚠️ PARTIAL COMPLIANCE
- JWT Tokens: Using 7-day access tokens (spec requirement)
  - Constitution recommends: 15-minute access tokens + 7-day refresh tokens
  - **Justification**: Spec explicitly requires 7-day expiration, refresh tokens out of scope
  - **Mitigation**: Document security tradeoff, plan refresh tokens for future
- Token Storage: localStorage (dev) or httpOnly cookies (prod) ✓
- Password Hashing: bcrypt with cost factor 12+ ✓
- Session Management: No token revocation (limitation documented) ⚠️

**API Security** ✓ PASS
- Rate limiting on authentication endpoints ✓
- Input validation and sanitization (Pydantic) ✓
- CORS whitelist specific origins in production ✓
- HTTPS enforced in production ✓

**Secrets Management** ✓ PASS
- Environment variables for all secrets ✓
- .env files never committed (.gitignore) ✓
- Secret rotation procedures documented ✓
- Principle of least privilege ✓

**Data Protection** ✓ PASS
- Encryption at rest (Neon DB) ✓
- TLS 1.3 for network communication ✓
- Audit logging for authentication events ✓

### Quality Gates

**Phase II Completion (Current Phase)** ✓ APPLICABLE
- Full CRUD operations for todos via REST API ✓ (already implemented)
- Next.js frontend consuming FastAPI backend ✓ (already implemented)
- Data persisting in Neon DB ✓ (already implemented)
- Type safety across frontend and backend ✓ (already implemented)
- API documentation (OpenAPI/Swagger) ✓ (already implemented)
- Minimum test coverage ✓ (already implemented)

**This Feature's Quality Gates**:
- All passwords hashed with bcrypt (never plain text)
- JWT tokens cryptographically signed with HS256
- Same BETTER_AUTH_SECRET used in both services
- Token expiration enforced (7 days)
- User isolation guaranteed (JWT user_id matches URL user_id)
- Error messages don't leak sensitive information
- CORS properly configured for production
- Environment variables documented

### Gate Evaluation

**Status**: ✓ PASS WITH JUSTIFICATIONS

**Violations Requiring Justification**:
1. **7-day token expiration** (vs constitution's 15-minute recommendation)
   - **Why Needed**: Spec explicitly requires 7-day expiration for user convenience
   - **Alternatives Considered**: 15-minute access + 7-day refresh tokens (rejected: out of scope)
   - **Mitigation**: Document security tradeoff, plan refresh token mechanism for future
   - **Review**: Approved by spec requirements

2. **No token revocation** (vs constitution's session management requirement)
   - **Why Needed**: Stateless JWT authentication, no server-side session storage
   - **Alternatives Considered**: Token blacklist (rejected: adds complexity, out of scope)
   - **Mitigation**: Document limitation, shorter expiration in future, monitor for abuse
   - **Review**: Acceptable for MVP, must be addressed before production scale

## Project Structure

### Documentation (this feature)

```text
specs/003-better-auth-jwt/
├── spec.md              # Feature specification (/sp.specify output)
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (integration scenarios)
├── contracts/           # Phase 1 output (API specifications)
│   ├── auth-api.yaml    # Authentication endpoints (OpenAPI)
│   └── jwt-schema.json  # JWT token structure
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)

backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User model (NEW - to be created)
│   │   └── task.py                # Task model (existing)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication endpoints (NEW - to be created)
│   │   └── tasks.py               # Task endpoints (existing - to be modified)
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py                # JWT verification middleware (NEW - to be created)
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py                # Authentication dependencies (NEW - to be created)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                # User schemas (NEW - to be created)
│   │   └── task.py                # Task schemas (existing)
│   └── utils/
│       ├── __init__.py
│       └── jwt.py                 # JWT utilities (NEW - to be created)
├── tests/
│   ├── unit/
│   │   ├── test_jwt_verification.py    # JWT verification tests (NEW)
│   │   └── test_user_isolation.py      # User isolation tests (NEW)
│   ├── integration/
│   │   ├── test_auth_flow.py           # End-to-end auth tests (NEW)
│   │   └── test_protected_routes.py    # Protected endpoint tests (NEW)
│   └── contract/
│       └── test_auth_api.py            # API contract tests (NEW)
├── alembic/
│   └── versions/
│       └── xxx_add_user_table.py       # User table migration (NEW - to be created)
├── .env.example                        # Environment variables template (to be updated)
└── requirements.txt                    # Python dependencies (to be updated)

frontend/
├── app/
│   ├── api/
│   │   └── auth/
│   │       └── [...all]/
│   │           └── route.ts            # Better Auth API route (NEW - to be created)
│   ├── login/
│   │   └── page.tsx                    # Login page (existing - to be modified)
│   ├── signup/
│   │   └── page.tsx                    # Signup page (existing - to be modified)
│   └── dashboard/
│       └── page.tsx                    # Dashboard (existing - already protected)
├── lib/
│   ├── auth.ts                         # Better Auth configuration (NEW - to be created)
│   └── api/
│       └── client.ts                   # API client (existing - to be modified for JWT)
├── contexts/
│   └── AuthContext.tsx                 # Auth context (existing - to be modified)
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx               # Login form (existing - to be modified)
│   │   └── SignupForm.tsx              # Signup form (existing - to be modified)
│   └── ProtectedRoute.tsx              # Route protection (existing - to be modified)
├── types/
│   └── auth.ts                         # Auth types (existing - to be modified)
├── middleware.ts                       # Next.js middleware (existing - to be modified)
├── .env.local.example                  # Environment variables template (to be updated)
└── package.json                        # npm dependencies (to be updated)
```

**Structure Decision**: Web application structure selected because this feature spans both Next.js frontend and FastAPI backend. The frontend handles authentication UI and token generation (Better Auth), while the backend handles token verification and user isolation (PyJWT middleware). Both services share the BETTER_AUTH_SECRET environment variable for JWT signing and verification.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 7-day token expiration (vs 15-min access + 7-day refresh) | Spec explicitly requires 7-day expiration for user convenience; refresh tokens out of scope | 15-minute access tokens would require refresh token mechanism (out of scope), causing poor UX with frequent re-authentication |
| No token revocation (vs session management) | Stateless JWT authentication per spec; no server-side session storage | Token blacklist adds complexity (Redis/database), increases latency, contradicts stateless design; acceptable for MVP with documented limitation |

## Phase 0: Research & Decisions

### Research Topics

1. **Better Auth Integration with Next.js 16**
   - Research: Better Auth compatibility with Next.js 16 App Router
   - Context: Feature 002 encountered Better Auth import errors
   - Goal: Determine if Better Auth client library works or if custom implementation needed

2. **JWT Token Structure Best Practices**
   - Research: Standard JWT claims for authentication
   - Context: Need to define token payload structure
   - Goal: Determine required claims (user_id, email, iat, exp) and optional claims

3. **FastAPI Middleware Architecture**
   - Research: Best practices for FastAPI authentication middleware
   - Context: Need to intercept all /api/* requests for JWT verification
   - Goal: Determine middleware vs dependency injection approach

4. **Token Storage Security**
   - Research: localStorage vs httpOnly cookies for JWT storage
   - Context: Need to balance security and implementation complexity
   - Goal: Document security tradeoffs and recommend approach

5. **User Isolation Patterns**
   - Research: Best practices for enforcing user data isolation
   - Context: Need to prevent users from accessing other users' data
   - Goal: Determine middleware vs route-level vs database-level enforcement

### Key Decisions

**Decision 1: Token Storage Location**
- **Options**: httpOnly cookies vs localStorage vs sessionStorage
- **Tradeoff**:
  - httpOnly cookies: More secure (XSS-proof) but needs CORS config
  - localStorage: Simpler implementation but vulnerable to XSS
  - sessionStorage: Cleared on tab close (less convenient)
- **Chosen**: localStorage for development, httpOnly cookies for production
- **Rationale**: Start with simpler localStorage for rapid development, migrate to httpOnly cookies before production deployment
- **Alternatives Considered**: sessionStorage rejected due to poor UX (cleared on tab close)

**Decision 2: Token Expiration Duration**
- **Options**: 1 hour vs 1 day vs 7 days vs 30 days
- **Tradeoff**: Security (shorter is better) vs UX (longer is convenient)
- **Chosen**: 7 days (per spec requirement)
- **Rationale**: Spec explicitly requires 7-day expiration; balances security and UX for MVP
- **Alternatives Considered**: 15-minute access + 7-day refresh tokens (rejected: out of scope)

**Decision 3: Password Requirements**
- **Options**: Minimal (6 chars) vs Moderate (8 chars, mixed) vs Strict (complex rules)
- **Tradeoff**: Security vs user friction
- **Chosen**: Minimum 8 characters, at least one number and letter
- **Rationale**: Balances security with user experience; aligns with industry standards
- **Alternatives Considered**: Strict rules (uppercase, lowercase, number, symbol) rejected due to user friction

**Decision 4: JWT Algorithm**
- **Options**: HS256 (symmetric) vs RS256 (asymmetric)
- **Tradeoff**: Simplicity vs multiple service support
- **Chosen**: HS256 with shared secret
- **Rationale**: Single backend service, simpler implementation, adequate security for shared secret
- **Alternatives Considered**: RS256 rejected (unnecessary complexity for single backend)

**Decision 5: User ID Match Enforcement**
- **Options**: Middleware vs Route-level vs Database-level
- **Tradeoff**: Centralized vs granular control
- **Chosen**: Middleware for consistency, route-level for special cases
- **Rationale**: Middleware provides centralized enforcement, reduces code duplication, easier to audit
- **Alternatives Considered**: Route-level only (rejected: code duplication, easy to forget)

**Decision 6: Better Auth Implementation**
- **Options**: Better Auth client library vs Custom JWT implementation
- **Tradeoff**: Library convenience vs implementation control
- **Chosen**: Custom JWT implementation if Better Auth client has compatibility issues
- **Rationale**: Feature 002 encountered Better Auth import errors; fallback to custom implementation
- **Alternatives Considered**: Wait for Better Auth fix (rejected: timeline constraints)

## Phase 1: Design & Contracts

### Implementation Phases

#### Phase 1: Better Auth Setup (Frontend - Next.js)
- Install Better Auth package: `npm install better-auth`
- Create auth configuration file: `lib/auth.ts`
- Configure Better Auth with:
  - Database adapter (for user storage)
  - Email/password provider
  - JWT plugin enabled
  - Token expiration settings (7 days)
- Set up BETTER_AUTH_SECRET in .env.local
- Create auth API route handler: `app/api/auth/[...all]/route.ts`
- Configure Better Auth client for frontend usage

#### Phase 2: User Database Schema (Backend - FastAPI)
- Extend User model in models.py to include:
  - id (primary key, UUID)
  - email (unique, indexed)
  - username (optional)
  - hashed_password (store Better Auth's bcrypt hash)
  - created_at, updated_at timestamps
  - is_active (boolean, default True)
- Create database migration to add User table
- Add email validation in schema
- Ensure User model matches Better Auth's expectations

#### Phase 3: Signup Implementation
**Frontend (Next.js):**
- Create signup API endpoint using Better Auth
- Build signup form component with:
  - Email input (validation: valid email format)
  - Password input (validation: min 8 chars, complexity rules)
  - Confirm password field
  - Submit handler
- Implement form validation and error display
- Hash password using Better Auth before storage
- Return JWT token upon successful signup

**Backend (FastAPI):**
- Create POST /api/auth/signup endpoint (if needed for custom logic)
- Validate email uniqueness
- Store user in database
- Return success response

#### Phase 4: Signin Implementation
**Frontend (Next.js):**
- Create signin API endpoint using Better Auth
- Build login form component with:
  - Email input
  - Password input
  - Submit handler
- Verify credentials against database
- Generate JWT token on successful authentication
- Store token in httpOnly cookie or localStorage
- Return user data and token to client

**Token Generation:**
- JWT payload structure:
```json
{
  "user_id": "123",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234567890
}
```
- Sign with BETTER_AUTH_SECRET
- Set expiration to 7 days from issue time

#### Phase 5: Frontend Token Management
- Create auth context/provider: `contexts/AuthContext.tsx`
- Implement token storage strategy:
  - Option A: httpOnly cookies (more secure)
  - Option B: localStorage (simpler, document security tradeoffs)
- Build useAuth() hook for accessing auth state
- Implement automatic token inclusion in API requests
- Create API client wrapper that adds Authorization header:
```javascript
headers: {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
}
```

#### Phase 6: FastAPI JWT Middleware
**Create middleware in app/middleware/auth.py:**
- Extract token from Authorization header
- Validate Bearer format: `Bearer <token>`
- Verify JWT signature using BETTER_AUTH_SECRET
- Decode token and extract payload
- Handle expired tokens (return 401)
- Handle invalid tokens (return 401)
- Handle missing tokens (return 401)
- Attach user info to request state for route handlers

**JWT Verification Logic:**
```python
import jwt
from fastapi import HTTPException, Request

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

#### Phase 7: Apply Middleware to Routes
- Add middleware to main.py
- Apply to all /api/{user_id}/tasks/* endpoints
- Middleware execution order:
  1. Extract token
  2. Verify token
  3. Extract user_id from JWT
  4. Compare JWT user_id with URL user_id
  5. Pass request to route handler OR return 401

**User ID Validation:**
```python
# In middleware or dependency
def validate_user_access(request: Request, user_id: int):
    token_user_id = request.state.user["user_id"]
    if str(token_user_id) != str(user_id):
        raise HTTPException(403, "Access denied")
```

#### Phase 8: Update API Routes for Auth
**Modify all task endpoints in routers/tasks.py:**
- Add dependency: `Depends(get_current_user)`
- Extract authenticated user from request state
- Enforce user_id matching in all queries
- Remove placeholder user_id logic
- Add authentication checks before data operations

**Example route update:**
```python
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    validate_user_access(current_user, user_id)
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

#### Phase 9: Error Handling & Responses
**Standardize 401 responses:**
```json
{
  "detail": "Authentication required",
  "status_code": 401
}
```

**Standardize 403 responses:**
```json
{
  "detail": "Access denied - user mismatch",
  "status_code": 403
}
```

**Handle edge cases:**
- Token missing: 401 "No authentication token provided"
- Token malformed: 401 "Invalid token format"
- Token expired: 401 "Token has expired"
- User mismatch: 403 "Cannot access another user's data"
- User not found: 401 "User no longer exists"

#### Phase 10: Environment Configuration
**Frontend .env.local:**
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend .env:**
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
DATABASE_URL=postgresql://...
FRONTEND_URL=http://localhost:3000
```

**Secret Generation:**
- Generate cryptographically secure secret (32+ characters)
- Use same secret in both services
- Document secret rotation process
- Never commit secrets to git

#### Phase 11: Frontend Auth Flow Integration
- Create protected route wrapper component
- Implement redirect logic:
  - Unauthenticated → /login
  - Authenticated → /dashboard
- Add logout functionality (clear token)
- Handle token expiration gracefully (show re-login prompt)
- Add loading states during auth checks

### Testing Strategy

**Authentication Flow Testing:**
1. ✅ User can sign up with valid email/password
2. ✅ Duplicate email registration fails
3. ✅ User can sign in with correct credentials
4. ✅ Sign in fails with wrong password
5. ✅ JWT token is returned on successful signin
6. ✅ Token contains correct user_id and email
7. ✅ Token expires after 7 days

**Authorization Testing:**
1. ✅ Request without token returns 401
2. ✅ Request with invalid token returns 401
3. ✅ Request with expired token returns 401
4. ✅ Request with valid token succeeds
5. ✅ User can access their own tasks
6. ✅ User cannot access another user's tasks (403)
7. ✅ Token user_id must match URL user_id

**Integration Testing:**
1. ✅ Signup → Signin → Access tasks (full flow works)
2. ✅ Multiple users can operate independently
3. ✅ Token persists across browser refresh (if cookies)
4. ✅ Logout clears authentication state
5. ✅ Protected routes redirect unauthenticated users

**Security Testing:**
- Test with tampered tokens (signature mismatch)
- Test with tokens from different secret keys
- Test user_id mismatch scenarios
- Test concurrent sessions (same user, different devices)
- Verify passwords are hashed (never stored plain text)

### Technical Examples

**Better Auth Configuration:**
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: {
    // database connection
  },
  emailAndPassword: {
    enabled: true,
  },
  jwt: {
    enabled: true,
    expiresIn: 60 * 60 * 24 * 7, // 7 days
  },
  secret: process.env.BETTER_AUTH_SECRET,
})
```

**FastAPI Middleware:**
```python
from starlette.middleware.base import BaseHTTPMiddleware

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            token = extract_token(request)
            if not token:
                return JSONResponse(
                    {"detail": "Authentication required"},
                    status_code=401
                )
            user = verify_token(token)
            request.state.user = user
        return await call_next(request)
```

### Development Workflow

1. Set up Better Auth in Next.js project
2. Create signup/signin UI and test token generation
3. Implement FastAPI middleware and test token verification
4. Connect frontend API client with token injection
5. Update all backend routes to require authentication
6. Test end-to-end auth flow
7. Handle edge cases and error scenarios
8. Document authentication process

### Quality Validation

- All passwords are hashed (never plain text)
- Tokens are cryptographically signed
- Same secret used in both services
- Token expiration is enforced
- User isolation is guaranteed
- Error messages don't leak sensitive info
- CORS is properly configured
- Environment variables are documented

### Security Checklist

- [ ] BETTER_AUTH_SECRET is strong (32+ chars)
- [ ] Secrets are in .env, not committed to git
- [ ] Passwords are hashed with bcrypt
- [ ] JWT tokens are signed with HS256
- [ ] Token expiration is set and enforced
- [ ] 401/403 responses are appropriate
- [ ] User ID validation prevents cross-user access
- [ ] CORS allows only trusted origins

## Next Steps

1. **Phase 0**: Create `research.md` with detailed technology decisions
2. **Phase 1**: Create `data-model.md` with User and JWT Token entities
3. **Phase 1**: Create `contracts/` with OpenAPI specifications for auth endpoints
4. **Phase 1**: Create `quickstart.md` with integration scenarios
5. **Phase 1**: Update agent context with Better Auth and PyJWT technologies
6. **Phase 2**: Run `/sp.tasks` to generate task breakdown from this plan
