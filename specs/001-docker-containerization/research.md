# Research: Docker Containerization Best Practices

**Feature**: 001-docker-containerization
**Date**: 2026-01-18
**Purpose**: Research Docker best practices, technical decisions, and optimization strategies for containerizing Next.js and FastAPI applications

## Research Summary

This document consolidates research findings for all technical decisions required to implement Docker containerization with AI-assisted optimization using Gordon.

## 1. Docker Multi-Stage Build Optimization

### Research Question
What are the optimal layer ordering and caching strategies for Next.js standalone builds?

### Findings

**Next.js Standalone Build Pattern**:
- Next.js 16+ supports `output: 'standalone'` in next.config.js
- Standalone output creates a minimal server.js with only required dependencies
- Reduces image size by 50-70% compared to full node_modules copy
- Requires copying public/ and .next/static/ directories separately

**Optimal Layer Ordering**:
1. Install production dependencies only (deps stage)
2. Install all dependencies and build (builder stage)
3. Copy standalone output and static assets (runner stage)

**Caching Strategy**:
- Copy package.json and package-lock.json first (before COPY . .)
- Run npm ci to leverage Docker layer caching
- Changes to source code don't invalidate dependency layers
- Use .dockerignore to exclude node_modules, .next, .git

**Decision**: Use 3-stage build (deps → builder → runner) with standalone output
**Rationale**: Maximizes layer caching, minimizes final image size, follows Next.js best practices
**Alternatives Considered**: 2-stage build (simpler but less optimized), single-stage (much larger images)

## 2. Python Container Best Practices

### Research Question
Should we use virtual environments in Docker? What are the tradeoffs between python:slim and python:alpine?

### Findings

**Virtual Environment in Docker**:
- **Recommendation**: Use virtual environment even in Docker
- **Benefits**: Clean dependency isolation, easier to copy between stages, follows Python best practices
- **Pattern**: Create venv in builder stage, copy entire venv to runner stage
- **Alternative**: Global pip install works but harder to manage in multi-stage builds

**Base Image Comparison**:

| Aspect | python:slim | python:alpine |
|--------|-------------|---------------|
| Base size | ~120MB | ~50MB |
| Compatibility | Excellent | Good (some issues) |
| Build time | Fast | Slower (compilation) |
| C extensions | Works out of box | Requires build tools |
| psycopg2 | Works natively | Needs compilation |

**Decision**: Use python:3.11-slim with virtual environment
**Rationale**: Better compatibility with psycopg2 and other C extensions, faster builds, slightly larger but more reliable
**Alternatives Considered**: python:alpine (smaller but compilation issues), global pip install (less isolated)

## 3. Docker Compose Networking

### Research Question
What networking strategy enables reliable service-to-service communication?

### Findings

**Bridge Network (Default)**:
- Docker Compose creates default bridge network automatically
- Services can reference each other by service name (DNS resolution)
- Example: frontend can reach backend at `http://backend:8000`
- Isolated from host network by default

**Custom Bridge Network**:
- Explicitly define network in docker-compose.yml
- Same DNS resolution capabilities
- Better control over network configuration
- Can define multiple networks for isolation

**Service Discovery**:
- Docker's embedded DNS server resolves service names to container IPs
- Works automatically within same network
- No additional configuration required

**Volume Mount Strategy for Hot-Reload**:
- Mount source directory as volume: `./frontend:/app`
- Exclude node_modules: `/app/node_modules` (anonymous volume)
- Exclude build artifacts: `/app/.next` (anonymous volume)
- Enables hot-reload without rebuilding image

**Decision**: Use explicit bridge network with service name DNS resolution
**Rationale**: Clear configuration, reliable service discovery, standard Docker Compose pattern
**Alternatives Considered**: Default network (works but less explicit), host network (breaks isolation)

## 4. Docker AI Agent (Gordon) Capabilities

### Research Question
What can Gordon do, and how should we integrate it?

### Findings

**Gordon Capabilities** (Docker Desktop 4.53+):
- Dockerfile generation from natural language descriptions
- Dockerfile analysis and optimization suggestions
- Build troubleshooting and error diagnosis
- Security best practices recommendations
- Image size optimization tips
- Layer caching optimization advice

**Command Patterns**:
```bash
# Analysis
docker ai "Review this Dockerfile and suggest optimizations" < Dockerfile

# Generation
docker ai "Generate a multi-stage Dockerfile for Next.js 16 with standalone output"

# Troubleshooting
docker ai "Why is my Docker build failing at npm install?"

# Best practices
docker ai "What security best practices should I follow for Python Docker images?"
```

**Limitations**:
- Requires Docker Desktop 4.53+ with Beta features enabled
- May not be available in all environments (CI/CD, older Docker versions)
- Suggestions need human review and validation
- Not a replacement for Docker expertise

**Decision**: Optional enhancement with documented fallback to standard Docker CLI
**Rationale**: Provides value when available but doesn't block implementation, maintains portability
**Alternatives Considered**: Require Gordon (limits adoption), skip Gordon (misses optimization opportunity)

## 5. Container Security Hardening

### Research Question
What security best practices should we implement for production containers?

### Findings

**Non-Root User Implementation**:
- Create dedicated user with specific UID/GID
- Frontend: `adduser --system --uid 1001 nextjs`
- Backend: `useradd -m -u 1001 appuser`
- Switch to non-root user before CMD: `USER nextjs`
- Prevents privilege escalation attacks

**Minimal Base Images**:
- Alpine: ~5-50MB base, minimal attack surface
- Slim: ~50-150MB base, better compatibility
- Full: ~200-500MB base, largest attack surface
- Fewer packages = fewer vulnerabilities

**Health Check Best Practices**:
- Implement application-level health endpoints (/health)
- Configure HEALTHCHECK in Dockerfile
- Set appropriate intervals (30s) and timeouts (10s)
- Include start period for slow-starting apps (40s)
- Return 200 OK for healthy, non-200 for unhealthy

**Additional Security Measures**:
- Use .dockerignore to exclude sensitive files
- Never hardcode secrets in Dockerfiles
- Use multi-stage builds to exclude build tools
- Run vulnerability scans with Docker Scout
- Keep base images updated

**Decision**: Implement non-root user, minimal base images, and health checks
**Rationale**: Industry standard security practices, required for Kubernetes deployment
**Alternatives Considered**: Root user (insecure), no health checks (unreliable detection)

## 6. Image Registry Strategies

### Research Question
What registry should we use, and how should we tag images?

### Findings

**Registry Options**:

| Registry | Pros | Cons | Cost |
|----------|------|------|------|
| Docker Hub | Easy, widely used, free tier | Public by default, rate limits | Free (public) |
| GitHub Container Registry | Integrated with GitHub, free | Requires GitHub account | Free |
| AWS ECR | Integrated with AWS, secure | AWS-specific, setup required | Pay per GB |
| Local Registry | Full control, no rate limits | Requires setup, not shared | Infrastructure cost |

**Image Tagging Conventions**:
- **latest**: Always points to most recent build (convenience)
- **Semantic versioning**: v1.0.0, v1.0.1, v1.1.0 (traceability)
- **Git commit hash**: abc123f (exact source tracking)
- **Build number**: build-42 (CI/CD integration)

**Best Practice**: Use multiple tags
```bash
docker tag myapp:latest myapp:v1.0.0
docker tag myapp:latest myapp:abc123f
docker push myapp:v1.0.0
docker push myapp:latest
```

**Image Metadata (Labels)**:
- org.opencontainers.image.version
- org.opencontainers.image.created
- org.opencontainers.image.revision (git commit)
- org.opencontainers.image.source (repository URL)

**Decision**: Docker Hub as primary registry, both latest and semantic version tags
**Rationale**: Accessible, free tier sufficient, widely used, supports both convenience and traceability
**Alternatives Considered**: Local registry (more setup), cloud registry (additional cost), latest only (no rollback)

## Technical Decisions Summary

### Decision Matrix

| Decision | Choice | Rationale | Impact |
|----------|--------|-----------|--------|
| Frontend base image | node:20-alpine | Smallest size, Next.js compatible | <200MB target achievable |
| Backend base image | python:3.11-slim | Best compatibility, reasonable size | <150MB target achievable |
| Multi-stage builds | Yes (3-stage frontend, 2-stage backend) | 50-70% size reduction | Smaller images, faster deploys |
| Virtual environment | Yes (Python only) | Clean isolation, easier copying | Better dependency management |
| Dockerfile separation | Separate dev/prod files | Clear separation of concerns | Easier to maintain |
| Docker Compose files | Separate dev/prod files | Different configurations | Clear environment distinction |
| Gordon AI | Optional enhancement | Value without dependency | Better optimization when available |
| Health checks | Application + Dockerfile | Reliable health detection | Kubernetes-ready |
| Non-root user | Yes (both services) | Security best practice | Reduced attack surface |
| Registry | Docker Hub | Accessible, free tier | Easy sharing and deployment |
| Tagging strategy | latest + semantic versions | Convenience + traceability | Easy rollback capability |

## Implementation Recommendations

### Priority 1 (Must Have)
1. Multi-stage Dockerfiles for both services
2. Non-root user execution
3. Health check endpoints
4. Docker Compose for local development
5. .dockerignore files
6. Environment variable configuration

### Priority 2 (Should Have)
1. Gordon AI optimization suggestions
2. Docker Scout security scanning
3. Semantic version tagging
4. Image metadata labels
5. Development hot-reload support

### Priority 3 (Nice to Have)
1. Build time optimization
2. Advanced layer caching
3. Multi-platform builds
4. Custom registry setup

## References

- Next.js Docker documentation: https://nextjs.org/docs/deployment#docker-image
- Docker multi-stage builds: https://docs.docker.com/build/building/multi-stage/
- Python Docker best practices: https://docs.docker.com/language/python/
- Docker Compose networking: https://docs.docker.com/compose/networking/
- Docker security best practices: https://docs.docker.com/develop/security-best-practices/
- Docker AI Agent (Gordon): Docker Desktop 4.53+ Beta features

## Conclusion

All research questions have been resolved with clear technical decisions. The implementation approach balances:
- **Image size optimization**: Multi-stage builds, minimal base images
- **Security**: Non-root users, minimal attack surface, health checks
- **Developer experience**: Hot-reload, clear documentation, Gordon AI assistance
- **Reliability**: Fallback strategies, proven patterns, comprehensive testing

No NEEDS CLARIFICATION items remain. Ready to proceed with Phase 1 design artifacts.
