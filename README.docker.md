# Docker Deployment Guide

**Todo Chatbot Application - Docker Containerization**

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Images](#docker-images)
- [Docker Compose](#docker-compose)
- [Environment Configuration](#environment-configuration)
- [Gordon AI Optimization](#gordon-ai-optimization)
- [Troubleshooting](#troubleshooting)
- [Performance Tips](#performance-tips)
- [Security](#security)

## Prerequisites

- Docker Desktop 4.53+ installed and running
- Docker Compose installed (included with Docker Desktop)
- 8GB RAM minimum, 20GB disk space
- Neon PostgreSQL database accessible
- OpenAI API key (for AI features)

**Optional:**
- Docker AI Agent (Gordon) enabled in Docker Desktop Beta features

## Quick Start

### 1. Setup Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
# Required variables:
# - DATABASE_URL (Neon PostgreSQL connection string)
# - BETTER_AUTH_SECRET (minimum 32 characters)
# - OPENAI_API_KEY (starts with sk-)
```

### 2. Start Services with Docker Compose

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Wait for services to be healthy (~40 seconds)
```

### 3. Verify Services

```bash
# Check service status
docker-compose ps

# Test frontend health
curl http://localhost:3000/api/health
# Expected: {"status":"healthy"}

# Test backend health
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Open in browser
open http://localhost:3000
```

### 4. Stop Services

```bash
# Stop all services
docker-compose down
```

## Docker Images

### Production Images

**Frontend (Next.js):**
- Base: `node:20-alpine`
- Size: ~301MB
- Multi-stage build (2 stages)
- Non-root user (nextjs, UID 1001)
- Health check: `/api/health`
- Port: 3000

**Backend (FastAPI):**
- Base: `python:3.11-alpine`
- Size: ~302MB (optimized from 472MB)
- Multi-stage build (2 stages)
- Non-root user (appuser, UID 1001)
- Health check: `/health`
- Port: 8000

### Building Images

```bash
# Build frontend production image
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend

# Build backend production image
docker build -t todo-backend:latest -f backend/Dockerfile ./backend

# Build both with Docker Compose
docker-compose -f docker-compose.prod.yml build
```

### Development Images

```bash
# Build development images (with hot-reload)
docker-compose build

# Or build individually
docker build -t todo-frontend:dev -f frontend/Dockerfile.dev ./frontend
docker build -t todo-backend:dev -f backend/Dockerfile.dev ./backend
```

## Docker Compose

### Development Environment

```bash
# Start development services (with hot-reload)
docker-compose up -d

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build
```

### Production Environment

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

### Service Communication

Services communicate via Docker network:
- Frontend → Backend: `http://backend:8000`
- Backend → Frontend: `http://frontend:3000`
- Host → Frontend: `http://localhost:3000`
- Host → Backend: `http://localhost:8000`

## Environment Configuration

### Required Variables

```env
# Database (Required)
DATABASE_URL=postgresql://user:password@host.neon.tech:5432/dbname?sslmode=require

# Authentication (Required)
BETTER_AUTH_SECRET=your-secret-key-minimum-32-characters-long

# OpenAI (Required for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here
AGENT_MODEL=gpt-4o

# Docker Registry (Optional - for pushing images)
DOCKER_REGISTRY=yourusername
VERSION=latest

# Frontend (Auto-configured)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_URL=http://localhost:3000
```

### Environment Variable Precedence

1. docker-compose.yml environment section
2. .env file in project root
3. Environment variables on host

## Gordon AI Optimization

### Using Gordon for Dockerfile Analysis

```bash
# Analyze frontend Dockerfile
docker ai "Review this Dockerfile and suggest optimizations" < frontend/Dockerfile

# Analyze backend Dockerfile
docker ai "Review this Dockerfile and suggest optimizations" < backend/Dockerfile

# Get specific optimization suggestions
docker ai "How can I reduce the size of my Next.js Docker image?"
docker ai "What security best practices should I follow for Python Docker images?"
```

### Optimization Results

**Backend Optimization:**
- Before: 472MB
- After: 302MB
- Reduction: 170MB (36% smaller)
- Changes: Switched to Alpine base, optimized healthcheck

**Frontend Optimization:**
- Before: 293MB
- After: 301MB
- Changes: Removed unused build stage, added curl for healthcheck

### Fallback to Standard Docker CLI

If Gordon is unavailable, all Docker operations work with standard Docker CLI:

```bash
# Standard Docker commands work without Gordon
docker build -t myimage .
docker run myimage
docker-compose up
```

## Troubleshooting

### Port Already in Use

**Problem:** `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution:**
```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or change port in docker-compose.yml
ports:
  - "3001:3000"  # Map to different host port
```

### Environment Variable Missing

**Problem:** `DATABASE_URL not set`

**Solution:**
```bash
# Create .env file
cp .env.example .env

# Edit with actual values
nano .env

# Restart services
docker-compose down
docker-compose up -d
```

### Container Exits Immediately

**Problem:** Container starts then exits

**Solution:**
```bash
# Check logs for errors
docker-compose logs backend

# Common causes:
# - Missing environment variables
# - Database connection failure
# - Syntax errors in code
# - Port conflicts

# Debug by running interactively
docker-compose run backend bash
```

### Network Connectivity Issues

**Problem:** Frontend can't reach backend

**Solution:**
```bash
# Verify both services on same network
docker network inspect todo-app_todo-network

# Verify DNS resolution
docker-compose exec frontend nslookup backend

# Check backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend
```

### Build Failures

**Problem:** Docker build fails

**Solution:**
```bash
# Clean build (no cache)
docker-compose build --no-cache

# Check Dockerfile syntax
docker ai "Review this Dockerfile for errors" < frontend/Dockerfile

# Check build context
ls -la frontend/
ls -la backend/

# Verify dependencies
cat frontend/package.json
cat backend/requirements.txt
```

### Health Check Failing

**Problem:** Container unhealthy

**Solution:**
```bash
# Check health check endpoint
curl http://localhost:3000/api/health
curl http://localhost:8000/health

# Verify endpoint exists in code
cat frontend/app/api/health/route.ts
cat backend/app/main.py

# Check container logs
docker-compose logs frontend
docker-compose logs backend
```

## Performance Tips

### Optimize Build Time

1. **Use layer caching**: Order Dockerfile commands from least to most frequently changed
2. **Use .dockerignore**: Exclude unnecessary files from build context
3. **Parallel builds**: Build frontend and backend simultaneously
4. **Use BuildKit**: Enable Docker BuildKit for faster builds
   ```bash
   DOCKER_BUILDKIT=1 docker-compose build
   ```

### Optimize Image Size

1. **Multi-stage builds**: Separate build and runtime stages
2. **Minimal base images**: Use alpine or slim variants
3. **Clean up**: Remove unnecessary files and caches
4. **Use .dockerignore**: Exclude large files from image

### Optimize Runtime Performance

1. **Resource limits**: Set CPU and memory limits in docker-compose.yml
2. **Health checks**: Configure appropriate intervals and timeouts
3. **Restart policies**: Use `unless-stopped` for production
4. **Network optimization**: Use bridge network for low latency

## Security

### Security Best Practices Implemented

- ✅ Non-root user in containers (UID 1001)
- ✅ Minimal base images (alpine/slim)
- ✅ No secrets in images
- ✅ Health checks configured
- ✅ Environment variables for secrets
- ✅ .dockerignore to exclude sensitive files

### Security Scanning

```bash
# Use Docker Scout (built into Docker Desktop)
docker scout quickview todo-frontend:latest
docker scout quickview todo-backend:latest

# Get detailed CVE report
docker scout cves todo-frontend:latest
docker scout cves todo-backend:latest

# Ask Gordon about security
docker ai "How can I improve security of my Docker images?"
```

### Security Checklist

- [ ] All secrets in environment variables (.env files)
- [ ] .env file in .gitignore (never committed)
- [ ] Non-root user execution verified
- [ ] Minimal base images used
- [ ] No secrets baked into Docker images
- [ ] Health checks configured
- [ ] Vulnerability scans run regularly

## Registry Operations

### Tagging Images

```bash
# Tag with version
docker tag todo-frontend:latest yourusername/todo-frontend:v1.0.0
docker tag todo-backend:latest yourusername/todo-backend:v1.0.0

# Tag with latest
docker tag todo-frontend:latest yourusername/todo-frontend:latest
docker tag todo-backend:latest yourusername/todo-backend:latest
```

### Pushing to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push images
docker push yourusername/todo-frontend:latest
docker push yourusername/todo-frontend:v1.0.0
docker push yourusername/todo-backend:latest
docker push yourusername/todo-backend:v1.0.0
```

### Pulling from Registry

```bash
# Pull images
docker pull yourusername/todo-frontend:v1.0.0
docker pull yourusername/todo-backend:v1.0.0

# Run pulled images
docker run -d -p 3000:3000 yourusername/todo-frontend:v1.0.0
docker run -d -p 8000:8000 \
  -e DATABASE_URL="your-db-url" \
  -e BETTER_AUTH_SECRET="your-secret" \
  -e OPENAI_API_KEY="your-key" \
  yourusername/todo-backend:v1.0.0
```

## Development Workflow

### Hot-Reload Development

1. **Start development services**:
   ```bash
   docker-compose up -d
   ```

2. **Make code changes**:
   - Frontend: Edit files in `frontend/` directory
   - Backend: Edit files in `backend/` directory

3. **Changes reflect automatically**:
   - Frontend: Next.js hot-reload (~1-3 seconds)
   - Backend: FastAPI auto-reload (~1-2 seconds)

4. **View logs to confirm reload**:
   ```bash
   docker-compose logs -f frontend
   docker-compose logs -f backend
   ```

## Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **Next.js Docker Guide**: https://nextjs.org/docs/deployment#docker-image
- **FastAPI Docker Guide**: https://fastapi.tiangolo.com/deployment/docker/
- **Docker AI Agent (Gordon)**: Docker Desktop 4.53+ Beta features

## Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Use Gordon AI: `docker ai "describe your problem"`
3. Review this documentation
4. Check environment variables in .env
5. Verify all prerequisites are met

## Summary

You've successfully containerized the Todo Chatbot application! Key achievements:

- ✅ Docker images built for frontend and backend
- ✅ Services running with Docker Compose
- ✅ Inter-container communication working
- ✅ Health checks configured and passing
- ✅ Development hot-reload enabled
- ✅ Images optimized (backend 36% smaller)
- ✅ Ready for Kubernetes deployment

**Quick Commands Reference**:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build

# Clean up
docker-compose down -v
```
