# Data Model: Docker Artifacts

**Feature**: 001-docker-containerization
**Date**: 2026-01-18
**Purpose**: Define the structure and relationships of Docker artifacts for containerizing the Todo Chatbot application

## Overview

This document describes the Docker artifacts (images, containers, networks, volumes, configurations) that comprise the containerized Todo Chatbot application. These are infrastructure entities, not application data models.

## Docker Artifacts

### 1. Frontend Docker Image

**Entity**: Frontend Docker Image
**Purpose**: Containerized Next.js application ready for deployment

**Structure**:
```
Frontend Image (node:20-alpine based)
├── Stage 1: deps (dependency installation)
│   ├── package.json
│   ├── package-lock.json
│   └── node_modules/ (production only)
├── Stage 2: builder (application build)
│   ├── All source files
│   ├── node_modules/ (all dependencies)
│   └── .next/ (build output)
└── Stage 3: runner (final runtime)
    ├── server.js (standalone server)
    ├── .next/standalone/
    ├── .next/static/
    ├── public/
    └── User: nextjs (UID 1001, non-root)
```

**Attributes**:
- **Base Image**: node:20-alpine
- **Target Size**: <200MB
- **Exposed Port**: 3000
- **User**: nextjs (UID 1001)
- **Working Directory**: /app
- **Health Check**: GET /api/health (30s interval, 10s timeout, 40s start period)
- **Entry Point**: node server.js

**Environment Variables**:
- NEXT_PUBLIC_API_URL: Backend API URL (e.g., http://backend:8000)
- BETTER_AUTH_SECRET: Authentication secret key
- BETTER_AUTH_URL: Frontend URL (e.g., http://localhost:3000)
- NODE_ENV: production
- NEXT_TELEMETRY_DISABLED: 1
- PORT: 3000
- HOSTNAME: 0.0.0.0

**Build Artifacts**:
- Production image: todo-frontend:latest
- Development image: todo-frontend:dev
- Tagged versions: todo-frontend:v1.0.0

### 2. Backend Docker Image

**Entity**: Backend Docker Image
**Purpose**: Containerized FastAPI application ready for deployment

**Structure**:
```
Backend Image (python:3.11-slim based)
├── Stage 1: builder (dependency installation)
│   ├── requirements.txt
│   ├── /opt/venv/ (virtual environment)
│   └── System packages (gcc, postgresql-client)
└── Stage 2: runner (final runtime)
    ├── /opt/venv/ (copied from builder)
    ├── app/ (application code)
    ├── agents/ (AI agent code)
    ├── mcp/ (MCP server code)
    └── User: appuser (UID 1001, non-root)
```

**Attributes**:
- **Base Image**: python:3.11-slim
- **Target Size**: <150MB
- **Exposed Port**: 8000
- **User**: appuser (UID 1001)
- **Working Directory**: /app
- **Health Check**: GET /health (30s interval, 10s timeout, 40s start period)
- **Entry Point**: uvicorn app.main:app --host 0.0.0.0 --port 8000

**Environment Variables**:
- DATABASE_URL: Neon PostgreSQL connection string
- BETTER_AUTH_SECRET: Authentication secret key
- OPENAI_API_KEY: OpenAI API key for AI features
- AGENT_MODEL: AI model to use (e.g., gpt-4o)
- FRONTEND_URL: Frontend URL (e.g., http://frontend:3000)
- PATH: /opt/venv/bin:$PATH (virtual environment)

**Build Artifacts**:
- Production image: todo-backend:latest
- Development image: todo-backend:dev
- Tagged versions: todo-backend:v1.0.0

### 3. Docker Compose Configuration

**Entity**: Docker Compose Configuration
**Purpose**: Orchestrate frontend and backend services with networking

**Structure**:
```yaml
Docker Compose Stack
├── Services
│   ├── frontend
│   │   ├── Build context: ./frontend
│   │   ├── Dockerfile: Dockerfile.dev (dev) / Dockerfile (prod)
│   │   ├── Ports: 3000:3000
│   │   ├── Environment: from .env
│   │   ├── Volumes: ./frontend:/app (dev only)
│   │   ├── Depends on: backend
│   │   └── Network: todo-network
│   └── backend
│       ├── Build context: ./backend
│       ├── Dockerfile: Dockerfile.dev (dev) / Dockerfile (prod)
│       ├── Ports: 8000:8000
│       ├── Environment: from .env
│       ├── Volumes: ./backend:/app (dev only)
│       └── Network: todo-network
└── Networks
    └── todo-network (bridge driver)
```

**Attributes**:
- **Version**: 3.8
- **Services**: 2 (frontend, backend)
- **Networks**: 1 (todo-network)
- **Volumes**: Optional (development hot-reload)
- **Environment Source**: .env file

**Service Dependencies**:
- Frontend depends on backend (starts after backend)
- Both services connect to same network
- Services discover each other via DNS (service names)

**Development vs Production**:

| Aspect | Development | Production |
|--------|-------------|------------|
| Dockerfile | Dockerfile.dev | Dockerfile |
| Volumes | Source code mounted | No volumes |
| Restart policy | no | unless-stopped |
| Build target | Development dependencies | Production optimized |
| Hot-reload | Enabled | Disabled |

### 4. Environment Configuration

**Entity**: Environment Configuration
**Purpose**: Externalize configuration for different environments

**Structure**:
```
Environment Variables
├── Database
│   └── DATABASE_URL (Neon PostgreSQL connection string)
├── Authentication
│   ├── BETTER_AUTH_SECRET (shared secret)
│   └── BETTER_AUTH_URL (frontend URL)
├── AI Integration
│   ├── OPENAI_API_KEY (OpenAI API key)
│   └── AGENT_MODEL (AI model identifier)
├── Service URLs
│   ├── NEXT_PUBLIC_API_URL (backend URL for frontend)
│   └── FRONTEND_URL (frontend URL for backend)
└── Docker Registry
    ├── DOCKER_REGISTRY (registry username/URL)
    └── VERSION (image version tag)
```

**Validation Rules**:
- DATABASE_URL: Must be valid PostgreSQL connection string
- BETTER_AUTH_SECRET: Minimum 32 characters
- OPENAI_API_KEY: Must start with "sk-"
- URLs: Must be valid HTTP/HTTPS URLs
- VERSION: Must follow semantic versioning (v1.0.0)

**Security Constraints**:
- All secrets in .env file (never committed to git)
- .env file in .gitignore
- .env.example provides template without secrets
- No default values for secrets in code

### 5. Container Network

**Entity**: Docker Bridge Network
**Purpose**: Enable inter-container communication with DNS resolution

**Structure**:
```
todo-network (bridge)
├── Frontend Container
│   ├── IP: Assigned by Docker (e.g., 172.18.0.2)
│   ├── Hostname: frontend
│   └── DNS: Resolves "backend" to backend container IP
└── Backend Container
    ├── IP: Assigned by Docker (e.g., 172.18.0.3)
    ├── Hostname: backend
    └── DNS: Resolves "frontend" to frontend container IP
```

**Attributes**:
- **Driver**: bridge
- **Subnet**: Auto-assigned by Docker (e.g., 172.18.0.0/16)
- **Gateway**: Auto-assigned by Docker (e.g., 172.18.0.1)
- **DNS**: Docker embedded DNS server
- **Isolation**: Isolated from host network and other Docker networks

**Communication Patterns**:
- Frontend → Backend: http://backend:8000/api/...
- Backend → Frontend: http://frontend:3000/... (if needed)
- Backend → Neon DB: External network via host gateway
- Host → Frontend: http://localhost:3000
- Host → Backend: http://localhost:8000

### 6. Container Registry

**Entity**: Container Registry
**Purpose**: Store and distribute Docker images

**Structure**:
```
Docker Hub Registry
├── Repository: {username}/todo-frontend
│   ├── latest (always newest)
│   ├── v1.0.0 (semantic version)
│   ├── v1.0.1 (semantic version)
│   └── Metadata (labels, build info)
└── Repository: {username}/todo-backend
    ├── latest (always newest)
    ├── v1.0.0 (semantic version)
    ├── v1.0.1 (semantic version)
    └── Metadata (labels, build info)
```

**Attributes**:
- **Registry**: Docker Hub (hub.docker.com)
- **Visibility**: Public or Private (user choice)
- **Authentication**: Docker Hub credentials
- **Rate Limits**: Docker Hub free tier limits apply
- **Alternative**: Local registry (registry:2)

**Image Metadata (Labels)**:
- org.opencontainers.image.version: Semantic version
- org.opencontainers.image.created: Build timestamp
- org.opencontainers.image.revision: Git commit hash
- org.opencontainers.image.source: Repository URL

## Relationships

### Image → Container
- Docker Image is the template
- Container is the running instance
- Multiple containers can run from same image
- Containers are ephemeral, images are persistent

### Container → Network
- Containers join networks at runtime
- Multiple containers can share same network
- Network provides DNS resolution and isolation
- Containers can join multiple networks

### Container → Volume
- Volumes persist data beyond container lifecycle
- Development: Source code mounted as volume
- Production: No volumes (stateless containers)
- Anonymous volumes for node_modules, .next

### Compose → Services
- Compose defines service configurations
- Services are container specifications
- Compose manages service lifecycle
- Compose creates networks and volumes

### Environment → Containers
- Environment variables injected at runtime
- Sourced from .env file via Compose
- Can be overridden at container start
- Validated by application code

## State Transitions

### Image Lifecycle
```
Source Code → Build → Image → Tag → Push → Registry
                ↓
            Test Locally
                ↓
            Deploy (Kubernetes)
```

### Container Lifecycle
```
Image → Create → Start → Running → Stop → Remove
                    ↓
                Health Check
                    ↓
            Healthy / Unhealthy
```

### Development Workflow
```
Code Change → Hot Reload → Container Updates → Test
     ↓
  Rebuild Image (if needed)
     ↓
  Test in Compose
     ↓
  Push to Registry
```

## Validation Rules

### Image Size Constraints
- Frontend image: MUST be <200MB
- Backend image: MUST be <150MB
- Verified with: `docker images | grep todo`

### Health Check Requirements
- Endpoint: MUST respond with 200 OK
- Interval: 30 seconds
- Timeout: 10 seconds
- Start period: 40 seconds
- Retries: 3 before marking unhealthy

### Security Requirements
- User: MUST NOT be root (UID 1001)
- Secrets: MUST NOT be in image layers
- Base images: MUST be minimal (alpine/slim)
- Vulnerabilities: MUST pass Docker Scout scan

### Network Requirements
- DNS resolution: Service names MUST resolve
- Port mapping: Host ports MUST not conflict
- Isolation: Containers MUST be isolated from host
- Communication: Frontend MUST reach backend

## Performance Characteristics

### Build Performance
- Frontend build: <10 minutes (target)
- Backend build: <5 minutes (target)
- Layer caching: Reduces rebuild to <2 minutes
- Parallel builds: Both images can build simultaneously

### Runtime Performance
- Container startup: <30 seconds
- Health check response: <1 second
- Frontend-backend latency: <500ms
- Database connection: <2 seconds
- Hot-reload: <3 seconds (development)

### Resource Usage
- Frontend container: ~100MB RAM, 0.1 CPU
- Backend container: ~200MB RAM, 0.2 CPU
- Network overhead: Minimal (<1ms)
- Disk usage: ~350MB total (both images)

## Conclusion

This data model defines all Docker artifacts required for containerizing the Todo Chatbot application. The model emphasizes:
- **Separation of concerns**: Frontend and backend as independent images
- **Security**: Non-root users, minimal base images, no secrets in images
- **Optimization**: Multi-stage builds, layer caching, size constraints
- **Reliability**: Health checks, proper networking, environment validation
- **Developer experience**: Hot-reload support, clear configuration, comprehensive documentation

All entities are well-defined with clear attributes, relationships, and validation rules. Ready for contract definition and implementation.
