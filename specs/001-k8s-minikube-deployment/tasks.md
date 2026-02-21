# Implementation Tasks: Kubernetes Deployment on Minikube

**Feature**: 001-k8s-minikube-deployment
**Branch**: `001-k8s-minikube-deployment`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Overview

This document contains all implementation tasks for deploying the Todo Chatbot application to a local Minikube Kubernetes cluster using Helm charts, kubectl-ai, and Kagent. Tasks are organized by user story to enable independent implementation and testing.

## Task Summary

- **Total Tasks**: 85
- **Setup Phase**: 3 tasks
- **Foundational Phase**: 4 tasks
- **User Story 1 (P1)**: 15 tasks
- **User Story 2 (P2)**: 20 tasks
- **User Story 3 (P3)**: 18 tasks
- **User Story 4 (P4)**: 12 tasks
- **User Story 5 (P5)**: 8 tasks
- **Polish Phase**: 5 tasks

## Implementation Strategy

**MVP Scope**: User Story 1 (P1) - Local Kubernetes Environment Setup

This delivers a fully functional Kubernetes cluster with all required tools installed and configured. It can be independently tested and provides the foundation for all subsequent deployments.

**Incremental Delivery**:
1. **Sprint 1**: US1 (Environment Setup) - Delivers working cluster
2. **Sprint 2**: US2 (Backend Deployment) - Delivers functional API
3. **Sprint 3**: US3 (Frontend Deployment) - Delivers complete application
4. **Sprint 4**: US4 (External Access) - Delivers production-like access
5. **Sprint 5**: US5 (AI Operations) - Delivers enhanced tooling

## Dependencies

### User Story Dependencies

```
US1 (Environment Setup)
  ↓
US2 (Backend Deployment) ← Must complete US1 first
  ↓
US3 (Frontend Deployment) ← Must complete US2 first
  ↓
US4 (External Access) ← Must complete US3 first
  ↓
US5 (AI Operations) ← Can run in parallel with US4
```

### Task Dependencies Within Stories

- **US1**: Sequential setup (tools → cluster → addons → namespace)
- **US2**: Helm chart creation can be parallel, deployment is sequential
- **US3**: Helm chart creation can be parallel, deployment is sequential
- **US4**: Ingress configuration depends on US3 completion
- **US5**: AI tool testing can be fully parallel

## Parallel Execution Opportunities

### User Story 1 (P1)
```bash
# Parallel tool installations (if on same platform)
T004, T005, T006, T007  # Install Minikube, Helm, kubectl-ai, Kagent

# Parallel verification
T015, T016, T017  # Verify installations
```

### User Story 2 (P2)
```bash
# Parallel Helm chart file creation
T022, T023, T024, T025, T026, T027, T028  # All template files

# Parallel validation
T029, T030  # Lint and dry-run
```

### User Story 3 (P3)
```bash
# Parallel Helm chart file creation
T040, T041, T042, T043, T044, T045  # All template files

# Parallel validation
T046, T047  # Lint and dry-run
```

### User Story 4 (P4)
```bash
# Parallel access testing
T059, T060  # Test ingress and port-forward simultaneously
```

### User Story 5 (P5)
```bash
# Fully parallel AI tool testing
T063, T064, T065, T066, T067, T068  # All kubectl-ai and Kagent tests
```

---

## Phase 1: Setup

**Goal**: Initialize project structure and documentation

### Tasks

- [x] T001 Create k8s directory structure in repository root
- [x] T002 Create deployment scripts directory at k8s/scripts/
- [x] T003 Create manifests directory at k8s/manifests/

---

## Phase 2: Foundational

**Goal**: Verify prerequisites and prepare environment

### Tasks

- [ ] T004 Verify Docker is installed and running on local machine
- [ ] T005 Verify local machine meets minimum requirements (4 CPU, 8GB RAM, 20GB disk)
- [ ] T006 Verify internet connectivity for downloading tools and images
- [ ] T007 Verify container images exist for frontend and backend in registry

---

## Phase 3: User Story 1 - Local Kubernetes Environment Setup (P1)

**Story Goal**: Set up a local Kubernetes cluster with all required tools for deployment

**Independent Test Criteria**:
- ✅ Minikube cluster running with Kubernetes 1.28+
- ✅ All nodes in Ready state
- ✅ kubectl-ai and Kagent installed and functional
- ✅ todo-app namespace created and isolated
- ✅ NGINX Ingress controller pods running
- ✅ Metrics server operational

**Why This Story First**: Foundation for all deployment activities. Without a working cluster, no other stories can proceed.

### Tasks

- [ ] T008 [US1] Install Minikube on local machine per platform (macOS/Linux/Windows)
- [ ] T009 [US1] Install Helm 3.x on local machine per platform
- [ ] T010 [P] [US1] Install kubectl-ai via npm or pip
- [ ] T011 [P] [US1] Install Kagent via pip or binary download
- [ ] T012 [US1] Start Minikube cluster with 4 CPUs, 8GB RAM, Docker driver
- [ ] T013 [US1] Verify Minikube cluster status and node readiness
- [ ] T014 [US1] Enable NGINX Ingress addon in Minikube
- [ ] T015 [US1] Enable metrics-server addon in Minikube for HPA support
- [ ] T016 [P] [US1] Verify NGINX Ingress controller pods are running in ingress-nginx namespace
- [ ] T017 [P] [US1] Verify metrics-server deployment is running in kube-system namespace
- [ ] T018 [US1] Configure kubectl context to use Minikube cluster
- [ ] T019 [US1] Create todo-app namespace in cluster
- [ ] T020 [US1] Verify namespace isolation and resource quotas
- [ ] T021 [P] [US1] Configure kubectl-ai with API key (OpenAI or Gemini)
- [ ] T022 [P] [US1] Initialize Kagent with Minikube context

**Story Completion Test**:
```bash
# Verify cluster
minikube status
kubectl get nodes
kubectl get namespaces | grep todo-app

# Verify addons
kubectl get pods -n ingress-nginx
kubectl get deployment metrics-server -n kube-system

# Verify AI tools
kubectl-ai --version
kagent version
```

---

## Phase 4: User Story 2 - Backend Service Deployment (P2)

**Story Goal**: Deploy backend service with proper configuration, database connectivity, and autoscaling

**Independent Test Criteria**:
- ✅ Backend Helm chart created and validated
- ✅ Backend pods running and passing health checks
- ✅ Backend service accessible within cluster
- ✅ Database connection established and functional
- ✅ HPA configured and responding to metrics
- ✅ Resource limits applied correctly

**Why This Story Second**: Backend is the core service. Frontend depends on backend availability.

### Tasks

#### Helm Chart Creation

- [ ] T023 [US2] Create backend Helm chart directory at k8s/helm/todo-backend/
- [ ] T024 [P] [US2] Create Chart.yaml for backend in k8s/helm/todo-backend/Chart.yaml
- [ ] T025 [P] [US2] Create values.yaml for backend in k8s/helm/todo-backend/values.yaml
- [ ] T026 [P] [US2] Create deployment template in k8s/helm/todo-backend/templates/deployment.yaml
- [ ] T027 [P] [US2] Create service template in k8s/helm/todo-backend/templates/service.yaml
- [ ] T028 [P] [US2] Create HPA template in k8s/helm/todo-backend/templates/hpa.yaml
- [ ] T029 [P] [US2] Create helpers template in k8s/helm/todo-backend/templates/_helpers.tpl
- [ ] T030 [P] [US2] Create NOTES.txt template in k8s/helm/todo-backend/templates/NOTES.txt
- [ ] T031 [P] [US2] Create values-dev.yaml for development overrides in k8s/helm/todo-backend/values-dev.yaml
- [ ] T032 [P] [US2] Create .helmignore file in k8s/helm/todo-backend/.helmignore

#### Chart Validation

- [ ] T033 [US2] Run helm lint on backend chart to validate syntax
- [ ] T034 [US2] Run helm install dry-run to validate template rendering

#### Secret Management

- [ ] T035 [US2] Create secrets.yaml.example in k8s/manifests/secrets.yaml.example
- [ ] T036 [US2] Document secret creation process in k8s/manifests/README.md
- [ ] T037 [US2] Create backend-secrets in todo-app namespace with DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY

#### Deployment

- [ ] T038 [US2] Deploy backend using helm install command in todo-app namespace
- [ ] T039 [US2] Verify backend pods reach Running state within 5 minutes
- [ ] T040 [US2] Verify backend liveness probes are passing
- [ ] T041 [US2] Verify backend readiness probes are passing
- [ ] T042 [US2] Verify backend service is created with correct ports

#### Testing

- [ ] T043 [US2] Test backend health endpoint via port-forward
- [ ] T044 [US2] Test database connectivity from backend pod
- [ ] T045 [US2] Verify backend service DNS resolution within cluster
- [ ] T046 [US2] Verify HPA is created and monitoring metrics
- [ ] T047 [US2] Verify resource limits are applied to backend pods
- [ ] T048 [US2] Check backend logs for startup errors

**Story Completion Test**:
```bash
# Verify deployment
kubectl get deployments -n todo-app
kubectl get pods -n todo-app
kubectl get hpa -n todo-app

# Test health
kubectl port-forward service/todo-backend 8000:8000 -n todo-app
curl http://localhost:8000/health

# Verify resources
kubectl describe pod <backend-pod> -n todo-app | grep -A 5 "Limits\|Requests"
```

---

## Phase 5: User Story 3 - Frontend Service Deployment (P3)

**Story Goal**: Deploy frontend service with proper configuration and backend connectivity

**Independent Test Criteria**:
- ✅ Frontend Helm chart created and validated
- ✅ Frontend pods (2 replicas) running and passing health checks
- ✅ Frontend service accessible within cluster
- ✅ Frontend can communicate with backend service
- ✅ Resource limits applied correctly

**Why This Story Third**: Frontend provides user interface and depends on backend being operational.

### Tasks

#### Helm Chart Creation

- [ ] T049 [US3] Create frontend Helm chart directory at k8s/helm/todo-frontend/
- [ ] T050 [P] [US3] Create Chart.yaml for frontend in k8s/helm/todo-frontend/Chart.yaml
- [ ] T051 [P] [US3] Create values.yaml for frontend in k8s/helm/todo-frontend/values.yaml
- [ ] T052 [P] [US3] Create deployment template in k8s/helm/todo-frontend/templates/deployment.yaml
- [ ] T053 [P] [US3] Create service template in k8s/helm/todo-frontend/templates/service.yaml
- [ ] T054 [P] [US3] Create ingress template in k8s/helm/todo-frontend/templates/ingress.yaml
- [ ] T055 [P] [US3] Create helpers template in k8s/helm/todo-frontend/templates/_helpers.tpl
- [ ] T056 [P] [US3] Create NOTES.txt template in k8s/helm/todo-frontend/templates/NOTES.txt
- [ ] T057 [P] [US3] Create values-dev.yaml for development overrides in k8s/helm/todo-frontend/values-dev.yaml
- [ ] T058 [P] [US3] Create .helmignore file in k8s/helm/todo-frontend/.helmignore

#### Chart Validation

- [ ] T059 [US3] Run helm lint on frontend chart to validate syntax
- [ ] T060 [US3] Run helm install dry-run to validate template rendering

#### Secret Management

- [ ] T061 [US3] Create frontend-secrets in todo-app namespace with BETTER_AUTH_SECRET

#### Deployment

- [ ] T062 [US3] Deploy frontend using helm install command in todo-app namespace
- [ ] T063 [US3] Verify frontend pods (2 replicas) reach Running state within 3 minutes
- [ ] T064 [US3] Verify frontend liveness probes are passing
- [ ] T065 [US3] Verify frontend readiness probes are passing
- [ ] T066 [US3] Verify frontend service is created with correct ports

#### Testing

- [ ] T067 [US3] Test frontend health endpoint via port-forward
- [ ] T068 [US3] Test frontend to backend connectivity from within pod
- [ ] T069 [US3] Verify frontend service DNS resolution within cluster
- [ ] T070 [US3] Verify resource limits are applied to frontend pods
- [ ] T071 [US3] Check frontend logs for startup errors
- [ ] T072 [US3] Verify both frontend replicas are load-balanced

**Story Completion Test**:
```bash
# Verify deployment
kubectl get deployments -n todo-app
kubectl get pods -n todo-app | grep frontend

# Test health
kubectl port-forward service/todo-frontend 3000:3000 -n todo-app
curl http://localhost:3000/api/health

# Test backend connectivity
kubectl exec -it deployment/todo-frontend -n todo-app -- wget -q -O- http://todo-backend:8000/health
```

---

## Phase 6: User Story 4 - External Access Configuration (P4)

**Story Goal**: Configure external access to the application via Ingress

**Independent Test Criteria**:
- ✅ Ingress resource created and configured
- ✅ Local DNS configured (todo.local)
- ✅ Application accessible via ingress URL
- ✅ Port-forwarding alternative documented and tested
- ✅ HTTP traffic routed correctly to services

**Why This Story Fourth**: External access is essential for user interaction but can be configured after core services are running.

### Tasks

#### Ingress Configuration

- [ ] T073 [US4] Verify NGINX Ingress controller is ready and accepting traffic
- [ ] T074 [US4] Create namespace.yaml manifest in k8s/manifests/namespace.yaml
- [ ] T075 [US4] Verify ingress resource is created by frontend Helm chart
- [ ] T076 [US4] Get Minikube IP address for local DNS configuration

#### DNS Configuration

- [ ] T077 [US4] Add todo.local entry to /etc/hosts (macOS/Linux) or hosts file (Windows)
- [ ] T078 [US4] Verify DNS resolution for todo.local

#### Access Testing

- [ ] T079 [US4] Test external access via http://todo.local in browser
- [ ] T080 [US4] Test external access via curl to http://todo.local
- [ ] T081 [P] [US4] Test port-forward access to frontend as alternative
- [ ] T082 [P] [US4] Test port-forward access to backend as alternative
- [ ] T083 [US4] Verify ingress routing to frontend service
- [ ] T084 [US4] Test end-to-end application flow (frontend → backend → database)

**Story Completion Test**:
```bash
# Verify ingress
kubectl get ingress -n todo-app
kubectl describe ingress todo-frontend -n todo-app

# Test access
curl http://todo.local
open http://todo.local

# Test port-forward alternative
kubectl port-forward service/todo-frontend 3000:3000 -n todo-app &
curl http://localhost:3000
```

---

## Phase 7: User Story 5 - AI-Assisted Operations and Optimization (P5)

**Story Goal**: Use kubectl-ai and Kagent for intelligent cluster operations

**Independent Test Criteria**:
- ✅ kubectl-ai generates valid Kubernetes manifests
- ✅ kubectl-ai can scale and manage deployments
- ✅ Kagent analyzes cluster health successfully
- ✅ Kagent provides optimization recommendations
- ✅ AI-assisted workflows documented

**Why This Story Fifth**: AI-assisted tools enhance operational efficiency but are not critical for basic deployment.

### Tasks

#### kubectl-ai Testing

- [ ] T085 [P] [US5] Test kubectl-ai manifest generation with natural language commands
- [ ] T086 [P] [US5] Test kubectl-ai deployment scaling operations
- [ ] T087 [P] [US5] Test kubectl-ai troubleshooting capabilities
- [ ] T088 [P] [US5] Document kubectl-ai command patterns in k8s/docs/kubectl-ai-guide.md

#### Kagent Testing

- [ ] T089 [P] [US5] Test Kagent cluster health analysis
- [ ] T090 [P] [US5] Test Kagent resource optimization recommendations
- [ ] T091 [P] [US5] Test Kagent problem diagnosis capabilities
- [ ] T092 [P] [US5] Document Kagent usage patterns in k8s/docs/kagent-guide.md

**Story Completion Test**:
```bash
# Test kubectl-ai
kubectl-ai "show me all pods in todo-app namespace"
kubectl-ai "scale the frontend to 3 replicas"
kubectl-ai "why is the backend pod failing?"

# Test Kagent
kagent "analyze the cluster health"
kagent "optimize resource allocation for todo-app namespace"
kagent "identify performance bottlenecks"
```

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Create deployment automation, documentation, and cleanup procedures

### Tasks

- [ ] T093 Create setup-minikube.sh script in k8s/scripts/setup-minikube.sh
- [ ] T094 Create deploy-all.sh script in k8s/scripts/deploy-all.sh
- [ ] T095 Create cleanup.sh script in k8s/scripts/cleanup.sh
- [ ] T096 Create test-deployment.sh script in k8s/scripts/test-deployment.sh
- [ ] T097 Create deployment runbook in k8s/docs/DEPLOYMENT.md

---

## Validation Checklist

### Pre-Deployment Validation

- [ ] All Helm charts pass `helm lint`
- [ ] All Helm charts pass `helm install --dry-run`
- [ ] All secrets are created in cluster
- [ ] Container images are available in registry
- [ ] Minikube has sufficient resources

### Post-Deployment Validation

- [ ] All pods in Running state
- [ ] All health checks passing
- [ ] All services have endpoints
- [ ] Ingress routing correctly
- [ ] HPA monitoring metrics
- [ ] Application accessible externally
- [ ] End-to-end functionality working

### Performance Validation

- [ ] Cluster startup < 2 minutes
- [ ] Backend deployment < 5 minutes
- [ ] Frontend deployment < 3 minutes
- [ ] Application response < 2 seconds
- [ ] HPA scaling < 30 seconds

---

## Troubleshooting Guide

### Common Issues

**Pods Not Starting**:
- Check: `kubectl describe pod <pod-name> -n todo-app`
- Verify: Image pull policy and registry access
- Check: Resource limits and node capacity

**Ingress Not Working**:
- Check: `kubectl get pods -n ingress-nginx`
- Verify: Ingress controller is running
- Fallback: Use port-forwarding

**HPA Not Scaling**:
- Check: `kubectl get hpa -n todo-app`
- Verify: Metrics server is running
- Check: `kubectl top pods -n todo-app`

**Database Connection Issues**:
- Check: Backend logs for connection errors
- Verify: Secrets are created correctly
- Test: Database accessibility from pod

---

## Task Execution Notes

### Format Legend

- `- [ ]` : Unchecked task (not started)
- `[TaskID]` : Sequential task identifier (T001, T002, etc.)
- `[P]` : Task can be executed in parallel with other [P] tasks in same phase
- `[US1]` : Task belongs to User Story 1 (similarly US2, US3, US4, US5)
- No story label : Setup, Foundational, or Polish phase task

### Execution Order

1. Complete Setup phase (T001-T003)
2. Complete Foundational phase (T004-T007)
3. Complete User Story 1 (T008-T022) - **MVP Milestone**
4. Complete User Story 2 (T023-T048)
5. Complete User Story 3 (T049-T072)
6. Complete User Story 4 (T073-T084)
7. Complete User Story 5 (T085-T092) - Can overlap with US4
8. Complete Polish phase (T093-T097)

### Parallel Execution

Tasks marked with `[P]` can be executed in parallel within their phase. See "Parallel Execution Opportunities" section for specific groupings.

---

**Tasks Status**: Ready for implementation
**Total Tasks**: 97
**Estimated Effort**: 3-4 days
**Next Step**: Begin with Setup phase (T001-T003)
