# Docker Compose Contract

**Feature**: 001-docker-containerization
**Date**: 2026-01-18
**Purpose**: Specification for Docker Compose orchestration of frontend and backend services

## Contract Overview

This contract defines the requirements and structure for Docker Compose configurations that orchestrate the Todo Chatbot application services.

## Requirements

### Functional Requirements
- **FR-001**: MUST define frontend and backend services
- **FR-002**: MUST configure bridge network for inter-container communication
- **FR-003**: MUST load environment variables from .env file
- **FR-004**: MUST expose ports 3000 (frontend) and 8000 (backend)
- **FR-005**: MUST configure service dependencies (frontend depends on backend)
- **FR-006**: MUST support volume mounts for development hot-reload
- **FR-007**: MUST provide separate configurations for development and production

### Non-Functional Requirements
- **NFR-001**: Services MUST start in correct order (backend before frontend)
- **NFR-002**: DNS resolution MUST work between services
- **NFR-003**: Environment variables MUST be validated before container start
- **NFR-004**: Compose up MUST complete in <2 minutes

## Docker Compose Structure

### Development Configuration (docker-compose.yml)

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - BETTER_AUTH_URL=http://localhost:3000
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    depends_on:
      - backend
    networks:
      - todo-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - AGENT_MODEL=${AGENT_MODEL}
      - FRONTEND_URL=http://frontend:3000
    volumes:
      - ./backend:/app
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge
```

**Purpose**: Local development with hot-reload support
**Features**: Volume mounts, development Dockerfiles, no restart policy

### Production Configuration (docker-compose.prod.yml)

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    image: ${DOCKER_REGISTRY}/todo-frontend:${VERSION:-latest}
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - todo-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    image: ${DOCKER_REGISTRY}/todo-backend:${VERSION:-latest}
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge
```

**Purpose**: Production deployment with optimized images
**Features**: Production Dockerfiles, restart policy, image tagging

## Environment Variables

### Required Variables (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Authentication
BETTER_AUTH_SECRET=your-secret-key-here

# OpenAI
OPENAI_API_KEY=sk-...
AGENT_MODEL=gpt-4o

# Docker Registry (production only)
DOCKER_REGISTRY=yourusername
VERSION=latest
```

### Variable Validation
- `DATABASE_URL`: Must be valid PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Minimum 32 characters
- `OPENAI_API_KEY`: Must start with "sk-"
- `DOCKER_REGISTRY`: Required for production
- `VERSION`: Semantic version or "latest"

## Service Configuration

### Frontend Service

**Build Context**: `./frontend`
**Dockerfile**: `Dockerfile.dev` (dev) / `Dockerfile` (prod)
**Ports**: `3000:3000` (host:container)
**Dependencies**: backend (starts after backend)
**Network**: todo-network

**Environment Variables**:
- `NEXT_PUBLIC_API_URL`: Backend API URL (http://backend:8000)
- `BETTER_AUTH_SECRET`: Shared authentication secret
- `BETTER_AUTH_URL`: Frontend URL (http://localhost:3000)

**Volumes (Development Only)**:
- `./frontend:/app`: Source code mount
- `/app/node_modules`: Anonymous volume (exclude from mount)
- `/app/.next`: Anonymous volume (exclude from mount)

### Backend Service

**Build Context**: `./backend`
**Dockerfile**: `Dockerfile.dev` (dev) / `Dockerfile` (prod)
**Ports**: `8000:8000` (host:container)
**Network**: todo-network

**Environment Variables**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Shared authentication secret
- `OPENAI_API_KEY`: OpenAI API key
- `AGENT_MODEL`: AI model identifier (default: gpt-4o)
- `FRONTEND_URL`: Frontend URL (http://frontend:3000)

**Volumes (Development Only)**:
- `./backend:/app`: Source code mount

### Network Configuration

**Network Name**: todo-network
**Driver**: bridge
**DNS**: Docker embedded DNS server
**Isolation**: Isolated from host and other networks

**Service Discovery**:
- Frontend resolves "backend" to backend container IP
- Backend resolves "frontend" to frontend container IP
- Services communicate via service names (not IPs)

## Commands

### Development Commands

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Check service status
docker-compose ps

# Stop all services
docker-compose down

# Rebuild images
docker-compose build

# Rebuild and start
docker-compose up --build
```

### Production Commands

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down

# Rebuild images
docker-compose -f docker-compose.prod.yml build

# Push images to registry
docker-compose -f docker-compose.prod.yml push
```

## Validation

### Service Startup Validation
```bash
# Start services
docker-compose up -d

# Wait for services to be healthy
sleep 40

# Check service status
docker-compose ps

# Expected: Both services "Up" and healthy
```

### Network Validation
```bash
# Inspect network
docker network inspect todo-app_todo-network

# Check DNS resolution from frontend
docker-compose exec frontend nslookup backend

# Check DNS resolution from backend
docker-compose exec backend nslookup frontend
```

### Communication Validation
```bash
# Test frontend → backend
docker-compose exec frontend wget -O- http://backend:8000/health

# Test host → frontend
curl http://localhost:3000/api/health

# Test host → backend
curl http://localhost:8000/health
```

### Environment Variable Validation
```bash
# Check frontend environment
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL

# Check backend environment
docker-compose exec backend env | grep DATABASE_URL
```

## Error Handling

### Common Issues

**Port Already in Use**:
```bash
# Error: Bind for 0.0.0.0:3000 failed: port is already allocated
# Solution: Stop conflicting service or change port mapping
docker-compose down
# Or change ports in docker-compose.yml
```

**Environment Variable Missing**:
```bash
# Error: DATABASE_URL not set
# Solution: Create .env file from .env.example
cp .env.example .env
# Edit .env with actual values
```

**Service Won't Start**:
```bash
# Check logs for errors
docker-compose logs backend

# Common causes:
# - Missing environment variables
# - Database connection failure
# - Port conflicts
# - Build failures
```

**Network Issues**:
```bash
# Frontend can't reach backend
# Solution: Verify both services on same network
docker network inspect todo-app_todo-network

# Verify DNS resolution
docker-compose exec frontend nslookup backend
```

## Testing Strategy

### Integration Testing
```bash
# Start services
docker-compose up -d

# Wait for health checks
sleep 40

# Test frontend health
curl http://localhost:3000/api/health
# Expected: {"status":"healthy"}

# Test backend health
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test frontend → backend communication
curl http://localhost:3000/api/tasks
# Expected: Task list or authentication error

# Cleanup
docker-compose down
```

### Hot-Reload Testing (Development)
```bash
# Start development services
docker-compose up -d

# Make code change in frontend
echo "// test change" >> frontend/app/page.tsx

# Verify hot-reload (check logs)
docker-compose logs -f frontend
# Expected: Recompiling message

# Make code change in backend
echo "# test change" >> backend/app/main.py

# Verify auto-reload (check logs)
docker-compose logs -f backend
# Expected: Reloading message

# Cleanup
docker-compose down
```

## Performance Characteristics

### Startup Performance
- Initial build: <10 minutes (both services)
- Subsequent starts: <30 seconds (cached images)
- Health check ready: <40 seconds (start period)

### Resource Usage
- Frontend container: ~100MB RAM, 0.1 CPU
- Backend container: ~200MB RAM, 0.2 CPU
- Network overhead: Minimal (<1ms latency)

### Development Hot-Reload
- Frontend: <3 seconds to reflect changes
- Backend: <3 seconds to reflect changes

## Security Considerations

- ✅ Environment variables from .env (not hardcoded)
- ✅ .env file in .gitignore (secrets not committed)
- ✅ Network isolation (bridge network)
- ✅ Non-root users in containers
- ✅ Restart policy for production (unless-stopped)

## Acceptance Criteria

- ✅ docker-compose up starts both services successfully
- ✅ Services communicate via service names (DNS resolution)
- ✅ Environment variables loaded from .env file
- ✅ Frontend accessible at http://localhost:3000
- ✅ Backend accessible at http://localhost:8000
- ✅ Health checks pass for both services
- ✅ Volume mounts enable hot-reload in development
- ✅ Production configuration uses optimized images
- ✅ Services restart automatically in production

## Related Contracts

- [frontend-dockerfile.contract.md](./frontend-dockerfile.contract.md) - Frontend Dockerfile specification
- [backend-dockerfile.contract.md](./backend-dockerfile.contract.md) - Backend Dockerfile specification
- [../data-model.md](../data-model.md) - Docker artifacts data model

## Version History

- v1.0.0 (2026-01-18): Initial contract specification
