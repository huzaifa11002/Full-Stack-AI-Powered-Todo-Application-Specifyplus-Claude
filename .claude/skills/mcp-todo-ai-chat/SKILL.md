---
name: mcp-todo-ai-chat
description: Implement a stateless AI-powered Todo chatbot using OpenAI Agents SDK, MCP server tools, FastAPI, and Neon DB. Use when building or validating conversational task management systems.
---

# Todo AI Chatbot with MCP & OpenAI Agents SDK

## Instructions

### 1. **Stateless Chat Architecture**
- Each `/api/{user_id}/chat` request is independent
- No in-memory session or agent state
- Conversation history is fetched from database every time
- Messages are persisted before and after agent execution

### 2. **Agent Configuration**
- Use OpenAI Agents SDK
- Provide agent with:
  - Clear behavior rules
  - MCP tools for task operations
  - Full conversation history
- Agent must decide when to call tools
- No manual routing or if/else task logic

### 3. **MCP Server Tools**
Expose the following stateless tools:

- **add_task**
  - Create a new task for user
- **list_tasks**
  - Retrieve tasks (all / pending / completed)
- **complete_task**
  - Mark task as completed
- **delete_task**
  - Remove task
- **update_task**
  - Update title or description

All tools:
- Require user_id
- Persist changes directly to Neon DB
- Return structured responses as defined

### 4. **Natural Language → Tool Mapping**
Agent must interpret user intent:
- "add / remember / create" → add_task
- "show / list / see" → list_tasks
- "done / complete" → complete_task
- "delete / remove" → delete_task
- "change / update" → update_task

For ambiguous requests:
- Ask clarifying question
- Or list tasks before action

### 5. **Database Models (SQLModel)**
- Task: user_id, title, description, completed, timestamps
- Conversation: user_id, timestamps
- Message: user_id, conversation_id, role, content

### 6. **Response Rules**
- Always confirm tool actions in friendly language
- Mention task title in confirmation
- Return tool_calls for transparency
- Handle errors gracefully (task not found, invalid ID)

## Successful Execution Criteria
- User can manage todos via natural language
- Agent consistently uses MCP tools
- No backend state leakage
- Conversation history persists correctly
- System scales horizontally
