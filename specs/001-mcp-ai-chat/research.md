# Research: MCP AI Chat Implementation

**Feature**: 001-mcp-ai-chat
**Date**: 2026-01-13
**Phase**: Phase 0 - Research & Discovery

## Overview

This document consolidates research findings for implementing an AI-powered conversational task management system using MCP (Model Context Protocol) SDK and OpenAI Agents SDK. The research resolves all technical unknowns identified in the implementation plan and establishes concrete patterns for implementation.

---

## 1. MCP SDK Integration Patterns

### 1.1 MCP SDK Overview

**Model Context Protocol (MCP)** is a standardized protocol for defining and invoking tools/functions that AI agents can use. The Official MCP SDK provides:
- Standardized tool definition format (JSON Schema)
- Server initialization and tool registration
- Tool invocation handling
- Type-safe parameter validation

### 1.2 MCP Server Setup Pattern

**Installation**:
```bash
pip install mcp
```

**Server Initialization**:
```python
from mcp import MCPServer

# Initialize MCP server
mcp_server = MCPServer(
    name="todo-mcp-server",
    version="1.0.0",
    description="MCP server for task management operations"
)
```

### 1.3 Tool Definition Pattern

**Tool Structure**:
```python
from mcp import Tool

tool = Tool(
    name="tool_name",
    description="Clear description of what the tool does",
    input_schema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param1"]
    }
)
```

**Best Practices**:
- Use clear, descriptive tool names (verb_noun format: add_task, list_tasks)
- Provide detailed descriptions for AI agent understanding
- Use JSON Schema for parameter validation
- Mark required parameters explicitly
- Include parameter descriptions for agent context

### 1.4 Tool Handler Pattern

**Handler Function Signature**:
```python
async def handle_tool_name(params: dict, session: Session) -> dict:
    """
    Tool handler implementation

    Args:
        params: Validated parameters from tool invocation
        session: Database session for data operations

    Returns:
        dict: Structured result with status and data
    """
    # Extract parameters
    user_id = params["user_id"]

    # Perform operation
    result = perform_operation(user_id, session)

    # Return structured response
    return {
        "status": "success",
        "data": result
    }
```

**Handler Best Practices**:
- Always validate user_id for user isolation
- Use database session passed as parameter (stateless)
- Return structured JSON responses
- Include error information in response (don't raise exceptions)
- Log operations for debugging and auditing

### 1.5 Tool Registration Pattern

```python
# Register tool with handler
mcp_server.add_tool(tool, handler_function)

# Register multiple tools
tools_and_handlers = [
    (add_task_tool, handle_add_task),
    (list_tasks_tool, handle_list_tasks),
    (complete_task_tool, handle_complete_task),
    (delete_task_tool, handle_delete_task),
    (update_task_tool, handle_update_task),
]

for tool, handler in tools_and_handlers:
    mcp_server.add_tool(tool, handler)
```

**Decision**: Use Official MCP SDK for standard compliance and community support.

---

## 2. OpenAI Agents SDK Architecture

### 2.1 OpenAI Agents SDK Overview

**OpenAI Agents SDK** provides:
- Agent creation with system instructions
- Tool/function calling integration
- Conversation history management
- Streaming and non-streaming responses
- Tool execution handling

### 2.2 Agent Configuration Pattern

**Installation**:
```bash
pip install openai-agents-sdk openai
```

**Configuration Setup**:
```python
import os
from openai import OpenAI

# OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Agent configuration
AGENT_MODEL = os.getenv("AGENT_MODEL", "gpt-4o")
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
AGENT_MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "1000"))

# System prompt
SYSTEM_PROMPT = """You are a helpful task management assistant..."""
```

**Best Practices**:
- Use environment variables for configuration
- Provide sensible defaults
- Keep system prompt focused and clear
- Use appropriate temperature (0.7 for conversational, 0.0 for deterministic)

### 2.3 Tool Format Conversion

**MCP to OpenAI Function Format**:
```python
def mcp_tool_to_openai_function(mcp_tool):
    """Convert MCP tool definition to OpenAI function format"""
    return {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.input_schema
        }
    }
```

**Rationale**: OpenAI Agents SDK expects tools in OpenAI function calling format, while MCP SDK uses its own format. This conversion function bridges the two.

### 2.4 Agent Creation Pattern

```python
from openai_agents import Agent

# Create agent with tools
agent = Agent(
    name="todo-assistant",
    model=AGENT_MODEL,
    instructions=SYSTEM_PROMPT,
    tools=[
        mcp_tool_to_openai_function(tool1),
        mcp_tool_to_openai_function(tool2),
        # ... more tools
    ],
    temperature=AGENT_TEMPERATURE
)
```

### 2.5 Agent Runner Pattern

**Runner Implementation**:
```python
from openai_agents import Runner
import json

async def run_agent(
    messages: List[Dict[str, str]],
    user_id: str,
    session: Session
) -> Dict:
    """
    Run agent with conversation history

    Args:
        messages: Conversation history [{"role": "user/assistant", "content": "..."}]
        user_id: Current user ID for tool execution
        session: Database session

    Returns:
        {
            "response": str,
            "tool_calls": List[Dict],
            "error": str (optional)
        }
    """
    try:
        # Create runner
        runner = Runner(
            agent=agent,
            client=openai_client
        )

        # Run agent with messages
        result = await runner.run(messages=messages)

        # Extract response
        assistant_message = result.messages[-1]
        response_text = assistant_message.content

        # Process tool calls
        tool_calls_info = []
        if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_params = json.loads(tool_call.function.arguments)

                # Add user_id to params
                tool_params["user_id"] = user_id

                # Execute tool via MCP handler
                handler = TOOL_HANDLERS.get(tool_name)
                if handler:
                    tool_result = await handler(tool_params, session)
                    tool_calls_info.append({
                        "tool": tool_name,
                        "params": tool_params,
                        "result": tool_result
                    })

        return {
            "response": response_text,
            "tool_calls": tool_calls_info,
            "error": None
        }

    except Exception as e:
        return {
            "response": "I encountered an error processing your request. Please try again.",
            "tool_calls": [],
            "error": str(e)
        }
```

**Decision**: Use GPT-4o for production (best accuracy), GPT-4o-mini for development (cost savings).

---

## 3. Stateless Conversation Management

### 3.1 Stateless Architecture Principles

**Key Principles**:
1. No in-memory conversation state between requests
2. All conversation data stored in database
3. Conversation history fetched from database before each request
4. Each request is independent and self-contained

**Benefits**:
- Horizontal scalability (any server can handle any request)
- No session affinity required
- Simpler deployment and recovery
- No state loss on server restart

### 3.2 Conversation History Retrieval Pattern

**Efficient Query Pattern**:
```python
from sqlmodel import Session, select

def get_conversation_history(
    conversation_id: int,
    session: Session,
    limit: int = 50
) -> List[Dict[str, str]]:
    """
    Retrieve conversation history from database

    Args:
        conversation_id: Conversation identifier
        session: Database session
        limit: Maximum messages to retrieve (default 50)

    Returns:
        List of message dicts [{"role": "user/assistant", "content": "..."}]
    """
    # Query messages ordered by creation time
    query = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .limit(limit)
    )

    messages = session.exec(query).all()

    # Convert to agent format
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

**Performance Optimization**:
- Index on `conversation_id` for fast retrieval
- Limit query to recent messages (50 default, configurable)
- Order by `created_at` for chronological history
- Use eager loading if relationships needed

### 3.3 Conversation State Management Strategy

**Request Flow**:
1. Receive user message with optional conversation_id
2. Get or create conversation
3. Fetch conversation history from database
4. Append new user message to history (in memory)
5. Run agent with complete history
6. Store user message in database
7. Store assistant response in database
8. Return response to user

**Database Operations**:
```python
# Get or create conversation
if conversation_id:
    conversation = session.get(Conversation, conversation_id)
else:
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

# Fetch history
history = get_conversation_history(conversation.id, session)

# Store user message
user_message = Message(
    conversation_id=conversation.id,
    user_id=user_id,
    role="user",
    content=request.message
)
session.add(user_message)
session.commit()

# Run agent with history + new message
history.append({"role": "user", "content": request.message})
agent_result = await run_agent(history, user_id, session)

# Store assistant response
assistant_message = Message(
    conversation_id=conversation.id,
    user_id=user_id,
    role="assistant",
    content=agent_result["response"],
    tool_calls=json.dumps(agent_result["tool_calls"])
)
session.add(assistant_message)
session.commit()
```

**Decision**: Store all messages without summarization initially. Optimize later if needed based on performance metrics.

---

## 4. Tool Invocation Flow

### 4.1 Complete Request/Response Flow

**Sequence Diagram**:
```
User → API Endpoint → Database → Agent → MCP Tools → Database → API Endpoint → User

Detailed Flow:
1. User sends message to POST /api/{user_id}/chat
2. API validates JWT token and user_id
3. API gets or creates conversation in database
4. API fetches conversation history from database
5. API stores user message in database
6. API calls agent runner with history + new message
7. Agent analyzes message and selects appropriate tool(s)
8. Agent invokes MCP tool(s) with parameters
9. MCP handler executes database operations
10. MCP handler returns structured result
11. Agent generates natural language response
12. API stores assistant response (with tool calls) in database
13. API returns response to user
```

### 4.2 Tool Invocation Pattern

**Agent Tool Selection**:
- Agent receives conversation history and new user message
- Agent analyzes user intent using system prompt guidance
- Agent selects appropriate tool(s) based on intent
- Agent extracts parameters from user message
- Agent invokes tool(s) with parameters

**Tool Execution**:
- MCP handler receives validated parameters
- Handler adds user_id to parameters (from request context)
- Handler performs database operation
- Handler returns structured result
- Agent receives result and incorporates into response

**Response Generation**:
- Agent generates natural language response based on tool results
- Agent confirms action taken ("✓ Added task: Buy groceries")
- Agent provides relevant details from tool results
- Agent asks for clarification if needed

### 4.3 Tool Handler Mapping

```python
# Map tool names to handler functions
TOOL_HANDLERS = {
    "add_task": handle_add_task,
    "list_tasks": handle_list_tasks,
    "complete_task": handle_complete_task,
    "delete_task": handle_delete_task,
    "update_task": handle_update_task,
}

# Execute tool in agent runner
handler = TOOL_HANDLERS.get(tool_name)
if handler:
    tool_result = await handler(tool_params, session)
else:
    tool_result = {"error": f"Unknown tool: {tool_name}"}
```

---

## 5. Error Handling Patterns

### 5.1 Error Categories

**1. AI Service Errors**:
- OpenAI API unavailable
- Rate limit exceeded
- Invalid API key
- Timeout

**2. Database Errors**:
- Connection failure
- Query timeout
- Constraint violation
- Transaction rollback

**3. Tool Execution Errors**:
- Task not found
- Invalid parameters
- User isolation violation
- Business logic error

**4. Validation Errors**:
- Invalid conversation_id
- Unauthorized access
- Malformed request
- Missing required fields

### 5.2 Error Handling Strategy

**AI Service Error Handling**:
```python
try:
    result = await runner.run(messages=messages)
except openai.APIError as e:
    logger.error(f"OpenAI API error: {str(e)}")
    return {
        "response": "I'm having trouble connecting to my AI service. Please try again in a moment.",
        "tool_calls": [],
        "error": "ai_service_unavailable"
    }
except openai.RateLimitError as e:
    logger.error(f"Rate limit exceeded: {str(e)}")
    return {
        "response": "I'm receiving too many requests right now. Please try again in a moment.",
        "tool_calls": [],
        "error": "rate_limit_exceeded"
    }
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    return {
        "response": "I encountered an unexpected error. Please try again.",
        "tool_calls": [],
        "error": "unknown_error"
    }
```

**Database Error Handling**:
```python
try:
    session.commit()
except IntegrityError as e:
    session.rollback()
    logger.error(f"Database integrity error: {str(e)}")
    raise HTTPException(500, "Failed to save conversation")
except Exception as e:
    session.rollback()
    logger.error(f"Database error: {str(e)}")
    raise HTTPException(500, "Database operation failed")
```

**Tool Execution Error Handling**:
```python
async def handle_complete_task(params: dict, session: Session) -> dict:
    try:
        user_id = params["user_id"]
        task_id = params["task_id"]

        # Fetch task with user validation
        task = session.exec(
            select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
        ).first()

        if not task:
            return {
                "status": "error",
                "error": "Task not found",
                "message": "The task you're trying to complete doesn't exist or you don't have access to it."
            }

        # Perform operation
        task.is_completed = True
        session.add(task)
        session.commit()

        return {
            "status": "success",
            "task_id": task.id,
            "title": task.title
        }

    except Exception as e:
        logger.error(f"Tool execution error: {str(e)}")
        return {
            "status": "error",
            "error": "execution_failed",
            "message": "Failed to complete the task. Please try again."
        }
```

### 5.3 User-Facing Error Messages

**Principles**:
- Never expose technical details to users
- Provide actionable guidance when possible
- Be friendly and conversational
- Log technical details for debugging

**Error Message Examples**:
- AI service unavailable: "I'm having trouble connecting to my AI service. Please try again in a moment."
- Task not found: "I couldn't find that task. Could you try listing your tasks first?"
- Unauthorized access: "You don't have permission to access that conversation."
- Ambiguous request: "I'm not sure what you'd like me to do. Could you be more specific?"

**Decision**: User-friendly messages in responses, technical details in logs.

---

## 6. Natural Language Understanding Optimization

### 6.1 System Prompt Design

**Effective System Prompt Structure**:
```python
SYSTEM_PROMPT = """You are a helpful task management assistant that helps users manage their todo list through natural conversation.

TOOL USAGE GUIDELINES:

1. ADD TASK (add_task):
   - Trigger phrases: "add", "create", "remember", "new task", "I need to"
   - Extract task title from user message
   - Include relevant details in description
   - Examples: "Add buy groceries", "Remember to call mom", "I need to finish report"

2. LIST TASKS (list_tasks):
   - Trigger phrases: "show", "list", "what are", "see my", "display"
   - Status filters:
     * "all" - default, shows everything
     * "pending" - only incomplete tasks
     * "completed" - only finished tasks
   - Examples: "Show my tasks", "What's pending?", "List completed items"

3. COMPLETE TASK (complete_task):
   - Trigger phrases: "done", "complete", "finish", "mark as done"
   - Requires task ID or description to identify task
   - Examples: "Mark task 3 as done", "I finished the report", "Task 5 is complete"

4. DELETE TASK (delete_task):
   - Trigger phrases: "delete", "remove", "cancel", "get rid of"
   - May require listing tasks first if only description provided
   - Examples: "Delete task 2", "Remove the meeting", "Cancel shopping task"

5. UPDATE TASK (update_task):
   - Trigger phrases: "change", "update", "modify", "rename", "edit"
   - Requires task ID and new title/description
   - Examples: "Change task 1 to...", "Update the meeting time", "Rename task 3"

CONVERSATION GUIDELINES:
- Always confirm actions taken ("✓ Added task: Buy groceries")
- If task ID is ambiguous, list tasks first
- Be friendly and conversational
- Handle errors gracefully (task not found, invalid input)
- Summarize tool results in natural language
- If user intent is unclear, ask for clarification

Remember: You must use the appropriate tool for each request. Never simulate tool results.
"""
```

**Key Elements**:
1. Clear role definition
2. Explicit tool usage guidelines with trigger phrases
3. Examples for each tool
4. Conversation guidelines for tone and behavior
5. Error handling guidance

### 6.2 Intent Recognition Patterns

**Common User Phrasings**:
- Create: "add", "create", "new", "remember", "I need to", "don't forget"
- Read: "show", "list", "what", "see", "display", "tell me"
- Update: "change", "update", "modify", "edit", "rename", "fix"
- Delete: "delete", "remove", "cancel", "get rid of", "forget"
- Complete: "done", "complete", "finish", "mark as done", "finished"

**Ambiguity Handling**:
- Multiple tasks with similar names: Ask for clarification with task IDs
- Unclear intent: Ask clarifying questions
- Missing information: Prompt for required details

### 6.3 Response Formatting

**Confirmation Messages**:
- Task created: "✓ Added task: {title}"
- Task listed: "Here are your tasks: [formatted list]"
- Task completed: "✓ Marked '{title}' as complete"
- Task deleted: "✓ Removed task: {title}"
- Task updated: "✓ Updated task {id}: {new_title}"

**Error Messages**:
- Task not found: "I couldn't find that task. Would you like to see your task list?"
- Ambiguous reference: "I found multiple tasks matching that description. Which one did you mean? [list with IDs]"
- Invalid operation: "I can't do that. [explanation]"

**Decision**: Use detailed system prompt with explicit tool usage guidelines and example phrasings.

---

## 7. Technology Decisions Summary

### 7.1 Core Technologies

| Technology | Decision | Rationale |
|------------|----------|-----------|
| MCP SDK | Official MCP SDK | Standard compliance, community support |
| AI Model | GPT-4o (prod), GPT-4o-mini (dev) | Best accuracy vs cost balance |
| Conversation Storage | Store all messages | Accurate context, optimize later if needed |
| Architecture | Stateless (database-backed) | Horizontal scalability, cloud-native |
| Streaming | Not implemented (MVP) | Timeline constraints, future enhancement |
| Error Handling | User-friendly messages + technical logs | Better UX, debugging capability |

### 7.2 Implementation Patterns

| Component | Pattern | Key Benefit |
|-----------|---------|-------------|
| Tool Definition | JSON Schema with MCP SDK | Type safety, validation |
| Tool Handlers | Async functions with structured returns | Consistent interface |
| Agent Configuration | Environment variables | Flexibility, security |
| Conversation History | Database query with limit | Performance, scalability |
| Tool Invocation | Handler mapping dictionary | Extensibility |
| Error Handling | Try-catch with graceful degradation | Reliability |

---

## 8. Performance Considerations

### 8.1 Database Query Optimization

**Indexes Required**:
- `conversation.user_id` (user isolation queries)
- `message.conversation_id` (history retrieval)
- `message.created_at` (chronological ordering)

**Query Optimization**:
- Limit conversation history to 50 messages (configurable)
- Use `select()` with explicit columns if needed
- Avoid N+1 queries with eager loading

### 8.2 AI Service Optimization

**Token Management**:
- Monitor conversation history length
- Implement token counting if needed
- Consider summarization for very long conversations (future)

**Response Time**:
- Target: 95th percentile under 3 seconds
- OpenAI API typically responds in 1-2 seconds
- Database queries should be under 100ms
- Total overhead (excluding AI): under 500ms

### 8.3 Scalability Considerations

**Horizontal Scaling**:
- Stateless architecture enables multiple server instances
- No session affinity required
- Database connection pooling for efficiency

**Database Scaling**:
- Neon DB handles connection pooling
- Consider read replicas for high read load (future)
- Monitor database performance metrics

---

## 9. Security Considerations

### 9.1 Authentication & Authorization

**JWT Validation**:
- Use existing Better Auth middleware
- Validate user_id matches token
- Reject unauthorized requests with 403

**User Isolation**:
- All database queries filter by user_id
- Tool handlers validate user_id
- Conversation access restricted to owner

### 9.2 Input Validation

**Request Validation**:
- Use Pydantic models for all API inputs
- Validate conversation_id exists and belongs to user
- Sanitize user message content

**Tool Parameter Validation**:
- MCP SDK validates against JSON Schema
- Additional business logic validation in handlers
- Reject invalid parameters with clear errors

### 9.3 Secrets Management

**Environment Variables**:
- `OPENAI_API_KEY`: OpenAI API key (required)
- `AGENT_MODEL`: Model name (default: gpt-4o)
- `AGENT_TEMPERATURE`: Temperature setting (default: 0.7)
- `DATABASE_URL`: Neon DB connection string (existing)

**Best Practices**:
- Never commit secrets to version control
- Use `.env` file for local development
- Use Kubernetes secrets for production
- Rotate API keys regularly

---

## 10. Testing Strategy

### 10.1 Unit Testing

**MCP Tool Handlers**:
- Test each handler independently
- Mock database session
- Verify correct database operations
- Test error scenarios

**Agent Runner**:
- Test with mock OpenAI responses
- Verify tool call extraction
- Test error handling

### 10.2 Integration Testing

**Chat Endpoint**:
- Test full request/response flow
- Verify conversation creation
- Verify history retrieval
- Test authentication
- Test user isolation

**End-to-End**:
- Test complete conversation flows
- Test multi-turn conversations
- Test all 5 task operations
- Test natural language variations

### 10.3 Test Coverage Goals

- Backend: 70% code coverage minimum
- Critical paths: 100% coverage
- Error scenarios: Comprehensive coverage
- Edge cases: Documented and tested

---

## 11. Monitoring & Observability

### 11.1 Logging Strategy

**Log Levels**:
- INFO: Request/response, tool invocations
- WARNING: Recoverable errors, rate limits
- ERROR: Unrecoverable errors, exceptions

**Log Content**:
- Request ID for tracing
- User ID (for debugging, not PII)
- Tool calls and results
- Error messages and stack traces
- Performance metrics (response times)

### 11.2 Metrics to Track

**Performance Metrics**:
- API response time (p50, p95, p99)
- Database query time
- OpenAI API latency
- Conversation history retrieval time

**Business Metrics**:
- Conversations created
- Messages per conversation
- Tool invocations by type
- Error rates by category

**Cost Metrics**:
- OpenAI API token usage
- Cost per conversation
- Cost per user

---

## 12. Next Steps

### 12.1 Immediate Actions

1. ✅ Research complete - all technical unknowns resolved
2. → Proceed to Phase 1: Design & Contracts
   - Create data-model.md
   - Create contracts/ directory with API specs
   - Create quickstart.md
   - Update agent context

### 12.2 Implementation Readiness

**Ready to Implement**:
- ✅ MCP SDK integration patterns established
- ✅ OpenAI Agents SDK architecture defined
- ✅ Stateless conversation management strategy designed
- ✅ Tool invocation flow documented
- ✅ Error handling patterns established
- ✅ System prompt design completed

**No Remaining Unknowns**:
- All "NEEDS CLARIFICATION" items resolved
- Implementation patterns documented
- Technology decisions made with rationale
- Performance and security considerations addressed

---

## Conclusion

This research document provides comprehensive guidance for implementing the MCP AI Chat feature. All technical unknowns have been resolved, and clear implementation patterns have been established for each component. The architecture is designed for scalability, reliability, and maintainability while meeting the 5-6 day timeline constraint.

**Key Takeaways**:
1. Use Official MCP SDK for standard-compliant tool definitions
2. Use OpenAI Agents SDK with GPT-4o for best accuracy
3. Implement stateless architecture with database-backed conversation history
4. Design comprehensive error handling with graceful degradation
5. Use detailed system prompts for effective natural language understanding
6. Prioritize user experience with friendly error messages
7. Monitor performance and costs for optimization opportunities

The implementation can now proceed to Phase 1 (Design & Contracts) with confidence.
