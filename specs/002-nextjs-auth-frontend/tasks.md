# Implementation Tasks: Next.js Authenticated Todo Frontend

**Feature**: Next.js Authenticated Todo Frontend
**Branch**: `002-nextjs-auth-frontend`
**Date**: 2026-01-10
**Status**: Ready for Implementation

## Overview

This document contains the complete task breakdown for implementing the Next.js 16 authenticated frontend. Tasks are organized by user story to enable independent implementation and testing. Each task follows the strict checklist format with task IDs, parallel markers, story labels, and exact file paths.

**Total Tasks**: 85
**MVP Tasks** (US1-US3): 45 tasks
**Enhancement Tasks** (US4-US7): 30 tasks
**Polish Tasks**: 10 tasks

## Task Format

```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

- **TaskID**: Sequential number (T001, T002, etc.)
- **[P]**: Parallel execution marker (different files, no dependencies)
- **[Story]**: User story label (US1, US2, etc.) - only for user story phases
- **Description**: Clear action with exact file path

## Implementation Strategy

**MVP First** (US1-US3): Authentication + View Tasks + Add Tasks
- Delivers core value: Users can sign up, sign in, view tasks, and add tasks
- Independently testable at each story completion
- Estimated: 2-3 days

**Enhancements** (US4-US7): Edit + Toggle + Delete + Logout
- Builds on MVP foundation
- Each story independently testable
- Estimated: 1-2 days

**Polish**: Responsive design, error handling, performance
- Cross-cutting concerns
- Estimated: 0.5-1 day

---

## Phase 1: Setup & Project Initialization

**Goal**: Initialize Next.js project with all dependencies and base configuration.

**Tasks**:

- [X] T001 Initialize Next.js 16+ project with TypeScript, ESLint, Tailwind CSS, App Router in frontend/ directory
- [X] T002 Install dependencies: better-auth, axios, react-hot-toast
- [X] T003 Create .env.local with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [X] T004 Create .gitignore with node_modules/, .next/, .env*, dist/, build/, *.log
- [X] T005 Configure tailwind.config.js with default breakpoints (640px, 768px, 1024px, 1280px, 1536px)
- [X] T006 Configure tsconfig.json with strict mode, paths aliases
- [X] T007 Create directory structure: app/, components/, lib/, types/, contexts/
- [X] T008 Create subdirectories: components/auth/, components/tasks/, components/ui/, lib/api/, lib/hooks/

**Acceptance**: Project initialized, dependencies installed, directory structure created, dev server starts successfully.

---

## Phase 2: Foundational Components & Types

**Goal**: Create reusable UI components and TypeScript type definitions used across all user stories.

**Tasks**:

- [X] T009 [P] Create types/auth.ts with User, AuthState, LoginCredentials, SignupData, AuthContextValue interfaces
- [X] T010 [P] Create types/task.ts with Task, TaskCreate, TaskUpdate, TaskFormData, TaskValidationErrors interfaces
- [X] T011 [P] Create types/api.ts with ApiError, ApiResponse, ApiErrorResponse, ApiClientConfig interfaces
- [X] T012 [P] Create components/ui/LoadingSpinner.tsx with size variants (sm, md, lg) and Tailwind animations
- [X] T013 [P] Create components/ui/Button.tsx with variants (primary, secondary, danger), sizes (sm, md, lg), loading state
- [X] T014 [P] Create components/ui/Input.tsx with label, error display, character count, focus/error states
- [X] T015 [P] Create components/ui/Modal.tsx with backdrop, centered card, close button, ESC key handler, body scroll prevention
- [X] T016 [P] Create app/globals.css with Tailwind directives and custom styles

**Acceptance**: All foundational types and UI components created, reusable across features, properly typed.

---

## Phase 3: User Story 1 - User Registration and Authentication (P1) 🎯 MVP

**Story Goal**: Users can create accounts, sign in, and access protected routes with JWT authentication.

**Independent Test Criteria**:
- ✅ Can sign up with valid email/password
- ✅ Signup validation works (password match, email format)
- ✅ Can login with registered credentials
- ✅ Login fails with wrong password
- ✅ Protected routes redirect to login when unauthenticated
- ✅ Login/signup pages redirect to dashboard when authenticated
- ✅ Token persists across page refresh

**Tasks**:

### Better Auth Configuration

- [X] T017 [US1] Create lib/auth.ts with Better Auth client configuration (signUp, signIn, signOut, getSession methods)
- [ ] T018 [US1] Create app/api/auth/[...all]/route.ts with Better Auth API route handler

### Authentication Context & State

- [X] T019 [US1] Create contexts/AuthContext.tsx with AuthState interface and AuthProvider component
- [X] T020 [US1] Implement token storage in localStorage in contexts/AuthContext.tsx
- [X] T021 [US1] Implement session checking on mount in contexts/AuthContext.tsx
- [X] T022 [US1] Create lib/hooks/useAuth.ts custom hook wrapping AuthContext

### Route Protection

- [X] T023 [US1] Create middleware.ts with authentication checks for /dashboard routes
- [X] T024 [US1] Implement redirect logic in middleware.ts (unauthenticated → /login, authenticated on /login → /dashboard)

### Authentication UI - Signup

- [X] T025 [US1] Create components/auth/AuthLayout.tsx with centered card, logo area, responsive container
- [X] T026 [US1] Create components/auth/SignupForm.tsx with email, password, confirmPassword fields
- [X] T027 [US1] Implement form validation in components/auth/SignupForm.tsx (email format, password strength, password match)
- [X] T028 [US1] Implement signup submission handler in components/auth/SignupForm.tsx (Better Auth signUp, auto-login, redirect)
- [X] T029 [US1] Create app/signup/page.tsx importing SignupForm and AuthLayout

### Authentication UI - Login

- [X] T030 [US1] Create components/auth/LoginForm.tsx with email and password fields
- [X] T031 [US1] Implement form validation in components/auth/LoginForm.tsx (email format, required fields)
- [X] T032 [US1] Implement login submission handler in components/auth/LoginForm.tsx (Better Auth signIn, token storage, redirect)
- [X] T033 [US1] Create app/login/page.tsx importing LoginForm and AuthLayout

### Root Layout

- [X] T034 [US1] Update app/layout.tsx to wrap children with AuthProvider
- [X] T035 [US1] Add Toaster component from react-hot-toast to app/layout.tsx

**Story Completion**: User Story 1 complete when all authentication flows work end-to-end.

---

## Phase 4: User Story 2 - View All Tasks (P2) 🎯 MVP

**Story Goal**: Authenticated users can view all their tasks in a responsive list with loading and empty states.

**Independent Test Criteria**:
- ✅ Can view all user's tasks after authentication
- ✅ Empty state shows when no tasks exist
- ✅ Loading state shows during task fetch
- ✅ Tasks display with title, description, completion status
- ✅ Responsive layout works on mobile (320px), tablet (768px), desktop (1024px+)

**Tasks**:

### API Client Setup

- [X] T036 [US2] Create lib/api/client.ts with Axios instance and base URL from env
- [X] T037 [US2] Implement request interceptor in lib/api/client.ts to add Authorization header with JWT token
- [X] T038 [US2] Implement response interceptor in lib/api/client.ts to handle 401 errors (logout, redirect)

### Task API Functions

- [X] T039 [US2] Create lib/api/tasks.ts with getTasks(userId) function using apiClient
- [X] T040 [US2] Implement error handling in lib/api/tasks.ts for network errors and API errors

### Task State Management

- [X] T041 [US2] Create lib/hooks/useTasks.ts with tasks state, isLoading, error
- [X] T042 [US2] Implement loadTasks() function in lib/hooks/useTasks.ts with error handling

### Dashboard Layout

- [X] T043 [US2] Create app/dashboard/page.tsx as protected route with user from useAuth
- [X] T044 [US2] Implement loading state in app/dashboard/page.tsx with LoadingSpinner
- [X] T045 [US2] Implement error state in app/dashboard/page.tsx with error message display
- [X] T046 [US2] Add header with app name and user email to app/dashboard/page.tsx

### Task List Components

- [X] T047 [US2] Create components/tasks/EmptyState.tsx with icon, message, and CTA
- [X] T048 [US2] Create components/tasks/TaskItem.tsx with checkbox, title, description, action buttons
- [X] T049 [US2] Implement responsive card styling in components/tasks/TaskItem.tsx (hover effects, touch-friendly 44px+ targets)
- [X] T050 [US2] Implement visual distinction for completed tasks in components/tasks/TaskItem.tsx (strikethrough, gray, opacity)
- [X] T051 [US2] Create components/tasks/TaskList.tsx with responsive grid (1 col mobile, 2 cols tablet, 3 cols desktop)
- [X] T052 [US2] Implement task sorting in components/tasks/TaskList.tsx (incomplete first, then completed)
- [X] T053 [US2] Add task count display in components/tasks/TaskList.tsx ("X of Y completed")
- [X] T054 [US2] Integrate TaskList and EmptyState in app/dashboard/page.tsx

**Story Completion**: User Story 2 complete when users can view all tasks with proper loading/empty states.

---

## Phase 5: User Story 3 - Add New Task (P2) 🎯 MVP

**Story Goal**: Authenticated users can create new tasks with title and optional description using optimistic updates.

**Independent Test Criteria**:
- ✅ Can create task with title only
- ✅ Can create task with title and description
- ✅ Form validation prevents empty title
- ✅ Task appears immediately in list (optimistic update)
- ✅ Loading state shows during API request
- ✅ Error handling reverts optimistic update on failure

**Tasks**:

### Task API Functions

- [X] T055 [US3] Add createTask(userId, data) function to lib/api/tasks.ts using apiClient

### Task State Management

- [X] T056 [US3] Implement addTask(data) function in lib/hooks/useTasks.ts with optimistic update
- [X] T057 [US3] Implement rollback logic in lib/hooks/useTasks.ts for failed createTask API calls

### Task Form Component

- [X] T058 [US3] Create components/tasks/TaskForm.tsx with title input, description textarea, submit button
- [X] T059 [US3] Implement controlled inputs with local state in components/tasks/TaskForm.tsx
- [X] T060 [US3] Implement form validation in components/tasks/TaskForm.tsx (title required, character limits)
- [X] T061 [US3] Add character count display in components/tasks/TaskForm.tsx (title: 200 max, description: 2000 max)
- [X] T062 [US3] Implement form submission handler in components/tasks/TaskForm.tsx with loading state
- [X] T063 [US3] Implement form reset on successful submission in components/tasks/TaskForm.tsx
- [X] T064 [US3] Add toast notifications in components/tasks/TaskForm.tsx (success, error)

### Modal Integration

- [X] T065 [US3] Wrap TaskForm in Modal component for create mode
- [X] T066 [US3] Add "Add Task" button to app/dashboard/page.tsx to open modal
- [X] T067 [US3] Implement modal state management in app/dashboard/page.tsx (isOpen, onClose)

**Story Completion**: User Story 3 complete when users can create tasks with optimistic updates and validation.

---

## Phase 6: User Story 4 - Edit Task Details (P3)

**Story Goal**: Authenticated users can edit existing task titles and descriptions with optimistic updates.

**Independent Test Criteria**:
- ✅ Can edit task title
- ✅ Can edit task description
- ✅ Form validation prevents empty title
- ✅ Changes appear immediately (optimistic update)
- ✅ Cancel discards changes
- ✅ Error handling reverts changes on failure

**Tasks**:

### Task API Functions

- [X] T068 [US4] Add updateTask(userId, taskId, data) function to lib/api/tasks.ts using apiClient

### Task State Management

- [X] T069 [US4] Implement updateTask(id, data) function in lib/hooks/useTasks.ts with optimistic update
- [X] T070 [US4] Implement rollback logic in lib/hooks/useTasks.ts for failed updateTask API calls

### Edit Modal Component

- [X] T071 [US4] Update components/tasks/TaskForm.tsx to accept initialData prop for edit mode
- [X] T072 [US4] Update components/tasks/TaskForm.tsx to change button text to "Update Task" in edit mode
- [X] T073 [US4] Add edit button to components/tasks/TaskItem.tsx
- [X] T074 [US4] Implement edit modal state in app/dashboard/page.tsx (editingTask, setEditingTask)
- [X] T075 [US4] Create edit modal in app/dashboard/page.tsx reusing TaskForm with initialData

**Story Completion**: User Story 4 complete when users can edit tasks with optimistic updates and validation.

---

## Phase 7: User Story 5 - Toggle Task Completion (P3)

**Story Goal**: Authenticated users can mark tasks as complete/incomplete with optimistic updates.

**Independent Test Criteria**:
- ✅ Can toggle task completion (check/uncheck)
- ✅ Visual state changes immediately (strikethrough, checkmark)
- ✅ Optimistic update shows new state instantly
- ✅ Error handling reverts state on failure
- ✅ Change persists after page refresh

**Tasks**:

### Task API Functions

- [X] T076 [US5] Add toggleTaskComplete(userId, taskId) function to lib/api/tasks.ts using apiClient

### Task State Management

- [X] T077 [US5] Implement toggleComplete(id) function in lib/hooks/useTasks.ts with optimistic update
- [X] T078 [US5] Implement rollback logic in lib/hooks/useTasks.ts for failed toggleTaskComplete API calls

### Task Item Integration

- [X] T079 [US5] Add checkbox onChange handler to components/tasks/TaskItem.tsx calling toggleComplete
- [X] T080 [US5] Add toast notifications for toggle success/error in components/tasks/TaskItem.tsx

**Story Completion**: User Story 5 complete when users can toggle task completion with optimistic updates.

---

## Phase 8: User Story 6 - Delete Task (P4)

**Story Goal**: Authenticated users can delete tasks with confirmation and optimistic updates.

**Independent Test Criteria**:
- ✅ Can delete task with confirmation
- ✅ Task removed immediately from UI (optimistic update)
- ✅ Cancel preserves task
- ✅ Error handling restores task on failure
- ✅ Loading state shows during deletion

**Tasks**:

### Task API Functions

- [X] T081 [US6] Add deleteTask(userId, taskId) function to lib/api/tasks.ts using apiClient

### Task State Management

- [X] T082 [US6] Implement removeTask(id) function in lib/hooks/useTasks.ts with optimistic update
- [X] T083 [US6] Implement rollback logic in lib/hooks/useTasks.ts for failed deleteTask API calls

### Delete Confirmation Modal

- [X] T084 [US6] Create components/tasks/DeleteConfirmModal.tsx with task title, Cancel and Delete buttons
- [X] T085 [US6] Implement loading state in components/tasks/DeleteConfirmModal.tsx during deletion
- [X] T086 [US6] Add delete button to components/tasks/TaskItem.tsx
- [X] T087 [US6] Implement delete modal state in app/dashboard/page.tsx (deletingTask, setDeletingTask)
- [X] T088 [US6] Create delete confirmation modal in app/dashboard/page.tsx

**Story Completion**: User Story 6 complete when users can delete tasks with confirmation and optimistic updates.

---

## Phase 9: User Story 7 - User Logout (P4)

**Story Goal**: Authenticated users can log out, clearing session and redirecting to login.

**Independent Test Criteria**:
- ✅ Logout clears auth state and redirects to login
- ✅ Token removed from localStorage
- ✅ Cannot access protected routes after logout
- ✅ Back button doesn't access protected content
- ✅ Can login again with new token

**Tasks**:

### Logout Implementation

- [X] T089 [US7] Implement logout() function in contexts/AuthContext.tsx (clear token, clear user, redirect)
- [X] T090 [US7] Add logout button to app/dashboard/page.tsx header
- [X] T091 [US7] Implement logout handler in app/dashboard/page.tsx calling useAuth().logout()
- [X] T092 [US7] Add toast notification for successful logout

**Story Completion**: User Story 7 complete when users can logout and session is properly cleared.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Goal**: Implement responsive design, error handling, performance optimizations, and final polish.

**Tasks**:

### Responsive Design

- [X] T093 [P] Implement mobile styles (320px-767px) in all components: single column, full-width, 44px+ tap targets
- [X] T094 [P] Implement tablet styles (768px-1023px) in all components: 2-column grid, 80% modal width
- [X] T095 [P] Implement desktop styles (1024px+) in all components: 3-column grid, max-w-7xl container, hover states

### Loading States

- [X] T096 [P] Create skeleton loaders for task list in components/tasks/TaskList.tsx (3-6 cards, pulse animation)
- [X] T097 [P] Implement button loading states in components/ui/Button.tsx (spinner, disabled, stable width)

### Error Handling

- [X] T098 [P] Implement global error handling for network errors in lib/api/client.ts
- [X] T099 [P] Add inline validation error display to all forms
- [X] T100 [P] Implement 403 error handling in lib/api/client.ts (access denied message)
- [X] T101 [P] Implement 404 error handling in lib/api/client.ts (not found message)

### Performance Optimization

- [X] T102 [P] Add React.memo to components/tasks/TaskItem.tsx to prevent unnecessary re-renders
- [X] T103 [P] Optimize useTasks hook dependencies in lib/hooks/useTasks.ts

### Landing Page (Optional)

- [X] T104 [P] Create app/page.tsx with app name, tagline, CTAs (Get Started, Login)
- [X] T105 [P] Implement auto-redirect in app/page.tsx if user is authenticated

**Phase Completion**: All polish tasks complete, application fully responsive and optimized.

---

## Dependencies & Execution Order

### User Story Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3)
                                                ↓
                                          Phase 6 (US4)
                                                ↓
                                          Phase 7 (US5)
                                                ↓
                                          Phase 8 (US6)
                                                ↓
                                          Phase 9 (US7)
                                                ↓
                                          Phase 10 (Polish)
```

**Critical Path**:
1. Setup (Phase 1) - MUST complete first
2. Foundational (Phase 2) - MUST complete before user stories
3. US1 (Phase 3) - MUST complete before US2 (authentication required)
4. US2 (Phase 4) - MUST complete before US3 (need task list to show new tasks)
5. US3 (Phase 5) - MUST complete before US4-US6 (need tasks to edit/toggle/delete)
6. US4-US7 (Phases 6-9) - Can be done in any order after US3
7. Polish (Phase 10) - Can be done in parallel with US4-US7 or after

### Parallel Execution Opportunities

**Phase 2 (Foundational)**: All tasks marked [P] can run in parallel (T009-T016)

**Phase 10 (Polish)**: All tasks marked [P] can run in parallel (T093-T105)

**Within User Stories**: Tasks affecting different files can run in parallel if marked [P]

---

## Task Summary

| Phase | User Story | Priority | Task Count | Parallel Tasks |
|-------|------------|----------|------------|----------------|
| 1 | Setup | - | 8 | 0 |
| 2 | Foundational | - | 8 | 8 |
| 3 | US1: Authentication | P1 🎯 | 19 | 0 |
| 4 | US2: View Tasks | P2 🎯 | 19 | 0 |
| 5 | US3: Add Tasks | P2 🎯 | 13 | 0 |
| 6 | US4: Edit Tasks | P3 | 8 | 0 |
| 7 | US5: Toggle Completion | P3 | 5 | 0 |
| 8 | US6: Delete Tasks | P4 | 8 | 0 |
| 9 | US7: Logout | P4 | 4 | 0 |
| 10 | Polish | - | 13 | 13 |
| **Total** | | | **105** | **21** |

---

## MVP Scope (Recommended First Delivery)

**Phases 1-5** (US1-US3): 67 tasks
- Setup & Foundational: 16 tasks
- Authentication (US1): 19 tasks
- View Tasks (US2): 19 tasks
- Add Tasks (US3): 13 tasks

**Estimated Time**: 2-3 days

**Deliverable**: Users can sign up, sign in, view tasks, and add new tasks. This is a complete, independently testable increment.

---

## Validation Checklist

After completing all tasks, verify:

- [ ] All 105 tasks marked as complete [X]
- [ ] All 7 user stories independently testable
- [ ] Manual testing checklist from quickstart.md completed
- [ ] No console errors or warnings
- [ ] TypeScript compilation successful with no errors
- [ ] ESLint passes with no warnings
- [ ] All environment variables configured
- [ ] Application runs on localhost:3000
- [ ] Backend API accessible at localhost:8001
- [ ] Responsive design works on 320px, 768px, 1024px+ screens
- [ ] All authentication flows work end-to-end
- [ ] All task operations work with optimistic updates
- [ ] Error handling works for network errors and API errors
- [ ] Loading states display correctly
- [ ] Toast notifications appear for all user actions

---

## Notes

- **Tests Deferred**: Per specification, automated tests are deferred to a later phase. Manual testing checklist provided in quickstart.md.
- **Backend Dependency**: Ensure FastAPI backend from spec 001-fastapi-todo-api is running at http://localhost:8001.
- **Better Auth**: May require custom integration for Next.js App Router. Allocate extra time if needed.
- **Optimistic Updates**: All task operations (create, update, delete, toggle) use optimistic updates with rollback on error.
- **Responsive Design**: Tailwind CSS breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1536px).
- **Type Safety**: 100% TypeScript with strict mode, no `any` types without justification.

---

**Tasks Generated**: 2026-01-10
**Ready for Implementation**: Yes
**Next Step**: Run `/sp.implement` to begin execution
