# Quickstart: Better Auth JWT Authentication Integration

**Feature**: 003-better-auth-jwt
**Date**: 2026-01-10
**Status**: Complete

## Overview

This quickstart guide provides integration scenarios for implementing JWT-based authentication using Better Auth (Next.js) and PyJWT (FastAPI). Follow these scenarios to integrate authentication into your application.

## Prerequisites

- Node.js 18+ and npm installed
- Python 3.11+ and pip installed
- PostgreSQL database (Neon DB) accessible
- Environment variables configured (.env files)

## Quick Setup

### 1. Install Dependencies

**Frontend (Next.js)**:
```bash
cd frontend
npm install better-auth
```

**Backend (FastAPI)**:
```bash
cd backend
pip install pyjwt bcrypt
```

### 2. Configure Environment Variables

**Frontend (.env.local)**:
```env
BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-in-production
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env)**:
```env
BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-in-production
DATABASE_URL=postgresql://user:password@host:port/database
FRONTEND_URL=http://localhost:3000
```

**Important**: Use the same `BETTER_AUTH_SECRET` in both services!

### 3. Generate Secret Key

```bash
# Generate cryptographically secure secret (32+ characters)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Integration Scenarios

### Scenario 1: User Signup

**Goal**: Allow new users to create an account and receive a JWT token.

**Frontend Implementation** (`app/signup/page.tsx`):

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, username }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Signup failed');
      }

      const data = await response.json();

      // Store token in localStorage (development)
      localStorage.setItem('token', data.access_token);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password (min 8 chars)"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        minLength={8}
      />
      <input
        type="text"
        placeholder="Username (optional)"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      {error && <p className="error">{error}</p>}
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

**Backend Implementation** (`app/routers/auth.py`):

```python
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os

from app.models.user import User
from app.schemas.user import UserCreate, TokenResponse, UserResponse
from app.dependencies.database import get_session

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

@router.post("/signup", response_model=TokenResponse, status_code=201)
async def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email.lower())
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(user_data.password)

    # Create user
    user = User(
        email=user_data.email.lower(),
        hashed_password=hashed_password,
        username=user_data.username
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate JWT token
    payload = {
        "user_id": user.id,
        "email": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )
```

**Expected Result**:
- User account created in database
- JWT token returned with 7-day expiration
- User redirected to dashboard

---

### Scenario 2: User Signin

**Goal**: Allow existing users to authenticate and receive a JWT token.

**Frontend Implementation** (`app/login/page.tsx`):

```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();

      // Store token in localStorage (development)
      localStorage.setItem('token', data.access_token);

      // Redirect to dashboard
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      {error && <p className="error">{error}</p>}
      <button type="submit">Sign In</button>
    </form>
  );
}
```

**Backend Implementation** (`app/routers/auth.py`):

```python
@router.post("/signin", response_model=TokenResponse)
async def signin(credentials: UserLogin, session: Session = Depends(get_session)):
    # Query user by email
    user = session.exec(
        select(User).where(User.email == credentials.email.lower())
    ).first()

    # Verify user exists and password is correct
    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Account is inactive")

    # Generate JWT token
    payload = {
        "user_id": user.id,
        "email": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )
```

**Expected Result**:
- User credentials verified
- JWT token returned with 7-day expiration
- User redirected to dashboard

---

### Scenario 3: Protected API Access

**Goal**: Make authenticated API requests with JWT token.

**Frontend Implementation** (`lib/api/client.ts`):

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: Add JWT token to all requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;

// Example usage: Get user's tasks
export async function getTasks(userId: string) {
  const response = await apiClient.get(`/api/users/${userId}/tasks`);
  return response.data;
}
```

**Backend Implementation** (`app/middleware/auth.py`):

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
import jwt
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude public paths
        public_paths = ["/health", "/ready", "/docs", "/openapi.json", "/api/auth/"]
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Require JWT for all other /api/* endpoints
        if request.url.path.startswith("/api/"):
            # Extract token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {"detail": "Authentication required"},
                    status_code=401
                )

            token = auth_header.replace("Bearer ", "")

            try:
                # Verify token
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                request.state.user = payload
            except jwt.ExpiredSignatureError:
                return JSONResponse(
                    {"detail": "Token has expired"},
                    status_code=401
                )
            except jwt.InvalidTokenError:
                return JSONResponse(
                    {"detail": "Invalid token"},
                    status_code=401
                )

        return await call_next(request)
```

**Register Middleware** (`app/main.py`):

```python
from fastapi import FastAPI
from app.middleware.auth import JWTAuthMiddleware

app = FastAPI()

# Add JWT authentication middleware
app.add_middleware(JWTAuthMiddleware)

# Register routers
from app.routers import auth, tasks
app.include_router(auth.router)
app.include_router(tasks.router)
```

**Expected Result**:
- All /api/* requests include Authorization header
- Middleware verifies token before reaching route handlers
- Invalid/expired tokens return 401 error
- Valid tokens allow request to proceed

---

### Scenario 4: User Isolation Enforcement

**Goal**: Ensure users can only access their own data.

**Backend Implementation** (`app/dependencies/auth.py`):

```python
from fastapi import Request, HTTPException

def get_current_user(request: Request) -> dict:
    """Extract current user from request state (set by middleware)."""
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Authentication required")
    return request.state.user

def validate_user_access(current_user: dict, user_id: str):
    """Validate that JWT user_id matches URL user_id parameter."""
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: cannot access other users' resources"
        )
```

**Route Implementation** (`app/routers/tasks.py`):

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.task import Task
from app.dependencies.auth import get_current_user, validate_user_access
from app.dependencies.database import get_session

router = APIRouter(prefix="/api/users/{user_id}/tasks", tags=["Tasks"])

@router.get("/")
async def get_tasks(
    user_id: str,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Validate user can access this resource
    validate_user_access(current_user, user_id)

    # Query tasks filtered by user_id
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()

    return tasks
```

**Expected Result**:
- User A can access their own tasks (user_id matches JWT)
- User A cannot access User B's tasks (403 Forbidden)
- All queries automatically filtered by user_id

---

## Testing Integration

### Test Signup Flow

```bash
# Test signup
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "username": "Test User"
  }'

# Expected response:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "user": {
#     "id": "550e8400-e29b-41d4-a716-446655440000",
#     "email": "test@example.com",
#     "username": "Test User",
#     "is_active": true,
#     "created_at": "2026-01-10T12:00:00Z"
#   }
# }
```

### Test Signin Flow

```bash
# Test signin
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Expected response: Same as signup
```

### Test Protected Endpoint

```bash
# Get user's tasks (with token)
curl -X GET http://localhost:8000/api/users/550e8400-e29b-41d4-a716-446655440000/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Expected response: Array of tasks

# Try to access another user's tasks (should fail)
curl -X GET http://localhost:8000/api/users/different-user-id/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Expected response: 403 Forbidden
```

---

## Common Issues & Troubleshooting

### Issue 1: "BETTER_AUTH_SECRET not set"

**Symptom**: Application fails to start or token generation fails

**Solution**:
1. Ensure `.env` and `.env.local` files exist
2. Verify `BETTER_AUTH_SECRET` is set in both files
3. Use the same secret in both frontend and backend
4. Restart both services after changing environment variables

### Issue 2: "Invalid token signature"

**Symptom**: 401 error when making authenticated requests

**Solution**:
1. Verify `BETTER_AUTH_SECRET` is identical in frontend and backend
2. Check token is being sent in correct format: `Authorization: Bearer <token>`
3. Ensure token hasn't expired (7-day expiration)
4. Verify token is being stored and retrieved correctly

### Issue 3: "Access denied: cannot access other users' resources"

**Symptom**: 403 error when accessing own resources

**Solution**:
1. Verify JWT `user_id` matches URL `user_id` parameter
2. Check user_id format (should be UUID string)
3. Ensure middleware is extracting user correctly from token
4. Verify route is using correct user_id from authenticated user

### Issue 4: "Token has expired"

**Symptom**: 401 error after 7 days

**Solution**:
1. User must sign in again to get new token
2. Implement token refresh mechanism (future enhancement)
3. Consider shorter expiration with refresh tokens

### Issue 5: Better Auth import errors

**Symptom**: Build fails with "Export betterAuth doesn't exist"

**Solution**:
1. Use custom JWT implementation instead of Better Auth client
2. Generate tokens manually using `jsonwebtoken` npm package
3. Follow feature 002 approach (direct API calls)

---

## Next Steps

1. **Implement Signup/Signin UI**: Create forms with validation
2. **Add JWT Middleware**: Implement token verification in FastAPI
3. **Update Protected Routes**: Add authentication to all /api/* endpoints
4. **Test End-to-End**: Verify signup → signin → protected access flow
5. **Migrate to httpOnly Cookies**: Replace localStorage before production
6. **Add Rate Limiting**: Prevent brute force attacks on auth endpoints
7. **Implement Logging**: Audit all authentication events

---

## Security Checklist

Before deploying to production:

- [ ] BETTER_AUTH_SECRET is strong (32+ characters, cryptographically random)
- [ ] Secrets are in .env files, not committed to git
- [ ] Passwords are hashed with bcrypt (cost factor 12+)
- [ ] JWT tokens are signed with HS256
- [ ] Token expiration is set to 7 days
- [ ] 401/403 responses are appropriate (don't leak info)
- [ ] User ID validation prevents cross-user access
- [ ] CORS allows only trusted origins
- [ ] HTTPS enforced in production (TLS 1.3)
- [ ] Rate limiting enabled on auth endpoints
- [ ] Tokens stored in httpOnly cookies (not localStorage)
- [ ] Content Security Policy (CSP) headers configured

---

## Additional Resources

- **OpenAPI Specification**: See `contracts/auth-api.yaml`
- **JWT Schema**: See `contracts/jwt-schema.json`
- **Data Model**: See `data-model.md`
- **Research Decisions**: See `research.md`
- **Implementation Plan**: See `plan.md`
