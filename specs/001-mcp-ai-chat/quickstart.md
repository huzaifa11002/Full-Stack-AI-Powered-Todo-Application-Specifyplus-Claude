# Quickstart Guide: MCP AI Chat

**Feature**: 001-mcp-ai-chat
**Date**: 2026-01-13
**Phase**: Phase 1 - Design & Contracts

## Overview

This guide provides step-by-step instructions for setting up and using the MCP AI Chat feature for local development. Follow these instructions to get the AI-powered conversational task management system running on your machine.

---

## Prerequisites

**Required**:
- Python 3.11 or higher
- PostgreSQL database (Neon DB account or local PostgreSQL)
- OpenAI API key
- Git
- pip (Python package manager)

**Recommended**:
- Virtual environment tool (venv, virtualenv, or conda)
- Postman or curl for API testing
- VS Code or PyCharm for development

---

## 1. Environment Setup

### 1.1 Clone Repository

```bash
git clone <repository-url>
cd todo-app
git checkout 001-mcp-ai-chat
```

### 1.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 1.3 Install Dependencies

```bash
# Navigate to backend directory
cd backend

# Install existing dependencies
pip install -r requirements.txt

# Install new dependencies for MCP AI Chat
pip install mcp openai-agents-sdk openai
```

### 1.4 Configure Environment Variables

Create or update `.env` file in the `backend/` directory:

```bash
# Existing variables
DATABASE_URL=postgresql://user:password@host:5432/database
BETTER_AUTH_SECRET=your-secret-key

# New variables for MCP AI Chat
OPENAI_API_KEY=sk-your-openai-api-key-here
AGENT_MODEL=gpt-4o
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=1000
```

**Getting an OpenAI API Key**:
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

**Important**: Never commit your `.env` file to version control!

---

## 2. Database Migration

### 2.1 Run Migration

The migration adds two new tables: `conversations` and `messages`.

```bash
# Navigate to backend directory (if not already there)
cd backend

# Run Alembic migration
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Running upgrade xxx -> yyy, Add Conversation and Message models
```

### 2.2 Verify Migration

Connect to your database and verify the new tables exist:

```sql
-- Check conversations table
SELECT * FROM conversations LIMIT 1;

-- Check messages table
SELECT * FROM messages LIMIT 1;

-- Verify indexes
\d conversations
\d messages
```

**Expected Tables**:
- `conversations` with columns: id, user_id, created_at, updated_at
- `messages` with columns: id, conversation_id, user_id, role, content, tool_calls, created_at

---

## 3. Local Development

### 3.1 Start Development Server

```bash
# From backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3.2 Verify Server is Running

Open your browser and navigate to:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

---

## 4. API Usage Examples

### 4.1 Authentication

First, obtain a JWT token using the existing authentication endpoint:

```bash
# Register or login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1
}
```

Save the `access_token` for subsequent requests.

### 4.2 Start New Conversation

```bash
# Send first message (creates new conversation)
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

**Response**:
```json
{
  "conversation_id": 1,
  "response": "✓ I've added 'Buy groceries' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "params": {
        "user_id": "1",
        "title": "Buy groceries"
      },
      "result": {
        "task_id": 5,
        "status": "created",
        "title": "Buy groceries"
      }
    }
  ]
}
```

### 4.3 Continue Conversation

```bash
# Send follow-up message in same conversation
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "conversation_id": 1,
    "message": "Show me my tasks"
  }'
```

**Response**:
```json
{
  "conversation_id": 1,
  "response": "Here are your tasks:\n1. Buy groceries (ID: 5)",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "params": {
        "user_id": "1",
        "status": "all"
      },
      "result": {
        "tasks": [
          {
            "id": 5,
            "title": "Buy groceries",
            "description": "",
            "completed": false,
            "created_at": "2026-01-13T10:00:00Z"
          }
        ],
        "count": 1,
        "status": "success"
      }
    }
  ]
}
```

### 4.4 Complete Task

```bash
curl -X POST http://localhost:8000/api/1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "conversation_id": 1,
    "message": "Mark task 5 as complete"
  }'
```

### 4.5 Natural Language Variations

The AI assistant understands various phrasings:

```bash
# Create task
"Add a task to call mom"
"I need to remember to buy milk"
"Create a new task: finish report"

# List tasks
"Show me my tasks"
"What do I need to do?"
"List all my todos"

# Complete task
"Mark task 3 as done"
"I finished the report"
"Task 5 is complete"

# Delete task
"Delete task 2"
"Remove the grocery task"
"Cancel that task"

# Update task
"Change task 1 to 'Buy groceries and cook dinner'"
"Update the meeting task"
"Rename task 3"
```

---

## 5. Testing

### 5.1 Run Unit Tests

```bash
# From backend directory
pytest tests/test_mcp_tools.py -v
pytest tests/test_agent.py -v
pytest tests/test_chat_endpoint.py -v
```

### 5.2 Run All Tests with Coverage

```bash
pytest --cov=app --cov=mcp --cov=agents --cov-report=html
```

**View Coverage Report**:
Open `htmlcov/index.html` in your browser.

### 5.3 Test Individual Components

**Test MCP Tools**:
```bash
pytest tests/test_mcp_tools.py::test_add_task -v
```

**Test Agent**:
```bash
pytest tests/test_agent.py::test_agent_add_task -v
```

**Test Chat Endpoint**:
```bash
pytest tests/test_chat_endpoint.py::test_chat_endpoint -v
```

---

## 6. Development Workflow

### 6.1 Making Changes

1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** to code

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Run linter**:
   ```bash
   ruff check .
   ruff format .
   ```

5. **Commit changes**:
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

### 6.2 Hot Reload

The development server automatically reloads when you make changes to Python files. No need to restart the server manually.

### 6.3 Debugging

**Enable Debug Logging**:
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Use Python Debugger**:
```python
# Add breakpoint in code
import pdb; pdb.set_trace()
```

---

## 7. Troubleshooting

### 7.1 Common Issues

**Issue**: `ModuleNotFoundError: No module named 'mcp'`
**Solution**: Install MCP SDK: `pip install mcp`

**Issue**: `openai.AuthenticationError: Invalid API key`
**Solution**: Check your `OPENAI_API_KEY` in `.env` file

**Issue**: `sqlalchemy.exc.OperationalError: could not connect to server`
**Solution**: Verify `DATABASE_URL` in `.env` and ensure database is running

**Issue**: `HTTPException: 403 Access denied`
**Solution**: Ensure JWT token is valid and user_id in URL matches authenticated user

**Issue**: `Agent returns "I encountered an error"`
**Solution**: Check server logs for detailed error message. Common causes:
- OpenAI API rate limit exceeded
- Invalid tool parameters
- Database connection issues

### 7.2 Checking Logs

**View Server Logs**:
```bash
# Server logs are printed to console
# Look for ERROR or WARNING messages
```

**Check Database Logs**:
```bash
# Connect to database and check recent queries
# Look for failed queries or constraint violations
```

### 7.3 Resetting Database

**Warning**: This will delete all data!

```bash
# Downgrade migration
alembic downgrade -1

# Upgrade again
alembic upgrade head
```

---

## 8. Configuration Options

### 8.1 Agent Configuration

Customize agent behavior in `.env`:

```bash
# Model selection
AGENT_MODEL=gpt-4o          # Best accuracy (higher cost)
# AGENT_MODEL=gpt-4o-mini   # Good accuracy (lower cost)
# AGENT_MODEL=gpt-3.5-turbo # Fast (lowest cost, less accurate)

# Temperature (0.0 = deterministic, 1.0 = creative)
AGENT_TEMPERATURE=0.7

# Max tokens in response
AGENT_MAX_TOKENS=1000
```

### 8.2 Database Configuration

```bash
# Connection pool size
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10

# Query timeout (seconds)
DATABASE_QUERY_TIMEOUT=30
```

### 8.3 API Configuration

```bash
# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Rate limiting
RATE_LIMIT_PER_MINUTE=60
```

---

## 9. Performance Optimization

### 9.1 Database Optimization

**Monitor Query Performance**:
```sql
-- Check slow queries
SELECT * FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check index usage
SELECT * FROM pg_stat_user_indexes
WHERE schemaname = 'public';
```

**Optimize Conversation History Retrieval**:
```python
# Limit history to recent messages
CONVERSATION_HISTORY_LIMIT = 50  # Configurable
```

### 9.2 AI Service Optimization

**Monitor Token Usage**:
- Check OpenAI dashboard for usage statistics
- Implement token counting if needed
- Consider summarization for long conversations

**Reduce Latency**:
- Use `gpt-4o-mini` for development (faster, cheaper)
- Implement caching for common queries (future)
- Use streaming responses (future enhancement)

---

## 10. Next Steps

### 10.1 After Setup

1. ✅ Environment configured
2. ✅ Database migrated
3. ✅ Server running
4. ✅ API tested
5. → Start implementing features (see `tasks.md` after running `/sp.tasks`)

### 10.2 Additional Resources

**Documentation**:
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/agents)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

**API Contracts**:
- OpenAPI spec: `specs/001-mcp-ai-chat/contracts/chat-api.yaml`
- MCP tools: `specs/001-mcp-ai-chat/contracts/mcp-tools.json`

**Design Documents**:
- Implementation plan: `specs/001-mcp-ai-chat/plan.md`
- Research findings: `specs/001-mcp-ai-chat/research.md`
- Data model: `specs/001-mcp-ai-chat/data-model.md`

---

## 11. Support

### 11.1 Getting Help

**Issues**:
- Check troubleshooting section above
- Review server logs for error messages
- Check OpenAI API status: https://status.openai.com/

**Questions**:
- Review design documents in `specs/001-mcp-ai-chat/`
- Check API documentation at http://localhost:8000/docs
- Review test files for usage examples

### 11.2 Contributing

**Before submitting PR**:
1. Run all tests: `pytest`
2. Run linter: `ruff check . && ruff format .`
3. Verify 70% code coverage: `pytest --cov`
4. Update documentation if needed
5. Add tests for new features

---

## Summary

**Quick Start Commands**:
```bash
# 1. Setup
git checkout 001-mcp-ai-chat
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install mcp openai-agents-sdk openai

# 2. Configure
# Edit .env file with OPENAI_API_KEY and DATABASE_URL

# 3. Migrate
alembic upgrade head

# 4. Run
uvicorn main:app --reload

# 5. Test
curl -X POST http://localhost:8000/api/1/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

**You're ready to start developing!** 🚀
