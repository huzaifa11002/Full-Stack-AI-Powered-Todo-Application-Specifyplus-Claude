---
id: 0002
title: Better Auth JWT Implementation Plan
stage: plan
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-better-auth-jwt
branch: 003-better-auth-jwt
user: user
command: /sp.plan
labels: ["planning", "authentication", "jwt", "better-auth", "fastapi", "nextjs", "security", "middleware", "pyjwt", "bcrypt"]
links:
  spec: specs/003-better-auth-jwt/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-better-auth-jwt/plan.md
  - specs/003-better-auth-jwt/research.md
  - specs/003-better-auth-jwt/data-model.md
  - specs/003-better-auth-jwt/contracts/auth-api.yaml
  - specs/003-better-auth-jwt/contracts/jwt-schema.json
  - specs/003-better-auth-jwt/quickstart.md
  - CLAUDE.md (updated with Better Auth and PyJWT technologies)
tests:
  - N/A (planning phase, no tests executed)
---

## Prompt

/sp.plan Implement Better Auth with JWT security integration

Create: Authentication flow diagram, JWT token structure, middleware architecture, secret key sharing strategy.

[User provided detailed implementation structure with 11 phases, 5 key decisions, testing strategy, technical details, and security checklist - see full prompt in command-args]

## Response snapshot

Created comprehensive implementation plan for Better Auth JWT authentication integration between Next.js frontend and FastAPI backend.

**Planning Artifacts Created**:
- **plan.md**: Complete implementation plan with 11 phases, constitution check, complexity tracking, and technical context
- **research.md**: 7 research topics with decisions, rationale, and alternatives considered
- **data-model.md**: 3 entities (User, JWT Token, Task) with schemas, relationships, and database migration
- **contracts/auth-api.yaml**: OpenAPI 3.0 specification for authentication endpoints (signup, signin, protected routes)
- **contracts/jwt-schema.json**: JSON schema for JWT token structure with validation rules
- **quickstart.md**: 4 integration scenarios with code examples and troubleshooting guide

**Key Technical Decisions**:
1. Token Storage: localStorage (dev) → httpOnly cookies (prod)
2. Token Expiration: 7 days (per spec requirement)
3. Password Requirements: 8 chars min, number + letter
4. JWT Algorithm: HS256 with shared BETTER_AUTH_SECRET
5. User Isolation: Middleware extraction + route validation
6. Better Auth: Server-side config with fallback to custom JWT

**Constitution Check**: PASS WITH JUSTIFICATIONS
- 7-day token expiration (vs 15-min recommendation): Justified by spec requirement
- No token revocation: Acceptable for MVP, documented limitation

**Implementation Phases**:
1. Better Auth Setup (Frontend)
2. User Database Schema (Backend)
3. Signup Implementation
4. Signin Implementation
5. Frontend Token Management
6. FastAPI JWT Middleware
7. Apply Middleware to Routes
8. Update API Routes for Auth
9. Error Handling & Responses
10. Environment Configuration
11. Frontend Auth Flow Integration

## Outcome

- ✅ Impact: Complete implementation plan created for Better Auth JWT authentication integration. Plan includes technical context, constitution check, 11 implementation phases, 7 research decisions, 3 data entities, OpenAPI contracts, JWT schema, and quickstart guide with 4 integration scenarios. Ready for /sp.tasks phase.
- 🧪 Tests: N/A (planning phase). Testing strategy defined in plan: authentication flow tests (7 scenarios), authorization tests (7 scenarios), integration tests (5 scenarios), security tests (5 scenarios).
- 📁 Files: Created 7 files: plan.md (comprehensive implementation plan), research.md (technology decisions), data-model.md (entity definitions), contracts/auth-api.yaml (OpenAPI spec), contracts/jwt-schema.json (JWT schema), quickstart.md (integration guide), CLAUDE.md (updated agent context)
- 🔁 Next prompts: Run /sp.tasks to generate task breakdown from implementation plan, or review planning artifacts for clarifications
- 🧠 Reflection: Planning phase completed successfully with comprehensive artifacts. User provided detailed implementation structure which was incorporated into plan. Constitution check identified 2 violations (7-day token expiration, no token revocation) which were justified per spec requirements. Research phase resolved 7 key decisions with rationale and alternatives. Data model defined 3 entities with relationships and migration script. API contracts created with OpenAPI 3.0 specification. Quickstart guide provides 4 integration scenarios with code examples. Plan is thorough and ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None. Planning phase completed successfully with all required artifacts generated.
- Graders run and results (PASS/FAIL): Constitution Check: PASS WITH JUSTIFICATIONS (2 violations justified). All mandatory planning artifacts created and validated.
- Prompt variant (if applicable): Standard /sp.plan workflow with detailed user-provided implementation structure incorporated into plan
- Next experiment (smallest change to try): Consider creating visual diagrams (authentication flow, JWT structure, middleware architecture) as separate artifacts to complement text-based planning documents
