# Implementation Plan: FastAPI Todo REST API

**Branch**: `001-fastapi-todo-api` | **Date**: 2026-01-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fastapi-todo-api/spec.md`

## Summary

Build a FastAPI REST API with Neon PostgreSQL for multi-user todo application. The API provides 6 CRUD endpoints with user isolation, SQLModel ORM for type-safe database operations, and Pydantic validation for all requests/responses. This is Phase II of the full-stack AI-powered todo application, establishing the backend foundation for future authentication and frontend integration.

**Primary Requirement**: RESTful API with complete CRUD operations for tasks, enforcing user isolation at the API level via `/api/{user_id}/tasks/*` pattern.

**Technical Approach**: Python FastAPI framework with SQLModel ORM connecting to Neon Serverless PostgreSQL. Dependency injection for database sessions, Pydantic models for validation, and proper HTTP status codes for all scenarios.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (latest stable), SQLModel, Pydantic v2, psycopg2-binary, python-dotenv, uvicorn[standard]
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, PostgreSQL-compatible)
**Testing**: Manual testing with Postman/Thunder Client (automated tests deferred to future phase)
**Target Platform**: Development server (local), HTTP endpoint accessible via localhost
**Project Type**: Web application (backend only for this phase)
**Performance Goals**: <500ms response time for all endpoints under normal load, support 100 concurrent requests
**Constraints**: Must use Neon cloud database (no local PostgreSQL), API structure `/api/{user_id}/tasks/*` strictly enforced, JSON-only responses
**Scale/Scope**: Support 1000+ tasks per user without performance degradation, pre-seeded users for testing

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Production-Ready Code Quality ✅
- **Type Safety**: Python type hints for all function signatures (SQLModel provides this)
- **Testing**: Manual testing for this phase; 70% coverage target deferred to future phase
- **Linting**: Ruff configured for Python linting and formatting
- **Documentation**: Architectural decisions documented in code comments

**Status**: PASS - Type safety via SQLModel/Pydantic, linting configured, testing strategy defined

### Cloud-Native Architecture ⚠️
- **Containerization**: Deferred to Phase IV (Kubernetes deployment)
- **Health Checks**: `/health` endpoint to be added in Phase 7
- **Graceful Shutdown**: SIGTERM handling to be implemented
- **Externalized Config**: Environment variables via .env file ✅
- **Stateless**: API is stateless, all state in Neon DB ✅

**Status**: PARTIAL - Core requirements met (stateless, env config), containerization deferred per project phases

### Security-First Approach ⚠️
- **Secrets Management**: Environment variables for DB credentials ✅
- **JWT Authentication**: Deferred to Spec 2 (explicitly out of scope)
- **Rate Limiting**: Deferred to future phase (explicitly out of scope)
- **Input Validation**: Pydantic models for all requests ✅
- **Parameterized Queries**: SQLModel uses parameterized queries ✅
- **CORS**: Basic CORS middleware for frontend integration ✅

**Status**: PARTIAL - Input validation and secure queries implemented, auth/rate limiting deferred per spec

### Database & Data Management ✅
- **SQLModel**: All models use SQLModel for type safety ✅
- **Migrations**: Alembic for schema changes (manual for initial setup) ✅
- **Connection Pooling**: SQLModel engine with default pooling ✅
- **Indexing**: Foreign keys and primary keys indexed by default ✅
- **Validation**: Pydantic models at API boundary ✅

**Status**: PASS - All database requirements met

### Developer Experience ✅
- **README**: Setup instructions to be documented ✅
- **Local Development**: Python venv, no Kubernetes required ✅
- **Environment Config**: .env template provided ✅
- **Documentation**: API endpoints documented in quickstart.md ✅

**Status**: PASS - All developer experience requirements met

### Overall Gate Status: ✅ PASS WITH JUSTIFIED DEFERRALS

**Justification for Deferrals**:
- Containerization (Phase IV): Project follows phased approach, Phase II focuses on API foundation
- JWT Authentication (Spec 2): Explicitly scoped to separate specification
- Rate Limiting: Explicitly out of scope for this specification
- Automated Testing: Manual testing sufficient for Phase II, automated tests in future phase

## Project Structure

### Documentation (this feature)

```text
specs/001-fastapi-todo-api/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entity models)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   └── openapi.yaml     # OpenAPI 3.0 specification
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # Database engine and session management
│   ├── models.py        # SQLModel database models (User, Task)
│   ├── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── __init__.py
│       └── tasks.py     # Task CRUD endpoints
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment variables template
├── .gitignore           # Python gitignore
├── requirements.txt     # Python dependencies
├── init_db.py           # Database initialization script
└── README.md            # Setup and usage instructions
```

**Structure Decision**: Web application structure (backend only) selected because this is Phase II of a full-stack application. Frontend will be added in Phase III. The `backend/` directory contains all API code with clear separation: `models.py` for database entities, `schemas.py` for API contracts, `routers/` for endpoint logic, and `database.py` for connection management.

## Complexity Tracking

> No constitution violations requiring justification. All deferrals are explicitly scoped per project phases.

## Phase 0: Research & Technology Decisions

### Research Topics

1. **SQLModel vs SQLAlchemy + Pydantic**
   - **Decision**: Use SQLModel
   - **Rationale**: SQLModel combines SQLAlchemy and Pydantic, providing type-safe ORM with automatic Pydantic model generation. Reduces boilerplate and ensures consistency between database models and API schemas.
   - **Alternatives Considered**:
     - Pure SQLAlchemy + separate Pydantic models (more boilerplate, potential inconsistencies)
     - Tortoise ORM (less mature, smaller ecosystem)

2. **User ID Type: Integer vs UUID**
   - **Decision**: Use Integer for Phase II
   - **Rationale**: Simpler for development and testing, sequential IDs easier to work with in manual testing. UUID can be migrated to in future phase for production security.
   - **Alternatives Considered**:
     - UUID (more secure, harder to guess, but more complex for testing)
     - String (flexible but no type safety benefits)

3. **Database Migration Strategy**
   - **Decision**: Manual table creation for Phase II, Alembic for future migrations
   - **Rationale**: Initial schema is simple (2 tables), manual creation is faster for MVP. Alembic will be configured for future schema changes.
   - **Alternatives Considered**:
     - Alembic from start (overhead for simple initial schema)
     - SQLModel.metadata.create_all() only (no migration tracking)

4. **Timestamp Handling**
   - **Decision**: Application-level timestamps with SQLModel default_factory
   - **Rationale**: Provides control over timestamp generation, consistent with Python datetime handling, easier to test.
   - **Alternatives Considered**:
     - Database-level defaults (less control, database-specific syntax)
     - Manual timestamp setting (error-prone, inconsistent)

5. **Error Response Format**
   - **Decision**: FastAPI default HTTPException with detail field
   - **Rationale**: Standard FastAPI pattern, consistent with framework conventions, automatic OpenAPI documentation.
   - **Alternatives Considered**:
     - Custom exception handler with structured error format (unnecessary complexity for Phase II)
     - Problem Details (RFC 7807) format (overkill for simple API)

6. **Soft Delete vs Hard Delete**
   - **Decision**: Hard delete for Phase II
   - **Rationale**: Simpler implementation, meets current requirements. Soft delete can be added in future phase if needed.
   - **Alternatives Considered**:
     - Soft delete with is_deleted flag (added complexity, not required by spec)

7. **Task Description Field Constraints**
   - **Decision**: Optional field, 2000 character limit
   - **Rationale**: Aligns with spec assumptions, provides flexibility while preventing abuse.
   - **Alternatives Considered**:
     - Required field (too restrictive for quick task creation)
     - No limit (potential for abuse, database bloat)

8. **User Validation Strategy**
   - **Decision**: Assume valid user_id for Phase II
   - **Rationale**: Authentication in Spec 2 will validate users. For Phase II, pre-seeded users sufficient for testing.
   - **Alternatives Considered**:
     - Check user exists on every request (performance overhead, redundant with future auth)
     - Foreign key constraint only (database-level validation sufficient)

### Best Practices Research

**FastAPI Project Structure**:
- Separate routers for different resource types
- Dependency injection for database sessions
- Pydantic models for request/response validation
- Centralized error handling

**SQLModel Patterns**:
- Use `Optional[type]` for nullable fields
- Define relationships with `Relationship()` for type safety
- Use `Field()` for constraints and metadata
- Separate table models from API models when needed

**Neon PostgreSQL**:
- Connection string format: `postgresql://user:password@host/database?sslmode=require`
- Connection pooling handled by SQLModel engine
- SSL required for Neon connections

**API Design**:
- RESTful resource naming (plural nouns)
- Proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Consistent status codes (200, 201, 204, 404, 400, 422, 500)
- JSON responses with consistent structure

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete entity definitions.

**Summary**:
- **User**: id (int), email (str, unique), username (str), created_at (datetime)
- **Task**: id (int), user_id (int, FK), title (str, max 200), description (str, max 2000, optional), is_completed (bool), created_at (datetime), updated_at (datetime)

**Relationships**: Task.user → User (many-to-one)

### API Contracts

See [contracts/openapi.yaml](./contracts/openapi.yaml) for complete OpenAPI specification.

**Endpoints**:
1. `GET /api/{user_id}/tasks` - List all tasks for user
2. `POST /api/{user_id}/tasks` - Create new task
3. `GET /api/{user_id}/tasks/{task_id}` - Get task details
4. `PUT /api/{user_id}/tasks/{task_id}` - Update task
5. `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle completion
6. `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
7. `GET /health` - Health check endpoint

### Quickstart Guide

See [quickstart.md](./quickstart.md) for complete setup instructions.

**Quick Setup**:
1. Create Python virtual environment
2. Install dependencies from requirements.txt
3. Configure .env with Neon database URL
4. Run init_db.py to create tables
5. Start server with `uvicorn app.main:app --reload`
6. Test endpoints with Postman/Thunder Client

## Implementation Phases

### Phase 1: Project Setup & Environment

**Objective**: Initialize Python project structure and dependencies

**Tasks**:
1. Create `backend/` directory structure
2. Initialize Python virtual environment: `python -m venv venv`
3. Create `requirements.txt` with dependencies:
   ```
   fastapi==0.109.0
   sqlmodel==0.0.14
   psycopg2-binary==2.9.9
   python-dotenv==1.0.0
   uvicorn[standard]==0.27.0
   pydantic==2.5.3
   ```
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.gitignore` for Python projects (venv/, __pycache__/, .env, *.pyc)
6. Create `.env.example` template
7. Create empty Python files: `__init__.py`, `main.py`, `database.py`, `models.py`, `schemas.py`, `routers/__init__.py`, `routers/tasks.py`

**Acceptance Criteria**:
- Virtual environment activates successfully
- All dependencies install without errors
- Project structure matches design
- .gitignore prevents committing sensitive files

### Phase 2: Database Foundation

**Objective**: Establish connection to Neon PostgreSQL and configure SQLModel

**Tasks**:
1. Create Neon Serverless PostgreSQL account at neon.tech
2. Create new database project and copy connection string
3. Add `DATABASE_URL` to `.env` file
4. Implement `database.py`:
   - Create SQLModel engine with connection string
   - Configure connection pooling (default settings)
   - Implement `get_session()` dependency for FastAPI
   - Add error handling for connection failures
5. Create `init_db.py` script to create tables
6. Test database connectivity

**Acceptance Criteria**:
- Database connection succeeds
- Connection string loaded from environment variable
- Session dependency works with FastAPI
- Error handling catches connection failures

### Phase 3: Data Models (SQLModel)

**Objective**: Define User and Task models with SQLModel

**Tasks**:
1. Implement `User` model in `models.py`:
   - Fields: id (int, primary key), email (str, unique), username (str), created_at (datetime)
   - Use `Field()` for constraints
   - Add `__repr__` for debugging
2. Implement `Task` model in `models.py`:
   - Fields: id (int, primary key), user_id (int, foreign key), title (str, max 200), description (Optional[str], max 2000), is_completed (bool, default False), created_at (datetime), updated_at (datetime)
   - Define relationship to User model
   - Add validation for title (not empty/whitespace)
   - Use `default_factory` for timestamps
3. Add table creation logic to `init_db.py`
4. Test model creation and relationships

**Acceptance Criteria**:
- Models create tables successfully
- Foreign key relationship works
- Constraints enforced (unique email, max lengths)
- Timestamps auto-populate
- Title validation prevents empty strings

### Phase 4: Request/Response Schemas (Pydantic)

**Objective**: Define Pydantic models for API validation

**Tasks**:
1. Implement `TaskCreate` schema in `schemas.py`:
   - Fields: title (str, min 1, max 200), description (Optional[str], max 2000)
   - Add validators for whitespace-only titles
2. Implement `TaskUpdate` schema:
   - Fields: title (Optional[str], max 200), description (Optional[str], max 2000), is_completed (Optional[bool])
   - All fields optional for partial updates
3. Implement `TaskResponse` schema:
   - All Task fields including id, timestamps
   - Configure `from_attributes=True` for ORM mode
4. Implement `TaskList` schema:
   - List of TaskResponse
5. Add example values for OpenAPI documentation

**Acceptance Criteria**:
- Schemas validate input correctly
- Invalid data rejected with 422 status
- Response serialization works
- OpenAPI docs show correct schemas

### Phase 5: API Endpoints Implementation

**Objective**: Implement all 6 task CRUD endpoints

**Tasks**:

**5.1: GET /api/{user_id}/tasks**
- Query tasks filtered by user_id
- Return empty array if no tasks
- Status: 200 OK

**5.2: POST /api/{user_id}/tasks**
- Accept TaskCreate schema
- Create task with user_id
- Set defaults: is_completed=False, timestamps
- Return created task with 201 Created

**5.3: GET /api/{user_id}/tasks/{task_id}**
- Fetch task by id
- Verify task.user_id == user_id (user isolation)
- Return 404 if not found or wrong user
- Status: 200 OK

**5.4: PUT /api/{user_id}/tasks/{task_id}**
- Accept TaskUpdate schema
- Verify task ownership
- Update only provided fields
- Update updated_at timestamp
- Return updated task with 200 OK

**5.5: PATCH /api/{user_id}/tasks/{task_id}/toggle**
- Toggle is_completed boolean
- Verify task ownership
- Update updated_at timestamp
- Return updated task with 200 OK

**5.6: DELETE /api/{user_id}/tasks/{task_id}**
- Verify task ownership
- Delete task from database
- Return 204 No Content

**Acceptance Criteria**:
- All endpoints return correct status codes
- User isolation enforced (can't access other users' tasks)
- Validation errors return 422
- Not found errors return 404
- Database operations succeed

### Phase 6: Error Handling & Validation

**Objective**: Implement comprehensive error handling

**Tasks**:
1. Add HTTPException handling for all error cases
2. Implement custom error responses with detail field
3. Handle database connection errors gracefully
4. Validate user_id and task_id formats (positive integers)
5. Handle constraint violations (unique, foreign key)
6. Add request body validation error responses
7. Implement 500 error handling for unexpected errors

**Acceptance Criteria**:
- All error scenarios return appropriate status codes
- Error messages are descriptive and user-friendly
- No sensitive information leaked in errors
- Database errors handled gracefully

### Phase 7: Main Application Setup

**Objective**: Configure FastAPI application and middleware

**Tasks**:
1. Implement `main.py`:
   - Create FastAPI app instance with title, version
   - Add CORS middleware (allow all origins for development)
   - Include task router with `/api` prefix
   - Add root endpoint `GET /` for health check
   - Add `/health` endpoint returning {"status": "healthy"}
   - Configure uvicorn settings
2. Add startup event handler to verify database connection
3. Add shutdown event handler for cleanup
4. Configure logging

**Acceptance Criteria**:
- Application starts successfully
- CORS allows frontend requests
- Health check endpoint works
- Routers properly included
- Logging configured

### Phase 8: Database Initialization & Documentation

**Objective**: Create database setup scripts and documentation

**Tasks**:
1. Complete `init_db.py` script:
   - Create all tables
   - Seed sample users for testing
   - Add error handling
2. Create `seed_data.py` (optional):
   - Add sample tasks for testing
3. Document database setup in README.md:
   - Neon account creation
   - Connection string configuration
   - Table creation process
4. Document API usage in README.md:
   - Endpoint descriptions
   - Example requests/responses
   - Error codes
5. Create Postman/Thunder Client collection (optional)

**Acceptance Criteria**:
- init_db.py creates all tables successfully
- Sample users seeded for testing
- README has complete setup instructions
- API endpoints documented with examples

## Testing Strategy

### Manual Testing Checklist

**User Story 1: Create and List Tasks (P1)**
- [ ] POST /api/1/tasks creates task with 201 status
- [ ] GET /api/1/tasks returns created task
- [ ] GET /api/1/tasks returns empty array for new user
- [ ] GET /api/1/tasks returns only user 1's tasks, not user 2's

**User Story 2: View and Update Task Details (P2)**
- [ ] GET /api/1/tasks/{id} returns task details with 200
- [ ] PUT /api/1/tasks/{id} updates task with 200
- [ ] GET /api/1/tasks/{id} returns 404 for non-existent task
- [ ] GET /api/2/tasks/{user1_task_id} returns 404 (user isolation)

**User Story 3: Toggle Task Completion (P3)**
- [ ] PATCH /api/1/tasks/{id}/toggle changes false → true
- [ ] PATCH /api/1/tasks/{id}/toggle changes true → false
- [ ] PATCH /api/1/tasks/{id}/toggle returns 404 for non-existent task
- [ ] Multiple toggles work correctly

**User Story 4: Delete Tasks (P4)**
- [ ] DELETE /api/1/tasks/{id} removes task with 204
- [ ] GET /api/1/tasks/{id} returns 404 after deletion
- [ ] Deleted task not in GET /api/1/tasks list
- [ ] DELETE /api/1/tasks/{id} returns 404 for non-existent task

**Edge Cases**
- [ ] Invalid user_id (negative, non-integer) returns 422
- [ ] Missing required fields returns 422
- [ ] Title exceeding 200 chars returns 422
- [ ] Description exceeding 2000 chars returns 422
- [ ] Empty/whitespace-only title returns 422
- [ ] Invalid JSON payload returns 422
- [ ] Database connection error returns 500

**Success Criteria Validation**
- [ ] All endpoints respond within 500ms
- [ ] User isolation 100% effective
- [ ] Data persists across server restarts
- [ ] Correct HTTP status codes for all scenarios
- [ ] 100 concurrent requests handled successfully

### Test Data

**Sample Users** (pre-seeded):
- User 1: id=1, email="user1@example.com", username="user1"
- User 2: id=2, email="user2@example.com", username="user2"
- User 3: id=3, email="user3@example.com", username="user3"

**Sample Tasks**:
- User 1: "Buy groceries", "Write report", "Call dentist"
- User 2: "Review PR", "Update documentation"

## Development Workflow

### Setup Process
1. Clone repository and checkout `001-fastapi-todo-api` branch
2. Navigate to `backend/` directory
3. Create virtual environment: `python -m venv venv`
4. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create `.env` file from `.env.example`
7. Add Neon database URL to `.env`
8. Run `python init_db.py` to create tables
9. Start server: `uvicorn app.main:app --reload`
10. Test with Postman/Thunder Client at `http://localhost:8000`

### Development Iteration
1. Make code changes
2. Server auto-reloads (uvicorn --reload)
3. Test endpoint with HTTP client
4. Check logs for errors
5. Iterate until working
6. Move to next endpoint

### Quality Checks
- Run Ruff linter: `ruff check .`
- Run Ruff formatter: `ruff format .`
- Check type hints: `mypy app/`
- Test all endpoints manually
- Verify user isolation
- Check error handling

## Deployment Preparation

### Environment Variables
```
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
ENVIRONMENT=development
```

### Requirements.txt (Pinned Versions)
```
fastapi==0.109.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-dotenv==1.0.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
```

### Health Check
- Endpoint: `GET /health`
- Response: `{"status": "healthy"}`
- Use for monitoring and load balancer checks

### CORS Configuration
- Development: Allow all origins (`*`)
- Production: Whitelist specific frontend origin (to be configured in Phase III)

## Architecture Decisions

### ADR-001: SQLModel for ORM
**Context**: Need type-safe ORM with Pydantic integration
**Decision**: Use SQLModel
**Consequences**: Reduced boilerplate, automatic Pydantic model generation, but less mature than SQLAlchemy

### ADR-002: Integer User IDs for Phase II
**Context**: Need to choose ID type for users and tasks
**Decision**: Use Integer for Phase II, migrate to UUID in production
**Consequences**: Simpler testing, but less secure (sequential IDs guessable)

### ADR-003: Hard Delete for Tasks
**Context**: Need to decide on deletion strategy
**Decision**: Hard delete (permanent removal)
**Consequences**: Simpler implementation, but no data recovery capability

### ADR-004: Manual Testing for Phase II
**Context**: Need testing strategy for MVP
**Decision**: Manual testing with Postman/Thunder Client
**Consequences**: Faster initial development, but no regression protection (automated tests in future phase)

### ADR-005: Application-Level Timestamps
**Context**: Need to manage created_at and updated_at timestamps
**Decision**: Use SQLModel default_factory with Python datetime
**Consequences**: More control, easier to test, but requires discipline to update updated_at

## Risks & Mitigations

### Risk: Neon Database Connectivity Issues
**Impact**: Blocks development and testing
**Mitigation**:
- Test connection immediately after setup
- Document connection string format clearly
- Provide troubleshooting guide in README
- Have fallback to local PostgreSQL if needed

### Risk: User Isolation Implementation Errors
**Impact**: Security vulnerability, data exposure
**Mitigation**:
- Thorough testing with multiple users
- Code review focusing on user_id filtering
- Document user isolation pattern clearly
- Add integration tests in future phase

### Risk: Concurrent Update Race Conditions
**Impact**: Data inconsistency
**Mitigation**:
- Document known limitation
- Consider optimistic locking in future phase
- Test concurrent requests manually
- Monitor for issues in production

### Risk: Missing Input Validation
**Impact**: Invalid data in database
**Mitigation**:
- Use Pydantic for all request validation
- Add database constraints (NOT NULL, CHECK)
- Test edge cases thoroughly
- Review validation logic in code review

## Next Steps

After completing this implementation plan:

1. **Run `/sp.tasks`** to generate detailed task breakdown from this plan
2. **Begin implementation** following the 8 phases sequentially
3. **Test each phase** before moving to the next
4. **Document issues** encountered for future reference
5. **Prepare for Spec 2** (Authentication & Authorization) once Phase II complete

## Success Metrics

- ✅ All 6 API endpoints functional
- ✅ User isolation enforced 100%
- ✅ Data persists across restarts
- ✅ Response times <500ms
- ✅ 100 concurrent requests handled
- ✅ All edge cases handled gracefully
- ✅ README with complete setup instructions
- ✅ API testable with standard HTTP clients
