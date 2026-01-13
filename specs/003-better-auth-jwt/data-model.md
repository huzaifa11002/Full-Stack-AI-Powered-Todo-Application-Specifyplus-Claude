# Data Model: Better Auth JWT Authentication Integration

**Feature**: 003-better-auth-jwt
**Date**: 2026-01-10
**Status**: Complete

## Overview

This document defines the data entities for JWT-based authentication. The system uses two primary entities: User (stored in database) and JWT Token (ephemeral, not stored).

## Entities

### 1. User

**Purpose**: Represents an authenticated user account with credentials and profile information.

**Storage**: PostgreSQL database (Neon DB) via SQLModel

**Lifecycle**: Created on signup, persists indefinitely (no deletion in MVP)

**Schema**:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    """User account with authentication credentials."""

    __tablename__ = "users"

    # Primary Key
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Unique user identifier (UUID)"
    )

    # Authentication
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address (unique, used for login)"
    )

    hashed_password: str = Field(
        max_length=255,
        description="Bcrypt-hashed password (never store plain text)"
    )

    # Profile (Optional)
    username: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Display name (optional)"
    )

    # Status
    is_active: bool = Field(
        default=True,
        description="Account active status (for future account suspension)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )
```

**Validation Rules**:
- `email`: Must be valid email format (validated by Pydantic)
- `email`: Must be unique (database constraint)
- `hashed_password`: Must be bcrypt hash (never plain text)
- `username`: Optional, max 50 characters
- `id`: UUID v4 format (auto-generated)

**Indexes**:
- Primary key: `id` (UUID)
- Unique index: `email` (for login lookups)
- Index: `id` (for foreign key relationships)

**Relationships**:
- One-to-Many with Task: `User.id` → `Task.user_id`

**State Transitions**:
```
[New User] --signup--> [Active User]
[Active User] --future: suspend--> [Inactive User]
[Inactive User] --future: reactivate--> [Active User]
```

**Security Considerations**:
- Password must be hashed with bcrypt (cost factor 12+)
- Never return `hashed_password` in API responses
- Email is case-insensitive for login (normalize to lowercase)
- UUID prevents user enumeration attacks

---

### 2. JWT Token

**Purpose**: Represents an authentication token for API access.

**Storage**: NOT stored in database (stateless authentication)

**Lifecycle**: Generated on signup/signin, expires after 7 days

**Structure**:

```typescript
interface JWTToken {
  // Header (automatically added by JWT library)
  header: {
    alg: "HS256",           // Algorithm: HMAC with SHA-256
    typ: "JWT"              // Type: JSON Web Token
  },

  // Payload (custom claims)
  payload: {
    user_id: string,        // User UUID from database
    email: string,          // User email address
    iat: number,            // Issued at (Unix timestamp)
    exp: number             // Expiration (Unix timestamp, iat + 7 days)
  },

  // Signature (automatically added by JWT library)
  signature: string         // HMAC-SHA256(header + payload, BETTER_AUTH_SECRET)
}
```

**Example Token**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1704931200,
  "exp": 1705536000
}
```

**Encoded Format**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAwIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNzA0OTMxMjAwLCJleHAiOjE3MDU1MzYwMDB9.signature
```

**Validation Rules**:
- `user_id`: Must be valid UUID matching database User.id
- `email`: Must match User.email in database
- `iat`: Must be valid Unix timestamp (not in future)
- `exp`: Must be iat + 604800 seconds (7 days)
- `signature`: Must be valid HMAC-SHA256 signature

**Security Considerations**:
- Signed with BETTER_AUTH_SECRET (32+ characters)
- Cannot be modified without invalidating signature
- Expiration enforced by PyJWT verification
- No sensitive data in payload (email is not sensitive)
- Token size: ~200-300 bytes (well under 1KB limit)

**Transmission**:
- Client → Server: `Authorization: Bearer <token>` header
- Server → Client: JSON response body on signup/signin

**Storage** (Client-side):
- Development: localStorage
- Production: httpOnly cookies

---

### 3. Task (Existing Entity - Modified)

**Purpose**: Represents a user's todo item.

**Storage**: PostgreSQL database (Neon DB) via SQLModel

**Modifications**: Add foreign key relationship to User

**Schema**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """User's todo task."""

    __tablename__ = "tasks"

    # Primary Key
    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier"
    )

    # Foreign Key (NEW)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner user ID (UUID)"
    )

    # Task Data
    title: str = Field(
        max_length=200,
        description="Task title"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional)"
    )

    is_completed: bool = Field(
        default=False,
        description="Completion status"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )

    # Relationship (NEW)
    user: Optional["User"] = Relationship(back_populates="tasks")
```

**Validation Rules**:
- `user_id`: Must reference existing User.id (foreign key constraint)
- `title`: Required, max 200 characters
- `description`: Optional, max 1000 characters

**Indexes**:
- Primary key: `id`
- Foreign key index: `user_id` (for efficient user task queries)

**User Isolation**:
- All queries MUST filter by `user_id` from JWT token
- Users can only access their own tasks
- Enforced by middleware + route validation

---

## Relationships

```
User (1) ----< (N) Task
  id              user_id
```

**Relationship Type**: One-to-Many

**Cardinality**:
- One User can have zero or many Tasks
- One Task belongs to exactly one User

**Referential Integrity**:
- Foreign key constraint: `Task.user_id` → `User.id`
- On User delete: CASCADE (future enhancement, not in MVP)

---

## Database Migration

**Migration**: Add User table and modify Task table

**Alembic Migration Script**:

```python
"""Add User table and user_id to Task

Revision ID: xxx_add_user_table
Revises: previous_revision
Create Date: 2026-01-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'xxx_add_user_table'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_email', 'users', ['email'])

    # Add user_id column to tasks table
    op.add_column('tasks', sa.Column('user_id', sa.String(), nullable=True))

    # Create foreign key constraint (after backfilling data)
    # Note: In production, backfill existing tasks with a default user_id first
    op.create_foreign_key(
        'fk_tasks_user_id',
        'tasks', 'users',
        ['user_id'], ['id']
    )
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'])

def downgrade():
    # Remove foreign key and index from tasks
    op.drop_index('ix_tasks_user_id', 'tasks')
    op.drop_constraint('fk_tasks_user_id', 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')

    # Drop users table
    op.drop_index('ix_users_email', 'users')
    op.drop_index('ix_users_id', 'users')
    op.drop_table('users')
```

**Migration Notes**:
- Existing tasks will need user_id backfilled (create default user or assign to first user)
- Foreign key constraint added after backfilling
- Indexes created for performance (email lookups, user task queries)

---

## Pydantic Schemas

**Purpose**: API request/response validation and serialization

### UserCreate (Request)

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """User signup request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 chars)")
    username: Optional[str] = Field(None, max_length=50, description="Display name (optional)")
```

### UserLogin (Request)

```python
class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
```

### UserResponse (Response)

```python
class UserResponse(BaseModel):
    """User data response (no password)."""
    id: str = Field(..., description="User UUID")
    email: str = Field(..., description="User email address")
    username: Optional[str] = Field(None, description="Display name")
    is_active: bool = Field(..., description="Account active status")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True  # Enable ORM mode
```

### TokenResponse (Response)

```python
class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    user: UserResponse = Field(..., description="User data")
```

---

## Data Flow

### Signup Flow

```
1. Client sends UserCreate (email, password, username)
2. Backend validates email format and uniqueness
3. Backend hashes password with bcrypt
4. Backend creates User record in database
5. Backend generates JWT token with user_id and email
6. Backend returns TokenResponse (token + user data)
7. Client stores token in localStorage/cookie
```

### Signin Flow

```
1. Client sends UserLogin (email, password)
2. Backend queries User by email
3. Backend verifies password against hashed_password
4. Backend generates JWT token with user_id and email
5. Backend returns TokenResponse (token + user data)
6. Client stores token in localStorage/cookie
```

### Protected API Request Flow

```
1. Client sends request with Authorization: Bearer <token>
2. Middleware extracts token from header
3. Middleware verifies token signature with BETTER_AUTH_SECRET
4. Middleware decodes token payload (user_id, email)
5. Middleware attaches user data to request.state
6. Route handler validates user_id matches URL parameter
7. Route handler queries database filtered by user_id
8. Route handler returns response
```

---

## Summary

**Entities**:
- User: Stored in database, represents user account
- JWT Token: Ephemeral, represents authentication session
- Task: Stored in database, belongs to User

**Key Relationships**:
- User (1) → Task (N)

**Security**:
- Passwords hashed with bcrypt (never plain text)
- JWT tokens signed with HS256 (HMAC-SHA256)
- User isolation enforced via user_id validation
- No sensitive data in JWT payload

**Next Steps**:
1. Create User model in `backend/app/models/user.py`
2. Create Pydantic schemas in `backend/app/schemas/user.py`
3. Generate Alembic migration for User table
4. Update Task model with user_id foreign key
5. Test database schema and relationships
