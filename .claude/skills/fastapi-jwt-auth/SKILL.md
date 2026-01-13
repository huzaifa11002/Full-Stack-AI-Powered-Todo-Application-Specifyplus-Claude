---
name: fastapi-jwt-auth
description: Secure FastAPI REST APIs using Better Auth issued JWT tokens. Use when implementing authentication, authorization, and user isolation.
---

# FastAPI JWT Authentication with Better Auth

## Instructions
Implement JWT-based authentication with the following requirements:

### 1. **JWT Verification**
- Read token from `Authorization: Bearer <token>`
- Verify signature using shared `BETTER_AUTH_SECRET`
- Validate token expiry (`exp`)
- Reject invalid or missing tokens with `401 Unauthorized`

### 2. **Auth Middleware / Dependency**
- Decode JWT once per request
- Extract user info (id, email)
- Attach authenticated user to request context

### 3. **User Isolation**
- Never accept user ID from request body or query
- Always use user ID from decoded JWT
- Filter all database queries by authenticated user ID
- Enforce task ownership on:
  - Create
  - Read
  - Update
  - Delete

### 4. **Stateless Security**
- No backend session storage
- No frontend verification calls
- Backend independently verifies JWT

### 5. **Environment Configuration**
- Use `BETTER_AUTH_SECRET` in:
  - Next.js (Better Auth)
  - FastAPI backend
- Secret must match exactly in both services

## Example FastAPI Dependency
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(
        token,
        os.environ["BETTER_AUTH_SECRET"],
        algorithms=["HS256"]
    )
    return payload["user_id"]
