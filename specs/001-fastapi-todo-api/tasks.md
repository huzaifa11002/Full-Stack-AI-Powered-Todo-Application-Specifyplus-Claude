---

description: "Task list for FastAPI Todo REST API implementation"
---

# Tasks: FastAPI Todo REST API

**Input**: Design documents from `/specs/001-fastapi-todo-api/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual testing with Postman/Thunder Client. Automated tests are deferred to future phase per specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for application code
- **Root**: `backend/` for configuration files
- Paths shown below use backend structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure (backend/app/, backend/app/routers/)
- [ ] T002 Initialize Python virtual environment in backend/ directory
- [ ] T003 Create requirements.txt in backend/ with pinned dependencies (fastapi==0.109.0, sqlmodel==0.0.14, psycopg2-binary==2.9.9, python-dotenv==1.0.0, uvicorn[standard]==0.27.0, pydantic==2.5.3)
- [ ] T004 Install dependencies from requirements.txt
- [ ] T005 [P] Create .gitignore in backend/ for Python projects (venv/, __pycache__/, .env, *.pyc)
- [ ] T006 [P] Create .env.example in backend/ with DATABASE_URL and ENVIRONMENT templates
- [ ] T007 [P] Create empty Python files: backend/app/__init__.py, backend/app/main.py, backend/app/database.py, backend/app/models.py, backend/app/schemas.py, backend/app/routers/__init__.py, backend/app/routers/tasks.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create Neon Serverless PostgreSQL account at neon.tech and create database project
- [ ] T009 Copy Neon connection string and add DATABASE_URL to backend/.env file
- [ ] T010 Implement database engine and session management in backend/app/database.py (SQLModel engine, connection pooling, get_session dependency)
- [ ] T011 [P] Implement User model in backend/app/models.py (id, email unique, username, created_at with default_factory)
- [ ] T012 [P] Implement Task model in backend/app/models.py (id, user_id FK, title max 200, description optional max 2000, is_completed default False, created_at, updated_at with default_factory, relationship to User)
- [ ] T013 [P] Implement TaskCreate schema in backend/app/schemas.py (title min 1 max 200, description optional max 2000, validator for whitespace-only titles)
- [ ] T014 [P] Implement TaskUpdate schema in backend/app/schemas.py (title optional max 200, description optional max 2000, is_completed optional, all fields optional for partial updates)
- [ ] T015 [P] Implement TaskResponse schema in backend/app/schemas.py (all Task fields, from_attributes=True for ORM mode)
- [ ] T016 Create init_db.py script in backend/ to create all tables using SQLModel.metadata.create_all()
- [ ] T017 Add sample user seeding to init_db.py (user1@example.com, user2@example.com, user3@example.com)
- [ ] T018 Run init_db.py to create tables and seed users, verify database schema

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and List Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable creating new tasks and retrieving all tasks for a specific user

**Independent Test**: Send POST requests to create tasks for user 1, then send GET request to retrieve list and verify all created tasks appear correctly. Create tasks for user 2 and verify user 1's GET request returns only user 1's tasks (user isolation).

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement GET /api/{user_id}/tasks endpoint in backend/app/routers/tasks.py (query tasks filtered by user_id, return empty array if no tasks, status 200)
- [ ] T020 [P] [US1] Implement POST /api/{user_id}/tasks endpoint in backend/app/routers/tasks.py (accept TaskCreate schema, create task with user_id, set is_completed=False and timestamps, return created task with status 201)
- [ ] T021 [US1] Configure FastAPI app in backend/app/main.py (create app instance, add CORS middleware allow all origins, include tasks router with /api prefix)
- [ ] T022 [US1] Add startup event handler in backend/app/main.py to verify database connection
- [ ] T023 [US1] Test US1 endpoints manually with Postman/Thunder Client (POST create task, GET list tasks, verify user isolation, verify empty array for new user)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View and Update Task Details (Priority: P2)

**Goal**: Enable retrieving individual task details and updating task information

**Independent Test**: Create a task via US1 endpoints, retrieve it by ID to verify details, update it with new title and description, confirm changes persisted. Attempt to access user 1's task as user 2 and verify 404 response (user isolation).

### Implementation for User Story 2

- [ ] T024 [P] [US2] Implement GET /api/{user_id}/tasks/{task_id} endpoint in backend/app/routers/tasks.py (fetch task by id, verify task.user_id == user_id for user isolation, return 404 if not found or wrong user, status 200)
- [ ] T025 [P] [US2] Implement PUT /api/{user_id}/tasks/{task_id} endpoint in backend/app/routers/tasks.py (accept TaskUpdate schema, verify task ownership, update only provided fields, update updated_at timestamp, return updated task with status 200, return 404 if not found)
- [ ] T026 [US2] Test US2 endpoints manually with Postman/Thunder Client (GET task details, PUT update task, verify 404 for non-existent task, verify 404 for wrong user access)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Toggle Task Completion (Priority: P3)

**Goal**: Enable quick toggling of task completion status without full update

**Independent Test**: Create a task with is_completed=false, send PATCH toggle request and verify it changes to true, toggle again and verify it returns to false. Verify updated_at timestamp changes on each toggle.

### Implementation for User Story 3

- [ ] T027 [US3] Implement PATCH /api/{user_id}/tasks/{task_id}/toggle endpoint in backend/app/routers/tasks.py (toggle is_completed boolean, verify task ownership, update updated_at timestamp, return updated task with status 200, return 404 if not found)
- [ ] T028 [US3] Test US3 endpoint manually with Postman/Thunder Client (toggle false to true, toggle true to false, verify 404 for non-existent task, test multiple rapid toggles)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Enable permanent deletion of tasks

**Independent Test**: Create a task, delete it, attempt to retrieve it and verify 404 response, confirm it no longer appears in task list. Attempt to delete non-existent task and verify 404 response.

### Implementation for User Story 4

- [ ] T029 [US4] Implement DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/app/routers/tasks.py (verify task ownership, delete task from database, return status 204 No Content, return 404 if not found)
- [ ] T030 [US4] Test US4 endpoint manually with Postman/Thunder Client (DELETE task, verify 404 on subsequent GET, verify task not in list, verify 404 for non-existent task)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T031 [P] Add GET / root endpoint in backend/app/main.py returning welcome message
- [ ] T032 [P] Add GET /health endpoint in backend/app/main.py returning {"status": "healthy"}
- [ ] T033 [P] Implement HTTPException error handling for all error cases in backend/app/routers/tasks.py (404 for not found, 422 for validation errors, 500 for server errors)
- [ ] T034 [P] Add input validation for user_id and task_id formats (positive integers) in backend/app/routers/tasks.py
- [ ] T035 [P] Handle database connection errors gracefully in backend/app/database.py
- [ ] T036 [P] Add shutdown event handler in backend/app/main.py for cleanup
- [ ] T037 [P] Configure logging in backend/app/main.py
- [ ] T038 Create README.md in backend/ with setup instructions (prerequisites, 9-step setup process, API usage examples)
- [ ] T039 Document API endpoints in README.md (all 6 endpoints with example requests/responses, error codes)
- [ ] T040 Test all edge cases manually (invalid user_id, missing fields, title/description exceeding limits, empty title, invalid JSON, database connection error)
- [ ] T041 Verify all success criteria (response times <500ms, user isolation 100%, data persists across restarts, correct status codes, 100 concurrent requests)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but builds on US1 endpoints for testing)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but builds on US1 endpoints for testing)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (but builds on US1 endpoints for testing)

### Within Each User Story

- **US1**: T019 and T020 can run in parallel (different endpoint implementations), then T021-T023 sequentially
- **US2**: T024 and T025 can run in parallel (different endpoint implementations), then T026
- **US3**: T027 then T028 (single endpoint)
- **US4**: T029 then T030 (single endpoint)

### Parallel Opportunities

- **Setup phase**: T005, T006, T007 can run in parallel (different files)
- **Foundational phase**: T011, T012 can run in parallel (different models in same file but independent), T013, T014, T015 can run in parallel (different schemas)
- **User Story 1**: T019, T020 can run in parallel (different endpoints)
- **User Story 2**: T024, T025 can run in parallel (different endpoints)
- **Polish phase**: T031, T032, T033, T034, T035, T036, T037 can run in parallel (different concerns)
- **Different user stories**: US1, US2, US3, US4 can be worked on in parallel by different team members after Foundational phase completes

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch US1 endpoint implementations in parallel:
Task T019: "Implement GET /api/{user_id}/tasks endpoint"
Task T020: "Implement POST /api/{user_id}/tasks endpoint"

# Then configure app and test sequentially:
Task T021: "Configure FastAPI app in main.py"
Task T022: "Add startup event handler"
Task T023: "Test US1 endpoints manually"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (T019-T023)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (T019-T023) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (T024-T026) → Test independently → Deploy/Demo
4. Add User Story 3 (T027-T028) → Test independently → Deploy/Demo
5. Add User Story 4 (T029-T030) → Test independently → Deploy/Demo
6. Add Polish (T031-T041) → Final testing → Production ready
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T019-T023)
   - Developer B: User Story 2 (T024-T026)
   - Developer C: User Story 3 (T027-T028)
   - Developer D: User Story 4 (T029-T030)
3. Stories complete and integrate independently
4. Team completes Polish together

---

## Notes

- [P] tasks = different files or independent concerns, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing with Postman/Thunder Client (automated tests deferred to future phase)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 41

**By Phase**:
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 11 tasks (BLOCKING)
- Phase 3 (US1 - MVP): 5 tasks
- Phase 4 (US2): 3 tasks
- Phase 5 (US3): 2 tasks
- Phase 6 (US4): 2 tasks
- Phase 7 (Polish): 11 tasks

**By User Story**:
- US1 (Create and List Tasks): 5 tasks (T019-T023)
- US2 (View and Update Task Details): 3 tasks (T024-T026)
- US3 (Toggle Task Completion): 2 tasks (T027-T028)
- US4 (Delete Tasks): 2 tasks (T029-T030)

**Parallel Opportunities**: 15 tasks marked with [P] can run in parallel within their phase

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (23 tasks total for working MVP)

**Independent Test Criteria**:
- US1: Create tasks and list them, verify user isolation
- US2: Get task details and update them, verify user isolation
- US3: Toggle completion status multiple times
- US4: Delete task and verify removal

**Format Validation**: ✅ All tasks follow checklist format with checkbox, ID, optional [P] and [Story] labels, and file paths
