# Data Model: FastAPI Todo REST API

**Feature**: 001-fastapi-todo-api
**Date**: 2026-01-10
**Purpose**: Entity definitions, relationships, and validation rules

## Overview

This document defines the data model for the FastAPI Todo REST API. The model consists of two primary entities: User and Task, with a one-to-many relationship (one user has many tasks).

## Entity Definitions

### User Entity

**Purpose**: Represents a user in the system who owns tasks. This entity establishes the foundation for user isolation but does not include authentication credentials (handled in Spec 2).

**Table Name**: `users`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier for the user |
| email | String(255) | UNIQUE, NOT NULL | User's email address (unique across system) |
| username | String(100) | NOT NULL | User's display name |
| created_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when user was created |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` (automatic from UNIQUE constraint)

**Validation Rules**:
- `email`: Must be valid email format (enforced by Pydantic)
- `email`: Must be unique across all users
- `username`: Cannot be empty or whitespace-only
- `created_at`: Automatically set on creation, immutable

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    username: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Sample Data**:
```json
{
  "id": 1,
  "email": "user1@example.com",
  "username": "user1",
  "created_at": "2026-01-10T10:00:00Z"
}
```

**Notes**:
- No password field (authentication deferred to Spec 2)
- No profile information (name, avatar, etc.) - minimal user entity for Phase II
- Users will be pre-seeded for testing purposes

---

### Task Entity

**Purpose**: Represents a todo item belonging to a user. Tasks are isolated by user - each task belongs to exactly one user.

**Table Name**: `tasks`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique identifier for the task |
| user_id | Integer | FOREIGN KEY → users.id, NOT NULL | ID of the user who owns this task |
| title | String(200) | NOT NULL | Task title/summary |
| description | String(2000) | NULLABLE | Optional detailed description |
| is_completed | Boolean | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when task was created |
| updated_at | DateTime | NOT NULL, DEFAULT NOW | Timestamp when task was last updated |

**Indexes**:
- Primary key index on `id` (automatic)
- Foreign key index on `user_id` (automatic)
- Composite index on `(user_id, created_at)` for efficient user task queries

**Validation Rules**:
- `title`: Cannot be empty or whitespace-only
- `title`: Maximum 200 characters
- `description`: Optional, maximum 2000 characters if provided
- `user_id`: Must reference an existing user (foreign key constraint)
- `is_completed`: Defaults to false on creation
- `created_at`: Automatically set on creation, immutable
- `updated_at`: Automatically set on creation, updated on modification

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=2000)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Sample Data**:
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and vegetables",
  "is_completed": false,
  "created_at": "2026-01-10T10:00:00Z",
  "updated_at": "2026-01-10T10:00:00Z"
}
```

**Notes**:
- Hard delete (no soft delete flag)
- No categories, tags, priorities, or due dates (out of scope for Phase II)
- No task sharing or collaboration features

---

## Relationships

### User → Tasks (One-to-Many)

**Type**: One-to-Many
**Direction**: User has many Tasks
**Foreign Key**: `tasks.user_id` → `users.id`

**Relationship Properties**:
- **Cardinality**: One user can have zero or many tasks
- **Cascade**: ON DELETE CASCADE (when user deleted, all their tasks deleted)
- **Referential Integrity**: Enforced by database foreign key constraint

**SQLModel Relationship**:
```python
# In User model
tasks: list["Task"] = Relationship(back_populates="user")

# In Task model
user: Optional[User] = Relationship(back_populates="tasks")
```

**Query Examples**:
```python
# Get all tasks for a user
user = session.get(User, user_id)
tasks = user.tasks

# Get user from task
task = session.get(Task, task_id)
owner = task.user
```

---

## State Transitions

### Task Completion State

**States**:
- `is_completed = False` (default): Task is pending/active
- `is_completed = True`: Task is completed

**Transitions**:
1. **Create**: New task starts with `is_completed = False`
2. **Toggle**: PATCH endpoint toggles between False ↔ True
3. **Update**: PUT endpoint can set `is_completed` to any value
4. **Delete**: Task removed from database (no state transition)

**State Diagram**:
```
[Created] → is_completed = False
    ↓
[Toggle/Update] ↔ is_completed = True
    ↓
[Delete] → Removed from database
```

**Business Rules**:
- No validation on state transitions (can toggle freely)
- No history of state changes (out of scope)
- Completion status does not affect other operations

---

## Validation Rules Summary

### User Validation

**Field-Level**:
- `email`: Valid email format, unique, max 255 chars
- `username`: Not empty, max 100 chars
- `created_at`: Auto-generated, immutable

**Entity-Level**:
- Email must be unique across all users
- All required fields must be present

### Task Validation

**Field-Level**:
- `title`: Not empty/whitespace, 1-200 chars
- `description`: Optional, max 2000 chars if provided
- `user_id`: Must reference existing user
- `is_completed`: Boolean (true/false)
- `created_at`: Auto-generated, immutable
- `updated_at`: Auto-generated, updated on modification

**Entity-Level**:
- Task must belong to a valid user
- Title cannot be only whitespace
- All required fields must be present

**API-Level** (enforced by Pydantic schemas):
- Request validation before database operations
- Response serialization with proper types
- Automatic 422 errors for invalid data

---

## Database Schema SQL

### Create Tables

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description VARCHAR(2000),
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at);
```

### Seed Data

```sql
-- Sample users
INSERT INTO users (email, username, created_at) VALUES
    ('user1@example.com', 'user1', NOW()),
    ('user2@example.com', 'user2', NOW()),
    ('user3@example.com', 'user3', NOW());

-- Sample tasks for user 1
INSERT INTO tasks (user_id, title, description, is_completed, created_at, updated_at) VALUES
    (1, 'Buy groceries', 'Milk, eggs, bread, and vegetables', FALSE, NOW(), NOW()),
    (1, 'Write report', 'Q4 financial report for management', FALSE, NOW(), NOW()),
    (1, 'Call dentist', 'Schedule annual checkup', FALSE, NOW(), NOW());

-- Sample tasks for user 2
INSERT INTO tasks (user_id, title, description, is_completed, created_at, updated_at) VALUES
    (2, 'Review PR', 'Review pull request #123 for authentication feature', FALSE, NOW(), NOW()),
    (2, 'Update documentation', 'Add API examples to README', TRUE, NOW(), NOW());
```

---

## Data Integrity Constraints

### Database-Level Constraints

1. **Primary Keys**: Ensure unique identification
   - `users.id` (auto-increment)
   - `tasks.id` (auto-increment)

2. **Foreign Keys**: Maintain referential integrity
   - `tasks.user_id` → `users.id` (ON DELETE CASCADE)

3. **Unique Constraints**: Prevent duplicates
   - `users.email` (unique across all users)

4. **Not Null Constraints**: Ensure required data
   - All fields except `tasks.description` are NOT NULL

5. **Check Constraints** (optional, enforced by application):
   - `title` length > 0
   - `email` valid format

### Application-Level Constraints

1. **Pydantic Validation**: Request/response validation
2. **SQLModel Field Constraints**: max_length, min_length
3. **Business Logic**: User isolation, timestamp management

---

## Performance Considerations

### Indexing Strategy

**Primary Indexes** (automatic):
- `users.id` (primary key)
- `tasks.id` (primary key)
- `users.email` (unique constraint)

**Foreign Key Indexes** (automatic):
- `tasks.user_id` (foreign key)

**Composite Indexes** (recommended):
- `(user_id, created_at)` on tasks table for efficient user task queries

### Query Optimization

**Common Queries**:
1. Get all tasks for user: `SELECT * FROM tasks WHERE user_id = ?`
   - Uses index on `user_id`
   - Expected: <10ms for 1000 tasks

2. Get single task: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`
   - Uses primary key index
   - Expected: <5ms

3. Count user tasks: `SELECT COUNT(*) FROM tasks WHERE user_id = ?`
   - Uses index on `user_id`
   - Expected: <5ms

**Optimization Notes**:
- No N+1 query problems (single query per endpoint)
- Connection pooling handles concurrent requests
- Indexes cover all WHERE clauses

---

## Migration Strategy

### Initial Setup (Phase II)

**Approach**: Manual table creation via `init_db.py` script

**Steps**:
1. Create tables using SQLModel.metadata.create_all()
2. Seed sample users
3. Verify schema with database inspection

### Future Migrations (Post-Phase II)

**Approach**: Alembic for schema changes

**Setup**:
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

**Migration Tracking**:
- All schema changes tracked in version control
- Reversible migrations for rollback capability
- Tested in development before production

---

## Data Model Evolution

### Phase II (Current)
- Basic User and Task entities
- Integer IDs
- Hard delete
- No authentication fields

### Future Phases (Planned)

**Spec 2 (Authentication)**:
- Add password_hash to User
- Add refresh_token table
- Add last_login timestamp

**Spec 3 (Frontend)**:
- No data model changes (consumes existing API)

**Spec 4 (Advanced Features)**:
- Add task categories, tags, priorities
- Add due dates and reminders
- Add task sharing/collaboration

**Production Enhancements**:
- Migrate to UUID IDs
- Add soft delete (is_deleted flag)
- Add audit trail (task history)
- Add pagination metadata

---

## References

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [Database Normalization](https://en.wikipedia.org/wiki/Database_normalization)
- [Foreign Key Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
