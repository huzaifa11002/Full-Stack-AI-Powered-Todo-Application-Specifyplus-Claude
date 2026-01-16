# Implementation Plan: MCP AI Chat for Task Management

**Branch**: `001-mcp-ai-chat` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mcp-ai-chat/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build an AI-powered conversational interface for task management using MCP (Model Context Protocol) server architecture with OpenAI Agents SDK. The system enables users to create, query, complete, update, and delete tasks through natural language conversation. The implementation is completely stateless, storing all conversation history in the database and retrieving it before each agent invocation. The MCP server exposes 5 task operation tools that the AI agent can invoke based on user intent, with all operations enforcing user isolation and JWT authentication.

**Key Technical Approach**:
- MCP server with Official MCP SDK for tool definitions and invocation
- OpenAI Agents SDK for natural language understanding and tool selection
- Stateless FastAPI endpoint that fetches conversation history from database before each request
- Database schema extension with Conversation and Message models
- Tool handlers that interact directly with existing Task model
- Structured JSON responses including conversation_id, response text, and tool call logs

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (latest stable), OpenAI Agents SDK, Official MCP SDK, SQLModel, Pydantic v2, psycopg2-binary, python-dotenv, uvicorn[standard]
**Storage**: Neon Serverless PostgreSQL (existing database extended with Conversation and Message tables)
**Testing**: pytest for unit/integration tests, pytest-asyncio for async tests, httpx for API testing
**Target Platform**: Linux server (containerized with Docker, deployed to Kubernetes)
**Project Type**: Web application (backend API extension)
**Performance Goals**:
- API response time: 95th percentile under 3 seconds (including AI service latency)
- Conversation history retrieval: under 500ms for conversations with up to 50 messages
- Database query performance: task operations complete in under 100ms
- Concurrent user support: handle at least 100 simultaneous conversations
**Constraints**:
- Completely stateless architecture (no in-memory conversation state)
- Must integrate with existing Better Auth JWT middleware
- Must use existing Task model and endpoints
- OpenAI API rate limits and usage costs
- Response times depend on external AI service latency
**Scale/Scope**:
- 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- 2 new database models (Conversation, Message)
- 1 new API endpoint (POST /api/{user_id}/chat)
- Support for multi-turn conversations with context maintenance
- Typical conversations: fewer than 50 messages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

**✅ I. Production-Ready Code Quality**
- Type safety: Python 3.11+ with type hints for all function signatures
- Testing coverage: Target 70% backend coverage (unit + integration tests)
- Linting: Ruff for Python linting and formatting
- Architectural decisions: Will document in code comments and ADRs

**✅ II. Cloud-Native Architecture**
- Stateless design: Explicitly required - no in-memory conversation state
- Health checks: Will use existing FastAPI health endpoints
- Graceful shutdown: FastAPI handles SIGTERM by default
- Configuration: Environment variables for all secrets (OPENAI_API_KEY)
- Containerization: Extends existing Docker setup

**⚠️ III. AI Integration Excellence**
- ✅ Timeouts: Will implement for OpenAI API calls
- ✅ Graceful degradation: Error handling when AI service unavailable
- ❌ **VIOLATION**: Streaming responses - Constitution requires streaming, but spec explicitly excludes it
- ✅ Context management: Conversation history with token awareness
- ✅ Cost monitoring: Specified in requirements
- ✅ Rate limiting: Specified in requirements

**✅ IV. Security-First Approach**
- Secrets: OPENAI_API_KEY in environment variables
- JWT authentication: Using existing Better Auth middleware
- Rate limiting: Will implement on chat endpoint
- Input sanitization: Pydantic models for all API inputs
- Parameterized queries: SQLModel handles this automatically
- User isolation: Enforced at database query level

**✅ V. Developer Experience**
- Documentation: Will create quickstart.md and API documentation
- Local development: Extends existing docker-compose setup
- Environment configuration: .env file with clear documentation
- Consistent patterns: Follows existing FastAPI patterns

### Quality Gates

**Phase III Specific Gates (from Constitution)**:
- ✅ OpenAI API properly integrated with conversation context
- ✅ MCP SDK correctly implemented for tool/function calling
- ✅ Graceful degradation if AI service unavailable
- ✅ Cost monitoring for OpenAI API usage implemented
- ✅ Rate limiting enforced on AI endpoints
- ❌ **GATE FAILURE**: Streaming responses working correctly - NOT IMPLEMENTED

### Gate Decision

**Status**: ⚠️ CONDITIONAL PASS with documented violation

**Violation**: Streaming responses requirement from Constitution Section III (AI Integration Excellence) conflicts with feature spec which explicitly excludes streaming as "optional enhancement."

**Justification for Proceeding**:
1. **Why Needed**: Initial MVP focuses on core functionality (stateless conversation, tool invocation, context management). Streaming adds significant complexity to state management and error handling.
2. **Alternatives Considered**:
   - Implement streaming from start: Rejected due to 5-6 day timeline constraint and increased complexity
   - Use polling: Rejected as it doesn't provide real-time feedback
3. **Mitigation**:
   - Document streaming as Phase 2 enhancement in Future Enhancements section
   - Design API response format to be compatible with future streaming implementation
   - Keep response times under 3 seconds to minimize user wait time
4. **Review**: Requires technical lead approval to proceed without streaming

**Re-evaluation Point**: After Phase 1 design, verify that non-streaming approach meets user experience requirements (3-second response time target).

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-ai-chat/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (MCP SDK, OpenAI Agents SDK research)
├── data-model.md        # Phase 1 output (Conversation, Message models)
├── quickstart.md        # Phase 1 output (setup and usage guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.json   # MCP tool definitions
├── checklists/
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models.py                    # EXTEND: Add Conversation, Message models
│   ├── schemas.py                   # EXTEND: Add ChatRequest, ChatResponse, ToolCallInfo
│   ├── database.py                  # EXISTING: Database session management
│   ├── middleware/
│   │   └── auth.py                  # EXISTING: JWT authentication middleware
│   └── routers/
│       ├── tasks.py                 # EXISTING: Task CRUD endpoints
│       └── chat.py                  # NEW: Chat endpoint
│
├── mcp/                             # NEW: MCP server implementation
│   ├── __init__.py
│   ├── server.py                    # MCP server initialization
│   ├── tools.py                     # Tool definitions (5 tools)
│   └── handlers.py                  # Tool implementation logic
│
├── agents/                          # NEW: OpenAI Agents SDK integration
│   ├── __init__.py
│   ├── config.py                    # Agent configuration and system prompt
│   ├── agent.py                     # Agent definition with tools
│   └── runner.py                    # Agent runner with tool execution
│
├── tests/                           # EXTEND: Add new test files
│   ├── test_mcp_tools.py           # NEW: MCP tool handler tests
│   ├── test_agent.py               # NEW: Agent behavior tests
│   └── test_chat_endpoint.py       # NEW: Chat API integration tests
│
├── alembic/                         # EXTEND: Add migration for new models
│   └── versions/
│       └── xxx_add_conversation_message_models.py  # NEW: Database migration
│
├── requirements.txt                 # EXTEND: Add mcp, openai-agents-sdk
├── .env.example                     # EXTEND: Add OPENAI_API_KEY
└── main.py                          # EXTEND: Register chat router
```

**Structure Decision**: Web application (backend extension). This feature extends the existing FastAPI backend with new MCP and agent modules. The frontend (Next.js) is out of scope for this phase - it will consume the chat API in a future phase. The structure follows the existing backend organization with clear separation between MCP tools, agent logic, and API endpoints.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| No streaming responses (Constitution III) | MVP focuses on core stateless conversation with tool invocation. Streaming adds significant complexity to state management, error handling, and testing within 5-6 day timeline. | Implementing streaming from start: Rejected due to timeline constraints and need to validate core architecture first. Polling approach: Rejected as it doesn't provide real-time feedback and increases server load. |

**Mitigation Plan**:
- Design API response format to be compatible with future streaming (can add `stream: true` parameter later)
- Keep response times under 3 seconds through optimization (database query performance, efficient conversation history retrieval)
- Document streaming implementation as Phase 2 enhancement with clear migration path
- Monitor user feedback on response times to prioritize streaming work

---

## Phase 0: Research & Discovery

**Objective**: Resolve all technical unknowns and establish implementation patterns for MCP SDK and OpenAI Agents SDK integration.

### Research Tasks

1. **MCP SDK Integration Patterns**
   - Research: Official MCP SDK documentation and examples
   - Goal: Understand tool definition format, server initialization, and tool handler patterns
   - Output: Document MCP server setup, tool registration, and handler implementation patterns

2. **OpenAI Agents SDK Architecture**
   - Research: OpenAI Agents SDK documentation, agent configuration, and runner patterns
   - Goal: Understand how to create agents with tools, run agents with conversation history, and process tool calls
   - Output: Document agent creation, tool format conversion (MCP to OpenAI), and runner implementation

3. **Stateless Conversation Management**
   - Research: Best practices for stateless conversation systems with database-backed history
   - Goal: Design efficient conversation history retrieval and context management
   - Output: Document conversation state management strategy, database query patterns, and performance optimization

4. **Tool Invocation Flow**
   - Research: How OpenAI Agents SDK handles tool calls and how to integrate with MCP handlers
   - Goal: Design the flow from user message → agent → tool selection → MCP handler → database → response
   - Output: Sequence diagram showing complete request/response flow with tool invocation

5. **Error Handling Patterns**
   - Research: Best practices for handling AI service errors, database errors, and tool execution failures
   - Goal: Design comprehensive error handling strategy with graceful degradation
   - Output: Document error scenarios, handling strategies, and user-facing error messages

6. **Natural Language Understanding Optimization**
   - Research: System prompt engineering for task management domain
   - Goal: Design effective system prompts that guide the agent to correctly interpret user intent
   - Output: Document system prompt structure, tool usage guidelines, and example phrasings

### Research Output

**Deliverable**: `research.md` containing:
- MCP SDK setup and tool definition patterns
- OpenAI Agents SDK agent creation and runner implementation
- Stateless conversation management strategy
- Tool invocation sequence diagram
- Error handling patterns and strategies
- System prompt design for task management
- Technology decisions with rationale

**Success Criteria**:
- All "NEEDS CLARIFICATION" items from Technical Context resolved
- Clear implementation patterns documented for each component
- Sequence diagrams showing data flow
- No remaining technical unknowns before Phase 1

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete with all technical unknowns resolved

### 1.1 Data Model Design

**Objective**: Design database schema extensions for conversation and message storage.

**Deliverable**: `data-model.md` containing:

**Conversation Model**:
```python
class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

**Message Model**:
```python
class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(...)  # "user" or "assistant"
    content: str = Field(...)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

**Indexes**:
- `conversation.user_id` (for user isolation queries)
- `message.conversation_id` (for history retrieval)
- `message.user_id` (for user isolation queries)

**Validation Rules**:
- `role` must be "user" or "assistant"
- `content` cannot be empty
- `tool_calls` must be valid JSON if present
- `user_id` must reference existing user

**State Transitions**:
- Conversation: created → updated (timestamp changes on new messages)
- Message: created (immutable after creation)

### 1.2 API Contracts

**Objective**: Define OpenAPI specification for chat endpoint and MCP tool schemas.

**Deliverable**: `contracts/` directory containing:

**1. Chat API Contract** (`contracts/chat-api.yaml`):
```yaml
openapi: 3.0.0
info:
  title: AI Chat API
  version: 1.0.0
paths:
  /api/{user_id}/chat:
    post:
      summary: Send message to AI chat assistant
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                conversation_id:
                  type: integer
                  nullable: true
                message:
                  type: string
              required:
                - message
      responses:
        200:
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  conversation_id:
                    type: integer
                  response:
                    type: string
                  tool_calls:
                    type: array
                    items:
                      type: object
                      properties:
                        tool:
                          type: string
                        params:
                          type: object
                        result:
                          type: object
        403:
          description: Access denied
        404:
          description: Conversation not found
        500:
          description: Internal server error
```

**2. MCP Tool Definitions** (`contracts/mcp-tools.json`):
```json
{
  "tools": [
    {
      "name": "add_task",
      "description": "Create a new task for the user",
      "input_schema": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "title": {"type": "string"},
          "description": {"type": "string"}
        },
        "required": ["user_id", "title"]
      }
    },
    {
      "name": "list_tasks",
      "description": "Retrieve user's tasks with optional status filter",
      "input_schema": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "status": {
            "type": "string",
            "enum": ["all", "pending", "completed"],
            "default": "all"
          }
        },
        "required": ["user_id"]
      }
    },
    {
      "name": "complete_task",
      "description": "Mark a task as completed",
      "input_schema": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
      }
    },
    {
      "name": "delete_task",
      "description": "Remove a task from the list",
      "input_schema": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
      }
    },
    {
      "name": "update_task",
      "description": "Modify task title or description",
      "input_schema": {
        "type": "object",
        "properties": {
          "user_id": {"type": "string"},
          "task_id": {"type": "integer"},
          "title": {"type": "string"},
          "description": {"type": "string"}
        },
        "required": ["user_id", "task_id"]
      }
    }
  ]
}
```

### 1.3 Quickstart Guide

**Objective**: Provide setup and usage instructions for developers.

**Deliverable**: `quickstart.md` containing:
- Environment setup (OPENAI_API_KEY, dependencies)
- Database migration instructions
- Local development workflow
- API usage examples with curl/httpx
- Testing instructions
- Troubleshooting common issues

### 1.4 Agent Context Update

**Objective**: Update agent-specific context file with new technologies.

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Expected Updates**:
- Add "OpenAI Agents SDK" to technology list
- Add "Official MCP SDK" to technology list
- Add "Conversation and Message models" to data models list
- Preserve existing manual additions

---

## Phase 2: Task Generation

**Note**: This phase is handled by the `/sp.tasks` command, NOT by `/sp.plan`.

**Prerequisites**:
- Phase 0 research complete
- Phase 1 design artifacts complete
- Constitution Check re-evaluated and passed

**Output**: `tasks.md` with dependency-ordered implementation tasks

**Expected Task Categories**:
1. Database schema extension (Conversation, Message models, migration)
2. MCP server setup (server initialization, tool definitions, handlers)
3. OpenAI Agents SDK integration (agent configuration, agent definition, runner)
4. Chat endpoint implementation (request/response handling, conversation management)
5. Error handling and validation
6. Testing (unit tests, integration tests, end-to-end tests)
7. Documentation updates

---

## Implementation Phases (Detailed)

### Phase 1: Database Schema Extension

**Files Modified**: `backend/app/models.py`, `backend/alembic/versions/xxx_add_conversation_message_models.py`

**Tasks**:
1. Add Conversation model to models.py
2. Add Message model to models.py
3. Create Alembic migration script
4. Add indexes on user_id and conversation_id
5. Test migration on local database
6. Create sample data for testing

**Acceptance Criteria**:
- Models pass SQLModel validation
- Migration runs successfully
- Indexes created correctly
- Can create and query conversations and messages

### Phase 2: MCP Server Setup

**Files Created**: `backend/mcp/__init__.py`, `backend/mcp/server.py`, `backend/mcp/tools.py`, `backend/mcp/handlers.py`

**Tasks**:
1. Install MCP SDK (`pip install mcp`)
2. Create mcp/ directory structure
3. Initialize MCP server in server.py
4. Define 5 tools in tools.py
5. Implement tool handlers in handlers.py
6. Register tools with MCP server
7. Test tool invocation independently

**Acceptance Criteria**:
- MCP server initializes without errors
- All 5 tools registered correctly
- Tool handlers interact with database
- User isolation enforced in handlers

### Phase 3: OpenAI Agents SDK Integration

**Files Created**: `backend/agents/__init__.py`, `backend/agents/config.py`, `backend/agents/agent.py`, `backend/agents/runner.py`

**Tasks**:
1. Install OpenAI Agents SDK (`pip install openai-agents-sdk`)
2. Create agents/ directory structure
3. Configure OpenAI client in config.py
4. Define system prompt in config.py
5. Create agent with tools in agent.py
6. Implement agent runner in runner.py
7. Test agent with sample messages

**Acceptance Criteria**:
- Agent initializes with correct tools
- Agent correctly interprets natural language
- Agent selects appropriate tools
- Tool calls execute successfully

### Phase 4: Chat Endpoint Implementation

**Files Modified**: `backend/app/routers/chat.py`, `backend/app/schemas.py`, `backend/main.py`

**Tasks**:
1. Create ChatRequest and ChatResponse schemas
2. Implement chat endpoint in routers/chat.py
3. Implement conversation creation/retrieval logic
4. Implement conversation history fetching
5. Integrate agent runner
6. Store user and assistant messages
7. Register chat router in main.py

**Acceptance Criteria**:
- Endpoint creates new conversations
- Endpoint retrieves existing conversations
- Conversation history loaded correctly
- Agent processes messages successfully
- Responses stored in database

### Phase 5: Error Handling & Validation

**Files Modified**: All implementation files

**Tasks**:
1. Add error handling for AI service failures
2. Add error handling for database failures
3. Add validation for tool parameters
4. Add validation for conversation access
5. Implement graceful degradation
6. Add comprehensive logging

**Acceptance Criteria**:
- AI service errors handled gracefully
- Database errors don't crash server
- Invalid inputs rejected with clear messages
- Unauthorized access prevented
- All errors logged appropriately

### Phase 6: Testing

**Files Created**: `backend/tests/test_mcp_tools.py`, `backend/tests/test_agent.py`, `backend/tests/test_chat_endpoint.py`

**Tasks**:
1. Write unit tests for MCP tool handlers
2. Write unit tests for agent runner
3. Write integration tests for chat endpoint
4. Write end-to-end conversation flow tests
5. Test natural language variations
6. Test error scenarios
7. Achieve 70% code coverage

**Acceptance Criteria**:
- All tests pass
- 70% code coverage achieved
- Edge cases covered
- Error scenarios tested

---

## Architecture Decisions Requiring ADRs

Based on the detailed implementation plan provided, the following architectural decisions should be documented:

**ADR-001: MCP SDK Choice**
- **Decision**: Use Official MCP SDK for tool definitions
- **Context**: Need standard-compliant tool invocation mechanism
- **Alternatives**: Custom implementation, other protocol libraries
- **Consequences**: Standard compliance, community support, potential limitations

**ADR-002: Agent Model Selection**
- **Decision**: Use GPT-4o for production, GPT-4o-mini for development
- **Context**: Balance between accuracy, cost, and speed
- **Alternatives**: GPT-3.5-turbo (cheaper but less accurate), Claude (different API)
- **Consequences**: Higher accuracy, higher cost, OpenAI vendor lock-in

**ADR-003: Conversation Storage Strategy**
- **Decision**: Store all messages without summarization
- **Context**: Need complete conversation history for context
- **Alternatives**: Summarize old messages, implement message limits
- **Consequences**: Database growth, accurate context, potential token costs

**ADR-004: Stateless Architecture**
- **Decision**: No in-memory conversation state, fetch from database each request
- **Context**: Cloud-native scalability requirement
- **Alternatives**: In-memory caching, session-based state
- **Consequences**: Horizontal scalability, database load, simpler deployment

**ADR-005: No Streaming Responses (MVP)**
- **Decision**: Implement non-streaming responses initially
- **Context**: 5-6 day timeline, focus on core functionality
- **Alternatives**: Implement streaming from start, use polling
- **Consequences**: Simpler implementation, potential user wait time, future enhancement needed

---

## Success Criteria

### Phase 0 Complete
- ✅ All technical unknowns resolved
- ✅ Implementation patterns documented
- ✅ Sequence diagrams created
- ✅ No remaining "NEEDS CLARIFICATION" items

### Phase 1 Complete
- ✅ Data models designed and documented
- ✅ API contracts defined (OpenAPI + MCP tools)
- ✅ Quickstart guide created
- ✅ Agent context updated

### Phase 2 Complete (via /sp.tasks)
- ✅ Tasks generated with dependencies
- ✅ Acceptance criteria defined for each task
- ✅ Test cases identified

### Implementation Complete
- ✅ All 5 MCP tools functional
- ✅ Agent correctly interprets natural language
- ✅ Conversation history persists across requests
- ✅ Server is completely stateless
- ✅ JWT authentication enforced
- ✅ User isolation maintained
- ✅ Tool calls logged and returned
- ✅ Errors handled gracefully
- ✅ 70% test coverage achieved
- ✅ Response times under 3 seconds (95th percentile)

---

## Next Steps

1. **Immediate**: Create `research.md` (Phase 0)
2. **After Research**: Create `data-model.md`, `contracts/`, `quickstart.md` (Phase 1)
3. **After Design**: Run `/sp.tasks` to generate implementation tasks (Phase 2)
4. **After Tasks**: Begin implementation following task order
5. **During Implementation**: Create ADRs for architectural decisions
6. **After Implementation**: Run comprehensive tests and validate success criteria

