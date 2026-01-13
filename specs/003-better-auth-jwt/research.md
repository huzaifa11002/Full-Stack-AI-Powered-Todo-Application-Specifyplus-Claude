# Research: Better Auth JWT Authentication Integration

**Feature**: 003-better-auth-jwt
**Date**: 2026-01-10
**Status**: Complete

## Overview

This document captures research findings and technology decisions for implementing JWT-based authentication using Better Auth (Next.js) and PyJWT (FastAPI). All decisions are based on spec requirements, constitution compliance, and lessons learned from feature 002.

## Research Topics

### 1. Better Auth Integration with Next.js 16

**Context**: Feature 002 encountered Better Auth client library import errors when building the Next.js application.

**Research Question**: Is Better Auth compatible with Next.js 16 App Router, or do we need a custom JWT implementation?

**Findings**:
- Better Auth library had export issues in feature 002: `betterAuth` export not found in `better-auth/client`
- The error suggested using `createAuthClient` instead
- Feature 002 resolved this by implementing direct API calls to FastAPI backend instead of using Better Auth client wrapper

**Decision**: Start with Better Auth server-side configuration, but prepare fallback to custom JWT implementation if client library issues persist

**Rationale**:
- Better Auth provides robust server-side authentication with bcrypt hashing
- JWT plugin simplifies token generation
- If client library fails, we can generate JWTs manually using `jsonwebtoken` npm package
- Timeline constraints (3-4 days) require pragmatic approach

**Alternatives Considered**:
- Wait for Better Auth fix: Rejected (timeline constraints)
- Use NextAuth.js: Rejected (spec explicitly requires Better Auth)
- Custom implementation from scratch: Rejected (reinventing the wheel, more error-prone)

**Implementation Approach**:
1. Install Better Auth: `npm install better-auth`
2. Configure server-side auth in `lib/auth.ts`
3. Create API route handler: `app/api/auth/[...all]/route.ts`
4. Test token generation
5. If client library fails, use direct fetch calls (as in feature 002)

---

### 2. JWT Token Structure Best Practices

**Context**: Need to define JWT payload structure that balances security, functionality, and token size.

**Research Question**: What claims should be included in JWT tokens for authentication and user isolation?

**Findings**:
- Standard JWT claims: `iss` (issuer), `sub` (subject), `aud` (audience), `exp` (expiration), `iat` (issued at)
- Custom claims: Application-specific data (user_id, email, roles, permissions)
- Token size considerations: Each claim adds to token size; keep minimal for performance
- Security best practices: Don't include sensitive data (passwords, SSNs, credit cards)

**Decision**: JWT payload structure
```json
{
  "user_id": "uuid-string",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234567890
}
```

**Rationale**:
- `user_id`: Required for user isolation (matching URL parameters)
- `email`: Useful for display, audit logging, and user identification
- `iat`: Standard claim for token issue time
- `exp`: Standard claim for token expiration (7 days from iat)
- Minimal payload keeps token size <1KB
- No roles/permissions (out of scope per spec)

**Alternatives Considered**:
- Include `username`: Rejected (optional field, not always present)
- Include `is_active`: Rejected (should be checked on each request, not cached in token)
- Include `roles`: Rejected (RBAC out of scope)
- Use `sub` instead of `user_id`: Rejected (less explicit, prefer clarity)

**Security Considerations**:
- Never include password or password hash in token
- Email is not sensitive (already visible to user)
- user_id is UUID (not sequential, doesn't leak user count)

---

### 3. FastAPI Middleware Architecture

**Context**: Need to intercept all /api/* requests for JWT verification before reaching route handlers.

**Research Question**: Should we use middleware or dependency injection for JWT verification?

**Findings**:
- **Middleware**: Intercepts all requests globally, runs before routing
  - Pros: Centralized, consistent, hard to bypass
  - Cons: Applies to all routes (need to exclude public endpoints)
- **Dependency Injection**: Applied per-route using `Depends()`
  - Pros: Granular control, explicit per-route
  - Cons: Easy to forget, code duplication, inconsistent

**Decision**: Use middleware for JWT verification with path-based exclusions

**Rationale**:
- Centralized enforcement reduces risk of forgetting authentication
- Easier to audit (single location for auth logic)
- Path-based exclusions handle public endpoints (health checks, auth endpoints)
- Aligns with security-first principle (fail-secure by default)

**Implementation**:
```python
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude public paths
        if request.url.path in ["/health", "/ready", "/docs", "/openapi.json"]:
            return await call_next(request)

        # Exclude auth endpoints
        if request.url.path.startswith("/api/auth/"):
            return await call_next(request)

        # Require JWT for all other /api/* endpoints
        if request.url.path.startswith("/api/"):
            token = extract_token(request)
            if not token:
                return JSONResponse({"detail": "Authentication required"}, status_code=401)
            user = verify_token(token)
            request.state.user = user

        return await call_next(request)
```

**Alternatives Considered**:
- Dependency injection only: Rejected (easy to forget, inconsistent)
- Hybrid (middleware + dependencies): Rejected (unnecessary complexity)
- Route-level decorators: Rejected (not idiomatic in FastAPI)

---

### 4. Token Storage Security

**Context**: Need to store JWT tokens on the client side for subsequent API requests.

**Research Question**: Should we use localStorage, sessionStorage, or httpOnly cookies?

**Findings**:
- **localStorage**:
  - Pros: Simple, persists across browser sessions, easy to implement
  - Cons: Vulnerable to XSS attacks (JavaScript can access), not cleared on tab close
- **sessionStorage**:
  - Pros: Cleared on tab close (better security), simple
  - Cons: Poor UX (user must re-login on every tab), vulnerable to XSS
- **httpOnly cookies**:
  - Pros: XSS-proof (JavaScript cannot access), automatic inclusion in requests
  - Cons: Requires CORS configuration, CSRF protection needed, more complex setup

**Decision**: localStorage for development, httpOnly cookies for production

**Rationale**:
- Start with localStorage for rapid development and testing
- Migrate to httpOnly cookies before production deployment
- Document security tradeoff in README
- Constitution requires security-first approach (httpOnly for production)

**Implementation Plan**:
1. **Development (localStorage)**:
   - Store token: `localStorage.setItem('token', token)`
   - Retrieve token: `localStorage.getItem('token')`
   - Clear token: `localStorage.removeItem('token')`
   - Add to requests: `Authorization: Bearer ${token}`

2. **Production (httpOnly cookies)**:
   - Set cookie on login: `Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict`
   - Browser automatically includes cookie in requests
   - Backend reads cookie: `request.cookies.get('token')`
   - CORS configuration: Allow credentials, whitelist frontend origin

**Alternatives Considered**:
- sessionStorage only: Rejected (poor UX, user must re-login frequently)
- httpOnly cookies from start: Rejected (adds complexity, slows development)
- In-memory only: Rejected (lost on page refresh, poor UX)

**Security Mitigation**:
- localStorage: Implement Content Security Policy (CSP) headers to reduce XSS risk
- httpOnly cookies: Implement CSRF protection (SameSite=Strict, CSRF tokens)
- Both: Use HTTPS in production (TLS 1.3)

---

### 5. User Isolation Patterns

**Context**: Need to prevent users from accessing other users' data (e.g., User A accessing User B's tasks).

**Research Question**: Where should user isolation be enforced: middleware, route-level, or database-level?

**Findings**:
- **Middleware-level**:
  - Pros: Centralized, consistent, runs before route handlers
  - Cons: Requires parsing URL parameters, may not fit all use cases
- **Route-level**:
  - Pros: Granular control, explicit per-route, flexible
  - Cons: Code duplication, easy to forget, inconsistent
- **Database-level**:
  - Pros: Guaranteed enforcement, works even if application logic fails
  - Cons: Requires row-level security (RLS), complex setup, performance overhead

**Decision**: Middleware for user_id extraction + route-level validation for enforcement

**Rationale**:
- Middleware extracts user_id from JWT and attaches to request state
- Route handlers validate user_id matches URL parameter
- Provides both centralized extraction and granular enforcement
- Easier to test and audit than pure middleware approach

**Implementation**:
```python
# Middleware: Extract user from JWT
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            token = extract_token(request)
            user = verify_token(token)
            request.state.user = user  # Attach to request
        return await call_next(request)

# Dependency: Validate user access
def get_current_user(request: Request) -> dict:
    if not hasattr(request.state, "user"):
        raise HTTPException(401, "Authentication required")
    return request.state.user

def validate_user_access(current_user: dict, user_id: str):
    if current_user["user_id"] != user_id:
        raise HTTPException(403, "Access denied: cannot access other users' resources")

# Route: Use dependency and validation
@router.get("/api/users/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    validate_user_access(current_user, user_id)
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks
```

**Alternatives Considered**:
- Middleware-only: Rejected (hard to parse all URL patterns, inflexible)
- Route-level only: Rejected (code duplication, easy to forget)
- Database RLS: Rejected (complex setup, out of scope for MVP)

**Testing Strategy**:
- Unit tests: Verify validate_user_access raises 403 on mismatch
- Integration tests: Verify User A cannot access User B's tasks
- Security tests: Attempt cross-user access with valid tokens

---

### 6. Password Requirements

**Context**: Need to balance security with user experience for password requirements.

**Research Question**: What password requirements should we enforce?

**Findings**:
- **NIST Guidelines (2017)**:
  - Minimum 8 characters
  - No complexity requirements (uppercase, lowercase, numbers, symbols)
  - Check against common password lists
  - No periodic password changes
- **Industry Practice**:
  - Most sites: 8-12 character minimum
  - Some sites: Complexity requirements (mixed case, numbers, symbols)
  - Trend: Moving away from strict complexity rules

**Decision**: Minimum 8 characters, at least one number and one letter

**Rationale**:
- Balances security with user experience
- Aligns with NIST guidelines (8 character minimum)
- Light complexity requirement (number + letter) prevents trivial passwords
- Avoids user friction from strict rules (uppercase, symbols, etc.)

**Implementation**:
```typescript
// Frontend validation
const validatePassword = (password: string): string | null => {
  if (password.length < 8) {
    return "Password must be at least 8 characters";
  }
  if (!/\d/.test(password)) {
    return "Password must contain at least one number";
  }
  if (!/[a-zA-Z]/.test(password)) {
    return "Password must contain at least one letter";
  }
  return null; // Valid
};
```

**Alternatives Considered**:
- Minimal (6 chars): Rejected (too weak, below NIST guidelines)
- Strict (uppercase, lowercase, number, symbol): Rejected (user friction, not significantly more secure)
- No requirements: Rejected (allows trivial passwords like "password")

**Future Enhancements**:
- Check against common password lists (e.g., Have I Been Pwned API)
- Password strength meter in UI
- Passphrase support (longer, easier to remember)

---

### 7. JWT Algorithm Selection

**Context**: Need to choose JWT signing algorithm for token generation and verification.

**Research Question**: Should we use symmetric (HS256) or asymmetric (RS256) algorithm?

**Findings**:
- **HS256 (HMAC with SHA-256)**:
  - Symmetric: Same secret for signing and verification
  - Pros: Simple, fast, adequate security for shared secret
  - Cons: Requires secure secret sharing between services
- **RS256 (RSA with SHA-256)**:
  - Asymmetric: Private key for signing, public key for verification
  - Pros: Public key can be shared freely, supports multiple verifiers
  - Cons: More complex, slower, requires key management

**Decision**: HS256 with shared BETTER_AUTH_SECRET

**Rationale**:
- Single backend service (FastAPI) verifies tokens
- Simpler implementation (no key pair management)
- Adequate security for shared secret (32+ characters)
- Faster performance (symmetric operations)
- Aligns with spec requirement (shared secret)

**Implementation**:
```typescript
// Frontend (Better Auth)
jwt.sign(payload, process.env.BETTER_AUTH_SECRET, { algorithm: 'HS256' });
```

```python
# Backend (PyJWT)
jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

**Alternatives Considered**:
- RS256: Rejected (unnecessary complexity for single backend)
- ES256 (ECDSA): Rejected (less common, library support varies)
- HS512: Rejected (no significant security benefit over HS256)

**Security Requirements**:
- BETTER_AUTH_SECRET must be 32+ characters
- Secret must be cryptographically random (not dictionary words)
- Secret must be stored in environment variables (never committed)
- Secret rotation procedure documented

---

## Summary of Decisions

| Decision | Chosen Approach | Rationale |
|----------|----------------|-----------|
| Better Auth Integration | Server-side config + fallback to custom JWT | Pragmatic approach given feature 002 issues |
| JWT Token Structure | user_id, email, iat, exp (minimal payload) | Balances functionality with token size |
| Authentication Enforcement | Middleware with path-based exclusions | Centralized, consistent, fail-secure |
| Token Storage | localStorage (dev) → httpOnly cookies (prod) | Rapid development, secure production |
| User Isolation | Middleware extraction + route validation | Centralized + granular enforcement |
| Password Requirements | 8 chars min, number + letter | Balances security with UX |
| JWT Algorithm | HS256 with shared secret | Simple, fast, adequate for single backend |

## Implementation Risks

1. **Better Auth Compatibility**: May need fallback to custom JWT implementation
   - Mitigation: Test early, prepare custom implementation

2. **Token Storage Security**: localStorage vulnerable to XSS
   - Mitigation: Migrate to httpOnly cookies before production, implement CSP

3. **7-day Token Expiration**: Long window for token theft/misuse
   - Mitigation: Document tradeoff, plan refresh tokens for future

4. **No Token Revocation**: Compromised tokens valid until expiration
   - Mitigation: Document limitation, monitor for abuse, plan blacklist for future

## Next Steps

1. Implement Better Auth server-side configuration
2. Create User model and database migration
3. Implement JWT middleware in FastAPI
4. Test end-to-end authentication flow
5. Document security considerations in README
