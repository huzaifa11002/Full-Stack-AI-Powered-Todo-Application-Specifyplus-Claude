# Frontend Dockerfile Contract

**Feature**: 001-docker-containerization
**Date**: 2026-01-18
**Purpose**: Specification for the Next.js frontend production Dockerfile

## Contract Overview

This contract defines the requirements and structure for the frontend production Dockerfile that creates an optimized Next.js container image.

## Requirements

### Functional Requirements
- **FR-001**: MUST use node:20-alpine as base image
- **FR-002**: MUST implement multi-stage build (deps → builder → runner)
- **FR-003**: MUST produce image <200MB in size
- **FR-004**: MUST run as non-root user (nextjs, UID 1001)
- **FR-005**: MUST expose port 3000
- **FR-006**: MUST implement HEALTHCHECK directive
- **FR-007**: MUST use Next.js standalone output mode
- **FR-008**: MUST copy public/ and .next/static/ directories
- **FR-009**: MUST set NODE_ENV=production
- **FR-010**: MUST disable Next.js telemetry

### Non-Functional Requirements
- **NFR-001**: Build MUST complete in <10 minutes on standard hardware
- **NFR-002**: Layer caching MUST be optimized (package.json before source)
- **NFR-003**: Image MUST pass Docker Scout vulnerability scan
- **NFR-004**: Health check MUST respond in <1 second

## Dockerfile Structure

### Stage 1: Dependencies (deps)
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app

# Install production dependencies only
COPY package.json package-lock.json* ./
RUN npm ci --only=production
```

**Purpose**: Install production dependencies in isolated stage
**Output**: node_modules/ with production dependencies only

### Stage 2: Builder
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app

# Install all dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source code
COPY . .

# Build Next.js application
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production
RUN npm run build
```

**Purpose**: Build Next.js application with all dependencies
**Output**: .next/ directory with standalone build

### Stage 3: Runner (Final Image)
```dockerfile
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

**Purpose**: Create minimal runtime image with only required files
**Output**: Production-ready container image

## Environment Variables

### Build-Time Variables
- `NEXT_TELEMETRY_DISABLED=1`: Disable Next.js telemetry
- `NODE_ENV=production`: Set production mode

### Runtime Variables (from .env)
- `NEXT_PUBLIC_API_URL`: Backend API URL (required)
- `BETTER_AUTH_SECRET`: Authentication secret (required)
- `BETTER_AUTH_URL`: Frontend URL (required)
- `PORT=3000`: HTTP port (default)
- `HOSTNAME=0.0.0.0`: Bind address (default)

## Dependencies

### Required Files
- `package.json`: Node.js dependencies
- `package-lock.json`: Locked dependency versions
- `next.config.js`: Next.js configuration with `output: 'standalone'`
- `app/api/health/route.ts`: Health check endpoint

### Required Configuration
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  // ... other config
}

module.exports = nextConfig
```

## Build Commands

### Build Production Image
```bash
docker build -t todo-frontend:latest -f frontend/Dockerfile ./frontend
```

### Build with Tag
```bash
docker build -t todo-frontend:v1.0.0 -f frontend/Dockerfile ./frontend
```

### Build with Gordon AI
```bash
docker ai "Build an optimized Next.js production image from ./frontend"
```

## Validation

### Size Validation
```bash
docker images todo-frontend:latest --format "{{.Size}}"
# Expected: <200MB
```

### User Validation
```bash
docker run --rm todo-frontend:latest whoami
# Expected: nextjs
```

### Health Check Validation
```bash
docker run -d --name test-frontend -p 3000:3000 todo-frontend:latest
sleep 40  # Wait for start period
docker inspect test-frontend --format='{{.State.Health.Status}}'
# Expected: healthy
docker rm -f test-frontend
```

### Port Validation
```bash
docker run -d --name test-frontend -p 3000:3000 todo-frontend:latest
curl http://localhost:3000/api/health
# Expected: {"status":"healthy"}
docker rm -f test-frontend
```

## Error Handling

### Build Failures
- **npm ci fails**: Check package-lock.json exists and is valid
- **npm run build fails**: Check Next.js configuration and source code
- **COPY fails**: Check files exist in build context

### Runtime Failures
- **Container exits immediately**: Check CMD and entry point
- **Health check fails**: Verify /api/health endpoint exists and responds
- **Permission denied**: Verify non-root user has access to required files

## Security Considerations

- ✅ Non-root user (nextjs, UID 1001)
- ✅ Minimal base image (alpine)
- ✅ No secrets in image layers
- ✅ Production dependencies only in final image
- ✅ Health check for monitoring
- ✅ Proper file ownership (chown nextjs:nodejs)

## Performance Optimization

### Layer Caching
1. Copy package files first (changes less frequently)
2. Install dependencies (cached if package files unchanged)
3. Copy source code last (changes most frequently)

### Image Size Optimization
- Use alpine base (smallest)
- Multi-stage build (exclude build tools)
- Production dependencies only
- Standalone output (minimal runtime)

### Build Speed Optimization
- Leverage Docker layer caching
- Use npm ci (faster than npm install)
- Parallel stage execution where possible

## Testing Strategy

### Build Testing
```bash
# Test build succeeds
docker build -t test-frontend ./frontend

# Test image size
SIZE=$(docker images test-frontend --format "{{.Size}}")
echo "Image size: $SIZE"

# Test non-root user
docker run --rm test-frontend whoami
```

### Runtime Testing
```bash
# Test container starts
docker run -d --name test-frontend -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://backend:8000 \
  -e BETTER_AUTH_SECRET=test-secret \
  test-frontend

# Test health check
sleep 40
docker inspect test-frontend --format='{{.State.Health.Status}}'

# Test HTTP response
curl http://localhost:3000/api/health

# Cleanup
docker rm -f test-frontend
```

## Acceptance Criteria

- ✅ Dockerfile builds without errors
- ✅ Image size is <200MB
- ✅ Container runs as non-root user (nextjs)
- ✅ Health check endpoint responds with 200 OK
- ✅ Container starts in <30 seconds
- ✅ Port 3000 is accessible
- ✅ Environment variables are loaded correctly
- ✅ No vulnerabilities in Docker Scout scan

## Related Contracts

- [backend-dockerfile.contract.md](./backend-dockerfile.contract.md) - Backend Dockerfile specification
- [docker-compose.contract.md](./docker-compose.contract.md) - Docker Compose specification
- [../data-model.md](../data-model.md) - Docker artifacts data model

## Version History

- v1.0.0 (2026-01-18): Initial contract specification
