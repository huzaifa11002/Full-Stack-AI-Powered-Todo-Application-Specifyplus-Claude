# Tasks: MCP AI Chat for Task Management

**Input**: Design documents from `/specs/001-mcp-ai-chat/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the feature specification, so test tasks are NOT included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/` for API, `frontend/` for UI (frontend out of scope)
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [ ] T001 Install MCP SDK in backend/requirements.txt (`mcp`)
- [ ] T002 Install OpenAI Agents SDK in backend/requirements.txt (`openai-agents-sdk`, `openai`)
- [ ] T003 [P] Add OPENAI_API_KEY to backend/.env.example with documentation
- [ ] T004 [P] Add AGENT_MODEL, AGENT_TEMPERATURE, AGENT_MAX_TOKENS to backend/.env.example

**Checkpoint**: Dependencies installed, environment template ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Schema Extension

- [ ] T005 [P] Create Conversation model in backend/app/models.py with user_id, created_at, updated_at fields
- [ ] T006 [P] Create Message model in backend/app/models.py with conversation_id, user_id, role, content, tool_calls, created_at fields
- [ ] T007 Create Alembic migration script in backend/alembic/versions/ for Conversation and Message tables with indexes
- [ ] T008 Add model validation for Message.role (must be "user" or "assistant") in backend/app/models.py
- [ ] T009 Add model validation for Message.content (cannot be empty) in backend/app/models.py

### API Schemas

- [ ] T010 [P] Create ChatRequest schema in backend/app/schemas.py with conversation_id (optional) and message fields
- [ ] T011 [P] Create ToolCallInfo schema in backend/app/schemas.py with tool, params, result fields
- [ ] T012 [P] Create ChatResponse schema in backend/app/schemas.py with conversation_id, response, tool_calls fields

### MCP Server Infrastructure

- [ ] T013 Create mcp/ directory structure in backend/mcp/ with __init__.py, server.py, tools.py, handlers.py
- [ ] T014 Initialize MCP server in backend/mcp/server.py with name "todo-mcp-server" and version "1.0.0"
- [ ] T015 Create TOOL_HANDLERS mapping dictionary in backend/mcp/handlers.py

### OpenAI Agents SDK Infrastructure

- [ ] T016 Create agents/ directory structure in backend/agents/ with __init__.py, config.py, agent.py, runner.py
- [ ] T017 Configure OpenAI client in backend/agents/config.py with API key from environment
- [ ] T018 Define SYSTEM_PROMPT in backend/agents/config.py with tool usage guidelines for all 5 task operations
- [ ] T019 Create mcp_tool_to_openai_function converter in backend/agents/agent.py

### Chat Endpoint Foundation

- [ ] T020 Create chat router file in backend/app/routers/chat.py
- [ ] T021 Implement conversation creation/retrieval logic in backend/app/routers/chat.py
- [ ] T022 Implement conversation history fetching function in backend/app/routers/chat.py (get messages ordered by created_at)
- [ ] T023 Implement message storage logic (user and assistant messages) in backend/app/routers/chat.py
- [ ] T024 Register chat router in backend/main.py with prefix "/api"

### Error Handling Infrastructure

- [ ] T025 [P] Add error handling for OpenAI API failures in backend/agents/runner.py (APIError, RateLimitError)
- [ ] T026 [P] Add error handling for database failures in backend/app/routers/chat.py (IntegrityError, rollback)
- [ ] T027 [P] Add logging configuration for chat operations in backend/app/routers/chat.py

**Checkpoint**: Foundation ready - database models created, MCP server initialized, agent infrastructure ready, chat endpoint structure in place. User story implementation can now begin.

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks through natural language conversation

**Independent Test**: Send chat message "Add a task to buy groceries" and verify task is created in database with correct title and user receives confirmation response

### MCP Tool Implementation

- [ ] T028 [P] [US1] Define add_task tool schema in backend/mcp/tools.py with user_id, title, description parameters
- [ ] T029 [US1] Implement handle_add_task handler in backend/mcp/handlers.py that creates Task in database
- [ ] T030 [US1] Add user validation in handle_add_task to ensure user exists in backend/mcp/handlers.py
- [ ] T031 [US1] Add error handling for task creation failures in handle_add_task in backend/mcp/handlers.py
- [ ] T032 [US1] Register add_task tool with MCP server in backend/mcp/server.py

### Agent Integration

- [ ] T033 [US1] Add add_task tool to agent tools list in backend/agents/agent.py
- [ ] T034 [US1] Implement agent runner with tool execution for add_task in backend/agents/runner.py
- [ ] T035 [US1] Add tool call logging for add_task operations in backend/agents/runner.py

### Chat Endpoint Integration

- [ ] T036 [US1] Integrate agent runner into chat endpoint POST /api/{user_id}/chat in backend/app/routers/chat.py
- [ ] T037 [US1] Add JWT authentication validation in chat endpoint in backend/app/routers/chat.py
- [ ] T038 [US1] Add user_id validation (must match authenticated user) in backend/app/routers/chat.py
- [ ] T039 [US1] Implement response formatting with tool_calls in backend/app/routers/chat.py

**Checkpoint**: User Story 1 complete - users can create tasks via natural language. Test independently before proceeding.

---

## Phase 4: User Story 2 - Conversational Task Querying (Priority: P1)

**Goal**: Enable users to query their tasks through natural language conversation

**Independent Test**: Create several tasks, then send "Show me my tasks" and verify response contains all tasks with correct details

### MCP Tool Implementation

- [ ] T040 [P] [US2] Define list_tasks tool schema in backend/mcp/tools.py with user_id and status (all/pending/completed) parameters
- [ ] T041 [US2] Implement handle_list_tasks handler in backend/mcp/handlers.py that queries tasks from database
- [ ] T042 [US2] Add status filtering logic (all, pending, completed) in handle_list_tasks in backend/mcp/handlers.py
- [ ] T043 [US2] Add user isolation enforcement in handle_list_tasks query in backend/mcp/handlers.py
- [ ] T044 [US2] Register list_tasks tool with MCP server in backend/mcp/server.py

### Agent Integration

- [ ] T045 [US2] Add list_tasks tool to agent tools list in backend/agents/agent.py
- [ ] T046 [US2] Update SYSTEM_PROMPT with list_tasks usage guidelines in backend/agents/config.py
- [ ] T047 [US2] Add tool call logging for list_tasks operations in backend/agents/runner.py

**Checkpoint**: User Story 2 complete - users can query tasks via natural language. Both US1 and US2 should work independently.

---

## Phase 5: User Story 3 - Task Completion via Chat (Priority: P2)

**Goal**: Enable users to mark tasks as complete through conversation

**Independent Test**: Create a task, then send "Mark task 5 as complete" and verify task status changes to completed in database

### MCP Tool Implementation

- [ ] T048 [P] [US3] Define complete_task tool schema in backend/mcp/tools.py with user_id and task_id parameters
- [ ] T049 [US3] Implement handle_complete_task handler in backend/mcp/handlers.py that updates task is_completed field
- [ ] T050 [US3] Add task existence validation in handle_complete_task in backend/mcp/handlers.py
- [ ] T051 [US3] Add user isolation enforcement (task must belong to user) in handle_complete_task in backend/mcp/handlers.py
- [ ] T052 [US3] Add error handling for task not found in handle_complete_task in backend/mcp/handlers.py
- [ ] T053 [US3] Register complete_task tool with MCP server in backend/mcp/server.py

### Agent Integration

- [ ] T054 [US3] Add complete_task tool to agent tools list in backend/agents/agent.py
- [ ] T055 [US3] Update SYSTEM_PROMPT with complete_task usage guidelines in backend/agents/config.py
- [ ] T056 [US3] Add tool call logging for complete_task operations in backend/agents/runner.py

**Checkpoint**: User Story 3 complete - users can complete tasks via natural language. US1, US2, and US3 should all work independently.

---

## Phase 6: User Story 4 - Task Modification and Deletion (Priority: P3)

**Goal**: Enable users to update or delete tasks through conversation

**Independent Test**: Create a task, then send "Update task 5 title to 'New title'" and verify task is updated. Then send "Delete task 5" and verify task is removed.

### MCP Tool Implementation - Update

- [ ] T057 [P] [US4] Define update_task tool schema in backend/mcp/tools.py with user_id, task_id, title (optional), description (optional) parameters
- [ ] T058 [US4] Implement handle_update_task handler in backend/mcp/handlers.py that updates task fields
- [ ] T059 [US4] Add task existence validation in handle_update_task in backend/mcp/handlers.py
- [ ] T060 [US4] Add user isolation enforcement in handle_update_task in backend/mcp/handlers.py
- [ ] T061 [US4] Add validation that at least one field (title or description) is provided in handle_update_task in backend/mcp/handlers.py
- [ ] T062 [US4] Register update_task tool with MCP server in backend/mcp/server.py

### MCP Tool Implementation - Delete

- [ ] T063 [P] [US4] Define delete_task tool schema in backend/mcp/tools.py with user_id and task_id parameters
- [ ] T064 [US4] Implement handle_delete_task handler in backend/mcp/handlers.py that deletes task from database
- [ ] T065 [US4] Add task existence validation in handle_delete_task in backend/mcp/handlers.py
- [ ] T066 [US4] Add user isolation enforcement in handle_delete_task in backend/mcp/handlers.py
- [ ] T067 [US4] Register delete_task tool with MCP server in backend/mcp/server.py

### Agent Integration

- [ ] T068 [US4] Add update_task and delete_task tools to agent tools list in backend/agents/agent.py
- [ ] T069 [US4] Update SYSTEM_PROMPT with update_task and delete_task usage guidelines in backend/agents/config.py
- [ ] T070 [US4] Add tool call logging for update_task and delete_task operations in backend/agents/runner.py

**Checkpoint**: User Story 4 complete - users can update and delete tasks via natural language. All user stories (US1-US4) should work independently.

---

## Phase 7: User Story 5 - Multi-Turn Conversation Context (Priority: P2)

**Goal**: Ensure conversation context is maintained across multiple turns

**Independent Test**: Send "Create a task to review report", then send "Actually, make that due tomorrow" and verify system understands the reference

**Note**: This user story is largely implemented through the foundational conversation history system (Phase 2, tasks T021-T023). This phase focuses on validation and enhancement.

### Context Management Validation

- [ ] T071 [US5] Verify conversation history is fetched before each agent run in backend/app/routers/chat.py
- [ ] T072 [US5] Verify user and assistant messages are stored after each interaction in backend/app/routers/chat.py
- [ ] T073 [US5] Verify conversation.updated_at is updated on new messages in backend/app/routers/chat.py
- [ ] T074 [US5] Add conversation history limit (50 messages) to prevent token overflow in backend/app/routers/chat.py

### Agent Context Enhancement

- [ ] T075 [US5] Enhance SYSTEM_PROMPT with context handling guidelines in backend/agents/config.py
- [ ] T076 [US5] Add conversation context validation in agent runner in backend/agents/runner.py

**Checkpoint**: User Story 5 complete - multi-turn conversations maintain context correctly. All user stories (US1-US5) should work independently.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

### Error Handling Enhancement

- [ ] T077 [P] Add comprehensive error logging for all tool handlers in backend/mcp/handlers.py
- [ ] T078 [P] Add user-friendly error messages for common failures in backend/agents/runner.py
- [ ] T079 [P] Add timeout configuration for OpenAI API calls in backend/agents/config.py

### Performance Optimization

- [ ] T080 [P] Add database query optimization (indexes verified) in backend/alembic/versions/
- [ ] T081 [P] Add conversation history query limit enforcement in backend/app/routers/chat.py
- [ ] T082 [P] Add database connection pooling configuration in backend/app/database.py

### Security Hardening

- [ ] T083 [P] Verify JWT authentication on all chat endpoints in backend/app/routers/chat.py
- [ ] T084 [P] Verify user isolation in all tool handlers in backend/mcp/handlers.py
- [ ] T085 [P] Add input sanitization for message content in backend/app/routers/chat.py
- [ ] T086 [P] Verify OPENAI_API_KEY is never logged or exposed in backend/agents/config.py

### Documentation

- [ ] T087 [P] Update backend/README.md with MCP AI Chat setup instructions
- [ ] T088 [P] Update backend/.env.example with all required environment variables
- [ ] T089 [P] Add API documentation for chat endpoint in backend/app/routers/chat.py docstrings

### Validation

- [ ] T090 Run database migration and verify tables created: `alembic upgrade head`
- [ ] T091 Verify all 5 MCP tools are registered and functional
- [ ] T092 Verify agent correctly interprets natural language for all operations
- [ ] T093 Verify conversation history persists across requests
- [ ] T094 Verify user isolation enforced in all operations
- [ ] T095 Run quickstart.md validation with all example commands

**Checkpoint**: All polish tasks complete - system is production-ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - US2 (Phase 4): Can start after Foundational - No dependencies on other stories (but logically follows US1)
  - US3 (Phase 5): Can start after Foundational - No dependencies on other stories
  - US4 (Phase 6): Can start after Foundational - No dependencies on other stories
  - US5 (Phase 7): Validation phase - depends on foundational conversation system
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent - can be implemented and tested alone
- **User Story 2 (P1)**: Independent - can be implemented and tested alone (works best with US1 for creating test data)
- **User Story 3 (P2)**: Independent - can be implemented and tested alone (requires tasks to exist for testing)
- **User Story 4 (P3)**: Independent - can be implemented and tested alone (requires tasks to exist for testing)
- **User Story 5 (P2)**: Built on foundational conversation system - validates context management

### Within Each User Story

- MCP tool definition before handler implementation
- Handler implementation before tool registration
- Tool registration before agent integration
- Agent integration before endpoint integration
- All story tasks complete before moving to next priority

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks can run in parallel
- T001-T004 can all be done simultaneously

**Phase 2 (Foundational)**: Many tasks can run in parallel
- Database models (T005, T006) can be done in parallel
- Schemas (T010, T011, T012) can be done in parallel
- Error handling tasks (T025, T026, T027) can be done in parallel

**Phase 3-7 (User Stories)**: Entire user stories can be worked on in parallel by different developers
- Once Foundational is complete, US1, US2, US3, US4 can all start in parallel
- Within each story, tool definition tasks marked [P] can run in parallel

**Phase 8 (Polish)**: Most tasks can run in parallel
- Error handling (T077, T078, T079) in parallel
- Performance (T080, T081, T082) in parallel
- Security (T083, T084, T085, T086) in parallel
- Documentation (T087, T088, T089) in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch User Story 1 tasks:

# Parallel: Define tool and implement handler simultaneously
Task T028: "Define add_task tool schema in backend/mcp/tools.py"
Task T029: "Implement handle_add_task handler in backend/mcp/handlers.py"

# Sequential: Register tool after definition
Task T032: "Register add_task tool with MCP server" (depends on T028)

# Parallel: Agent integration tasks
Task T033: "Add add_task tool to agent tools list"
Task T034: "Implement agent runner with tool execution"
Task T035: "Add tool call logging"

# Sequential: Endpoint integration after agent ready
Task T036-T039: Chat endpoint integration (depends on T033-T035)
```

---

## Parallel Example: Multiple User Stories

```bash
# After Foundational phase completes, different developers can work on different stories:

Developer A: Phase 3 (User Story 1 - Task Creation)
  - Tasks T028-T039

Developer B: Phase 4 (User Story 2 - Task Querying)
  - Tasks T040-T047

Developer C: Phase 5 (User Story 3 - Task Completion)
  - Tasks T048-T056

# All three stories can be developed and tested independently
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T027) - CRITICAL
3. Complete Phase 3: User Story 1 (T028-T039)
4. Complete Phase 4: User Story 2 (T040-T047)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo MVP with task creation and querying

**MVP Scope**: 47 tasks (T001-T047)
**MVP Value**: Users can create and view tasks through natural language conversation

### Incremental Delivery

1. **Foundation** (T001-T027): Setup + Foundational → 27 tasks
2. **MVP** (T028-T047): Add US1 + US2 → 20 tasks → Deploy/Demo
3. **Enhancement 1** (T048-T056): Add US3 (Task Completion) → 9 tasks → Deploy/Demo
4. **Enhancement 2** (T057-T070): Add US4 (Update/Delete) → 14 tasks → Deploy/Demo
5. **Enhancement 3** (T071-T076): Validate US5 (Context) → 6 tasks → Deploy/Demo
6. **Polish** (T077-T095): Final improvements → 19 tasks → Production release

**Total Tasks**: 95 tasks
**Estimated Effort**: 5-6 days (per plan.md timeline)

### Parallel Team Strategy

With 3 developers after Foundational phase:

1. **Week 1, Days 1-2**: All developers complete Setup + Foundational together (T001-T027)
2. **Week 1, Days 3-5**: Parallel development
   - Developer A: User Story 1 (T028-T039)
   - Developer B: User Story 2 (T040-T047)
   - Developer C: User Story 3 (T048-T056)
3. **Week 2, Days 1-2**: Sequential or parallel
   - Developer A: User Story 4 (T057-T070)
   - Developer B: User Story 5 (T071-T076)
   - Developer C: Start Polish (T077-T089)
4. **Week 2, Day 3**: All developers complete validation (T090-T095)

---

## Task Summary

**Total Tasks**: 95
**By Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 23 tasks
- Phase 3 (US1 - Task Creation): 12 tasks
- Phase 4 (US2 - Task Querying): 8 tasks
- Phase 5 (US3 - Task Completion): 9 tasks
- Phase 6 (US4 - Update/Delete): 14 tasks
- Phase 7 (US5 - Context): 6 tasks
- Phase 8 (Polish): 19 tasks

**By User Story**:
- US1 (Natural Language Task Creation): 12 tasks
- US2 (Conversational Task Querying): 8 tasks
- US3 (Task Completion via Chat): 9 tasks
- US4 (Task Modification and Deletion): 14 tasks
- US5 (Multi-Turn Conversation Context): 6 tasks
- Infrastructure (Setup + Foundational + Polish): 46 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase

**MVP Scope**: First 47 tasks (Setup + Foundational + US1 + US2)

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **No test tasks**: Tests not explicitly requested in specification
- **Independent stories**: Each user story can be completed and tested independently
- **Stateless architecture**: Conversation history managed through database (foundational)
- **User isolation**: Enforced in all tool handlers and endpoint validation
- **Error handling**: Comprehensive error handling for AI service, database, and tool failures
- **Security**: JWT authentication, input validation, user isolation throughout
- **Performance**: Database indexes, query limits, connection pooling
- **Documentation**: Inline docstrings, README updates, API documentation

**Format Validation**: ✅ All 95 tasks follow the required checklist format with ID, optional [P] marker, optional [Story] label, and file paths
