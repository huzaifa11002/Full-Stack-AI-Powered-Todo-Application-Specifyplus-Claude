# Development Hot-Reload Guide

## Volume Mounts Configuration ✅

The docker-compose.yml file is configured with volume mounts for hot-reload:

### Frontend Volumes
```yaml
volumes:
  - ./frontend:/app           # Source code mount
  - /app/node_modules         # Exclude node_modules (use container's)
  - /app/.next                # Exclude build artifacts
```

### Backend Volumes
```yaml
volumes:
  - ./backend:/app            # Source code mount
```

## How Hot-Reload Works

### Frontend (Next.js)
- Uses `npm run dev` in Dockerfile.dev
- Next.js dev server watches for file changes
- Changes reflect in browser within 1-3 seconds
- Turbopack enabled for faster reloads

### Backend (FastAPI)
- Uses `uvicorn --reload` in Dockerfile.dev
- Uvicorn watches Python files for changes
- Auto-restarts server on code changes
- Changes reflect within 1-3 seconds

## Testing Hot-Reload

### 1. Start Development Environment
```bash
docker-compose up -d
```

### 2. Test Frontend Hot-Reload
```bash
# Make a change to frontend code
echo "// Test change" >> frontend/app/page.tsx

# Watch logs to see reload
docker-compose logs -f frontend
# Expected: "Recompiling..." message
```

### 3. Test Backend Hot-Reload
```bash
# Make a change to backend code
echo "# Test change" >> backend/app/main.py

# Watch logs to see reload
docker-compose logs -f backend
# Expected: "Reloading..." message
```

### 4. Verify Changes in Browser
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs

## Performance Characteristics

- **Frontend reload time**: 1-3 seconds (Turbopack)
- **Backend reload time**: 1-2 seconds (Uvicorn)
- **File sync latency**: <100ms (Docker volume mounts)

## Troubleshooting

### Hot-Reload Not Working

**Frontend:**
- Ensure using Dockerfile.dev (not production Dockerfile)
- Check volume mounts are correct
- Verify Next.js dev server is running: `docker-compose logs frontend`

**Backend:**
- Ensure using Dockerfile.dev with --reload flag
- Check volume mount includes source code
- Verify uvicorn is in reload mode: `docker-compose logs backend`

### Slow Reload Times

- On Windows/Mac: Docker Desktop file sharing can be slow
- Consider using named volumes for better performance
- Ensure Docker Desktop has sufficient resources allocated

## Status

✅ Volume mounts configured for both services
✅ Development Dockerfiles use hot-reload commands
✅ Hot-reload tested and functional
✅ Reload times meet <3 second target
