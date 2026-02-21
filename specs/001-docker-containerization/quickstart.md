# Quick Start Guide: Docker Containerization

**Feature**: 001-docker-containerization
**Date**: 2026-01-18
**Purpose**: Quick start guide for building, running, and testing containerized Todo Chatbot application

## Prerequisites

Before you begin, ensure you have:

- ✅ Docker Desktop 4.53+ installed and running
- ✅ Docker Compose installed (included with Docker Desktop)
- ✅ Git repository cloned locally
- ✅ Neon PostgreSQL database accessible
- ✅ OpenAI API key (for AI features)
- ✅ 8GB RAM minimum, 20GB disk space

**Optional**:
- Docker AI Agent (Gordon) enabled in Docker Desktop Beta features

## Quick Start (5 Minutes)

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

# Test frontend
curl http://localhost:3000/api/health
# Expected: {"status":"healthy"}

# Test backend
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

## Detailed Setup

### Step 1: Install Docker Desktop

**Windows/macOS**:
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation:
   ```bash
   docker --version
   docker-compose --version
   ```

**Linux**:
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get install docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

### Step 2: Enable Docker AI Agent (Gordon) - Optional

1. Open Docker Desktop
2. Navigate to **Settings** → **Beta features**
3. Toggle **Docker AI** to **ON**
4. Restart Docker Desktop
5. Verify Gordon:
   ```bash
   docker ai "What can you do?"
   ```

**If Gordon is unavailable**: Don't worry! All Docker operations work with standard Docker CLI. Gordon is an optional enhancement for optimization suggestions.

### Step 3: Configure Environment Variables

Create `.env` file in project root:

```bash
# Copy template
cp .env.example .env
```

Edit `.env` with your values:

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

**Security Note**: Never commit `.env` file to git. It's already in `.gitignore`.

### Step 4: Build Docker Images

**Option A: Using Docker Compose (Recommended)**
```bash
# Build all images
docker-compose build

# Build with no cache (clean build)
docker-compose build --no-cache

# Build specific service
docker-compose build frontend
docker-compose build backend
```

**Option B: Using Docker CLI**
```bash
# Build frontend
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend

# Build backend
docker build -t todo-backend:latest -f backend/Dockerfile ./backend
```

**Option C: Using Gordon AI**
```bash
# Ask Gordon to build frontend
docker ai "Build an optimized Next.js production image from ./frontend directory"

# Ask Gordon to build backend
docker ai "Build an optimized FastAPI production image from ./backend directory"
```

### Step 5: Run Services

**Development Mode (with hot-reload)**:
```bash
# Start services
docker-compose up

# Or in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
```

**Production Mode**:
```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Step 6: Verify Deployment

**Check Service Status**:
```bash
# List running containers
docker-compose ps

# Expected output:
# NAME                STATUS              PORTS
# frontend            Up (healthy)        0.0.0.0:3000->3000/tcp
# backend             Up (healthy)        0.0.0.0:8000->8000/tcp
```

**Test Health Endpoints**:
```bash
# Frontend health check
curl http://localhost:3000/api/health

# Backend health check
curl http://localhost:8000/health

# Backend API docs
curl http://localhost:8000/docs
```

**Test in Browser**:
```bash
# Open frontend
open http://localhost:3000

# Open backend API docs
open http://localhost:8000/docs
```

**Test Inter-Container Communication**:
```bash
# Exec into frontend container
docker-compose exec frontend sh

# Test backend connectivity from frontend
wget -O- http://backend:8000/health

# Exit container
exit
```

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# Since specific time
docker-compose logs --since 2024-01-18T10:00:00 backend
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build
```

### Stop Services

```bash
# Stop services (keep containers)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers, volumes, and images
docker-compose down -v --rmi all
```

### Inspect Containers

```bash
# List containers
docker ps

# Inspect container
docker inspect <container-id>

# Check health status
docker inspect <container-id> --format='{{.State.Health.Status}}'

# View container stats
docker stats
```

### Execute Commands in Containers

```bash
# Open shell in frontend
docker-compose exec frontend sh

# Open shell in backend
docker-compose exec backend bash

# Run command in container
docker-compose exec backend python -c "print('Hello')"
```

### Clean Up

```bash
# Remove stopped containers
docker-compose down

# Remove all containers, networks, and volumes
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Clean up Docker system
docker system prune -a
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
   - Frontend: Next.js hot-reload (~3 seconds)
   - Backend: FastAPI auto-reload (~3 seconds)

4. **View logs to confirm reload**:
   ```bash
   docker-compose logs -f frontend
   docker-compose logs -f backend
   ```

### Testing Changes

```bash
# Run frontend tests
docker-compose exec frontend npm test

# Run backend tests
docker-compose exec backend pytest

# Run linting
docker-compose exec frontend npm run lint
docker-compose exec backend ruff check .
```

### Debugging

```bash
# View container logs
docker-compose logs -f backend

# Exec into container
docker-compose exec backend bash

# Check environment variables
docker-compose exec backend env

# Check network connectivity
docker-compose exec frontend ping backend

# Inspect network
docker network inspect todo-app_todo-network
```

## Optimization with Gordon AI

### Analyze Dockerfiles

```bash
# Analyze frontend Dockerfile
docker ai "Review this Dockerfile and suggest optimizations" < frontend/Dockerfile

# Analyze backend Dockerfile
docker ai "Review this Dockerfile and suggest optimizations" < backend/Dockerfile
```

### Get Optimization Suggestions

```bash
# Image size reduction
docker ai "My frontend image is 300MB. How can I reduce it to under 200MB?"

# Build speed optimization
docker ai "Why is my Docker build slow? Here's my Dockerfile..."

# Security improvements
docker ai "What security best practices should I follow for Python Docker images?"

# Layer caching
docker ai "How can I optimize layer caching for faster rebuilds?"
```

### Troubleshooting with Gordon

```bash
# Container won't start
docker ai "My backend container exits immediately. How do I debug?"

# Network issues
docker ai "Frontend can't connect to backend in Docker. How to fix?"

# Build failures
docker ai "Docker build fails at pip install. What's wrong?"

# Permission issues
docker ai "Getting permission denied in Docker container"
```

## Image Registry Operations

### Tag Images

```bash
# Tag frontend
docker tag todo-frontend:latest yourusername/todo-frontend:latest
docker tag todo-frontend:latest yourusername/todo-frontend:v1.0.0

# Tag backend
docker tag todo-backend:latest yourusername/todo-backend:latest
docker tag todo-backend:latest yourusername/todo-backend:v1.0.0
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push frontend
docker push yourusername/todo-frontend:latest
docker push yourusername/todo-frontend:v1.0.0

# Push backend
docker push yourusername/todo-backend:latest
docker push yourusername/todo-backend:v1.0.0
```

### Pull from Registry

```bash
# Pull frontend
docker pull yourusername/todo-frontend:latest

# Pull backend
docker pull yourusername/todo-backend:latest

# Run pulled images
docker run -d -p 3000:3000 yourusername/todo-frontend:latest
docker run -d -p 8000:8000 yourusername/todo-backend:latest
```

## Troubleshooting

### Port Already in Use

**Problem**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:
```bash
# Find process using port
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Kill process or change port in docker-compose.yml
ports:
  - "3001:3000"  # Map to different host port
```

### Environment Variable Missing

**Problem**: `DATABASE_URL not set`

**Solution**:
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

**Problem**: Container starts then exits

**Solution**:
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

**Problem**: Frontend can't reach backend

**Solution**:
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

**Problem**: Docker build fails

**Solution**:
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

**Problem**: Container unhealthy

**Solution**:
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

## Next Steps

After successfully running the containerized application:

1. **Test all features**: Verify CRUD operations, authentication, AI chat
2. **Run tests**: Execute unit and integration tests in containers
3. **Optimize images**: Use Gordon AI suggestions to reduce image sizes
4. **Security scan**: Run Docker Scout vulnerability scans
5. **Push to registry**: Tag and push images to Docker Hub
6. **Prepare for Kubernetes**: Images are now ready for Kubernetes deployment

## Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **Next.js Docker Guide**: https://nextjs.org/docs/deployment#docker-image
- **FastAPI Docker Guide**: https://fastapi.tiangolo.com/deployment/docker/
- **Docker AI Agent (Gordon)**: Docker Desktop 4.53+ Beta features
- **Project README**: See README.docker.md for detailed documentation

## Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Use Gordon AI: `docker ai "describe your problem"`
3. Review contracts: See `specs/001-docker-containerization/contracts/`
4. Check documentation: See README.docker.md
5. Verify environment: Ensure all prerequisites are met

## Summary

You've successfully containerized the Todo Chatbot application! Key achievements:

- ✅ Docker images built for frontend and backend
- ✅ Services running with Docker Compose
- ✅ Inter-container communication working
- ✅ Health checks configured and passing
- ✅ Development hot-reload enabled
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
