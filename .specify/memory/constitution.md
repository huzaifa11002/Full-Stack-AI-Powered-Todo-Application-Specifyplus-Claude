<!--
Sync Impact Report:
- Version: NEW → 1.0.0 (Initial constitution creation)
- Modified principles: N/A (initial creation)
- Added sections: All sections (Core Principles, Code Quality Standards, Architecture Standards,
  Database & Data Management, Security Requirements, Technology Stack Constraints, Deployment Requirements,
  Development Workflow, Success Criteria & Quality Gates, Governance)
- Removed sections: None
- Templates requiring updates:
  ✅ plan-template.md - Constitution Check section will reference these principles
  ✅ spec-template.md - Requirements align with functional requirements structure
  ✅ tasks-template.md - Task categorization reflects testing and quality standards
- Follow-up TODOs: None - all placeholders filled
-->

# Full-Stack AI-Powered Todo Application Constitution

## Core Principles

### I. Production-Ready Code Quality

All code MUST be deployable, maintainable, and follow industry best practices. This is non-negotiable.

**Requirements**:
- TypeScript/Python type safety: 100% typed code, no `any` types without explicit justification documented in code comments
- Testing coverage: Minimum 70% for backend APIs, 60% for frontend components
- Linting: ESLint for TypeScript/JavaScript, Ruff for Python with zero warnings in production builds
- All architectural decisions MUST be documented in code comments at the point of implementation

**Rationale**: Production-ready code prevents technical debt accumulation, reduces maintenance burden, and ensures system reliability. Type safety catches errors at compile time rather than runtime. Testing coverage provides confidence in refactoring and changes.

### II. Cloud-Native Architecture

Design for scalability, resilience, and containerized deployment from the start. Systems MUST be built with distributed computing principles.

**Requirements**:
- All services MUST be containerized using Docker with multi-stage builds
- Services MUST implement health check endpoints (`/health`, `/ready`)
- Services MUST handle graceful shutdown (SIGTERM handling)
- Configuration MUST be externalized (12-factor app principles)
- Services MUST be stateless where possible; state stored in external systems

**Rationale**: Cloud-native design enables horizontal scaling, fault tolerance, and deployment flexibility. Building these patterns from the start is significantly easier than retrofitting them later.

### III. AI Integration Excellence

Seamless integration of AI capabilities with proper error handling, fallbacks, and cost management.

**Requirements**:
- All AI API calls MUST have timeout configurations
- All AI integrations MUST implement graceful degradation when AI services are unavailable
- Streaming responses MUST be implemented for real-time user feedback
- Conversation context MUST be managed efficiently to minimize token usage
- Cost monitoring MUST be implemented for all AI API usage
- Rate limiting MUST be enforced to prevent cost overruns

**Rationale**: AI services are external dependencies that can fail, have variable latency, and incur costs. Proper integration patterns ensure system reliability and cost predictability.

### IV. Security-First Approach

Authentication, authorization, data protection, and secure API communication throughout the system.

**Requirements**:
- All secrets MUST be stored in environment variables, never hardcoded
- JWT-based authentication with refresh tokens MUST be implemented
- API rate limiting MUST be enforced on all public endpoints
- Input sanitization MUST be performed at API boundaries
- CORS configuration MUST be properly configured for production
- Kubernetes secrets MUST use sealed secrets or external secrets operator
- All database queries MUST use parameterized queries (no string concatenation)
- All user input MUST be validated using Pydantic models

**Rationale**: Security vulnerabilities can lead to data breaches, service disruption, and loss of user trust. Security must be built in from the start, not added as an afterthought.

### V. Developer Experience

Clear documentation, consistent patterns, and easy local development setup enable team productivity.

**Requirements**:
- README MUST include setup instructions for each development phase
- Local development MUST work without Kubernetes (docker-compose fallback)
- Environment-specific configurations MUST be clearly documented (dev, staging, prod)
- Code patterns MUST be consistent across the codebase
- CI/CD pipeline considerations MUST be documented
- All APIs MUST have OpenAPI/Swagger documentation

**Rationale**: Good developer experience reduces onboarding time, minimizes configuration errors, and enables faster iteration. Clear documentation prevents knowledge silos.

## Code Quality Standards

### Type Safety
- **TypeScript**: Use strict mode, no implicit any, prefer interfaces over types for public APIs
- **Python**: Use type hints for all function signatures, enable mypy strict mode
- **Validation**: Use Pydantic v2 for all data validation at API boundaries

### Testing Requirements
- **Backend APIs**: Minimum 70% code coverage
  - Unit tests for business logic
  - Integration tests for API endpoints
  - Contract tests for external service interactions
- **Frontend Components**: Minimum 60% code coverage
  - Component tests using React Testing Library
  - Integration tests for user flows
  - E2E tests for critical paths (optional but recommended)

### Linting & Formatting
- **Frontend**: ESLint with TypeScript rules, Prettier for formatting
- **Backend**: Ruff for linting and formatting, isort for import sorting
- **Pre-commit hooks**: All checks MUST pass before commit
- **CI/CD**: Zero warnings policy in production builds

### Code Review
- All architectural decisions MUST be documented in code comments
- Complex algorithms MUST include explanation comments
- Public APIs MUST have JSDoc/docstring documentation
- Breaking changes MUST be flagged in PR descriptions

## Architecture Standards

### Phase II: Next.js + FastAPI Foundation
- **RESTful API Design**: Follow REST principles, use proper HTTP methods and status codes
- **Separation of Concerns**: Clear boundaries between models, services, and API layers
- **SQLModel**: Type-safe database operations with Pydantic integration
- **API Versioning**: Use URL versioning (`/api/v1/`) for all endpoints
- **Error Handling**: Consistent error response format across all endpoints

### Phase III: AI Chatbot Integration
- **OpenAI API**: Use official SDK with proper error handling
- **Rate Limiting**: Implement token bucket algorithm for API calls
- **Streaming**: Use Server-Sent Events (SSE) for real-time responses
- **Context Management**: Implement conversation history with token limit awareness
- **MCP SDK**: Follow official Model Context Protocol patterns for tool/function calling
- **Fallback Strategy**: Graceful degradation when AI unavailable (cached responses, error messages)

### Phase IV: Kubernetes Deployment
- **Docker**: Multi-stage builds for minimal image size, layer caching optimization
- **Helm Charts**: Configuration management with values files for each environment
- **Health Checks**: Liveness and readiness probes for all services
- **Resource Management**: CPU/memory limits and requests defined for all pods
- **Persistent Volumes**: StatefulSets for database, proper volume claim templates

### Phase V: Cloud Production
- **Event-Driven**: Kafka for asynchronous communication between services
- **Service Mesh**: Dapr for service-to-service communication, retry policies, circuit breakers
- **Observability**: Structured logging (JSON), metrics (Prometheus), distributed tracing (Jaeger)
- **Auto-scaling**: Horizontal Pod Autoscaler (HPA) based on CPU/memory and custom metrics
- **Disaster Recovery**: Backup strategy, restore procedures, documented runbooks

## Database & Data Management

### Schema Management
- **SQLModel**: All database models MUST use SQLModel for type safety
- **Migrations**: Alembic for all schema changes, no manual SQL modifications
- **Versioning**: All migrations MUST be versioned and reversible
- **Review**: All schema changes MUST be reviewed before production deployment

### Connection Management
- **Pooling**: Connection pooling MUST be configured for Neon DB
- **Timeouts**: Query timeouts MUST be set to prevent long-running queries
- **Retry Logic**: Transient failures MUST be retried with exponential backoff

### Performance
- **Indexing**: Indexes MUST be created for all foreign keys and frequently queried columns
- **Query Optimization**: N+1 queries MUST be avoided, use eager loading where appropriate
- **Caching**: Consider caching for frequently accessed, rarely changed data

### Data Validation
- **API Boundary**: All input MUST be validated using Pydantic models
- **Database Constraints**: Use database constraints (NOT NULL, UNIQUE, CHECK) where appropriate
- **Business Logic**: Complex validation MUST be in service layer, not database triggers

## Security Requirements

### Authentication & Authorization
- **JWT Tokens**: Use short-lived access tokens (15 minutes) and long-lived refresh tokens (7 days)
- **Token Storage**: Access tokens in memory, refresh tokens in httpOnly cookies
- **Password Hashing**: Use bcrypt with appropriate cost factor (12+)
- **Session Management**: Implement token revocation for logout

### API Security
- **Rate Limiting**: Implement per-IP and per-user rate limits
- **Input Sanitization**: Validate and sanitize all user input
- **CORS**: Whitelist specific origins in production, no wildcard (*)
- **HTTPS Only**: Enforce HTTPS in production, HSTS headers

### Secrets Management
- **Environment Variables**: All secrets in .env files (never committed)
- **Kubernetes**: Use sealed secrets or external secrets operator
- **Rotation**: Document secret rotation procedures
- **Access Control**: Principle of least privilege for all service accounts

### Data Protection
- **Encryption at Rest**: Database encryption enabled in Neon DB
- **Encryption in Transit**: TLS 1.3 for all network communication
- **PII Handling**: Document what constitutes PII, implement appropriate protections
- **Audit Logging**: Log all authentication events and sensitive operations

## Technology Stack Constraints

### Fixed Technologies (Non-Negotiable)

**Frontend**:
- Next.js 16+ (App Router pattern mandatory)
- React 18+
- TypeScript 5+
- Tailwind CSS for styling

**Backend**:
- FastAPI (latest stable)
- Python 3.11+
- SQLModel for ORM
- Pydantic v2 for validation

**Database**:
- Neon DB (PostgreSQL-compatible)
- Alembic for migrations

**AI Integration**:
- OpenAI ChatKit
- OpenAI Agents SDK
- Official MCP SDK (Model Context Protocol)

**Container Orchestration**:
- Docker for containerization
- Kubernetes for orchestration
- Minikube for local development
- DigitalOcean Kubernetes (DOKS) for cloud production

**Infrastructure Tools**:
- Helm for Kubernetes package management
- kubectl-ai for AI-assisted Kubernetes operations
- kagent for Kubernetes agent operations
- Kafka for event streaming (Phase V)
- Dapr for service mesh (Phase V)

## Deployment Requirements

### Docker Images
- **Multi-stage Builds**: Separate build and runtime stages
- **Layer Caching**: Order Dockerfile commands for optimal caching
- **Minimal Base Images**: Use alpine or distroless images where possible
- **Security Scanning**: Images MUST pass vulnerability scans before deployment
- **Tagging**: Use semantic versioning for image tags, never use `latest` in production

### Kubernetes Manifests
- **Resource Limits**: All pods MUST define CPU and memory limits and requests
- **Health Endpoints**: All services MUST implement `/health` and `/ready` endpoints
- **Graceful Shutdown**: All services MUST handle SIGTERM for graceful shutdown
- **ConfigMaps**: Use ConfigMaps for non-sensitive configuration
- **Secrets**: Use Sealed Secrets or External Secrets Operator for sensitive data

### Deployment Strategy
- **Zero Downtime**: Use rolling updates with appropriate readiness probes
- **Rollback Plan**: Document rollback procedures for each deployment
- **Canary Deployments**: Consider canary deployments for high-risk changes
- **Blue-Green**: Document blue-green deployment strategy for major releases

## Development Workflow

### Local Development
- **Docker Compose**: MUST provide docker-compose.yml for local development without Kubernetes
- **Environment Setup**: README MUST include step-by-step setup instructions
- **Hot Reload**: Development servers MUST support hot reload for rapid iteration
- **Database Seeding**: Provide scripts for seeding local database with test data

### Environment Configuration
- **Development**: Local development with docker-compose, mock external services
- **Staging**: Kubernetes cluster mirroring production, real external services
- **Production**: DigitalOcean DOKS, all production services and monitoring

### CI/CD Pipeline
- **Automated Testing**: All tests MUST run on every PR
- **Linting**: All linting checks MUST pass before merge
- **Build Verification**: Docker images MUST build successfully
- **Deployment**: Document automated deployment strategy for each environment

### Documentation Requirements
- **README**: Setup instructions, architecture overview, development workflow
- **API Documentation**: OpenAPI/Swagger for all REST endpoints
- **Runbooks**: Operational procedures for common tasks and incident response
- **ADRs**: Architecture Decision Records for significant technical decisions

## Success Criteria & Quality Gates

### Phase II Completion (Next.js + FastAPI)
- ✓ Full CRUD operations for todos via REST API
- ✓ Next.js frontend consuming FastAPI backend
- ✓ Data persisting correctly in Neon DB
- ✓ Type safety across frontend and backend (no `any` types)
- ✓ Basic error handling and loading states
- ✓ API documentation (OpenAPI/Swagger)
- ✓ Minimum test coverage achieved (70% backend, 60% frontend)

**Quality Gate**: Phase III cannot begin until all Phase II criteria are met and verified.

### Phase III Completion (AI Chatbot)
- ✓ Chatbot can create, read, update, delete todos via natural language
- ✓ OpenAI API properly integrated with conversation context
- ✓ MCP SDK correctly implemented for tool/function calling
- ✓ Graceful degradation if AI service unavailable
- ✓ Cost monitoring for OpenAI API usage implemented
- ✓ Rate limiting enforced on AI endpoints
- ✓ Streaming responses working correctly

**Quality Gate**: Phase IV cannot begin until AI integration is stable with proper error handling tested.

### Phase IV Completion (Kubernetes)
- ✓ All services containerized and running in Minikube
- ✓ Services communicate correctly within cluster
- ✓ Persistent volumes configured for database
- ✓ kubectl-ai and kagent successfully deployed
- ✓ Can scale pods and verify load distribution
- ✓ Health checks and readiness probes functioning
- ✓ Resource limits and requests properly configured

**Quality Gate**: Phase V cannot begin until local Kubernetes deployment is reproducible on any machine.

### Phase V Completion (Cloud Production)
- ✓ Production deployment on DigitalOcean DOKS
- ✓ Kafka event streaming operational
- ✓ Dapr sidecars handling service-to-service communication
- ✓ Monitoring and logging pipeline active (metrics, logs, traces)
- ✓ Auto-scaling configured and tested under load
- ✓ Disaster recovery plan documented and tested
- ✓ Security audit passed (no critical vulnerabilities)
- ✓ Load testing completed (performance benchmarks met)

**Quality Gate**: Production release requires load testing completion, security audit pass, and documented rollback procedures.

### Cross-Phase Quality Gates
- **Before Phase III**: Phase II MUST be fully functional with all CRUD operations tested
- **Before Phase IV**: AI integration MUST be stable with proper error handling
- **Before Phase V**: Local Kubernetes deployment MUST be reproducible on any machine
- **Production Release**: Load testing completed, security audit passed, rollback procedure documented and tested

## Governance

### Constitution Authority
This constitution supersedes all other development practices and guidelines. When conflicts arise between this constitution and other documentation, the constitution takes precedence.

### Amendment Process
1. **Proposal**: Any team member can propose amendments via documented rationale
2. **Review**: Amendments MUST be reviewed by technical leads
3. **Impact Analysis**: Assess impact on existing code, templates, and workflows
4. **Approval**: Amendments require consensus from technical leads
5. **Migration Plan**: Breaking changes MUST include migration plan and timeline
6. **Documentation**: Update all dependent templates and documentation
7. **Version Bump**: Follow semantic versioning for constitution updates

### Compliance Verification
- All pull requests MUST verify compliance with constitution principles
- Code reviews MUST check for adherence to standards defined herein
- Complexity violations MUST be justified and documented
- Regular audits SHOULD be conducted to ensure ongoing compliance

### Complexity Justification
Any violation of constitution principles MUST be justified with:
- **Why Needed**: Specific problem being solved
- **Alternatives Considered**: Simpler approaches and why they were rejected
- **Mitigation**: How complexity is contained and documented
- **Review**: Approval from technical lead required

### Version Control
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

**Version**: 1.0.0 | **Ratified**: 2026-01-10 | **Last Amended**: 2026-01-10
