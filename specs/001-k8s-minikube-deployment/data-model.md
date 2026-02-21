# Data Model: Kubernetes Resources

**Feature**: 001-k8s-minikube-deployment
**Date**: 2026-01-20
**Status**: Complete

## Overview

This document defines all Kubernetes resources required for deploying the Todo Chatbot application to Minikube. Resources are organized by type and include complete specifications.

## Resource Hierarchy

```
Namespace: todo-app
├── Deployments
│   ├── todo-frontend (2 replicas)
│   └── todo-backend (1-5 replicas, HPA-managed)
├── Services
│   ├── todo-frontend (ClusterIP)
│   └── todo-backend (ClusterIP)
├── Ingress
│   └── todo-frontend (NGINX)
├── ConfigMaps
│   ├── frontend-config
│   └── backend-config
├── Secrets
│   ├── frontend-secrets
│   └── backend-secrets
└── HorizontalPodAutoscaler
    └── todo-backend-hpa
```

## 1. Namespace

**Purpose**: Logical isolation for all Todo application resources

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    app: todo-chatbot
    environment: development
```

**Attributes**:
- **name**: `todo-app` - Unique identifier for the namespace
- **labels**: Metadata for organization and selection

## 2. Deployments

### 2.1 Frontend Deployment

**Purpose**: Manages frontend (Next.js) pod replicas with health checks and resource limits

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: todo-app
  labels:
    app: todo-frontend
    component: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
        component: frontend
    spec:
      containers:
      - name: frontend
        image: yourusername/todo-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://todo-backend:8000"
        - name: BETTER_AUTH_URL
          value: "http://todo.local"
        envFrom:
        - secretRef:
            name: frontend-secrets
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
          successThreshold: 1
        readinessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
          successThreshold: 1
        resources:
          requests:
            cpu: 250m
            memory: 256Mi
          limits:
            cpu: 500m
            memory: 512Mi
```

**Key Attributes**:
- **replicas**: 2 - Fixed replica count (no autoscaling)
- **image**: Container image from Docker Hub or local registry
- **ports**: Exposes port 3000 for HTTP traffic
- **env**: Non-sensitive configuration (API URLs)
- **envFrom**: Sensitive configuration from Secrets
- **livenessProbe**: Detects unhealthy containers, triggers restart
- **readinessProbe**: Controls traffic routing to ready pods
- **resources**: CPU and memory requests/limits for scheduling and QoS

### 2.2 Backend Deployment

**Purpose**: Manages backend (FastAPI) pod replicas with health checks, resource limits, and HPA support

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app
  labels:
    app: todo-backend
    component: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
        component: backend
    spec:
      containers:
      - name: backend
        image: yourusername/todo-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        env:
        - name: FRONTEND_URL
          value: "http://todo-frontend:3000"
        - name: AGENT_MODEL
          value: "gpt-4o"
        envFrom:
        - secretRef:
            name: backend-secrets
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
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
```

**Key Attributes**:
- **replicas**: 1 - Initial replica count (HPA will manage scaling)
- **image**: Container image from Docker Hub or local registry
- **ports**: Exposes port 8000 for HTTP traffic
- **env**: Non-sensitive configuration (URLs, model names)
- **envFrom**: Sensitive configuration from Secrets (DB credentials, API keys)
- **livenessProbe**: Detects unhealthy containers, triggers restart
- **readinessProbe**: Controls traffic routing to ready pods
- **resources**: Higher limits than frontend due to AI operations

## 3. Services

### 3.1 Frontend Service

**Purpose**: Provides stable network endpoint for frontend pods

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: todo-app
  labels:
    app: todo-frontend
    component: frontend
spec:
  type: ClusterIP
  ports:
  - port: 3000
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app: todo-frontend
```

**Key Attributes**:
- **type**: ClusterIP - Internal cluster access only
- **port**: 3000 - Service port
- **targetPort**: http - Maps to container port named "http"
- **selector**: Routes traffic to pods with matching labels

### 3.2 Backend Service

**Purpose**: Provides stable network endpoint for backend pods

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app
  labels:
    app: todo-backend
    component: backend
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app: todo-backend
```

**Key Attributes**:
- **type**: ClusterIP - Internal cluster access only
- **port**: 8000 - Service port
- **targetPort**: http - Maps to container port named "http"
- **selector**: Routes traffic to pods with matching labels

## 4. Ingress

### 4.1 Frontend Ingress

**Purpose**: Exposes frontend service externally via NGINX Ingress Controller

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-frontend
  namespace: todo-app
  labels:
    app: todo-frontend
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

**Key Attributes**:
- **ingressClassName**: nginx - Uses NGINX Ingress Controller
- **host**: todo.local - Hostname for accessing application
- **path**: / - Root path routes to frontend
- **backend**: Routes to todo-frontend service on port 3000
- **annotations**: NGINX-specific configuration

**DNS Configuration Required**:
```bash
# Add to /etc/hosts
$(minikube ip) todo.local
```

## 5. ConfigMaps

### 5.1 Frontend ConfigMap

**Purpose**: Non-sensitive frontend configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config
  namespace: todo-app
  labels:
    app: todo-frontend
data:
  NEXT_PUBLIC_API_URL: "http://todo-backend:8000"
  BETTER_AUTH_URL: "http://todo.local"
  NODE_ENV: "production"
```

**Key Attributes**:
- **data**: Key-value pairs for configuration
- Non-sensitive values only (URLs, feature flags)

### 5.2 Backend ConfigMap

**Purpose**: Non-sensitive backend configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  namespace: todo-app
  labels:
    app: todo-backend
data:
  FRONTEND_URL: "http://todo-frontend:3000"
  AGENT_MODEL: "gpt-4o"
  LOG_LEVEL: "info"
```

**Key Attributes**:
- **data**: Key-value pairs for configuration
- Non-sensitive values only (URLs, model names, log levels)

## 6. Secrets

### 6.1 Frontend Secrets

**Purpose**: Sensitive frontend configuration

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: frontend-secrets
  namespace: todo-app
  labels:
    app: todo-frontend
type: Opaque
stringData:
  BETTER_AUTH_SECRET: "your-secret-key-here"
```

**Key Attributes**:
- **type**: Opaque - Generic secret type
- **stringData**: Plain text values (base64 encoded by Kubernetes)
- Contains sensitive authentication secrets

**Creation Command**:
```bash
kubectl create secret generic frontend-secrets \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key" \
  -n todo-app
```

### 6.2 Backend Secrets

**Purpose**: Sensitive backend configuration

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secrets
  namespace: todo-app
  labels:
    app: todo-backend
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@host:5432/dbname"
  BETTER_AUTH_SECRET: "your-secret-key-here"
  OPENAI_API_KEY: "sk-..."
```

**Key Attributes**:
- **type**: Opaque - Generic secret type
- **stringData**: Plain text values (base64 encoded by Kubernetes)
- Contains database credentials and API keys

**Creation Command**:
```bash
kubectl create secret generic backend-secrets \
  --from-literal=DATABASE_URL="postgresql://user:pass@host:5432/db" \
  --from-literal=BETTER_AUTH_SECRET="your-secret-key" \
  --from-literal=OPENAI_API_KEY="sk-..." \
  -n todo-app
```

## 7. HorizontalPodAutoscaler

### 7.1 Backend HPA

**Purpose**: Automatically scales backend pods based on CPU and memory utilization

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
  namespace: todo-app
  labels:
    app: todo-backend
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
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
```

**Key Attributes**:
- **scaleTargetRef**: Targets todo-backend Deployment
- **minReplicas**: 1 - Minimum pod count
- **maxReplicas**: 5 - Maximum pod count (fits within Minikube resources)
- **metrics**: CPU (70%) and Memory (80%) thresholds
- **behavior**: Scale-up immediate, scale-down delayed (5 min stabilization)

**Requirements**:
- Metrics server must be enabled: `minikube addons enable metrics-server`
- Resource requests/limits must be defined in Deployment

## Resource Relationships

### Service Discovery

**Frontend → Backend Communication**:
```
Frontend Pod → todo-backend Service (DNS) → Backend Pod(s)
```

**DNS Resolution**:
- Service name: `todo-backend`
- Fully qualified: `todo-backend.todo-app.svc.cluster.local`
- Short form works within same namespace: `todo-backend`

### External Access Flow

**User → Application**:
```
User Browser → todo.local (DNS) → Minikube IP → NGINX Ingress → todo-frontend Service → Frontend Pod(s)
```

### Scaling Behavior

**HPA Scaling Logic**:
```
1. Metrics Server collects pod metrics every 15s
2. HPA evaluates metrics every 15s
3. If CPU > 70% or Memory > 80%:
   - Calculate desired replicas
   - Scale up immediately (up to 100% per minute)
4. If CPU < 70% and Memory < 80%:
   - Wait 5 minutes (stabilization window)
   - Scale down gradually (max 50% per minute)
```

## Resource Validation

### Validation Commands

**Namespace**:
```bash
kubectl get namespace todo-app
kubectl describe namespace todo-app
```

**Deployments**:
```bash
kubectl get deployments -n todo-app
kubectl describe deployment todo-frontend -n todo-app
kubectl describe deployment todo-backend -n todo-app
```

**Pods**:
```bash
kubectl get pods -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

**Services**:
```bash
kubectl get services -n todo-app
kubectl describe service todo-frontend -n todo-app
kubectl get endpoints -n todo-app
```

**Ingress**:
```bash
kubectl get ingress -n todo-app
kubectl describe ingress todo-frontend -n todo-app
```

**ConfigMaps & Secrets**:
```bash
kubectl get configmaps -n todo-app
kubectl get secrets -n todo-app
kubectl describe configmap frontend-config -n todo-app
```

**HPA**:
```bash
kubectl get hpa -n todo-app
kubectl describe hpa todo-backend-hpa -n todo-app
```

## Resource Sizing Summary

**Total Resources at Minimum Scale**:
- Frontend: 2 pods × 250m CPU = 500m request, 1000m limit
- Backend: 1 pod × 500m CPU = 500m request, 1000m limit
- **Total**: 1000m (1 CPU) request, 2000m (2 CPU) limit

**Total Resources at Maximum Scale**:
- Frontend: 2 pods × 250m CPU = 500m request, 1000m limit
- Backend: 5 pods × 500m CPU = 2500m request, 5000m limit
- **Total**: 3000m (3 CPU) request, 6000m (6 CPU) limit

**Minikube Capacity**: 4 CPU, 8GB RAM
**Headroom**: 1 CPU for system pods and bursting

---

**Data Model Status**: Complete
**Date**: 2026-01-20
**Next**: Create Helm chart templates in contracts/
