# Implementation Plan: Kubernetes Deployment on Minikube

**Branch**: `001-k8s-minikube-deployment` | **Date**: 2026-01-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-k8s-minikube-deployment/spec.md`

## Summary

Deploy the Todo Chatbot application to a local Minikube Kubernetes cluster using Helm charts for package management, with AI-assisted operations via kubectl-ai and Kagent. The deployment includes frontend (Next.js) and backend (FastAPI) services with proper resource management, health checks, autoscaling, and external access via NGINX Ingress. The implementation follows cloud-native best practices with ConfigMaps for configuration, Secrets for sensitive data, and comprehensive monitoring capabilities.

## Technical Context

**Language/Version**: YAML (Kubernetes manifests), Helm Chart templates, Bash scripts for automation
**Primary Dependencies**:
- Minikube (local Kubernetes cluster)
- Helm 3.x (package manager)
- kubectl (Kubernetes CLI)
- kubectl-ai (AI-assisted Kubernetes operations)
- Kagent (cluster health analysis)
- Docker (container runtime)
- NGINX Ingress Controller

**Storage**: External Neon PostgreSQL (no in-cluster database), optional PersistentVolumes for stateful components
**Testing**:
- Helm chart validation (helm lint, dry-run)
- Deployment verification (kubectl get, describe)
- Health check testing (liveness/readiness probes)
- End-to-end application testing
- kubectl-ai and Kagent functional testing

**Target Platform**: Local Minikube cluster (Kubernetes 1.28+) on macOS/Linux/Windows
**Project Type**: Infrastructure/DevOps - Kubernetes deployment configuration
**Performance Goals**:
- Cluster startup within 2 minutes
- Backend deployment within 5 minutes
- Frontend deployment within 3 minutes
- Application response time under 2 seconds
- HPA scaling response within 30 seconds

**Constraints**:
- Local machine resources (4 CPU cores, 8GB RAM minimum)
- Minikube-only deployment (no cloud Kubernetes)
- NGINX Ingress only (no alternative ingress controllers)
- Helm 3.x only (no Helm 2.x)
- External Neon PostgreSQL (no in-cluster database)
- Basic monitoring only (no Prometheus/Grafana)

**Scale/Scope**:
- 2 services (frontend, backend)
- 2 Helm charts
- 1 namespace (todo-app)
- 3-7 pods (depending on scaling)
- 2 ConfigMaps, 2 Secrets
- 1 Ingress resource
- 1 HPA (backend only)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Cloud-Native Architecture ✅
- **Requirement**: All services containerized, health checks, graceful shutdown, externalized configuration
- **Status**: PASS - Existing Docker images available, health endpoints implemented, configuration via ConfigMaps/Secrets
- **Evidence**: Frontend and backend already containerized from previous phases, `/health` and `/api/health` endpoints exist

### Deployment Requirements ✅
- **Requirement**: Multi-stage builds, resource limits, health endpoints, ConfigMaps/Secrets
- **Status**: PASS - Docker images use multi-stage builds, Helm charts will define resource limits and health probes
- **Evidence**: Existing Dockerfiles use multi-stage builds, plan includes resource limit definitions

### Security Requirements ✅
- **Requirement**: Secrets in environment variables, no hardcoded secrets, Kubernetes secrets for sensitive data
- **Status**: PASS - Secrets stored in Kubernetes Secrets, accessed via environment variables
- **Evidence**: Plan includes creation of frontend-secrets and backend-secrets with proper secret management

### Developer Experience ✅
- **Requirement**: Clear documentation, local development support, consistent patterns
- **Status**: PASS - Comprehensive documentation provided, Minikube enables local Kubernetes development
- **Evidence**: Plan includes detailed setup instructions, quickstart guide, and troubleshooting procedures

### Technology Stack Constraints ✅
- **Requirement**: Docker, Kubernetes, Helm, kubectl-ai, kagent
- **Status**: PASS - All required tools specified in plan
- **Evidence**: Plan explicitly uses Docker, Kubernetes (Minikube), Helm 3.x, kubectl-ai, and Kagent

### Quality Gates ⚠️
- **Requirement**: Phase IV completion criteria (all services containerized, health checks, resource limits)
- **Status**: PARTIAL - Containerization complete, health checks exist, resource limits to be defined in Helm charts
- **Action Required**: Define and validate resource limits during implementation

**Overall Gate Status**: PASS with action items - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/001-k8s-minikube-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - Tool installation and best practices
├── data-model.md        # Phase 1 output - Kubernetes resource definitions
├── quickstart.md        # Phase 1 output - Quick deployment guide
├── contracts/           # Phase 1 output - Helm chart templates and values
│   ├── frontend-chart/  # Frontend Helm chart structure
│   └── backend-chart/   # Backend Helm chart structure
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Kubernetes deployment configuration (new)
k8s/
├── helm/
│   ├── todo-frontend/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── values-dev.yaml
│   │   ├── values-prod.yaml
│   │   └── templates/
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       ├── ingress.yaml
│   │       ├── configmap.yaml
│   │       ├── secret.yaml
│   │       └── _helpers.tpl
│   └── todo-backend/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-prod.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── hpa.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           └── _helpers.tpl
├── manifests/
│   ├── namespace.yaml
│   └── secrets.yaml.example
└── scripts/
    ├── setup-minikube.sh
    ├── deploy-all.sh
    ├── cleanup.sh
    └── test-deployment.sh

# Existing application code (unchanged)
frontend/
├── src/
├── public/
├── Dockerfile
└── package.json

backend/
├── src/
├── tests/
├── Dockerfile
└── requirements.txt
```

**Structure Decision**: Infrastructure-as-Code approach with dedicated `k8s/` directory for all Kubernetes-related configuration. Helm charts organized by service (frontend/backend) with environment-specific values files. Existing application code remains unchanged, only deployment configuration is added.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations requiring justification. All requirements align with cloud-native architecture and deployment best practices.

## Phase 0: Research & Discovery

### Research Topics

1. **Minikube Installation & Configuration**
   - Installation methods for macOS, Linux, Windows
   - Resource allocation best practices (CPU, memory, disk)
   - Driver selection (Docker, VirtualBox, Hyper-V)
   - Addon management (ingress, metrics-server, dashboard)

2. **Helm 3.x Best Practices**
   - Chart structure and organization
   - Values file patterns for multi-environment deployments
   - Template functions and helpers
   - Chart versioning and dependencies
   - Linting and validation

3. **kubectl-ai Integration**
   - Installation methods (npm, pip)
   - API key configuration (OpenAI/Gemini)
   - Command patterns and capabilities
   - Integration with existing kubectl workflows

4. **Kagent Integration**
   - Installation and setup
   - Cluster health analysis capabilities
   - Optimization recommendation patterns
   - Integration with Minikube

5. **Kubernetes Resource Management**
   - Resource requests vs limits
   - Quality of Service (QoS) classes
   - Resource quota and limit ranges
   - Best practices for CPU and memory allocation

6. **Health Check Patterns**
   - Liveness vs readiness probes
   - Probe configuration (initialDelaySeconds, periodSeconds, failureThreshold)
   - Health endpoint implementation
   - Startup probes for slow-starting containers

7. **Horizontal Pod Autoscaler (HPA)**
   - Metrics server requirements
   - CPU and memory-based scaling
   - Custom metrics (future consideration)
   - Scaling behavior configuration

8. **NGINX Ingress Controller**
   - Minikube ingress addon
   - Ingress resource configuration
   - Path-based routing
   - Local DNS configuration (/etc/hosts)

### Research Outputs

**Decision 1: Minikube Driver Selection**
- **Chosen**: Docker driver
- **Rationale**: Cross-platform compatibility, no additional virtualization layer, better performance on modern systems
- **Alternatives**: VirtualBox (older, slower), Hyper-V (Windows-only), Podman (less mature)

**Decision 2: Helm Chart Organization**
- **Chosen**: Separate charts for frontend and backend
- **Rationale**: Independent versioning, deployment, and scaling; follows microservices principles
- **Alternatives**: Umbrella chart (adds complexity), single chart with conditionals (harder to maintain)

**Decision 3: Resource Allocation Strategy**
- **Chosen**: Conservative limits with room for bursting
  - Frontend: 250m CPU request, 500m limit; 256Mi memory request, 512Mi limit
  - Backend: 500m CPU request, 1000m limit; 512Mi memory request, 1Gi limit
- **Rationale**: Prevents resource starvation while allowing performance bursts, fits within Minikube constraints
- **Alternatives**: No limits (risk of resource exhaustion), aggressive limits (performance degradation)

**Decision 4: Ingress vs NodePort vs LoadBalancer**
- **Chosen**: NGINX Ingress Controller
- **Rationale**: Production-like setup, supports path-based routing, standard Kubernetes pattern
- **Alternatives**: NodePort (less production-like), LoadBalancer (requires cloud provider)

**Decision 5: HPA Configuration**
- **Chosen**: CPU (70%) and Memory (80%) based scaling for backend only
- **Rationale**: Backend is compute-intensive (AI operations), frontend is stateless and can use fixed replicas
- **Alternatives**: CPU only (less accurate), custom metrics (added complexity)

**Decision 6: Secret Management**
- **Chosen**: Kubernetes Secrets (base64 encoded)
- **Rationale**: Native Kubernetes solution, sufficient for local development
- **Alternatives**: Sealed Secrets (overkill for local), External Secrets Operator (requires external service)

## Phase 1: Design & Architecture

### Data Model (Kubernetes Resources)

See [data-model.md](./data-model.md) for complete resource definitions.

**Key Resources**:
- **Namespace**: `todo-app` - Logical isolation for all application resources
- **Deployments**: Frontend (2 replicas), Backend (1-5 replicas with HPA)
- **Services**: ClusterIP for internal communication
- **Ingress**: NGINX-based routing for external access
- **ConfigMaps**: Non-sensitive configuration (API URLs, feature flags)
- **Secrets**: Sensitive data (database credentials, API keys)
- **HorizontalPodAutoscaler**: Backend autoscaling based on CPU/memory

### API Contracts (Helm Charts)

See [contracts/](./contracts/) for complete Helm chart templates.

**Frontend Chart** (`k8s/helm/todo-frontend/`):
- Chart.yaml: Metadata and versioning
- values.yaml: Default configuration
- templates/deployment.yaml: Pod specification with health probes
- templates/service.yaml: ClusterIP service
- templates/ingress.yaml: External access configuration
- templates/configmap.yaml: Non-sensitive configuration
- templates/_helpers.tpl: Template helper functions

**Backend Chart** (`k8s/helm/todo-backend/`):
- Chart.yaml: Metadata and versioning
- values.yaml: Default configuration with HPA settings
- templates/deployment.yaml: Pod specification with health probes
- templates/service.yaml: ClusterIP service
- templates/hpa.yaml: Horizontal Pod Autoscaler
- templates/configmap.yaml: Non-sensitive configuration
- templates/_helpers.tpl: Template helper functions

### Deployment Workflow

1. **Environment Setup** (Phase 1)
   - Install Minikube, Helm, kubectl-ai, Kagent
   - Start Minikube cluster with required resources
   - Enable ingress and metrics-server addons
   - Create todo-app namespace

2. **Secret Creation** (Phase 2)
   - Create frontend-secrets (BETTER_AUTH_SECRET)
   - Create backend-secrets (DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY)

3. **Backend Deployment** (Phase 3)
   - Validate backend Helm chart (lint, dry-run)
   - Deploy backend with Helm
   - Verify pod status and health checks
   - Test database connectivity

4. **Frontend Deployment** (Phase 4)
   - Validate frontend Helm chart (lint, dry-run)
   - Deploy frontend with Helm
   - Verify pod status and health checks
   - Test backend connectivity

5. **Ingress Configuration** (Phase 5)
   - Configure local DNS (/etc/hosts)
   - Verify ingress routing
   - Test external access

6. **AI Tools Integration** (Phase 6)
   - Use kubectl-ai for deployment verification
   - Use Kagent for cluster health analysis
   - Document AI-assisted workflows

7. **Testing & Validation** (Phase 7)
   - End-to-end application testing
   - Load testing for HPA validation
   - Failure scenario testing

### Quickstart Guide

See [quickstart.md](./quickstart.md) for step-by-step deployment instructions.

## Phase 2: Implementation Tasks

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides high-level task categories.

### Task Categories

1. **Environment Setup Tasks**
   - Install Minikube on target platform
   - Install Helm 3.x
   - Install kubectl-ai
   - Install Kagent
   - Start Minikube cluster
   - Enable required addons

2. **Helm Chart Creation Tasks**
   - Create frontend Helm chart structure
   - Create backend Helm chart structure
   - Define values.yaml for each chart
   - Create deployment templates
   - Create service templates
   - Create ingress template (frontend)
   - Create HPA template (backend)
   - Create helper templates

3. **Secret Management Tasks**
   - Create secret manifests
   - Document secret creation process
   - Create secrets in cluster

4. **Deployment Tasks**
   - Validate Helm charts
   - Deploy backend service
   - Deploy frontend service
   - Configure ingress
   - Verify deployments

5. **Testing Tasks**
   - Test health endpoints
   - Test inter-service communication
   - Test external access
   - Test HPA scaling
   - Test kubectl-ai integration
   - Test Kagent integration
   - End-to-end application testing

6. **Documentation Tasks**
   - Create deployment runbook
   - Document troubleshooting procedures
   - Create cleanup procedures
   - Document AI-assisted workflows

## Architectural Decisions

### ADR-001: Separate Helm Charts for Frontend and Backend

**Context**: Need to decide between single umbrella chart vs separate charts for frontend and backend services.

**Decision**: Use separate Helm charts for frontend and backend.

**Rationale**:
- Independent versioning and deployment cycles
- Clearer separation of concerns
- Easier to scale and manage individually
- Follows microservices best practices
- Simpler chart structure and maintenance

**Consequences**:
- Positive: Independent deployment and rollback
- Positive: Clearer ownership and responsibility
- Negative: Need to manage two chart releases
- Negative: Shared configuration must be duplicated or externalized

**Alternatives Considered**:
- Umbrella chart: Adds complexity, couples deployment cycles
- Single chart with conditionals: Harder to maintain, less flexible

### ADR-002: NGINX Ingress for External Access

**Context**: Need to expose application externally from Minikube cluster.

**Decision**: Use NGINX Ingress Controller with Minikube ingress addon.

**Rationale**:
- Production-like setup for local development
- Standard Kubernetes pattern
- Supports path-based routing
- Easy to configure with Minikube addon
- Widely used and well-documented

**Consequences**:
- Positive: Production-like environment
- Positive: Path-based routing capabilities
- Positive: Standard Kubernetes pattern
- Negative: Requires local DNS configuration (/etc/hosts)
- Negative: More complex than NodePort

**Alternatives Considered**:
- NodePort: Simpler but less production-like
- LoadBalancer: Requires cloud provider, not available in Minikube
- Port-forwarding: Manual, not persistent

### ADR-003: HPA for Backend Only

**Context**: Need to decide which services should have autoscaling.

**Decision**: Implement Horizontal Pod Autoscaler for backend service only, use fixed 2 replicas for frontend.

**Rationale**:
- Backend handles compute-intensive AI operations
- Frontend is stateless and lightweight
- Backend load varies with user requests
- Frontend load is relatively constant
- Simplifies configuration and monitoring

**Consequences**:
- Positive: Backend scales with demand
- Positive: Efficient resource utilization
- Positive: Simpler frontend configuration
- Negative: Frontend cannot scale automatically
- Mitigation: Frontend can be manually scaled if needed

**Alternatives Considered**:
- HPA for both: Added complexity, frontend doesn't need it
- No HPA: Backend cannot handle load spikes
- Fixed high replica count: Wastes resources during low load

### ADR-004: Conservative Resource Limits

**Context**: Need to define CPU and memory limits for pods within Minikube constraints.

**Decision**: Use conservative resource requests with room for bursting:
- Frontend: 250m CPU request, 500m limit; 256Mi memory request, 512Mi limit
- Backend: 500m CPU request, 1000m limit; 512Mi memory request, 1Gi limit

**Rationale**:
- Prevents resource starvation
- Allows performance bursts when needed
- Fits within Minikube resource constraints (4 CPU, 8GB RAM)
- Provides headroom for multiple pods
- Enables proper scheduling and QoS

**Consequences**:
- Positive: Stable pod scheduling
- Positive: Prevents resource exhaustion
- Positive: Allows performance bursts
- Negative: May underutilize resources during low load
- Mitigation: HPA scales backend based on actual usage

**Alternatives Considered**:
- No limits: Risk of resource exhaustion, pod eviction
- Aggressive limits: Performance degradation, frequent throttling
- Generous limits: Cannot fit multiple pods in Minikube

### ADR-005: Kubernetes Secrets for Local Development

**Context**: Need to manage sensitive configuration (database credentials, API keys).

**Decision**: Use native Kubernetes Secrets (base64 encoded) for local Minikube deployment.

**Rationale**:
- Native Kubernetes solution
- Sufficient security for local development
- Simple to create and manage
- No additional dependencies
- Standard pattern for Kubernetes

**Consequences**:
- Positive: Simple and standard approach
- Positive: No additional tools required
- Negative: Base64 encoding is not encryption
- Negative: Not suitable for production without additional security
- Mitigation: Document production secret management requirements (Sealed Secrets, External Secrets Operator)

**Alternatives Considered**:
- Sealed Secrets: Overkill for local development
- External Secrets Operator: Requires external secret store
- Plain ConfigMaps: Insecure, violates best practices

## Testing Strategy

### Helm Chart Validation
1. **Linting**: `helm lint` for syntax and best practices
2. **Dry-run**: `helm install --dry-run --debug` to validate rendering
3. **Template validation**: Verify all templates render correctly
4. **Values validation**: Test with different values files

### Deployment Testing
1. **Pod status**: Verify all pods reach Running state
2. **Health checks**: Verify liveness and readiness probes pass
3. **Replica count**: Verify correct number of replicas created
4. **Resource limits**: Verify limits and requests applied correctly
5. **Environment variables**: Verify ConfigMaps and Secrets mounted

### Service Testing
1. **Service creation**: Verify services created with correct ports
2. **Endpoints**: Verify service endpoints populated
3. **DNS resolution**: Test service name resolution within cluster
4. **Inter-service communication**: Test frontend to backend connectivity

### Ingress Testing
1. **Ingress controller**: Verify NGINX ingress controller running
2. **Ingress rules**: Verify ingress resources created
3. **External access**: Test access via ingress hostname
4. **Path routing**: Verify correct routing to services

### Autoscaling Testing
1. **HPA creation**: Verify HPA resource created
2. **Metrics server**: Verify metrics server providing data
3. **Scale-up**: Generate load and verify pod scaling
4. **Scale-down**: Remove load and verify pod scale-down

### kubectl-ai Testing
1. **Installation**: Verify kubectl-ai installed and configured
2. **Manifest generation**: Test natural language to YAML generation
3. **Deployment operations**: Test scaling and management commands
4. **Troubleshooting**: Test diagnostic capabilities

### Kagent Testing
1. **Installation**: Verify Kagent installed and configured
2. **Health analysis**: Test cluster health analysis
3. **Optimization**: Test resource optimization recommendations
4. **Diagnostics**: Test problem diagnosis capabilities

### Application Testing
1. **Frontend access**: Verify frontend accessible via ingress
2. **Backend API**: Test API endpoints respond correctly
3. **Database connectivity**: Verify backend connects to Neon DB
4. **Authentication**: Test auth flow works end-to-end
5. **Chat interface**: Test AI chatbot functionality

### Failure Scenario Testing
1. **Pod failure**: Kill pod and verify automatic restart
2. **Resource exhaustion**: Test behavior when limits exceeded
3. **Database unavailability**: Test graceful degradation
4. **Ingress failure**: Test fallback to port-forwarding
5. **HPA limits**: Test behavior when max replicas reached

## Risk Analysis

### Risk 1: Minikube Resource Constraints
- **Probability**: Medium
- **Impact**: High
- **Mitigation**: Define conservative resource limits, document minimum requirements, provide resource monitoring commands
- **Contingency**: Reduce replica counts, disable HPA, use port-forwarding instead of ingress

### Risk 2: kubectl-ai/Kagent Installation Issues
- **Probability**: Medium
- **Impact**: Low
- **Mitigation**: Provide multiple installation methods, document troubleshooting steps, make AI tools optional
- **Contingency**: Use standard kubectl commands, manual cluster analysis

### Risk 3: Ingress DNS Configuration
- **Probability**: Low
- **Impact**: Medium
- **Mitigation**: Provide clear /etc/hosts configuration instructions, offer port-forwarding alternative
- **Contingency**: Use port-forwarding for local access

### Risk 4: HPA Metrics Server Issues
- **Probability**: Low
- **Impact**: Medium
- **Mitigation**: Verify metrics-server addon enabled, provide troubleshooting steps
- **Contingency**: Use fixed replica count, manual scaling

### Risk 5: Container Image Availability
- **Probability**: Low
- **Impact**: High
- **Mitigation**: Verify images exist in registry before deployment, document image building process
- **Contingency**: Build images locally, use Minikube's Docker daemon

## Success Criteria

### Phase 0 Completion (Research)
- ✅ All research topics documented in research.md
- ✅ Tool installation methods documented for all platforms
- ✅ Best practices identified and documented
- ✅ All architectural decisions made and documented

### Phase 1 Completion (Design)
- ✅ data-model.md created with all Kubernetes resource definitions
- ✅ Helm chart structures defined in contracts/
- ✅ quickstart.md created with deployment instructions
- ✅ All templates and values files specified

### Phase 2 Completion (Implementation)
- ✅ Minikube cluster running with required addons
- ✅ kubectl-ai and Kagent installed and functional
- ✅ Helm charts created and validated
- ✅ Secrets created in cluster
- ✅ Backend deployed and healthy
- ✅ Frontend deployed and healthy
- ✅ Ingress configured and accessible
- ✅ HPA configured and functional
- ✅ All tests passing
- ✅ Documentation complete

### Quality Gates
- **Before Phase 1**: All research complete, decisions documented
- **Before Phase 2**: All design artifacts created, Helm charts validated
- **Before Production**: All tests passing, documentation complete, deployment reproducible

## Next Steps

1. **Run `/sp.tasks`** to generate detailed implementation tasks from this plan
2. **Execute Phase 0**: Create research.md with detailed findings
3. **Execute Phase 1**: Create data-model.md, contracts/, and quickstart.md
4. **Execute Phase 2**: Implement Helm charts and deployment scripts (via /sp.tasks)
5. **Validate**: Test deployment end-to-end
6. **Document**: Create runbooks and troubleshooting guides

---

**Plan Status**: Complete - Ready for task generation via `/sp.tasks`
**Last Updated**: 2026-01-20
**Next Command**: `/sp.tasks` to generate implementation tasks
