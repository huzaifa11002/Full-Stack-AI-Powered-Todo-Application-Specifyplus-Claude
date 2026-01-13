# FastAPI Todo REST API

Multi-user todo application with user isolation, built with FastAPI, SQLModel, and Neon PostgreSQL.

## Features

- ✅ RESTful API with 6 CRUD endpoints
- ✅ User isolation (users can only access their own tasks)
- ✅ Type-safe database operations with SQLModel
- ✅ Pydantic validation for all requests/responses
- ✅ Automatic API documentation with OpenAPI/Swagger
- ✅ Health check endpoint for monitoring
- ✅ CORS support for frontend integration

## Tech Stack

- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.14
- **Database**: Neon Serverless PostgreSQL
- **Validation**: Pydantic 2.10+
- **Server**: Uvicorn with auto-reload

## Prerequisites

- Python 3.11 or higher
- Neon PostgreSQL account (free tier available at [neon.tech](https://neon.tech))
- Git (for cloning the repository)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-app/backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

1. Create a Neon PostgreSQL account at [neon.tech](https://neon.tech)
2. Create a new project and database
3. Copy the connection string (it should look like: `postgresql://user:password@host.neon.tech/dbname?sslmode=require`)
4. Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
```

### 5. Initialize Database

```bash
python init_db.py
```

This will:
- Create the `users` and `tasks` tables
- Seed 3 sample users for testing (user1@example.com, user2@example.com, user3@example.com)

### 6. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Health Check

```http
GET /health
```

**Response**: `200 OK`
```json
{
  "status": "healthy"
}
```

### List All Tasks for User

```http
GET /api/{user_id}/tasks
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "is_completed": false,
    "created_at": "2026-01-10T10:00:00Z",
    "updated_at": "2026-01-10T10:00:00Z"
  }
]
```

### Create New Task

```http
POST /api/{user_id}/tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_completed": false,
  "created_at": "2026-01-10T10:00:00Z",
  "updated_at": "2026-01-10T10:00:00Z"
}
```

### Get Task Details

```http
GET /api/{user_id}/tasks/{task_id}
```

**Response**: `200 OK` or `404 Not Found` (if task doesn't exist or belongs to another user)

### Update Task

```http
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "description": "Updated shopping list",
  "is_completed": true
}
```

**Response**: `200 OK`

### Toggle Task Completion

```http
PATCH /api/{user_id}/tasks/{task_id}/toggle
```

**Response**: `200 OK` (toggles `is_completed` between true/false)

### Delete Task

```http
DELETE /api/{user_id}/tasks/{task_id}
```

**Response**: `204 No Content`

## Testing with cURL

### Create a task
```bash
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk and eggs"}'
```

### List all tasks
```bash
curl http://localhost:8000/api/1/tasks
```

### Get task details
```bash
curl http://localhost:8000/api/1/tasks/1
```

### Update task
```bash
curl -X PUT http://localhost:8000/api/1/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and cook", "is_completed": true}'
```

### Toggle completion
```bash
curl -X PATCH http://localhost:8000/api/1/tasks/1/toggle
```

### Delete task
```bash
curl -X DELETE http://localhost:8000/api/1/tasks/1
```

## User Isolation

The API enforces strict user isolation:
- Users can only access their own tasks
- Attempting to access another user's task returns `404 Not Found`
- The `user_id` in the URL path determines task ownership

**Example**:
```bash
# User 1 creates a task
curl -X POST http://localhost:8000/api/1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "User 1 task"}'

# User 2 cannot access User 1's task
curl http://localhost:8000/api/2/tasks/1
# Returns: 404 Not Found
```

## Sample Users

The database is pre-seeded with 3 test users:

| User ID | Email | Username |
|---------|-------|----------|
| 1 | user1@example.com | user1 |
| 2 | user2@example.com | user2 |
| 3 | user3@example.com | user3 |

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET/PUT/PATCH request
- `201 Created` - Successful POST request
- `204 No Content` - Successful DELETE request
- `404 Not Found` - Task not found or access denied
- `422 Unprocessable Entity` - Validation error (invalid input)
- `500 Internal Server Error` - Server error

## Validation Rules

### Task Title
- **Required**: Yes
- **Min Length**: 1 character
- **Max Length**: 200 characters
- **Validation**: Cannot be empty or whitespace-only

### Task Description
- **Required**: No
- **Max Length**: 2000 characters

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── database.py      # Database engine and session management
│   ├── models.py        # SQLModel database models
│   ├── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── __init__.py
│       └── tasks.py     # Task CRUD endpoints
├── .env                 # Environment variables (not committed)
├── .env.example         # Environment variables template
├── .gitignore           # Python gitignore
├── requirements.txt     # Python dependencies
├── init_db.py           # Database initialization script
└── README.md            # This file
```

## Development

### Running with Auto-Reload

```bash
uvicorn app.main:app --reload
```

The server will automatically restart when you make code changes.

### Accessing API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the Swagger UI interface.

## Troubleshooting

### Database Connection Failed

**Error**: `ValueError: DATABASE_URL environment variable is not set`

**Solution**: Create a `.env` file with your Neon database connection string.

### Port Already in Use

**Error**: `[Errno 10048] error while attempting to bind on address`

**Solution**: Either kill the process using port 8000 or start the server on a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Make sure you're running commands from the `backend/` directory and your virtual environment is activated.

## Next Steps

This is Phase II of the full-stack AI-powered todo application. Future phases include:

- **Phase III**: Next.js frontend with AI chatbot integration
- **Phase IV**: Kubernetes deployment
- **Phase V**: Cloud production deployment

## License

This project is part of the Full-Stack AI-Powered Todo Application specification.
