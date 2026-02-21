---
name: cloud-native-k8s-ai-deployer
description: Safely containerize, package, and deploy cloud-native applications on local Kubernetes using Docker AI (Gordon), Helm Charts, kubectl-ai, and Kagent with pre-flight error handling and AI-assisted operations.
---

# AI-Assisted Kubernetes Deployment Workflow

## Objective
Deploy a cloud-native application (frontend + backend) to Minikube using Docker, Helm, kubectl-ai, and Kagent — with **error-first validation** and **AI-driven DevOps automation**.

---

## Phase 1 — Preflight Validation (MANDATORY)

Before any containerization or deployment:

### 1. Project Structure Validation
- Confirm frontend and backend directories exist
- Verify `package.json`, `pyproject.toml`, or equivalent build files
- Ensure production build commands are defined

### 2. Docker Readiness Check
- Docker Desktop running
- Gordon (Docker AI Agent) enabled
- Dockerfile presence or auto-generation readiness

### 3. Kubernetes Environment Validation
- Minikube installed and running
- kubectl context set to Minikube
- Helm installed
- kubectl-ai and Kagent available

### 4. Configuration Validation
- Required environment variables exist
- Secrets not hardcoded
- Ports exposed correctly
- No localhost dependencies inside containers

### 5. Build Feasibility Test
- Run local builds
- Validate Docker build simulation
- Abort pipeline if any build or lint error occurs

If any check fails:
- Return structured error
- Provide exact fix
- STOP execution

---

## Phase 2 — Containerization (Docker AI / Gordon)

Only after Phase 1 passes:

1. Use Docker AI Agent (Gordon) to:
   - Generate optimized Dockerfiles
   - Suggest multi-stage builds
   - Optimize image size
   - Detect security vulnerabilities

2. Build images
3. Tag images for Minikube
4. Validate containers run locally

Fallback:
- If Gordon unavailable, use standard Docker CLI or AI-generated commands

---

## Phase 3 — Helm Chart Generation

1. Use kubectl-ai or Kagent to:
   - Generate Helm chart scaffolding
   - Define Deployments, Services, ConfigMaps
   - Set resource limits and probes

2. Ensure:
   - Separate charts for frontend and backend
   - Values.yaml supports replicas, env vars, ports
   - Secrets injected via Kubernetes secrets

---

## Phase 4 — Kubernetes Deployment (Minikube)

1. Deploy Helm charts to Minikube
2. Validate:
   - Pods running
   - Services exposed
   - No CrashLoopBackOff
   - Logs clean

3. Use kubectl-ai for:
   - Debugging failed pods
   - Scaling replicas
   - Restarting deployments

4. Use Kagent for:
   - Cluster health analysis
   - Resource optimization
   - Performance recommendations

---

## Phase 5 — Post-Deployment Validation

- Frontend reachable
- Backend API responding
- Database connectivity verified
- No auth or runtime errors
- Metrics healthy

---

## Deployment Rules
- Never deploy if preflight validation fails
- Never suppress Docker or Kubernetes errors
- Never bypass Helm charts
- Always use AI agents for diagnostics first
- Always return actionable fixes

---

## Successful Deployment Criteria
- Containers built successfully
- Helm charts install cleanly
- Pods healthy
- Services accessible
- System stable on Minikube
