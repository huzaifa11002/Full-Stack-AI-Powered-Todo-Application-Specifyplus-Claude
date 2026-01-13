# Implementation Plan: Next.js Authenticated Todo Frontend

**Branch**: `002-nextjs-auth-frontend` | **Date**: 2026-01-10 | **Spec**: [specs/002-nextjs-auth-frontend/spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-nextjs-auth-frontend/spec.md`

## Summary

Build a responsive Next.js 16 App Router frontend with Better Auth authentication integration, consuming the FastAPI backend via JWT-secured requests. Implements 7 user stories covering authentication (signup/signin), task CRUD operations (view, add, edit, delete, toggle completion), and logout functionality. Features responsive design (320px-2560px), optimistic UI updates, comprehensive error handling, and custom reusable components styled exclusively with Tailwind CSS. Targets modern browsers with <2s task operations, <100ms loading indicators, and <500ms error feedback.

## Technical Context

**Language/Version**: TypeScript 5.0+, Node.js 18+
**Primary Dependencies**: Next.js 16+, React 18+, Tailwind CSS 3+, Better Auth (client), Axios, react-hot-toast
**Storage**: Browser localStorage for JWT tokens (per spec decision), API backend for data persistence
**Testing**: Manual testing (automated tests deferred to later phase)
**Target Platform**: Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web application (frontend only)
**Performance Goals**: <2s task operations, <100ms loading indicators, <500ms error messages
**Constraints**: Next.js App Router only (no Pages Router), Tailwind CSS exclusively, no external component libraries, controlled components with manual validation
**Scale/Scope**: Single-page application, 7 user stories, 25 implementation phases, 4-5 day timeline

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Production-Ready Code Quality
- ✅ **TypeScript**: 100% typed code, no `any` without justification
- ⚠️ **Testing Coverage**: Deferred (manual testing initially, automated tests in later phase)
- ✅ **Linting**: ESLint + Prettier configured
- ✅ **Documentation**: Architectural decisions documented in code comments

**Justification for Testing Deferral**: Per feature specification, manual testing is acceptable for initial implementation. Automated testing (70% backend, 60% frontend) will be addressed in subsequent phases as this is frontend-only work.

### II. Cloud-Native Architecture
- ✅ **Stateless Design**: Frontend is stateless, state managed client-side or via API
- N/A **Containerization**: Not applicable for frontend-only phase
- N/A **Health Checks**: Not applicable for frontend-only phase

### III. AI Integration Excellence
- N/A **Not applicable**: No AI features in this phase

### IV. Security-First Approach
- ✅ **Secrets Management**: Environment variables in `.env.local` (never committed)
- ✅ **JWT Storage**: localStorage (per spec decision, acknowledged security tradeoff)
- ✅ **Input Validation**: Client-side validation for all forms
- ✅ **CORS**: Assumed properly configured on backend
- ✅ **No Token Exposure**: JWT never in URLs, logs, or error messages

**JWT Storage Justification**: localStorage chosen over httpOnly cookies for simplicity per spec decision. Acknowledged security tradeoff documented in research.md.

### V. Developer Experience
- ✅ **Documentation**: quickstart.md with setup instructions
- ✅ **Local Development**: Next.js dev server with hot reload
- ✅ **Environment Config**: `.env.local` for API URL
- ✅ **Consistent Patterns**: Reusable components (Button, Input, Modal, TaskForm)

**GATE STATUS**: ✅ PASS (with justified deferrals)

## Project Structure

### Documentation (this feature)

```text
specs/002-nextjs-auth-frontend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entities and types)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (TypeScript type definitions)
│   ├── auth.types.ts
│   ├── task.types.ts
│   └── api.types.ts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/  # New Next.js application
├── app/
│   ├── layout.tsx                    # Root layout with AuthProvider, Toaster
│   ├── page.tsx                      # Landing page (optional, redirects to dashboard)
│   ├── login/
│   │   └── page.tsx                  # Login page
│   ├── signup/
│   │   └── page.tsx                  # Signup page
│   ├── dashboard/
│   │   └── page.tsx                  # Protected dashboard with tasks
│   └── api/
│       └── auth/
│           └── [...all]/route.ts     # Better Auth API route handler
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx             # Login form with validation
│   │   ├── SignupForm.tsx            # Signup form with validation
│   │   └── AuthLayout.tsx            # Shared layout for auth pages
│   ├── tasks/
│   │   ├── TaskList.tsx              # Responsive task grid
│   │   ├── TaskItem.tsx              # Individual task card
│   │   ├── TaskForm.tsx              # Create/edit task form (modal)
│   │   ├── EmptyState.tsx            # No tasks placeholder
│   │   └── DeleteConfirmModal.tsx    # Delete confirmation modal
│   └── ui/
│       ├── Button.tsx                # Reusable button (variants, loading)
│       ├── Input.tsx                 # Reusable input (validation, errors)
│       ├── Modal.tsx                 # Reusable modal (backdrop, ESC)
│       └── LoadingSpinner.tsx        # Reusable spinner (sizes)
├── lib/
│   ├── auth.ts                       # Better Auth client configuration
│   ├── api/
│   │   ├── client.ts                 # Axios instance with interceptors
│   │   └── tasks.ts                  # Task API functions
│   └── hooks/
│       ├── useAuth.ts                # Auth context hook
│       └── useTasks.ts               # Task state management hook
├── types/
│   ├── auth.ts                       # User, AuthState, LoginCredentials
│   ├── task.ts                       # Task, TaskCreate, TaskUpdate
│   └── api.ts                        # ApiError, ApiResponse
├── contexts/
│   └── AuthContext.tsx               # Auth state provider
├── middleware.ts                     # Route protection
├── .env.local                        # Environment variables (not committed)
├── tailwind.config.js                # Tailwind configuration
├── tsconfig.json                     # TypeScript configuration
└── package.json                      # Dependencies
```

**Structure Decision**: Web application structure with frontend-only implementation. Backend already exists from specification 001-fastapi-todo-api. Frontend will be a separate Next.js application that consumes the FastAPI backend via REST API.

## Phase 0: Research & Technology Decisions

**Objective**: Resolve all technology choices and integration patterns before implementation.

### Research Topics

1. **Better Auth Integration with Next.js App Router**
   - Decision: Use Better Auth client library with custom integration
   - Rationale: Better Auth provides JWT authentication, but may need custom setup for App Router
   - Alternatives: Custom JWT implementation (rejected: reinventing the wheel)

2. **JWT Token Storage Strategy**
   - Decision: localStorage
   - Rationale: Simplicity, persistence across sessions, matches spec decision
   - Alternatives: httpOnly cookies (more secure but complex), sessionStorage (no persistence)

3. **State Management Approach**
   - Decision: React Context API
   - Rationale: Built-in, sufficient for app scope, no additional dependencies
   - Alternatives: Zustand (lightweight but unnecessary), Redux (overkill for this scope)

4. **Task Form Mode**
   - Decision: Modal
   - Rationale: Cleaner UI, focused interaction, consistent with edit flow
   - Alternatives: Inline form (always visible but cluttered), separate page (more navigation)

5. **Task Edit Mode**
   - Decision: Modal
   - Rationale: Consistency with create flow, clear focus
   - Alternatives: Inline editing (quick but complex), separate page (more navigation)

6. **Task Sorting Strategy**
   - Decision: Incomplete tasks first, then completed
   - Rationale: Better UX for todo app, prioritizes active tasks
   - Alternatives: Newest first (chronological), custom sort (user control but complex)

7. **Mobile Navigation Pattern**
   - Decision: Top navigation with logout button
   - Rationale: Simple single-page app, consistent across devices
   - Alternatives: Bottom nav (thumb-friendly but unnecessary), hamburger menu (space-saving but hidden)

**Output**: `research.md` documenting all decisions with rationale and alternatives.

## Phase 1: Design & Contracts

**Objective**: Define data models, API contracts, and setup documentation.

### Deliverables

1. **data-model.md**: Entity definitions
   - User: id, email, username (optional)
   - Task: id, user_id, title, description, is_completed, created_at, updated_at
   - AuthSession: user, token, isAuthenticated, isLoading

2. **contracts/**: TypeScript type definitions
   - `auth.types.ts`: User, AuthState, LoginCredentials, SignupData
   - `task.types.ts`: Task, TaskCreate, TaskUpdate
   - `api.types.ts`: ApiError, ApiResponse<T>

3. **quickstart.md**: Setup instructions
   - Prerequisites (Node.js 18+, npm/yarn/pnpm)
   - Installation steps (`npx create-next-app`, dependencies)
   - Environment configuration (`.env.local`)
   - Running dev server (`npm run dev`)
   - Testing instructions (manual test checklist)

4. **Agent Context Update**: Run `.specify/scripts/bash/update-agent-context.sh claude`
   - Add: Next.js 16+, TypeScript 5+, Tailwind CSS 3+, Better Auth, Axios, react-hot-toast

## Phase 2-26: Implementation Phases

### Phase 2: Next.js Project Setup
- Initialize: `npx create-next-app@latest` (TypeScript, ESLint, Tailwind, App Router)
- Install: `npm install better-auth axios react-hot-toast`
- Create directory structure (app/, components/, lib/, types/, contexts/)
- Configure `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8001`
- Configure Tailwind (default breakpoints: 640px, 768px, 1024px, 1280px, 1536px)

### Phase 3: Better Auth Client Configuration
- **lib/auth.ts**: Better Auth client (signUp, signIn, signOut, getSession)
- **app/api/auth/[...all]/route.ts**: Better Auth API route handler
- Configure `BETTER_AUTH_SECRET` in `.env.local`

### Phase 4: Authentication Context & State Management
- **contexts/AuthContext.tsx**: AuthContext with AuthState interface
- **lib/hooks/useAuth.ts**: Custom hook wrapping AuthContext
- Implement: login, signup, logout, token storage (localStorage), session checking

### Phase 5: Route Protection Middleware
- **middleware.ts**: Authentication checks for protected routes
- Redirect logic: unauthenticated → /login, authenticated on /login → /dashboard
- Matcher config: `['/dashboard/:path*']`

### Phase 6: Authentication UI - Login Page
- **app/login/page.tsx**: Login page wrapper
- **components/auth/LoginForm.tsx**: Form with email/password, validation, error handling
- Styling: Tailwind (max-w-md, responsive, focus states, error states)
- Integration: Better Auth signIn, token storage, redirect to /dashboard

### Phase 7: Authentication UI - Signup Page
- **app/signup/page.tsx**: Signup page wrapper
- **components/auth/SignupForm.tsx**: Form with email/password/confirm, validation
- **components/auth/AuthLayout.tsx**: Shared layout (centered card, logo, shadows)
- Integration: Better Auth signUp, auto-login, redirect to /dashboard

### Phase 8: API Client Setup
- **lib/api/client.ts**: Axios instance with base URL
- Request interceptor: Add `Authorization: Bearer ${token}` header
- Response interceptor: Handle 401 (logout, redirect), 403 (error message), parse errors

### Phase 9: Task API Functions
- **lib/api/tasks.ts**: API functions
  - `getTasks(userId)`: GET /api/{userId}/tasks
  - `createTask(userId, data)`: POST /api/{userId}/tasks
  - `getTask(userId, taskId)`: GET /api/{userId}/tasks/{taskId}
  - `updateTask(userId, taskId, data)`: PUT /api/{userId}/tasks/{taskId}
  - `deleteTask(userId, taskId)`: DELETE /api/{userId}/tasks/{taskId}
  - `toggleTaskComplete(userId, taskId)`: PATCH /api/{userId}/tasks/{taskId}/complete
- TypeScript types, error handling

### Phase 10: Task State Management Hook
- **lib/hooks/useTasks.ts**: Custom hook
- State: tasks[], isLoading, error
- Functions: loadTasks, addTask, updateTask, removeTask, toggleComplete
- Optimistic updates with rollback on error

### Phase 11: Dashboard Layout
- **app/dashboard/page.tsx**: Protected route
- Layout: Header (logo, user, logout), TaskForm, TaskList, EmptyState
- Loading/error states

### Phase 12: Task Creation Component
- **components/tasks/TaskForm.tsx**: Modal form
- Fields: title (required, max 200 chars), description (optional, max 2000 chars)
- Validation: required, character limits, character count
- Submit: optimistic update, loading state, error handling

### Phase 13: Task List Component
- **components/tasks/TaskList.tsx**: Responsive grid
- Layout: 1 col (mobile), 2 cols (tablet), 3 cols (desktop)
- Sorting: incomplete first, then completed
- Task count display

### Phase 14: Task Item Component
- **components/tasks/TaskItem.tsx**: Task card
- Display: checkbox, title (strikethrough if complete), description, date
- Actions: edit button, delete button
- Styling: hover effects, touch-friendly (44px+), visual distinction for completed

### Phase 15: Task Edit Functionality
- **components/tasks/EditTaskModal.tsx**: Modal reusing TaskForm
- Pass existing task data, change button to "Update Task"
- Handle API call, close modal on success

### Phase 16: Task Delete Confirmation
- **components/tasks/DeleteConfirmModal.tsx**: Confirmation modal
- Display task title, "Cancel" and "Delete" buttons
- Loading state on delete, close on success

### Phase 17: Empty State Component
- **components/tasks/EmptyState.tsx**: No tasks placeholder
- Display: icon, "No tasks yet" message, "Create your first task" CTA

### Phase 18: Reusable UI Components
- **components/ui/Button.tsx**: Variants (primary, secondary, danger), sizes (sm, md, lg), loading state
- **components/ui/Input.tsx**: Label, error display, character count, focus/error states
- **components/ui/Modal.tsx**: Backdrop, centered card, close button (X), ESC key, prevent body scroll
- **components/ui/LoadingSpinner.tsx**: Animated spinner, size variants

### Phase 19: Toast Notifications
- Install: `npm install react-hot-toast`
- **app/layout.tsx**: Add `<Toaster position="top-right" />`
- Use throughout: success (task created/updated/deleted, login), error (network, validation)

### Phase 20: Responsive Design Implementation
- Mobile (320px-767px): 1 col, full-width, stack vertically, 44px+ tap targets
- Tablet (768px-1023px): 2 cols, 80% modal width
- Desktop (1024px+): 3 cols, max-w-7xl container, hover states, max-w-lg modals
- Tailwind classes: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

### Phase 21: Loading States
- Skeleton loaders: 3-6 cards, pulse animation, match TaskItem dimensions
- Button loading: spinner, disabled, stable width
- Full-page loading: centered spinner

### Phase 22: Error Handling
- Network errors: toast message, console log, retry option
- Validation errors: inline display, red border, prevent submission
- 401: logout, redirect to /login, "Session expired" message
- 403: "Access denied" message
- 404: "Task not found" message, remove from UI
- Optional: Error Boundary component

### Phase 23: TypeScript Type Definitions
- **types/task.ts**: Task, TaskCreate, TaskUpdate
- **types/auth.ts**: User, AuthState, LoginCredentials, SignupData
- **types/api.ts**: ApiError, ApiResponse<T>

### Phase 24: Performance Optimization
- React.memo for TaskItem (prevent re-renders)
- Optimize useTasks hook dependencies
- Optimistic updates for all operations
- Consider lazy loading modals

### Phase 25: Logout Functionality
- Add logout button to dashboard header
- Handle: auth.signOut(), clear localStorage, clear context, redirect to /login
- Optional: confirmation modal

### Phase 26: Landing Page (Optional)
- **app/page.tsx**: App name, tagline, description, CTAs (Get Started, Login)
- Auto-redirect if authenticated
- Responsive hero section

## Architecture Decision Records

### ADR-001: Task Form Mode (Modal vs Inline vs Separate Page)
- **Decision**: Modal
- **Context**: Need to create/edit tasks without cluttering dashboard
- **Options**: Inline form (always visible), Modal (overlay), Separate page (navigation)
- **Rationale**: Modal provides clean UI, focused interaction, consistent with edit flow
- **Consequences**: Requires modal component, ESC/backdrop handling

### ADR-002: Edit Mode (Inline vs Modal vs Separate Page)
- **Decision**: Modal
- **Context**: Need to edit existing tasks
- **Options**: Inline editing (quick), Modal (focused), Separate page (navigation)
- **Rationale**: Consistency with create flow, clear focus, reuses TaskForm
- **Consequences**: Same modal component, consistent UX

### ADR-003: Token Storage (localStorage vs sessionStorage vs httpOnly cookies)
- **Decision**: localStorage
- **Context**: Need to persist JWT tokens across sessions
- **Options**: localStorage (persistent), sessionStorage (session-only), httpOnly cookies (secure)
- **Rationale**: Simplicity, persistence, matches spec decision
- **Consequences**: XSS vulnerability (mitigated by input sanitization), no automatic expiration

### ADR-004: State Management (React Context vs Zustand vs Redux)
- **Decision**: React Context API
- **Context**: Need global auth and task state
- **Options**: React Context (built-in), Zustand (lightweight), Redux (powerful)
- **Rationale**: Built-in, sufficient for scope, no additional dependencies
- **Consequences**: May need Zustand if complexity grows

### ADR-005: Task Sorting (Incomplete First vs Newest First vs Custom Sort)
- **Decision**: Incomplete tasks first, then completed
- **Context**: Need to display tasks in useful order
- **Options**: Incomplete first (priority), Newest first (chronological), Custom sort (user control)
- **Rationale**: Better UX for todo app, prioritizes active tasks
- **Consequences**: Simple implementation, no user customization

### ADR-006: Mobile Navigation (Bottom Nav vs Hamburger vs Top Nav)
- **Decision**: Top navigation with logout button
- **Context**: Need navigation for single-page app
- **Options**: Bottom nav (thumb-friendly), Hamburger menu (space-saving), Top nav (consistent)
- **Rationale**: Simple SPA, consistent across devices, minimal navigation needs
- **Consequences**: Logout always visible, no hidden navigation

## Testing Strategy

### Authentication Flow Testing
1. ✅ Sign up with valid email/password
2. ✅ Signup validation (password match, email format)
3. ✅ Login with registered credentials
4. ✅ Login fails with wrong password
5. ✅ Protected routes redirect to login when unauthenticated
6. ✅ Login/signup pages redirect to dashboard when authenticated
7. ✅ Logout clears auth state and redirects to login
8. ✅ Token persists across page refresh

### Task Operations Testing
1. ✅ Create new task with title only
2. ✅ Create task with title and description
3. ✅ Form validation prevents empty title
4. ✅ View all user's tasks
5. ✅ Edit task title
6. ✅ Edit task description
7. ✅ Toggle task completion (check/uncheck)
8. ✅ Delete task with confirmation
9. ✅ Empty state shows when no tasks
10. ✅ Task list updates immediately after operations (optimistic)

### Responsive Design Testing
1. ✅ Mobile (320px): Single column, touch-friendly
2. ✅ Mobile (375px): iPhone standard size works
3. ✅ Tablet (768px): Two columns, good spacing
4. ✅ Desktop (1024px): Three columns, optimal layout
5. ✅ Desktop (1440px): Content doesn't stretch too wide
6. ✅ Forms usable on all screen sizes
7. ✅ Buttons tappable on touch devices (44px+)
8. ✅ Text readable without zooming

### Error Handling Testing
1. ✅ Network error shows friendly message
2. ✅ 401 error redirects to login
3. ✅ Invalid form submission shows validation errors
4. ✅ API errors show toast notifications
5. ✅ Loading states show during async operations
6. ✅ Can retry after failed operation

### UI/UX Testing
1. ✅ All buttons have loading states
2. ✅ Hover effects work on desktop
3. ✅ Focus states visible for keyboard navigation
4. ✅ Modals can be closed with ESC key
5. ✅ Modals can be closed by clicking backdrop
6. ✅ Toast notifications appear and auto-dismiss
7. ✅ Completed tasks visually distinct (strikethrough, gray)
8. ✅ Smooth animations on task appear/disappear

## Risks & Mitigation

1. **Better Auth Integration Complexity**
   - Risk: Limited documentation for Next.js App Router
   - Mitigation: Allocate extra time, review examples, fallback to custom JWT if needed

2. **JWT Token Expiration Handling**
   - Risk: Token expiration during active sessions disrupts UX
   - Mitigation: Implement token refresh or graceful expiration with clear messaging

3. **Optimistic Update Failures**
   - Risk: Network errors cause UI/server state divergence
   - Mitigation: Robust rollback, automatic retry, clear error messages

4. **Responsive Design Complexity**
   - Risk: Custom components without UI library increases development time
   - Mitigation: Create reusable primitives early, consistent Tailwind utilities

5. **TypeScript Learning Curve**
   - Risk: Team adaptation to strict typing
   - Mitigation: Proper config, type inference, allocated learning time

6. **API Endpoint Dependency**
   - Risk: Frontend blocked if backend not ready
   - Mitigation: Mock API responses, API client abstraction layer

7. **Cross-Browser Compatibility**
   - Risk: Modern features may not work in older browsers
   - Mitigation: Define minimum versions, test on target browsers early

8. **Performance on Slow Networks**
   - Risk: Large bundles or inefficient API calls impact UX
   - Mitigation: Code splitting, bundle optimization, proper loading states

9. **State Management Complexity**
   - Risk: React hooks may become unwieldy
   - Mitigation: Consider Zustand if Context becomes too complex

10. **Timeline Pressure**
    - Risk: 4-5 day timeline is aggressive
    - Mitigation: Strict P1/P2 prioritization, defer P3/P4 if needed

## Quality Validation

- ✅ All 5 core todo features work end-to-end
- ✅ Responsive on mobile, tablet, desktop
- ✅ JWT automatically included in requests
- ✅ Loading states on all async operations
- ✅ Error handling for all failure cases
- ✅ Clean, consistent UI styling
- ✅ Type safety with TypeScript
- ✅ No console errors or warnings

## Complexity Tracking

*No constitution violations requiring justification.*

---

**Next Steps**:
1. Generate `research.md` (Phase 0)
2. Generate `data-model.md` (Phase 1)
3. Generate `contracts/` (Phase 1)
4. Generate `quickstart.md` (Phase 1)
5. Update agent context (Phase 1)
6. Begin implementation (Phase 2-26)
