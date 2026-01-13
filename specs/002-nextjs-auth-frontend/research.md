# Research & Technology Decisions

**Feature**: Next.js Authenticated Todo Frontend
**Branch**: `002-nextjs-auth-frontend`
**Date**: 2026-01-10

## Overview

This document captures all technology decisions and integration patterns researched during Phase 0 of the implementation planning process. Each decision includes the chosen approach, rationale, and alternatives considered.

---

## Decision 1: Better Auth Integration with Next.js App Router

**Context**: Need to implement authentication for the Next.js 16 App Router frontend, integrating with the FastAPI backend that uses Better Auth.

**Decision**: Use Better Auth client library with custom integration for Next.js App Router

**Rationale**:
- Better Auth provides JWT authentication out of the box
- Reduces implementation time compared to custom JWT handling
- Provides session management and token refresh capabilities
- Official library with community support

**Alternatives Considered**:
1. **Custom JWT Implementation**
   - Pros: Full control, no external dependencies
   - Cons: Reinventing the wheel, more code to maintain, potential security issues
   - Rejected: Unnecessary complexity when Better Auth exists

2. **NextAuth.js**
   - Pros: Popular, well-documented, Next.js-specific
   - Cons: Spec requires Better Auth, would need backend changes
   - Rejected: Spec explicitly requires Better Auth

**Implementation Notes**:
- Better Auth client will be configured in `lib/auth.ts`
- API route handler at `app/api/auth/[...all]/route.ts` for Better Auth operations
- May require custom integration code for App Router compatibility
- Token storage handled separately (see Decision 2)

**References**:
- Better Auth documentation: https://better-auth.com/docs
- Next.js App Router authentication patterns

---

## Decision 2: JWT Token Storage Strategy

**Context**: Need to store JWT tokens on the client side for authenticated API requests. Must balance security, persistence, and implementation complexity.

**Decision**: localStorage

**Rationale**:
- **Simplicity**: Easy to implement, no server-side configuration needed
- **Persistence**: Tokens persist across browser sessions (user stays logged in)
- **Spec Alignment**: Matches the explicit decision in the feature specification
- **Development Speed**: Faster implementation for 4-5 day timeline

**Alternatives Considered**:
1. **httpOnly Cookies**
   - Pros: More secure (not accessible via JavaScript), automatic CSRF protection
   - Cons: Requires server-side configuration, more complex implementation, CORS complications
   - Rejected: Complexity outweighs security benefit for this phase

2. **sessionStorage**
   - Pros: Cleared when browser closes, slightly more secure
   - Cons: No persistence (user must re-login every session), poor UX
   - Rejected: Poor user experience

**Security Considerations**:
- **XSS Vulnerability**: localStorage is vulnerable to XSS attacks
- **Mitigation**: Input sanitization, Content Security Policy headers, no eval() usage
- **Acknowledged Tradeoff**: Security vs. simplicity tradeoff documented and accepted per spec

**Implementation Notes**:
- Token stored in localStorage with key `token`
- Token retrieved on app initialization to restore session
- Token cleared on logout
- Token automatically included in API requests via Axios interceptor

---

## Decision 3: State Management Approach

**Context**: Need to manage global state for authentication (user, token, isAuthenticated) and task data (tasks list, loading states).

**Decision**: React Context API

**Rationale**:
- **Built-in**: No additional dependencies, part of React core
- **Sufficient Scope**: App has limited global state needs (auth + tasks)
- **Simple**: Easy to understand and maintain
- **Performance**: Adequate for this app size (single dashboard, limited components)

**Alternatives Considered**:
1. **Zustand**
   - Pros: Lightweight (1KB), simpler API than Redux, good performance
   - Cons: Additional dependency, unnecessary for this scope
   - Rejected: Overkill for current needs, can migrate later if needed

2. **Redux Toolkit**
   - Pros: Powerful, excellent DevTools, industry standard
   - Cons: Boilerplate, learning curve, overkill for small app
   - Rejected: Too complex for this scope

3. **Jotai/Recoil**
   - Pros: Atomic state management, fine-grained updates
   - Cons: Additional dependencies, learning curve
   - Rejected: Unnecessary complexity

**Implementation Notes**:
- `AuthContext` for authentication state (user, token, isAuthenticated, isLoading)
- `useTasks` custom hook for task state (can use Context if needed, or local state)
- Context providers wrapped in `app/layout.tsx`
- Custom hooks (`useAuth`, `useTasks`) for consuming context

**Migration Path**:
- If Context becomes unwieldy, can migrate to Zustand with minimal refactoring
- Hooks abstraction makes state management implementation swappable

---

## Decision 4: Task Form Mode

**Context**: Need to decide how users create new tasks - inline form, modal overlay, or separate page.

**Decision**: Modal

**Rationale**:
- **Clean UI**: Keeps dashboard uncluttered when not creating tasks
- **Focused Interaction**: Modal provides clear focus on task creation
- **Consistency**: Matches edit flow (also modal), consistent UX
- **Mobile-Friendly**: Full-screen modal on mobile provides good experience

**Alternatives Considered**:
1. **Inline Form**
   - Pros: Always visible, no modal interaction needed
   - Cons: Clutters dashboard, takes up space even when not used
   - Rejected: Poor UX when not actively creating tasks

2. **Separate Page**
   - Pros: Maximum space for form, clear navigation
   - Cons: Extra navigation step, breaks flow, overkill for simple form
   - Rejected: Unnecessary navigation overhead

**Implementation Notes**:
- Modal triggered by "Add Task" button
- Modal component reusable for both create and edit
- ESC key and backdrop click to close
- Form validation before submission
- Loading state during API call

---

## Decision 5: Task Edit Mode

**Context**: Need to decide how users edit existing tasks - inline editing, modal, or separate page.

**Decision**: Modal

**Rationale**:
- **Consistency**: Matches create flow, users learn one interaction pattern
- **Component Reuse**: Same `TaskForm` component used for create and edit
- **Clear Focus**: Modal provides focused editing experience
- **Prevents Accidental Edits**: Explicit edit action required

**Alternatives Considered**:
1. **Inline Editing**
   - Pros: Quick edits, no modal interaction
   - Cons: Complex implementation, accidental edits, state management complexity
   - Rejected: Implementation complexity outweighs benefits

2. **Separate Page**
   - Pros: Maximum space, clear navigation
   - Cons: Extra navigation, breaks flow, overkill for simple edit
   - Rejected: Unnecessary navigation overhead

**Implementation Notes**:
- Edit button on each task card
- Modal opens with pre-filled form data
- Same `TaskForm` component with `initialData` prop
- Button text changes to "Update Task"
- Optimistic update on save

---

## Decision 6: Task Sorting Strategy

**Context**: Need to decide how to order tasks in the list - by completion status, creation date, or user preference.

**Decision**: Incomplete tasks first, then completed tasks

**Rationale**:
- **Todo App Best Practice**: Prioritizes active tasks that need attention
- **User Intent**: Users primarily care about incomplete tasks
- **Simple Implementation**: No complex sorting logic or user preferences
- **Clear Visual Separation**: Incomplete and completed tasks naturally grouped

**Alternatives Considered**:
1. **Newest First (Chronological)**
   - Pros: Simple, predictable, shows recent activity
   - Cons: Completed tasks mixed with incomplete, harder to find active tasks
   - Rejected: Poor UX for todo app use case

2. **Custom Sort (User-Defined)**
   - Pros: Maximum flexibility, user control
   - Cons: Complex implementation, UI for sorting controls, state persistence
   - Rejected: Out of scope, unnecessary complexity

3. **Alphabetical**
   - Pros: Predictable ordering
   - Cons: Doesn't prioritize by importance or status
   - Rejected: Not useful for todo app

**Implementation Notes**:
- Sorting logic in `TaskList` component
- Array.sort() with custom comparator: `(a, b) => a.is_completed - b.is_completed`
- No user controls needed
- Can add sorting options in future if needed

---

## Decision 7: Mobile Navigation Pattern

**Context**: Need to decide navigation pattern for mobile devices - bottom nav, hamburger menu, or top nav.

**Decision**: Top navigation with logout button

**Rationale**:
- **Simple SPA**: Single-page app with minimal navigation needs
- **Consistent**: Same navigation across all screen sizes
- **Always Visible**: Logout always accessible, no hidden menus
- **Minimal Overhead**: No complex navigation state management

**Alternatives Considered**:
1. **Bottom Navigation**
   - Pros: Thumb-friendly on mobile, modern pattern
   - Cons: Unnecessary for single-page app, takes up screen space
   - Rejected: Overkill for minimal navigation needs

2. **Hamburger Menu**
   - Pros: Space-saving, hides navigation when not needed
   - Cons: Hidden navigation, extra tap to access, unnecessary for simple app
   - Rejected: Adds complexity without benefit

**Implementation Notes**:
- Header component with logo, user email, and logout button
- Sticky header on mobile for always-accessible logout
- Responsive padding and sizing
- Logout button styled as secondary button

---

## Decision 8: HTTP Client Library

**Context**: Need to make HTTP requests to the FastAPI backend with JWT authentication.

**Decision**: Axios

**Rationale**:
- **Interceptors**: Built-in request/response interceptors for JWT injection and error handling
- **Automatic JSON**: Automatic JSON parsing and serialization
- **Error Handling**: Better error handling than fetch
- **Familiar API**: Widely used, team likely familiar

**Alternatives Considered**:
1. **Fetch API**
   - Pros: Built-in, no dependencies, modern browsers support
   - Cons: Manual interceptor implementation, more boilerplate, less ergonomic
   - Rejected: More work to implement interceptors

2. **SWR/React Query**
   - Pros: Caching, automatic refetching, optimistic updates
   - Cons: Additional dependency, learning curve, may be overkill
   - Rejected: Can add later if caching becomes important

**Implementation Notes**:
- Axios instance created in `lib/api/client.ts`
- Base URL from environment variable
- Request interceptor adds `Authorization: Bearer ${token}` header
- Response interceptor handles 401 (logout), 403 (error), network errors
- All API functions use this configured client

---

## Decision 9: Form Validation Approach

**Context**: Need to validate user input in forms (login, signup, task creation/editing).

**Decision**: Manual validation with controlled components

**Rationale**:
- **Spec Requirement**: Spec explicitly requires controlled components with manual validation
- **Simple Forms**: Forms are simple (2-3 fields), don't need complex validation library
- **Full Control**: Complete control over validation logic and error messages
- **No Dependencies**: Reduces bundle size

**Alternatives Considered**:
1. **React Hook Form**
   - Pros: Less boilerplate, built-in validation, performance optimized
   - Cons: Additional dependency, spec requires manual validation
   - Rejected: Spec explicitly excludes form libraries

2. **Formik**
   - Pros: Popular, comprehensive, good for complex forms
   - Cons: Additional dependency, overkill for simple forms, spec excludes it
   - Rejected: Spec explicitly excludes form libraries

**Implementation Notes**:
- Controlled inputs with `value` and `onChange`
- Validation functions for each form
- Error state object: `{ fieldName: errorMessage }`
- Real-time validation on blur or submit
- Display errors inline below inputs

---

## Decision 10: UI Component Library

**Context**: Need UI components (buttons, inputs, modals) for the application.

**Decision**: Custom components with Tailwind CSS

**Rationale**:
- **Spec Requirement**: Spec explicitly requires custom components, no external libraries
- **Tailwind CSS**: Spec requires Tailwind CSS exclusively for styling
- **Full Control**: Complete control over styling and behavior
- **Learning**: Good practice for building reusable components

**Alternatives Considered**:
1. **Material-UI (MUI)**
   - Pros: Comprehensive, accessible, well-tested
   - Cons: Large bundle, spec excludes it, opinionated styling
   - Rejected: Spec explicitly excludes component libraries

2. **Chakra UI**
   - Pros: Accessible, composable, good DX
   - Cons: Spec excludes it, additional dependency
   - Rejected: Spec explicitly excludes component libraries

3. **shadcn/ui**
   - Pros: Copy-paste components, Tailwind-based, customizable
   - Cons: Still an external library, spec excludes it
   - Rejected: Spec explicitly excludes component libraries

**Implementation Notes**:
- Build reusable components: Button, Input, Modal, LoadingSpinner
- Use Tailwind CSS for all styling
- Variants via props (e.g., `variant="primary"`)
- Consistent design system (colors, spacing, typography)
- Accessibility considerations (ARIA labels, keyboard navigation)

---

## Summary of Decisions

| Decision | Chosen Approach | Key Rationale |
|----------|----------------|---------------|
| Authentication | Better Auth client | Spec requirement, JWT support |
| Token Storage | localStorage | Simplicity, persistence, spec decision |
| State Management | React Context API | Built-in, sufficient scope |
| Task Form Mode | Modal | Clean UI, focused interaction |
| Task Edit Mode | Modal | Consistency with create |
| Task Sorting | Incomplete first | Todo app best practice |
| Mobile Navigation | Top nav | Simple SPA, always visible |
| HTTP Client | Axios | Interceptors, ergonomic API |
| Form Validation | Manual | Spec requirement, simple forms |
| UI Components | Custom + Tailwind | Spec requirement, full control |

---

## Open Questions & Future Considerations

1. **Token Refresh**: How to handle JWT expiration during active sessions?
   - Current: Graceful logout with "Session expired" message
   - Future: Implement refresh token flow

2. **Offline Support**: What happens when user loses connection?
   - Current: Error messages, no offline mode
   - Future: Service worker, offline queue (out of scope per spec)

3. **Performance Optimization**: When to implement advanced optimizations?
   - Current: Basic optimizations (React.memo, optimistic updates)
   - Future: Code splitting, lazy loading, bundle analysis

4. **Accessibility**: What level of WCAG compliance?
   - Current: Basic WCAG 2.1 Level A (semantic HTML, keyboard nav)
   - Future: Full WCAG 2.1 Level AA compliance

5. **Testing**: When to add automated tests?
   - Current: Manual testing
   - Future: Unit tests (60% coverage), integration tests, E2E tests

---

**Phase 0 Complete**: All technology decisions documented and justified. Ready to proceed to Phase 1 (Design & Contracts).
