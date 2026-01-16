---
name: todo-mcp-server
description: Build a stateless MCP server for Todo AI Chatbot using Official MCP SDK and Neon PostgreSQL. Use when implementing MCP tools for task management.
---

# MCP Server – Todo Task Operations

## Instructions

### 1. **MCP Server Principles**
- Use Official MCP SDK only
- MCP server must be stateless
- No in-memory variables
- No agent or conversation logic
- Database is the single source of truth

---

### 2. **Exposed MCP Tools**

#### Tool: add_task
Purpose: Create a new task  
Parameters:
- user_id (string, required)
- title (string, required)
- description (string, optional)

Returns:
- task_id
- status
- title

---

#### Tool: list_tasks
Purpose: Retrieve tasks  
Parameters:
- user_id (string, required)
- status (string, optional: all | pending | completed)

Returns:
- Array of task objects

---

#### Tool: complete_task
Purpose: Mark task as completed  
Parameters:
- user_id (string, required)
- task_id (integer, required)

Returns:
- task_id
- status
- title

---

#### Tool: delete_task
Purpose: Delete a task  
Parameters:
- user_id (string, required)
- task_id (integer, required)

Returns:
- task_id
- status
- title

---

#### Tool: update_task
Purpose: Update task title or description  
Parameters:
- user_id (string, required)
- task_id (integer, required)
- title (string, optional)
- description (string, optional)

Returns:
- task_id
- status
- title

---

### 3. **Database Enforcement (Neon + SQLModel)**
- Every query must filter by user_id
- Never expose another user’s tasks
- Ensure task existence before mutation
- Use transactions for write operations

---

### 4. **Error Handling Rules**
- Task not found → return structured error
- Invalid parameters → return validation error
- Never raise raw exceptions to agent

---

### 5. **Tool Behavior Guarantees**
- Tools are deterministic
- Tools are idempotent where possible
- Tools do not depend on call order
- Tools do not store state between calls

---

## Successful MCP Server Criteria
- All tools callable by OpenAI Agents SDK
- Agent controls logic, MCP controls data
- Stateless execution guaranteed
- Ready for horizontal scaling
