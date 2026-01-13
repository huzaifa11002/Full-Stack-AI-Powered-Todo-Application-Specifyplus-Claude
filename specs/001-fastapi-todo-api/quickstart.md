# Quickstart Guide: FastAPI Todo REST API

**Feature**: 001-fastapi-todo-api
**Date**: 2026-01-10
**Purpose**: Setup instructions and usage guide for developers

## Overview

This guide will help you set up and run the FastAPI Todo REST API on your local machine. The API provides complete CRUD operations for tasks with user isolation.

**Time to Complete**: 15-20 minutes
**Prerequisites**: Python 3.11+, Neon PostgreSQL account, internet connection

## Prerequisites

### Required Software

- **Python 3.11 or higher**: [Download Python](https://www.python.org/downloads/)
- **pip**: Included with Python
- **Git**: For cloning the repository
- **HTTP Client**: Postman, Thunder Client, or curl for testing

### Required Accounts

- **Neon PostgreSQL**: Free account at [neon.tech](https://neon.tech)

### Verify Prerequisites

```bash
# Check Python version (should be 3.11+)
python --version

# Check pip
pip --version

# Check Git
git --version
```

## Setup Instructions

### Step 1: Clone Repository and Checkout Branch

```bash
# Clone the repository
git clone <repository-url>
cd todo-app

# Checkout the feature branch
git checkout 001-fastapi-todo-api
```

### Step 2: Navigate to Backend Directory

```bash
cd backend
```

### Step 3: Create Python Virtual Environment

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**:
```bash
python -m venv venv
source venv/bin/activate
```

**Verify activation**: Your terminal prompt should show `(venv)` prefix.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output**: Installation of FastAPI, SQLModel, psycopg2-binary, python-dotenv, uvicorn, and pydantic.

**Troubleshooting**:
- If `psycopg2-binary` fails on Windows, install Visual C++ Build Tools
- If installation is slow, use: `pip install -r requirements.txt --no-cache-dir`

### Step 5: Create Neon Database

1. Go to [neon.tech](https://neon.tech) and sign up/login
2. Click "Create Project"
3. Choose a project name (e.g., "todo-app")
4. Select region closest to you
5. Click "Create Project"
6. Copy the connection string (looks like: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`)

### Step 6: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file and add your Neon connection string:
   ```
   DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
   ENVIRONMENT=development
   ```

**Important**: Never commit `.env` file to Git (it's in `.gitignore`).

### Step 7: Initialize Database

```bash
python init_db.py
```

**Expected output**:
```
Creating database tables...
Tables created successfully!
Seeding sample users...
Sample users created:
  - User 1: user1@example.com
  - User 2: user2@example.com
  - User 3: user3@example.com
Database initialization complete!
```

**Troubleshooting**:
- If connection fails, verify DATABASE_URL in `.env`
- Ensure Neon database is running (check Neon dashboard)
- Check firewall/network settings

### Step 8: Start the API Server

```bash
uvicorn app.main:app --reload
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Server is now running at**: `http://localhost:8000`

### Step 9: Verify Installation

Open your browser and navigate to:
- **API Root**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs (interactive Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

**Expected response** from health check:
```json
{
  "status": "healthy"
}
```

## API Usage

### Base URL

```
http://localhost:8000/api/{user_id}/tasks
```

### Authentication

**Note**: Authentication is not implemented in Phase II. Use pre-seeded user IDs (1, 2, 3) for testing.

### Available Endpoints

#### 1. List All Tasks for User

**Request**:
```http
GET /api/1/tasks
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread, and vegetables",
    "is_completed": false,
    "created_at": "2026-01-10T10:00:00Z",
    "updated_at": "2026-01-10T10:00:00Z"
  }
]
```

#### 2. Create New Task

**Request**:
```http
POST /api/1/tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread, and vegetables"
}
```

**Response** (201 Created):
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

#### 3. Get Task Details

**Request**:
```http
GET /api/1/tasks/1
```

**Response** (200 OK):
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

#### 4. Update Task

**Request**:
```http
PUT /api/1/tasks/1
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "description": "Updated shopping list",
  "is_completed": true
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries and cook dinner",
  "description": "Updated shopping list",
  "is_completed": true,
  "created_at": "2026-01-10T10:00:00Z",
  "updated_at": "2026-01-10T15:00:00Z"
}
```

#### 5. Toggle Task Completion

**Request**:
```http
PATCH /api/1/tasks/1/toggle
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": true,
  "created_at": "2026-01-10T10:00:00Z",
  "updated_at": "2026-01-10T15:00:00Z"
}
```

#### 6. Delete Task

**Request**:
```http
DELETE /api/1/tasks/1
```

**Response** (204 No Content):
```
(empty response body)
```

### Error Responses

#### 404 Not Found
```json
{
  "detail": "Task not found or access denied"
}
```

#### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "type": "string_too_short"
    }
  ]
}
```

#### 500 Server Error
```json
{
  "detail": "Internal server error"
}
```

## Testing with HTTP Clients

### Using curl

**Create Task**:
```bash
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs"}'
```

**List Tasks**:
```bash
curl http://localhost:8000/api/1/tasks
```

**Get Task**:
```bash
curl http://localhost:8000/api/1/tasks/1
```

**Update Task**:
```bash
curl -X PUT http://localhost:8000/api/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title", "is_completed": true}'
```

**Toggle Task**:
```bash
curl -X PATCH http://localhost:8000/api/1/tasks/1/toggle
```

**Delete Task**:
```bash
curl -X DELETE http://localhost:8000/api/1/tasks/1
```

### Using Postman

1. Open Postman
2. Import the OpenAPI spec from `specs/001-fastapi-todo-api/contracts/openapi.yaml`
3. Set base URL to `http://localhost:8000`
4. Test each endpoint using the imported collection

### Using Thunder Client (VS Code)

1. Install Thunder Client extension in VS Code
2. Create new request
3. Set method and URL (e.g., `GET http://localhost:8000/api/1/tasks`)
4. Add headers if needed (Content-Type: application/json)
5. Add request body for POST/PUT requests
6. Click "Send"

## Development Workflow

### Making Changes

1. **Edit code** in `backend/app/` directory
2. **Server auto-reloads** (thanks to `--reload` flag)
3. **Test changes** with HTTP client
4. **Check logs** in terminal for errors
5. **Iterate** until working

### Running Linter

```bash
# Check code style
ruff check .

# Format code
ruff format .
```

### Checking Types

```bash
mypy app/
```

### Stopping the Server

Press `CTRL+C` in the terminal where uvicorn is running.

### Deactivating Virtual Environment

```bash
deactivate
```

## Common Issues & Solutions

### Issue: "Module not found" error

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Database connection fails

**Solution**:
1. Verify DATABASE_URL in `.env` file
2. Check Neon dashboard - ensure database is running
3. Test connection string in a PostgreSQL client
4. Ensure `?sslmode=require` is in connection string

### Issue: Port 8000 already in use

**Solution**: Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: "Table already exists" error

**Solution**: Drop and recreate tables:
```bash
# Connect to Neon database and run:
DROP TABLE tasks;
DROP TABLE users;

# Then run init_db.py again
python init_db.py
```

### Issue: CORS errors from frontend

**Solution**: CORS is configured to allow all origins in development. If issues persist, check `main.py` CORS middleware configuration.

## Next Steps

### For Development

1. **Implement endpoints** following the plan in `plan.md`
2. **Test each endpoint** before moving to the next
3. **Document issues** encountered
4. **Commit changes** regularly

### For Testing

1. **Create test collection** in Postman/Thunder Client
2. **Test all user stories** from `spec.md`
3. **Verify user isolation** with multiple user IDs
4. **Test edge cases** (invalid input, missing fields, etc.)

### For Production

1. **Add authentication** (Spec 2)
2. **Configure CORS** for specific frontend origin
3. **Set up monitoring** and logging
4. **Deploy to cloud** platform
5. **Configure HTTPS** and SSL certificates

## Additional Resources

- **API Documentation**: http://localhost:8000/docs (when server running)
- **Feature Spec**: `specs/001-fastapi-todo-api/spec.md`
- **Implementation Plan**: `specs/001-fastapi-todo-api/plan.md`
- **Data Model**: `specs/001-fastapi-todo-api/data-model.md`
- **OpenAPI Contract**: `specs/001-fastapi-todo-api/contracts/openapi.yaml`

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the implementation plan and spec
3. Check FastAPI documentation: https://fastapi.tiangolo.com/
4. Check SQLModel documentation: https://sqlmodel.tiangolo.com/

## Quick Reference

### Sample User IDs (Pre-seeded)
- User 1: `user1@example.com`
- User 2: `user2@example.com`
- User 3: `user3@example.com`

### API Endpoints Summary
- `GET /api/{user_id}/tasks` - List tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `PATCH /api/{user_id}/tasks/{task_id}/toggle` - Toggle completion
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `GET /health` - Health check

### Status Codes
- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error
