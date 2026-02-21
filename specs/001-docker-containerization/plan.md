# Implementation Plan: Docker Containerization with AI-Assisted Optimization

**Branch**: `001-docker-containerization` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-docker-containerization/spec.md`

## Summary

Containerize the existing Next.js frontend and FastAPI backend applications using Docker with multi-stage builds, optimize images using Docker AI Agent (Gordon), and prepare for Kubernetes deployment. The implementation creates production-ready Docker images (frontend <200MB, backend <150MB), Docker Compose configurations for local development, and comprehensive documentation for deployment workflows.

**Technical Approach**: Multi-stage Dockerfiles for both applications using minimal base images (node:alpine, python:slim), Docker Compose for orchestration, bridge networking for inter-container communication, environment variable configuration via .env files, and optional Gordon AI integration for optimization suggestions with fallback to standard Docker CLI.

## Technical Context

**Language/Version**:
- Frontend: Node.js 20+ with Next.js 16+ (TypeScript 5+)
- Backend: Python 3.11+ with FastAPI (latest stable)

**Primary Dependencies**:
- Frontend: Next.js 16+, React 18+, Tailwind CSS, Better Auth (client)
- Backend: FastAPI, SQLModel, Pydantic v2, uvicorn, psycopg2-binary, OpenAI SDK, MCP SDK
- Docker: Docker Desktop 4.53+, Docker Compose, Docker AI Agent (Gordon - optional)

**Storage**:
- Neon PostgreSQL (cloud-hosted, accessed from containers)
- Container volumes for development hot-reload (optional)
- Docker registry (Docker Hub or local) for image storage

**Testing**:
- Dockerfile build verification (both images build successfully)
- Container runtime testing (services start and respond)
- Inter-container networking tests (frontend ↔ backend communication)
- Health check endpoint validation
- Image size verification (<200MB frontend, <150MB backend)
- Docker Compose integration testing

**Target Platform**:
- Development: Docker Desktop on Windows/macOS/Linux
- Local Testing: Docker Compose with bridge networking
- Deployment Target: Kubernetes (prepared but not deployed in this feature)
- Container Registry: Docker Hub (public/private) or local registry

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- Image build time: <10 minutes on standard development machine
- Container startup time: <30 seconds for both services
- Health check response: <1 second
- Frontend-backend communication: <500ms response time
- Database connection establishment: <2 seconds

**Constraints**:
- Frontend image size: <200MB
- Backend image size: <150MB
- Must use node:alpine base for frontend
- Must use python:slim base for backend
- Must implement non-root user execution
- Must support fallback to standard Docker CLI if Gordon unavailable
- Must work with existing Neon PostgreSQL database (no local database container)

**Scale/Scope**:
- 2 Docker images (frontend, backend)
- 2 Dockerfiles per service (production + development)
- 2 Docker Compose files (development + production)
- 1 Docker network (bridge)
- Multiple environment variables (~10-15 per service)
- Documentation for Gordon AI usage patterns

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **I. Production-Ready Code Quality**
- Dockerfiles will follow best practices (multi-stage builds, layer caching)
- Health check endpoints will be implemented for monitoring
- Documentation will be comprehensive and tested
- No type safety concerns (Dockerfiles are declarative)

✅ **II. Cloud-Native Architecture**
- All services containerized with Docker multi-stage builds
- Health check endpoints implemented (`/health`, `/ready`)
- Graceful shutdown handling (SIGTERM in containers)
- Configuration externalized via environment variables
- Services remain stateless (state in Neon PostgreSQL)

✅ **III. AI Integration Excellence**
- Gordon AI integration is optional enhancement, not requirement
- Fallback to standard Docker CLI ensures reliability
- No AI API costs (Gordon is local Docker Desktop feature)
- Documentation includes Gordon usage patterns

✅ **IV. Security-First Approach**
- All secrets in environment variables (.env files)
- Non-root user execution in all containers
- Minimal base images (alpine/slim) reduce attack surface
- No secrets baked into Docker images
- CORS and security headers remain in application code

✅ **V. Developer Experience**
- README.docker.md provides clear setup instructions
- Docker Compose enables local development without Kubernetes
- Separate Dockerfile.dev for development hot-reload
- Environment configuration clearly documented (.env.example)
- Gordon AI provides interactive assistance

### Architecture Standards Compliance

✅ **Phase II: Next.js + FastAPI Foundation**
- Existing REST API structure preserved in containers
- No changes to API design or separation of concerns
- Containerization is infrastructure layer, not application layer

✅ **Phase IV: Kubernetes Deployment** (Preparation)
- Multi-stage builds optimize image size
- Health checks implemented for liveness/readiness probes
- Resource limits will be defined in Kubernetes manifests (separate feature)
- Images prepared for Kubernetes deployment

### Deployment Requirements Compliance

✅ **Docker Images**
- Multi-stage builds: Separate build and runtime stages
- Layer caching: Dockerfile commands ordered for optimal caching
- Minimal base images: node:alpine and python:slim
- Security scanning: Docker Scout integration documented
- Tagging: Semantic versioning strategy defined

✅ **Development Workflow**
- Docker Compose provided for local development
- README includes step-by-step setup instructions
- Hot reload supported via volume mounts (Dockerfile.dev)
- Environment configuration documented (.env.example)

### Quality Gates

✅ **No Constitution Violations**: This feature is purely infrastructure containerization and does not modify application code, business logic, or API contracts. All constitution principles are maintained.

## Project Structure

### Documentation (this feature)

```text
specs/001-docker-containerization/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Docker best practices research
├── data-model.md        # Docker artifacts model
├── quickstart.md        # Quick start guide
├── contracts/           # Docker contracts
│   ├── frontend-dockerfile.contract.md
│   ├── backend-dockerfile.contract.md
│   └── docker-compose.contract.md
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)
frontend/
├── .dockerignore        # Files to exclude from Docker build
├── Dockerfile           # Production multi-stage build
├── Dockerfile.dev       # Development with hot-reload
├── next.config.js       # Updated for standalone output
├── app/
│   └── api/
│       └── health/
│           └── route.ts # Health check endpoint
└── ... (existing Next.js files)

backend/
├── .dockerignore        # Files to exclude from Docker build
├── Dockerfile           # Production multi-stage build
├── Dockerfile.dev       # Development with hot-reload
├── requirements.txt     # Python dependencies
├── app/
│   └── main.py          # Updated with /health endpoint
└── ... (existing FastAPI files)

# Docker orchestration (project root)
docker-compose.yml       # Development environment
docker-compose.prod.yml  # Production environment
.env.example             # Environment variable template
.env                     # Local environment variables (gitignored)
README.docker.md         # Docker deployment guide
```

**Structure Decision**: Web application structure selected because the project has distinct frontend (Next.js) and backend (FastAPI) components. Each component gets its own Dockerfile and .dockerignore. Docker Compose orchestrates both services with a shared network. This structure aligns with the existing codebase organization and enables independent image builds while maintaining integration testing capabilities.

## Complexity Tracking

> **No violations - this section is empty**

This feature introduces no complexity violations. Containerization is a standard infrastructure practice that:
- Does not add new projects (uses existing frontend/backend)
- Does not introduce new architectural patterns (containers are deployment mechanism)
- Follows Docker best practices (multi-stage builds, minimal images)
- Maintains existing application architecture unchanged

## Phase 0: Research & Technical Decisions

### Research Topics

1. **Docker Multi-Stage Build Optimization**
   - Research optimal layer ordering for Next.js standalone builds
   - Investigate node:alpine vs node:slim tradeoffs
   - Determine best practices for npm dependency caching

2. **Python Container Best Practices**
   - Research virtual environment usage in Docker containers
   - Investigate python:slim vs python:alpine compatibility
   - Determine optimal pip caching strategies

3. **Docker Compose Networking**
   - Research bridge network vs custom network tradeoffs
   - Investigate service discovery patterns (service names as hostnames)
   - Determine volume mount strategies for development hot-reload

4. **Docker AI Agent (Gordon) Capabilities**
   - Research Gordon command patterns and syntax
   - Investigate Gordon's optimization suggestion quality
   - Determine fallback strategies when Gordon unavailable

5. **Container Security Hardening**
   - Research non-root user implementation patterns
   - Investigate minimal base image security benefits
   - Determine health check best practices

6. **Image Registry Strategies**
   - Research Docker Hub vs local registry tradeoffs
   - Investigate image tagging conventions (semantic versioning)
   - Determine image metadata best practices (labels, build info)

### Technical Decisions

**Decision 1: Base Image Selection**
- **Frontend**: node:20-alpine
  - Rationale: Alpine provides smallest image size (~40MB base) while maintaining compatibility with Next.js
  - Alternatives: node:20-slim (larger but better compatibility), node:20 (full Debian, too large)
  - Tradeoff: Alpine uses musl libc instead of glibc, but Next.js handles this well

- **Backend**: python:3.11-slim
  - Rationale: Slim provides good balance of size (~120MB base) and compatibility with Python packages
  - Alternatives: python:3.11-alpine (smaller but compilation issues with some packages), python:3.11 (too large)
  - Tradeoff: Slim is larger than alpine but avoids compilation issues with psycopg2 and other C extensions

**Decision 2: Multi-Stage Build Strategy**
- **Approach**: Separate builder and runner stages for both frontend and backend
  - Frontend: deps → builder → runner (3 stages)
  - Backend: builder → runner (2 stages)
- **Rationale**: Eliminates build tools and intermediate files from final image, reducing size by 50-70%
- **Alternatives**: Single-stage build (simpler but much larger images)

**Decision 3: Virtual Environment in Docker**
- **Approach**: Use Python virtual environment in Docker containers
- **Rationale**: Isolates dependencies, enables clean copying between stages, follows Python best practices
- **Alternatives**: Global pip install (simpler but less isolated, harder to copy between stages)

**Decision 4: Development vs Production Dockerfiles**
- **Approach**: Separate Dockerfile.dev for development with hot-reload
- **Rationale**: Development needs volume mounts and dev dependencies, production needs optimization
- **Alternatives**: Single Dockerfile with build args (more complex, harder to maintain)

**Decision 5: Docker Compose Configuration**
- **Approach**: Separate docker-compose.yml (dev) and docker-compose.prod.yml (production)
- **Rationale**: Different volume mounts, restart policies, and build targets for each environment
- **Alternatives**: Single compose file with profiles (more complex, harder to understand)

**Decision 6: Gordon AI Integration**
- **Approach**: Optional enhancement with documented fallback to standard Docker CLI
- **Rationale**: Gordon provides value but shouldn't be required dependency
- **Alternatives**: Require Gordon (limits adoption), skip Gordon entirely (misses optimization opportunity)

**Decision 7: Health Check Implementation**
- **Approach**: Implement /health endpoints in both applications, configure HEALTHCHECK in Dockerfiles
- **Rationale**: Enables container orchestration to detect unhealthy containers
- **Alternatives**: No health checks (containers might run but be unhealthy), external health checks only

**Decision 8: Environment Variable Management**
- **Approach**: .env.example template, .env for local values (gitignored)
- **Rationale**: Prevents secrets in version control, provides clear documentation
- **Alternatives**: Hardcoded values (insecure), separate files per service (more complex)

**Decision 9: Image Tagging Strategy**
- **Approach**: Both `latest` and semantic version tags (e.g., `v1.0.0`)
- **Rationale**: Latest for convenience, versions for traceability and rollback
- **Alternatives**: Latest only (no rollback), versions only (less convenient), git commit hash (too granular)

**Decision 10: Container Registry**
- **Approach**: Docker Hub as primary, document local registry as alternative
- **Rationale**: Docker Hub is accessible, free tier sufficient, widely used
- **Alternatives**: Local registry (more setup), cloud registry (additional cost)

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete Docker artifacts model including:
- Frontend Docker Image structure
- Backend Docker Image structure
- Docker Compose configuration
- Environment variable schema
- Container network topology

### API Contracts

See [contracts/](./contracts/) directory for:
- `frontend-dockerfile.contract.md` - Frontend Dockerfile specification
- `backend-dockerfile.contract.md` - Backend Dockerfile specification
- `docker-compose.contract.md` - Docker Compose configuration specification

### Quick Start Guide

See [quickstart.md](./quickstart.md) for:
- Prerequisites and installation
- Building Docker images
- Running with Docker Compose
- Testing containerized applications
- Using Gordon AI for optimization
- Troubleshooting common issues

## Implementation Phases

### Phase 1: Docker Desktop & Gordon Setup (P1)
**Goal**: Install and configure Docker environment with Gordon AI

**Tasks**:
1. Install Docker Desktop 4.53+
2. Enable Docker AI Agent (Gordon) in settings
3. Verify Gordon availability with test commands
4. Document fallback procedures if Gordon unavailable

**Acceptance**:
- Docker Desktop running and accessible
- Gordon responds to test queries
- Fallback to standard Docker CLI documented

### Phase 2: Project Structure Preparation (P1)
**Goal**: Organize project files for containerization

**Tasks**:
1. Create .dockerignore files for frontend and backend
2. Create directory structure for Docker files
3. Create .env.example template
4. Document project structure in README.docker.md

**Acceptance**:
- .dockerignore files exclude unnecessary files
- Directory structure matches plan
- .env.example includes all required variables

### Phase 3: Frontend Dockerfile Creation (P1)
**Goal**: Create production and development Dockerfiles for Next.js

**Tasks**:
1. Create frontend/Dockerfile with multi-stage build
2. Update next.config.js for standalone output
3. Create frontend/app/api/health/route.ts endpoint
4. Create frontend/Dockerfile.dev for development
5. Test frontend image builds successfully
6. Verify image size <200MB

**Acceptance**:
- Frontend Dockerfile builds without errors
- Image size under 200MB
- Non-root user configured
- Health check endpoint responds
- Development Dockerfile supports hot-reload

### Phase 4: Backend Dockerfile Creation (P1)
**Goal**: Create production and development Dockerfiles for FastAPI

**Tasks**:
1. Create backend/Dockerfile with multi-stage build
2. Add /health endpoint to backend/app/main.py
3. Create backend/Dockerfile.dev for development
4. Test backend image builds successfully
5. Verify image size <150MB

**Acceptance**:
- Backend Dockerfile builds without errors
- Image size under 150MB
- Non-root user configured
- Health check endpoint responds
- Development Dockerfile supports hot-reload

### Phase 5: Docker Compose Configuration (P1)
**Goal**: Create Docker Compose files for orchestration

**Tasks**:
1. Create docker-compose.yml for development
2. Create docker-compose.prod.yml for production
3. Configure bridge network for inter-container communication
4. Configure environment variable loading from .env
5. Configure volume mounts for development hot-reload
6. Test docker-compose up starts all services

**Acceptance**:
- docker-compose up starts both services
- Services communicate via service names
- Environment variables loaded correctly
- Volume mounts enable hot-reload in dev mode

### Phase 6: Environment Variables Configuration (P1)
**Goal**: Document and configure environment variables

**Tasks**:
1. Create comprehensive .env.example
2. Document all required variables
3. Create local .env from template
4. Test environment variable loading in containers

**Acceptance**:
- .env.example includes all variables
- Variables documented with descriptions
- Containers load variables correctly

### Phase 7: Gordon AI Optimization (P2)
**Goal**: Use Gordon to optimize Dockerfiles

**Tasks**:
1. Run Gordon analysis on frontend Dockerfile
2. Run Gordon analysis on backend Dockerfile
3. Implement Gordon's optimization suggestions
4. Document Gordon commands used
5. Measure improvements (size, build time)
6. Verify fallback to standard CLI works

**Acceptance**:
- Gordon provides actionable suggestions
- Optimizations implemented and measured
- Gordon commands documented
- Fallback procedures tested

### Phase 8: Build and Test Images (P1)
**Goal**: Build and verify Docker images

**Tasks**:
1. Build frontend production image
2. Build backend production image
3. Verify image sizes meet targets
4. Test individual container startup
5. Test health check endpoints
6. Test database connectivity from backend

**Acceptance**:
- Both images build successfully
- Image sizes under targets
- Containers start without errors
- Health checks respond correctly
- Backend connects to Neon PostgreSQL

### Phase 9: Container Networking Verification (P1)
**Goal**: Verify inter-container communication

**Tasks**:
1. Start services with Docker Compose
2. Test frontend → backend API calls
3. Test DNS resolution between containers
4. Verify bridge network configuration
5. Test port mappings (host:container)

**Acceptance**:
- Frontend reaches backend via service name
- DNS resolution works correctly
- Network inspection shows correct configuration
- Port mappings work as expected

### Phase 10: Image Optimization & Security (P2)
**Goal**: Optimize images and verify security

**Tasks**:
1. Run Docker Scout vulnerability scans
2. Implement security recommendations
3. Optimize layer caching
4. Verify non-root user execution
5. Document security best practices

**Acceptance**:
- Vulnerability scans show minimal issues
- Security recommendations implemented
- Layer caching optimized
- Non-root user verified

### Phase 11: Registry Operations (P2)
**Goal**: Tag and push images to registry

**Tasks**:
1. Login to Docker Hub
2. Tag images with semantic versions
3. Push images to registry
4. Verify images accessible from registry
5. Test pulling and running from registry
6. Document registry operations

**Acceptance**:
- Images tagged with versions
- Images pushed successfully
- Images pullable from registry
- Images run correctly after pull

### Phase 12: Development Hot-Reload (P3)
**Goal**: Configure volume mounts for hot-reload

**Tasks**:
1. Configure volume mounts in docker-compose.yml
2. Test frontend hot-reload with code changes
3. Test backend hot-reload with code changes
4. Document hot-reload setup

**Acceptance**:
- Volume mounts configured correctly
- Frontend hot-reload works (<3s)
- Backend hot-reload works (<3s)

### Phase 13: Documentation & Testing (P1)
**Goal**: Complete documentation and final testing

**Tasks**:
1. Create README.docker.md with full guide
2. Document Gordon AI usage patterns
3. Document troubleshooting procedures
4. Run complete end-to-end test
5. Verify all acceptance criteria met

**Acceptance**:
- README.docker.md complete and tested
- Gordon usage documented
- Troubleshooting guide complete
- All acceptance criteria verified

## Testing Strategy

### Build Testing
- Frontend Dockerfile builds without errors
- Backend Dockerfile builds without errors
- Multi-stage builds complete successfully
- Image sizes under target thresholds (<200MB frontend, <150MB backend)
- Non-root user configured correctly in both images

### Runtime Testing
- Frontend container starts and serves on port 3000
- Backend container starts and serves on port 8000
- Health endpoints return 200 OK within 1 second
- Environment variables loaded correctly from .env
- Backend connects to Neon PostgreSQL within 2 seconds
- Containers restart automatically (if configured)

### Integration Testing
- docker-compose up starts all services without errors
- Frontend can reach backend via service name (http://backend:8000)
- Backend can reach frontend via service name (http://frontend:3000)
- DNS resolution works between containers
- Port mappings correct (host:container)
- Volume mounts work correctly in development mode

### Optimization Testing
- Gordon provides helpful optimization suggestions
- Gordon troubleshoots build failures effectively
- Gordon recommends security improvements
- Fallback to standard Docker CLI works when Gordon unavailable
- Image sizes optimized after Gordon suggestions

### Security Testing
- Images scan clean with Docker Scout (minimal vulnerabilities)
- Non-root user execution verified
- No secrets in images (verified with docker history)
- Health checks configured and responding

### Registry Testing
- Images tagged with semantic versions
- Images pushed to Docker Hub successfully
- Images can be pulled from registry on different machine
- Pulled images run correctly without modification

### Performance Testing
- Image build completes in under 10 minutes
- Container startup completes in under 30 seconds
- Health check response under 1 second
- Frontend-backend communication under 500ms
- Database connection establishment under 2 seconds
- Hot-reload reflects changes within 3 seconds

## Risk Analysis

### Risk 1: Gordon AI Unavailable
**Impact**: Medium - Optimization suggestions unavailable
**Mitigation**: Fallback to standard Docker CLI documented, manual optimization guidelines provided
**Contingency**: Use Docker best practices documentation, community resources

### Risk 2: Image Size Exceeds Targets
**Impact**: Medium - Slower deployments, higher storage costs
**Mitigation**: Multi-stage builds, minimal base images, .dockerignore optimization
**Contingency**: Iterate on Dockerfile optimization, use Gordon suggestions

### Risk 3: Network Connectivity Issues
**Impact**: High - Containers cannot communicate
**Mitigation**: Bridge network configuration tested, DNS resolution verified
**Contingency**: Use explicit IP addresses, debug with docker network inspect

### Risk 4: Environment Variable Misconfiguration
**Impact**: High - Services fail to start or connect
**Mitigation**: .env.example template, validation in application code
**Contingency**: Container logs provide clear error messages

### Risk 5: Neon PostgreSQL Connectivity
**Impact**: High - Backend cannot access database
**Mitigation**: Connection string tested, network access verified
**Contingency**: Use docker network host mode for debugging

### Risk 6: Build Failures on Different Platforms
**Impact**: Medium - Inconsistent builds across team
**Mitigation**: Use specific base image versions, document platform requirements
**Contingency**: Use Docker buildx for multi-platform builds

## Success Metrics

- ✅ Frontend Docker image builds successfully and is <200MB
- ✅ Backend Docker image builds successfully and is <150MB
- ✅ Both images build in under 10 minutes on standard hardware
- ✅ docker-compose up starts entire stack successfully
- ✅ Frontend communicates with backend with <500ms response time
- ✅ Backend connects to Neon PostgreSQL in <2 seconds
- ✅ Health check endpoints respond in <1 second
- ✅ Images tagged and pushed to registry in <5 minutes
- ✅ Images can be pulled and run on different machine
- ✅ Gordon AI provides at least one optimization suggestion per Dockerfile
- ✅ Fallback to standard Docker CLI works without Gordon
- ✅ Development hot-reload reflects changes in <3 seconds
- ✅ All documentation complete and tested

## Next Steps

After completing this plan:
1. Run `/sp.tasks` to generate detailed implementation tasks
2. Implement tasks in priority order (P1 → P2 → P3)
3. Test each phase before proceeding to next
4. Document Gordon AI interactions and optimizations
5. Prepare images for Kubernetes deployment (separate feature)
