# Backend Dockerfile Contract

**Feature**: 001-docker-containerization
**Date**: 2026-01-18
**Purpose**: Specification for the FastAPI backend production Dockerfile

## Contract Overview

This contract defines the requirements and structure for the backend production Dockerfile that creates an optimized FastAPI container image.

## Requirements

### Functional Requirements
- **FR-001**: MUST use python:3.11-slim as base image
- **FR-002**: MUST implement multi-stage build (builder → runner)
- **FR-003**: MUST produce image <150MB in size
- **FR-004**: MUST run as non-root user (appuser, UID 1001)
- **FR-005**: MUST expose port 8000
- **FR-006**: MUST implement HEALTHCHECK directive
- **FR-007**: MUST use Python virtual environment
- **FR-008**: MUST install postgresql-client for database connectivity
- **FR-009**: MUST copy app/, agents/, and mcp/ directories
- **FR-010**: MUST use uvicorn as ASGI server

### Non-Functional Requirements
- **NFR-001**: Build MUST complete in <10 minutes on standard hardware
- **NFR-002**: Layer caching MUST be optimized (requirements.txt before source)
- **NFR-003**: Image MUST pass Docker Scout vulnerability scan
- **NFR-004**: Health check MUST respond in <1 second

## Dockerfile Structure

### Stage 1: Builder
```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
```

**Purpose**: Install dependencies with build tools in isolated stage
**Output**: /opt/venv/ with all Python packages

### Stage 2: Runner (Final Image)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# Copy application code
COPY --chown=appuser:appuser ./app ./app
COPY --chown=appuser:appuser ./agents ./agents
COPY --chown=appuser:appuser ./mcp ./mcp

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Purpose**: Create minimal runtime image with only required files
**Output**: Production-ready container image

## Environment Variables

### Runtime Variables (from .env)
- `DATABASE_URL`: Neon PostgreSQL connection string (required)
- `BETTER_AUTH_SECRET`: Authentication secret (required)
- `OPENAI_API_KEY`: OpenAI API key (required)
- `AGENT_MODEL`: AI model identifier (default: gpt-4o)
- `FRONTEND_URL`: Frontend URL (optional)
- `PATH=/opt/venv/bin:$PATH`: Virtual environment path (set in Dockerfile)

## Dependencies

### Required Files
- `requirements.txt`: Python dependencies
- `app/`: FastAPI application code
- `app/main.py`: FastAPI app with /health endpoint
- `agents/`: AI agent code
- `mcp/`: MCP server code

### Required Configuration
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ... other endpoints
```

## Build Commands

### Build Production Image
```bash
docker build -t todo-backend:latest -f backend/Dockerfile ./backend
```

### Build with Tag
```bash
docker build -t todo-backend:v1.0.0 -f backend/Dockerfile ./backend
```

### Build with Gordon AI
```bash
docker ai "Build an optimized FastAPI production image from ./backend"
```

## Validation

### Size Validation
```bash
docker images todo-backend:latest --format "{{.Size}}"
# Expected: <150MB
```

### User Validation
```bash
docker run --rm todo-backend:latest whoami
# Expected: appuser
```

### Health Check Validation
```bash
docker run -d --name test-backend -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host/db" \
  -e BETTER_AUTH_SECRET="test-secret" \
  -e OPENAI_API_KEY="sk-test" \
  todo-backend:latest

sleep 40  # Wait for start period
docker inspect test-backend --format='{{.State.Health.Status}}'
# Expected: healthy
docker rm -f test-backend
```

### Port Validation
```bash
docker run -d --name test-backend -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host/db" \
  -e BETTER_AUTH_SECRET="test-secret" \
  -e OPENAI_API_KEY="sk-test" \
  todo-backend:latest

curl http://localhost:8000/health
# Expected: {"status":"healthy"}
docker rm -f test-backend
```

### Database Connectivity
```bash
docker run -d --name test-backend -p 8000:8000 \
  -e DATABASE_URL="your-neon-url" \
  -e BETTER_AUTH_SECRET="test-secret" \
  -e OPENAI_API_KEY="sk-test" \
  todo-backend:latest

# Check logs for successful database connection
docker logs test-backend
docker rm -f test-backend
```

## Error Handling

### Build Failures
- **pip install fails**: Check requirements.txt syntax and package availability
- **gcc not found**: Verify system dependencies installed in builder stage
- **COPY fails**: Check directories exist in build context

### Runtime Failures
- **Container exits immediately**: Check CMD and uvicorn configuration
- **Health check fails**: Verify /health endpoint exists and responds
- **Permission denied**: Verify non-root user has access to required files
- **Database connection fails**: Check DATABASE_URL and network connectivity

## Security Considerations

- ✅ Non-root user (appuser, UID 1001)
- ✅ Minimal base image (slim)
- ✅ No secrets in image layers
- ✅ Virtual environment isolation
- ✅ Health check for monitoring
- ✅ Proper file ownership (chown appuser:appuser)
- ✅ Build tools excluded from final image

## Performance Optimization

### Layer Caching
1. Install system dependencies first (changes rarely)
2. Copy requirements.txt (changes less frequently)
3. Install Python packages (cached if requirements unchanged)
4. Copy source code last (changes most frequently)

### Image Size Optimization
- Use slim base (smaller than full Python)
- Multi-stage build (exclude gcc and build tools)
- Virtual environment (clean dependency isolation)
- Clean apt cache (rm -rf /var/lib/apt/lists/*)

### Build Speed Optimization
- Leverage Docker layer caching
- Use --no-cache-dir for pip (no cache storage)
- Parallel stage execution where possible

## Testing Strategy

### Build Testing
```bash
# Test build succeeds
docker build -t test-backend ./backend

# Test image size
SIZE=$(docker images test-backend --format "{{.Size}}")
echo "Image size: $SIZE"

# Test non-root user
docker run --rm test-backend whoami
```

### Runtime Testing
```bash
# Test container starts
docker run -d --name test-backend -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host/db" \
  -e BETTER_AUTH_SECRET="test-secret" \
  -e OPENAI_API_KEY="sk-test" \
  test-backend

# Test health check
sleep 40
docker inspect test-backend --format='{{.State.Health.Status}}'

# Test HTTP response
curl http://localhost:8000/health

# Test API endpoint
curl http://localhost:8000/docs  # OpenAPI docs

# Cleanup
docker rm -f test-backend
```

## Acceptance Criteria

- ✅ Dockerfile builds without errors
- ✅ Image size is <150MB
- ✅ Container runs as non-root user (appuser)
- ✅ Health check endpoint responds with 200 OK
- ✅ Container starts in <30 seconds
- ✅ Port 8000 is accessible
- ✅ Environment variables are loaded correctly
- ✅ Database connection succeeds
- ✅ No vulnerabilities in Docker Scout scan

## Related Contracts

- [frontend-dockerfile.contract.md](./frontend-dockerfile.contract.md) - Frontend Dockerfile specification
- [docker-compose.contract.md](./docker-compose.contract.md) - Docker Compose specification
- [../data-model.md](../data-model.md) - Docker artifacts data model

## Version History

- v1.0.0 (2026-01-18): Initial contract specification
