---
id: 0001
title: Better Auth JWT Specification
stage: spec
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-better-auth-jwt
branch: 003-better-auth-jwt
user: user
command: /sp.specify
labels: ["specification", "authentication", "jwt", "better-auth", "fastapi", "nextjs", "security", "middleware"]
links:
  spec: specs/003-better-auth-jwt/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-better-auth-jwt/spec.md
  - specs/003-better-auth-jwt/checklists/requirements.md
tests:
  - Requirements checklist validation: PASS (52/52 items)
---

## Prompt

/sp.specify Better Auth authentication with JWT-secured FastAPI backend integration

Target audience: Full-stack developers implementing secure user authentication and authorization

Focus: User signup/signin with Better Auth, JWT token generation, and FastAPI middleware for token verification and user validation

Success criteria:
- Better Auth installed and configured with JWT plugin in Next.js
- Users can successfully sign up with email and password
- Users can sign in and receive valid JWT token
- JWT tokens include user_id, email, and expiration claims
- FastAPI middleware intercepts all /api/* requests and verifies JWT
- Middleware extracts user information from valid tokens
- User ID from JWT matches user_id in URL parameters (enforced)
- Unauthorized requests (no token/invalid token) return 401 with clear message
- Token expiration properly configured (7 days default)
- Shared BETTER_AUTH_SECRET environment variable used in both services
- Protected endpoints reject requests without valid tokens
- User can only access their own tasks (verified via JWT user_id)

Constraints:
- Technology: Better Auth (Next.js frontend) + PyJWT (FastAPI backend)
- Authentication method: JWT tokens only (no session-based auth)
- Token transmission: Authorization: Bearer <token> header exclusively
- Secret management: Environment variables (.env files, not hardcoded)
- Password hashing: Better Auth's built-in bcrypt
- Token storage: httpOnly cookies or localStorage (document choice)
- Timeline: Complete within 3-4 days

Not building:
- OAuth providers (Google, GitHub, Facebook login)
- Password reset/forgot password functionality
- Email verification workflow
- Two-factor authentication (2FA)
- Role-based access control (RBAC) or permissions
- User profile management endpoints
- Admin dashboard or user management UI
- Refresh token rotation mechanism
- Account deletion or deactivation
- Session management across devices
- "Remember me" functionality

## Response snapshot

Created comprehensive feature specification for Better Auth JWT authentication integration between Next.js frontend and FastAPI backend.

**Specification Structure**:
- **4 User Stories** with priority levels (P1: Registration, Login, Protected API Access; P2: User Isolation)
- Each story includes: priority justification, independent test description, and Given/When/Then acceptance scenarios
- **10 Edge Cases** covering token expiration, concurrent logins, secret rotation, malformed tokens, etc.

**Requirements**:
- **33 Functional Requirements** organized into 5 categories:
  - Authentication & Token Management (FR-001 to FR-007)
  - FastAPI Middleware & Verification (FR-008 to FR-014)
  - User Isolation & Authorization (FR-015 to FR-018)
  - Error Handling & Security (FR-019 to FR-024)
  - Token Storage & Transmission (FR-025 to FR-028)
  - Configuration & Environment (FR-029 to FR-033)
- **Key Entities**: User, JWT Token, Task with attributes and relationships

**Success Criteria**:
- **10 Measurable Outcomes** (SC-001 to SC-010) covering Better Auth installation, user signup/signin, JWT verification, middleware functionality, user isolation enforcement, and token configuration

**Assumptions, Constraints, Dependencies**:
- **15 Assumptions** about database, environment, dependencies, and token management
- **20 Out of Scope Items** explicitly excluding OAuth, password reset, 2FA, RBAC, refresh tokens, etc.
- **Dependencies**: Better Auth (npm), PyJWT (pip), PostgreSQL, features 001 & 002
- **Constraints**: Technology stack (Better Auth + PyJWT), JWT-only auth, Bearer token transmission, 7-day expiration, 3-4 day timeline

**Risk Analysis**:
- **Technical Risks**: Better Auth compatibility (High), token size growth (Medium), clock skew (Medium)
- **Security Risks**: Secret compromise (Critical), localStorage XSS vulnerability (High), long token expiration (Medium)
- **Operational Risks**: No token revocation (High), secret rotation coordination (Medium), re-login UX (Low)
- All risks include mitigation strategies and impact assessments

**Quality Validation**:
- Created requirements checklist with 52 validation items
- All items passed (52/52 completed)
- No [NEEDS CLARIFICATION] markers remaining
- Specification ready for planning phase

## Outcome

- ✅ Impact: Complete feature specification created for Better Auth JWT authentication integration. Specification includes 4 prioritized user stories, 33 functional requirements, 10 success criteria, comprehensive assumptions/constraints/dependencies, and risk analysis. Quality validated with 52/52 checklist items passed. Ready for `/sp.plan` phase.
- 🧪 Tests: Requirements checklist validation: PASS (52/52 items). All mandatory sections present and complete. No clarifications needed.
- 📁 Files: Created 2 files: specs/003-better-auth-jwt/spec.md (comprehensive specification), specs/003-better-auth-jwt/checklists/requirements.md (quality validation checklist)
- 🔁 Next prompts: Run `/sp.plan` to create technical implementation plan, or run `/sp.clarify` if any questions arise about requirements
- 🧠 Reflection: Specification creation was straightforward with clear user requirements. All 12 success criteria from user input were incorporated into functional requirements and success criteria. User explicitly provided constraints (Better Auth + PyJWT, JWT-only, Bearer tokens, 7-day expiration) and exclusions (OAuth, password reset, 2FA, RBAC, etc.), which made scoping clear. Risk analysis identified potential Better Auth compatibility issues (learned from feature 002 implementation). Specification is comprehensive and unambiguous, ready for planning without clarifications.

## Evaluation notes (flywheel)

- Failure modes observed: None. Specification creation completed successfully with all requirements captured and validated.
- Graders run and results (PASS/FAIL): Requirements checklist: PASS (52/52 items completed). All mandatory sections present, user stories prioritized, requirements specific and testable, success criteria measurable, no placeholders remaining.
- Prompt variant (if applicable): Standard /sp.specify workflow with detailed user requirements including success criteria, constraints, and explicit exclusions
- Next experiment (smallest change to try): Consider adding a "Security Considerations" section to the spec template for authentication-heavy features to ensure security risks are surfaced early in the specification phase
