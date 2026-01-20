# Docker Registry Deployment Guide

## Image Tagging Completed ✅

Images have been tagged with both `latest` and semantic version tags:

**Backend:**
- `yourusername/todo-backend:latest`
- `yourusername/todo-backend:v1.0.0`

**Frontend:**
- `yourusername/todo-frontend:latest`
- `yourusername/todo-frontend:v1.0.0`

## Pushing to Docker Hub (Manual Step)

To push images to Docker Hub, follow these steps:

### 1. Login to Docker Hub
```bash
docker login
# Enter your Docker Hub username and password/token
```

### 2. Push Images
```bash
# Push backend images
docker push yourusername/todo-backend:latest
docker push yourusername/todo-backend:v1.0.0

# Push frontend images
docker push yourusername/todo-frontend:latest
docker push yourusername/todo-frontend:v1.0.0
```

### 3. Verify on Docker Hub
Visit https://hub.docker.com/u/yourusername to verify images are uploaded.

### 4. Pull and Test on Different Machine
```bash
# Pull images
docker pull yourusername/todo-backend:v1.0.0
docker pull yourusername/todo-frontend:v1.0.0

# Run containers
docker run -d -p 8000:8000 \
  -e DATABASE_URL="your-db-url" \
  -e BETTER_AUTH_SECRET="your-secret" \
  -e OPENAI_API_KEY="your-key" \
  yourusername/todo-backend:v1.0.0

docker run -d -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
  yourusername/todo-frontend:v1.0.0
```

## Alternative: Local Registry

For testing without Docker Hub:

```bash
# Start local registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for local registry
docker tag todo-backend:optimized localhost:5000/todo-backend:v1.0.0
docker tag todo-frontend:optimized localhost:5000/todo-frontend:v1.0.0

# Push to local registry
docker push localhost:5000/todo-backend:v1.0.0
docker push localhost:5000/todo-frontend:v1.0.0

# Pull from local registry
docker pull localhost:5000/todo-backend:v1.0.0
docker pull localhost:5000/todo-frontend:v1.0.0
```

## Image Metadata

Images include proper labels for traceability:
- Version information
- Build date
- Git commit hash (if in CI/CD)
- Repository URL

## Status

✅ Images tagged with semantic versions
✅ Ready for registry push (requires credentials)
✅ Local registry alternative documented
⏸️ Actual push to Docker Hub requires user credentials
