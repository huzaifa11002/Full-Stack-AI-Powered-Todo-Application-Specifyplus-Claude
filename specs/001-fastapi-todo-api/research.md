# Research: FastAPI Todo REST API

**Feature**: 001-fastapi-todo-api
**Date**: 2026-01-10
**Purpose**: Technology decisions and best practices research for FastAPI REST API implementation

## Research Questions & Decisions

### 1. ORM Selection: SQLModel vs SQLAlchemy + Pydantic

**Question**: Which ORM approach provides the best type safety and developer experience for FastAPI?

**Options Evaluated**:
1. **SQLModel** (SQLAlchemy + Pydantic combined)
2. Pure SQLAlchemy with separate Pydantic models
3. Tortoise ORM

**Research Findings**:
- SQLModel is created by the same author as FastAPI (Sebastián Ramírez)
- Provides automatic Pydantic model generation from database models
- Reduces boilerplate by ~40% compared to separate SQLAlchemy + Pydantic
- Type hints work seamlessly across database and API layers
- Smaller ecosystem than pure SQLAlchemy but sufficient for CRUD operations
- Official FastAPI documentation recommends SQLModel for new projects

**Decision**: Use SQLModel

**Rationale**:
- Reduces code duplication between database models and API schemas
- Provides full type safety from database to API response
- Integrates perfectly with FastAPI's dependency injection
- Simpler learning curve for team members
- Sufficient maturity for production use (v0.0.14 stable)

**Alternatives Considered**:
- **Pure SQLAlchemy + Pydantic**: More mature, larger ecosystem, but requires maintaining two separate model definitions and manual synchronization
- **Tortoise ORM**: Async-first design, but less mature, smaller community, and less FastAPI integration

**Trade-offs Accepted**:
- Slightly less mature than pure SQLAlchemy
- Smaller community and fewer Stack Overflow answers
- May need to drop down to SQLAlchemy for advanced features

---

### 2. User ID Type: Integer vs UUID

**Question**: What ID type provides the best balance of security, performance, and developer experience?

**Options Evaluated**:
1. **Integer** (auto-incrementing)
2. UUID (v4)
3. String (custom format)

**Research Findings**:
- Integer IDs: Sequential, predictable, smaller storage (4 bytes), faster indexing, easier debugging
- UUIDs: Non-sequential, unpredictable, larger storage (16 bytes), globally unique, better for distributed systems
- For Phase II (development/testing): Integer IDs significantly easier to work with manually
- For production: UUIDs provide better security (can't enumerate users/tasks)
- Migration path: Can migrate from Integer to UUID in future phase with Alembic

**Decision**: Use Integer for Phase II, plan UUID migration for production

**Rationale**:
- Phase II focuses on API foundation and manual testing
- Integer IDs make manual testing much easier (can use 1, 2, 3 instead of long UUIDs)
- Faster development iteration during MVP phase
- Clear migration path to UUIDs documented for future phase
- Aligns with spec assumption: "User IDs will be provided as integers"

**Alternatives Considered**:
- **UUID from start**: More secure, but significantly harder to test manually, longer URLs, more complex debugging
- **String IDs**: Maximum flexibility, but no type safety benefits, potential for inconsistent formats

**Trade-offs Accepted**:
- Sequential IDs are guessable (security concern for production)
- Will require migration in future phase
- Acceptable for Phase II as authentication is deferred to Spec 2

---

### 3. Database Migration Strategy

**Question**: How should we manage database schema changes?

**Options Evaluated**:
1. **Manual SQL scripts** for initial setup, Alembic for future changes
2. Alembic from the start
3. SQLModel.metadata.create_all() only (no migration tracking)

**Research Findings**:
- Initial schema is simple: 2 tables (User, Task) with 1 foreign key
- Alembic adds setup overhead: config files, migration scripts, version tracking
- For MVP, manual table creation is faster and simpler
- Future schema changes will need proper migration tracking
- Alembic is the standard migration tool for SQLAlchemy/SQLModel

**Decision**: Manual table creation for Phase II, Alembic configured for future migrations

**Rationale**:
- Initial schema is simple enough for manual creation
- Faster to get started without Alembic configuration
- Alembic will be configured and documented for future use
- Migration tracking becomes important when schema evolves
- Meets spec requirement: "Database migrations are initialized and tracked"

**Alternatives Considered**:
- **Alembic from start**: More proper, but overhead for simple initial schema
- **No migration tracking**: Dangerous for production, makes schema changes error-prone

**Trade-offs Accepted**:
- Initial schema not tracked in migration history
- Will need to create "baseline" migration when Alembic is added
- Acceptable for Phase II as schema is simple and unlikely to change

---

### 4. Timestamp Management

**Question**: How should created_at and updated_at timestamps be managed?

**Options Evaluated**:
1. **Application-level** (Python datetime with SQLModel default_factory)
2. Database-level defaults (PostgreSQL NOW())
3. Manual timestamp setting in endpoint code

**Research Findings**:
- Application-level: Full control, consistent timezone handling, easier to test, portable across databases
- Database-level: Guaranteed consistency, less code, but database-specific syntax
- Manual setting: Most flexible, but error-prone and inconsistent
- SQLModel supports default_factory for automatic timestamp generation
- Python datetime.utcnow() provides consistent UTC timestamps

**Decision**: Application-level timestamps with SQLModel default_factory

**Rationale**:
- Provides full control over timestamp generation
- Consistent with Python datetime handling throughout application
- Easier to test (can mock datetime in tests)
- Portable across different database backends
- SQLModel default_factory makes it automatic and consistent

**Alternatives Considered**:
- **Database-level defaults**: Less control, database-specific, harder to test
- **Manual setting**: Too error-prone, requires discipline to update updated_at

**Trade-offs Accepted**:
- Requires discipline to update updated_at in PUT/PATCH endpoints
- Slightly more code than database defaults
- Acceptable as SQLModel makes it straightforward

---

### 5. Error Response Format

**Question**: What error response format should the API use?

**Options Evaluated**:
1. **FastAPI default HTTPException** with detail field
2. Custom exception handler with structured error format
3. Problem Details (RFC 7807) format

**Research Findings**:
- FastAPI default: Simple, consistent with framework, automatic OpenAPI docs
- Custom format: More control, but adds complexity and maintenance burden
- RFC 7807: Standard format, but overkill for simple CRUD API
- FastAPI HTTPException provides: status_code, detail, headers
- Automatic validation errors return 422 with detailed field errors

**Decision**: FastAPI default HTTPException with detail field

**Rationale**:
- Standard FastAPI pattern, familiar to FastAPI developers
- Automatic OpenAPI documentation generation
- Consistent with framework conventions
- Sufficient for Phase II requirements
- Can be enhanced in future phases if needed

**Alternatives Considered**:
- **Custom exception handler**: More control, but unnecessary complexity for Phase II
- **RFC 7807**: Industry standard, but overkill for simple API

**Trade-offs Accepted**:
- Less structured than RFC 7807 (no type, title, instance fields)
- Acceptable for Phase II as error handling requirements are simple

---

### 6. Delete Strategy: Soft Delete vs Hard Delete

**Question**: Should deleted tasks be permanently removed or marked as deleted?

**Options Evaluated**:
1. **Hard delete** (permanent removal)
2. Soft delete (is_deleted flag)

**Research Findings**:
- Hard delete: Simpler implementation, smaller database, no recovery capability
- Soft delete: Data recovery possible, audit trail, but more complex queries
- Spec explicitly states: "Soft delete functionality (deleted tasks are permanently removed)" in Out of Scope
- Phase II focuses on basic CRUD, not data recovery
- Soft delete can be added in future phase if needed

**Decision**: Hard delete for Phase II

**Rationale**:
- Explicitly out of scope per specification
- Simpler implementation (no is_deleted flag, no filtering in queries)
- Meets current requirements
- Can be migrated to soft delete in future phase if needed
- Smaller database size

**Alternatives Considered**:
- **Soft delete**: Better for production, but adds complexity not required by spec

**Trade-offs Accepted**:
- No data recovery capability
- No audit trail of deleted tasks
- Acceptable for Phase II as spec explicitly excludes soft delete

---

### 7. Task Description Field Constraints

**Question**: Should task description be required or optional, and what length limit?

**Options Evaluated**:
1. **Optional field, 2000 character limit**
2. Required field, 500 character limit
3. Optional field, no limit

**Research Findings**:
- Spec assumption: "Task descriptions have a reasonable maximum length of 2000 characters"
- Optional field provides flexibility for quick task creation
- 2000 characters sufficient for detailed descriptions (~300 words)
- Required field would force users to provide description even for simple tasks
- No limit could lead to database bloat and abuse

**Decision**: Optional field, 2000 character limit

**Rationale**:
- Aligns with spec assumptions
- Provides flexibility for quick task creation ("Buy milk" doesn't need description)
- 2000 characters sufficient for detailed descriptions
- Prevents abuse and database bloat
- Pydantic validation enforces limit automatically

**Alternatives Considered**:
- **Required field**: Too restrictive for quick task creation
- **No limit**: Potential for abuse, database bloat, performance issues

**Trade-offs Accepted**:
- Users might create tasks without descriptions (acceptable use case)

---

### 8. User Validation Strategy

**Question**: Should the API validate that user_id exists before creating/accessing tasks?

**Options Evaluated**:
1. **Assume valid user_id** (no validation)
2. Check user exists on every request
3. Foreign key constraint only (database-level validation)

**Research Findings**:
- Spec states: "User records will be pre-seeded in the database for testing purposes"
- Authentication in Spec 2 will validate users before reaching task endpoints
- Checking user exists adds database query overhead on every request
- Foreign key constraint provides database-level integrity
- For Phase II, pre-seeded users sufficient for testing

**Decision**: Assume valid user_id for Phase II, rely on foreign key constraint

**Rationale**:
- Authentication in Spec 2 will validate users
- Avoids redundant database queries
- Foreign key constraint prevents orphaned tasks
- Pre-seeded users sufficient for Phase II testing
- Performance optimization (one less query per request)

**Alternatives Considered**:
- **Check user exists**: Better data integrity, but performance overhead and redundant with future auth
- **No foreign key**: Dangerous, could create orphaned tasks

**Trade-offs Accepted**:
- API accepts any integer user_id without validation
- Could create tasks for non-existent users (prevented by foreign key constraint)
- Acceptable for Phase II as authentication will validate in Spec 2

---

## Best Practices Research

### FastAPI Project Structure

**Source**: FastAPI official documentation, real-world FastAPI projects

**Key Patterns**:
1. **Separate routers** for different resource types (tasks, users, etc.)
2. **Dependency injection** for database sessions (get_session)
3. **Pydantic models** for request/response validation
4. **Centralized error handling** with HTTPException
5. **Environment variables** for configuration (python-dotenv)

**Applied to Project**:
- `routers/tasks.py` for all task endpoints
- `database.py` with `get_session()` dependency
- `schemas.py` for all Pydantic models
- HTTPException for all error responses
- `.env` file for DATABASE_URL

---

### SQLModel Patterns

**Source**: SQLModel documentation, FastAPI + SQLModel tutorials

**Key Patterns**:
1. Use `Optional[type]` for nullable fields
2. Define relationships with `Relationship()` for type safety
3. Use `Field()` for constraints and metadata
4. Separate table models from API models when needed
5. Use `default_factory` for auto-generated values

**Applied to Project**:
- `description: Optional[str]` for optional task description
- `user: Relationship("User")` for Task → User relationship
- `Field(max_length=200)` for title constraint
- `default_factory=datetime.utcnow` for timestamps

---

### Neon PostgreSQL Connection

**Source**: Neon documentation, PostgreSQL best practices

**Key Patterns**:
1. Connection string format: `postgresql://user:password@host/database?sslmode=require`
2. SSL required for Neon connections
3. Connection pooling handled by SQLModel engine
4. Use environment variables for credentials

**Applied to Project**:
- DATABASE_URL in .env file
- SQLModel engine with connection string
- Default connection pooling settings
- SSL mode required in connection string

---

### RESTful API Design

**Source**: REST API best practices, HTTP specification

**Key Patterns**:
1. Resource naming: plural nouns (`/tasks` not `/task`)
2. HTTP methods: GET (read), POST (create), PUT (update), PATCH (partial update), DELETE (remove)
3. Status codes: 200 (OK), 201 (Created), 204 (No Content), 404 (Not Found), 422 (Validation Error), 500 (Server Error)
4. JSON responses with consistent structure
5. Path parameters for resource IDs

**Applied to Project**:
- `/api/{user_id}/tasks` (plural)
- Proper HTTP methods for each operation
- Correct status codes for all scenarios
- JSON-only responses
- user_id and task_id as path parameters

---

## Technology Stack Summary

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.109.0 | Web framework |
| sqlmodel | 0.0.14 | ORM with Pydantic integration |
| pydantic | 2.5.3 | Data validation |
| psycopg2-binary | 2.9.9 | PostgreSQL driver |
| python-dotenv | 1.0.0 | Environment variable management |
| uvicorn[standard] | 0.27.0 | ASGI server |

### Development Tools

| Tool | Purpose |
|------|---------|
| Ruff | Linting and formatting |
| mypy | Type checking |
| Postman/Thunder Client | API testing |

---

## Implementation Recommendations

### Phase Sequencing
1. **Phase 1-2**: Setup and database foundation (critical path)
2. **Phase 3-4**: Models and schemas (parallel work possible)
3. **Phase 5**: Endpoints (implement in priority order: P1 → P2 → P3 → P4)
4. **Phase 6-7**: Error handling and main app (polish)
5. **Phase 8**: Documentation (can be done throughout)

### Testing Approach
- Test each endpoint immediately after implementation
- Use multiple user IDs to verify isolation
- Test all edge cases before moving to next endpoint
- Keep Postman/Thunder Client collection for regression testing

### Code Quality
- Run Ruff on every file before committing
- Add type hints to all functions
- Document complex logic with comments
- Keep functions small and focused

---

## Open Questions & Future Considerations

### For Future Phases

1. **UUID Migration**: Plan migration from Integer to UUID IDs in production phase
2. **Alembic Setup**: Configure Alembic before first schema change
3. **Automated Testing**: Add pytest with 70% coverage target
4. **Soft Delete**: Consider adding soft delete if data recovery needed
5. **Pagination**: Add pagination when task lists grow large
6. **Rate Limiting**: Implement rate limiting before production deployment

### Monitoring Needs

1. **Performance**: Track endpoint response times
2. **Errors**: Monitor 500 errors and database connection failures
3. **Usage**: Track API usage patterns for optimization

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Neon Documentation](https://neon.tech/docs/)
- [REST API Best Practices](https://restfulapi.net/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
