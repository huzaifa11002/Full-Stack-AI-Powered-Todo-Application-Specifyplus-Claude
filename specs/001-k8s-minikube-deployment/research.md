# Research: Kubernetes Deployment on Minikube

**Feature**: 001-k8s-minikube-deployment
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document contains research findings for deploying the Todo Chatbot application to a local Minikube Kubernetes cluster using Helm charts, kubectl-ai, and Kagent.

## 1. Minikube Installation & Configuration

### Installation Methods

**macOS**:
```bash
# Using Homebrew (recommended)
brew install minikube

# Verify installation
minikube version
```

**Linux**:
```bash
# Download and install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

**Windows**:
```powershell
# Using Chocolatey
choco install minikube

# Or download installer from https://minikube.sigs.k8s.io/docs/start/
```

### Resource Allocation Best Practices

**Minimum Requirements**:
- CPU: 4 cores
- Memory: 8GB RAM
- Disk: 20GB free space

**Recommended Configuration**:
```bash
minikube start --cpus=4 --memory=8192 --disk-size=20g --driver=docker
```

**Rationale**:
- 4 CPUs: Sufficient for frontend (2 replicas) + backend (1-5 replicas) + system pods
- 8GB RAM: Accommodates application pods with defined limits + Kubernetes system components
- 20GB disk: Container images + logs + temporary data
- Docker driver: Best cross-platform compatibility and performance

### Driver Selection

**Decision**: Docker driver (recommended)

**Comparison**:

| Driver | Pros | Cons | Use Case |
|--------|------|------|----------|
| Docker | Cross-platform, no extra virtualization, fast | Requires Docker installed | **Recommended for most users** |
| VirtualBox | Mature, stable | Slower, requires VirtualBox | Legacy systems |
| Hyper-V | Native Windows virtualization | Windows-only, requires Hyper-V enabled | Windows enterprise |
| Podman | Docker alternative | Less mature, limited support | Docker-free environments |

### Addon Management

**Required Addons**:
```bash
# Enable NGINX Ingress Controller
minikube addons enable ingress

# Enable Metrics Server (for HPA)
minikube addons enable metrics-server

# Optional: Enable Dashboard
minikube addons enable dashboard
```

**Addon Verification**:
```bash
# List enabled addons
minikube addons list

# Verify ingress controller pods
kubectl get pods -n ingress-nginx

# Verify metrics server
kubectl get deployment metrics-server -n kube-system
```

## 2. Helm 3.x Best Practices

### Chart Structure and Organization

**Standard Helm Chart Structure**:
```
chart-name/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── values-dev.yaml     # Development environment overrides
├── values-prod.yaml    # Production environment overrides
├── templates/          # Kubernetes manifest templates
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   ├── NOTES.txt      # Post-install instructions
│   └── _helpers.tpl   # Template helper functions
├── charts/            # Chart dependencies (if any)
└── .helmignore        # Files to ignore
```

### Values File Patterns

**Multi-Environment Strategy**:
1. **values.yaml**: Default values, development-friendly
2. **values-dev.yaml**: Development-specific overrides
3. **values-prod.yaml**: Production-specific overrides

**Usage**:
```bash
# Development deployment
helm install myapp ./chart -f values.yaml -f values-dev.yaml

# Production deployment
helm install myapp ./chart -f values.yaml -f values-prod.yaml
```

### Template Functions and Helpers

**Common Helper Patterns** (_helpers.tpl):
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "chart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "chart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "chart.labels" -}}
helm.sh/chart: {{ include "chart.chart" . }}
{{ include "chart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "chart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Chart Versioning

**Semantic Versioning**:
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible functionality additions
- PATCH: Backward-compatible bug fixes

**Chart.yaml Example**:
```yaml
apiVersion: v2
name: todo-frontend
description: Helm chart for Todo Frontend (Next.js)
type: application
version: 1.0.0        # Chart version
appVersion: "1.0.0"   # Application version
```

### Linting and Validation

**Validation Commands**:
```bash
# Lint chart for errors and best practices
helm lint ./chart

# Dry-run to validate rendering
helm install myapp ./chart --dry-run --debug

# Template rendering without installation
helm template myapp ./chart

# Validate against Kubernetes API
helm install myapp ./chart --dry-run --debug | kubectl apply --dry-run=client -f -
```

## 3. kubectl-ai Integration

### Installation Methods

**npm (Node.js required)**:
```bash
npm install -g kubectl-ai

# Verify installation
kubectl-ai --version
```

**pip (Python required)**:
```bash
pip install kubectl-ai

# Verify installation
kubectl-ai --version
```

### API Key Configuration

**OpenAI Configuration**:
```bash
# Set API key as environment variable
export OPENAI_API_KEY="sk-..."

# Or create config file
mkdir -p ~/.kubectl-ai
cat > ~/.kubectl-ai/config.yaml <<EOF
api_key: ${OPENAI_API_KEY}
model: gpt-4o
temperature: 0.7
EOF
```

**Gemini Configuration**:
```bash
# Set API key as environment variable
export GEMINI_API_KEY="your-gemini-api-key"

# Update config file
cat > ~/.kubectl-ai/config.yaml <<EOF
api_key: ${GEMINI_API_KEY}
provider: gemini
model: gemini-pro
temperature: 0.7
EOF
```

### Command Patterns and Capabilities

**Deployment Operations**:
```bash
# Deploy resources
kubectl-ai "deploy a nginx pod with 2 replicas"

# Scale deployments
kubectl-ai "scale the frontend deployment to 3 replicas"

# Update resources
kubectl-ai "update the backend deployment to use image version 2.0"
```

**Information Queries**:
```bash
# Status checks
kubectl-ai "show me all pods in the todo-app namespace"
kubectl-ai "are all pods running in the cluster?"

# Resource inspection
kubectl-ai "describe the frontend service"
kubectl-ai "show me the logs of the backend pod"
```

**Troubleshooting**:
```bash
# Diagnose issues
kubectl-ai "why is the frontend pod in CrashLoopBackOff?"
kubectl-ai "check why the pods are failing"

# Network debugging
kubectl-ai "test connectivity from frontend to backend service"
```

### Integration with kubectl Workflows

**Best Practices**:
1. Use kubectl-ai for exploratory operations and quick tasks
2. Use standard kubectl for scripted/automated operations
3. Verify kubectl-ai generated commands before execution
4. Use kubectl-ai for learning Kubernetes patterns

## 4. Kagent Integration

### Installation and Setup

**Installation** (check official documentation for latest method):
```bash
# Via pip (if available)
pip install kagent

# Or download binary
curl -LO https://github.com/kagent/releases/latest/download/kagent
chmod +x kagent
sudo mv kagent /usr/local/bin/

# Verify installation
kagent version
```

**Initialization**:
```bash
# Initialize with Minikube context
kagent init --context minikube

# Verify connection
kagent "check cluster connectivity"
```

### Cluster Health Analysis Capabilities

**Health Analysis Commands**:
```bash
# Overall cluster health
kagent "analyze the cluster health"

# Resource utilization
kagent "show me resource utilization across all nodes"

# Namespace-specific analysis
kagent "analyze the todo-app namespace for issues"

# Pod health check
kagent "are there any unhealthy pods?"
```

### Optimization Recommendation Patterns

**Resource Optimization**:
```bash
# Get optimization suggestions
kagent "optimize resource allocation for todo-app namespace"

# Cost analysis
kagent "what resources are being wasted in my cluster?"

# Scaling recommendations
kagent "should I scale up or down any deployments?"
```

**Performance Analysis**:
```bash
# Identify bottlenecks
kagent "identify performance bottlenecks"

# Network analysis
kagent "diagnose network connectivity issues in todo-app"

# Pod restart analysis
kagent "why are my pods restarting frequently?"
```

### Integration with Minikube

**Minikube-Specific Considerations**:
- Kagent should recognize single-node cluster limitations
- Resource recommendations should account for local machine constraints
- Network analysis should consider Minikube networking model

## 5. Kubernetes Resource Management

### Resource Requests vs Limits

**Definitions**:
- **Requests**: Minimum resources guaranteed to the pod (used for scheduling)
- **Limits**: Maximum resources the pod can consume (enforced by kubelet)

**Best Practices**:
```yaml
resources:
  requests:
    cpu: 250m      # Guaranteed CPU
    memory: 256Mi  # Guaranteed memory
  limits:
    cpu: 500m      # Maximum CPU (throttled if exceeded)
    memory: 512Mi  # Maximum memory (OOMKilled if exceeded)
```

### Quality of Service (QoS) Classes

**QoS Classes** (automatically assigned):

1. **Guaranteed**: requests == limits for all containers
   - Highest priority, last to be evicted
   - Best for critical workloads

2. **Burstable**: requests < limits (or only requests defined)
   - Medium priority
   - Good for most applications

3. **BestEffort**: No requests or limits defined
   - Lowest priority, first to be evicted
   - Only for non-critical workloads

**Recommendation**: Use **Burstable** QoS for our application (requests < limits)

### Resource Allocation for Todo App

**Frontend (Next.js)**:
```yaml
resources:
  requests:
    cpu: 250m      # 0.25 CPU cores
    memory: 256Mi  # 256 MiB
  limits:
    cpu: 500m      # 0.5 CPU cores (2x burst)
    memory: 512Mi  # 512 MiB (2x burst)
```

**Rationale**:
- Next.js is relatively lightweight
- 2 replicas = 500m CPU request, 1000m limit total
- Leaves room for backend and system pods

**Backend (FastAPI + AI)**:
```yaml
resources:
  requests:
    cpu: 500m      # 0.5 CPU cores
    memory: 512Mi  # 512 MiB
  limits:
    cpu: 1000m     # 1 CPU core (2x burst)
    memory: 1Gi    # 1 GiB (2x burst)
```

**Rationale**:
- AI operations are CPU-intensive
- Needs more memory for model inference
- HPA will scale based on these limits

**Total Resource Usage** (at minimum scale):
- Frontend: 2 replicas × 250m CPU = 500m request, 1000m limit
- Backend: 1 replica × 500m CPU = 500m request, 1000m limit
- System pods: ~500m CPU, ~1Gi memory
- **Total**: ~1.5 CPU request, ~2.5 CPU limit, ~2.5Gi memory

**Fits within Minikube**: 4 CPU, 8GB RAM ✅

## 6. Health Check Patterns

### Liveness vs Readiness Probes

**Liveness Probe**:
- Purpose: Detect if container is alive
- Action: Restart container if probe fails
- Use case: Detect deadlocks, infinite loops

**Readiness Probe**:
- Purpose: Detect if container is ready to serve traffic
- Action: Remove from service endpoints if probe fails
- Use case: Prevent traffic to initializing/overloaded pods

**Startup Probe** (optional):
- Purpose: Detect if application has started
- Action: Disable liveness/readiness until startup succeeds
- Use case: Slow-starting applications

### Probe Configuration Best Practices

**Frontend Health Check**:
```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 30  # Wait 30s after container starts
  periodSeconds: 10        # Check every 10s
  timeoutSeconds: 5        # Timeout after 5s
  failureThreshold: 3      # Restart after 3 consecutive failures
  successThreshold: 1      # Consider healthy after 1 success

readinessProbe:
  httpGet:
    path: /api/health
    port: 3000
  initialDelaySeconds: 10  # Start checking after 10s
  periodSeconds: 5         # Check every 5s
  timeoutSeconds: 3        # Timeout after 3s
  failureThreshold: 3      # Remove from service after 3 failures
  successThreshold: 1      # Add to service after 1 success
```

**Backend Health Check**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
  successThreshold: 1

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
  successThreshold: 1
```

### Health Endpoint Implementation

**Requirements**:
- Return 200 OK when healthy
- Return 5xx when unhealthy
- Check critical dependencies (database, external services)
- Keep checks lightweight (< 1s response time)
- Don't include non-critical checks in liveness probe

## 7. Horizontal Pod Autoscaler (HPA)

### Metrics Server Requirements

**Installation**:
```bash
# Enable metrics-server addon in Minikube
minikube addons enable metrics-server

# Verify metrics-server is running
kubectl get deployment metrics-server -n kube-system

# Test metrics availability
kubectl top nodes
kubectl top pods -n todo-app
```

### CPU and Memory-Based Scaling

**HPA Configuration for Backend**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # Scale up when CPU > 70%
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80  # Scale up when memory > 80%
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60  # Scale down max 50% per minute
    scaleUp:
      stabilizationWindowSeconds: 0  # Scale up immediately
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60  # Scale up max 100% per minute
```

**Rationale**:
- CPU threshold: 70% allows headroom for bursts
- Memory threshold: 80% prevents OOM kills
- Scale-down delay: Prevents flapping during variable load
- Scale-up immediate: Responds quickly to load spikes

### Custom Metrics (Future Consideration)

**Potential Custom Metrics**:
- Request rate (requests per second)
- Request latency (p95, p99)
- Queue depth (for async processing)
- AI API call rate

**Note**: Custom metrics require Prometheus Adapter or similar, out of scope for Phase IV.

## 8. NGINX Ingress Controller

### Minikube Ingress Addon

**Enable Ingress**:
```bash
# Enable NGINX Ingress Controller
minikube addons enable ingress

# Verify ingress controller pods
kubectl get pods -n ingress-nginx

# Wait for ingress controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

### Ingress Resource Configuration

**Frontend Ingress**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-frontend
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: todo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 3000
```

### Path-Based Routing

**Multiple Services**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app
spec:
  ingressClassName: nginx
  rules:
  - host: todo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: todo-backend
            port:
              number: 8000
```

### Local DNS Configuration

**Add to /etc/hosts** (macOS/Linux):
```bash
# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

# Add to /etc/hosts
echo "$MINIKUBE_IP todo.local" | sudo tee -a /etc/hosts

# Verify
ping todo.local
```

**Add to C:\Windows\System32\drivers\etc\hosts** (Windows):
```powershell
# Get Minikube IP
$MINIKUBE_IP = minikube ip

# Add to hosts file (run as Administrator)
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "$MINIKUBE_IP todo.local"
```

## Research Conclusions

### Key Decisions Summary

1. **Minikube Driver**: Docker (cross-platform, performant)
2. **Helm Chart Organization**: Separate charts for frontend/backend
3. **Resource Allocation**: Conservative with burst capacity
4. **Ingress**: NGINX Ingress Controller (production-like)
5. **HPA**: Backend only, CPU + Memory metrics
6. **Secret Management**: Kubernetes Secrets (sufficient for local)

### Implementation Readiness

All research topics have been investigated and decisions documented. The implementation can proceed with:
- Clear installation procedures for all tools
- Defined resource allocation strategy
- Health check patterns established
- HPA configuration specified
- Ingress setup documented

### Next Steps

Proceed to Phase 1: Design & Architecture
- Create data-model.md with Kubernetes resource definitions
- Create contracts/ with Helm chart templates
- Create quickstart.md with deployment instructions

---

**Research Status**: Complete
**Date**: 2026-01-20
**Next Phase**: Phase 1 - Design & Architecture
