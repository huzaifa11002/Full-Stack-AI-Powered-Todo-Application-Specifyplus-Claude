# Quick Start Guide

**Feature**: Next.js Authenticated Todo Frontend
**Branch**: `002-nextjs-auth-frontend`
**Date**: 2026-01-10

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 9.0.0 or higher (comes with Node.js)
  - Alternative: yarn 1.22+ or pnpm 8.0+
- **Git**: For version control
- **Code Editor**: VS Code recommended (with ESLint and Prettier extensions)

**Backend Requirement**: The FastAPI backend from specification `001-fastapi-todo-api` must be running and accessible at `http://localhost:8001`.

---

## Installation

### Step 1: Initialize Next.js Project

```bash
# Navigate to the repository root
cd /path/to/todo-app

# Create Next.js application in frontend directory
npx create-next-app@latest frontend

# When prompted, select the following options:
# ✔ Would you like to use TypeScript? … Yes
# ✔ Would you like to use ESLint? … Yes
# ✔ Would you like to use Tailwind CSS? … Yes
# ✔ Would you like to use `src/` directory? … No
# ✔ Would you like to use App Router? (recommended) … Yes
# ✔ Would you like to customize the default import alias (@/*)? … No
```

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Dependencies

```bash
# Install required packages
npm install better-auth axios react-hot-toast

# Install development dependencies (optional but recommended)
npm install -D @types/node @types/react @types/react-dom
```

**Installed Packages**:
- `better-auth`: Authentication library for JWT handling
- `axios`: HTTP client for API requests
- `react-hot-toast`: Toast notifications for user feedback

### Step 4: Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# Create .env.local file
touch .env.local
```

Add the following environment variables:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8001

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production
BETTER_AUTH_URL=http://localhost:3000
```

**Important**:
- Never commit `.env.local` to version control
- Change `BETTER_AUTH_SECRET` to a secure random string in production
- Ensure the backend API is running at the specified URL

### Step 5: Create Project Structure

Create the required directory structure:

```bash
# Create directories
mkdir -p app/login app/signup app/dashboard app/api/auth
mkdir -p components/auth components/tasks components/ui
mkdir -p lib/api lib/hooks
mkdir -p types
mkdir -p contexts

# Verify structure
tree -L 2 -d
```

Expected structure:
```
frontend/
├── app/
│   ├── api/
│   ├── dashboard/
│   ├── login/
│   └── signup/
├── components/
│   ├── auth/
│   ├── tasks/
│   └── ui/
├── contexts/
├── lib/
│   ├── api/
│   └── hooks/
└── types/
```

---

## Development

### Start Development Server

```bash
# Start Next.js development server
npm run dev
```

The application will be available at: **http://localhost:3000**

**Expected Output**:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- event compiled client and server successfully in 2.5s
```

### Verify Backend Connection

Before testing the frontend, ensure the FastAPI backend is running:

```bash
# In a separate terminal, check backend health
curl http://localhost:8001/health

# Expected response:
# {"status":"healthy"}
```

---

## Testing

### Manual Testing Checklist

Since automated tests are deferred to a later phase, use this manual testing checklist:

#### Authentication Flow
- [ ] Navigate to http://localhost:3000
- [ ] Click "Sign Up" or navigate to /signup
- [ ] Create account with valid email and password
- [ ] Verify redirect to /dashboard after signup
- [ ] Click "Logout"
- [ ] Verify redirect to /login
- [ ] Login with created credentials
- [ ] Verify redirect to /dashboard
- [ ] Refresh page, verify still authenticated
- [ ] Try accessing /dashboard in incognito mode, verify redirect to /login

#### Task Operations
- [ ] Create task with title only
- [ ] Create task with title and description
- [ ] Verify tasks appear in list immediately (optimistic update)
- [ ] Toggle task completion (check/uncheck)
- [ ] Edit task title
- [ ] Edit task description
- [ ] Delete task with confirmation
- [ ] Verify empty state when no tasks exist

#### Responsive Design
- [ ] Test on mobile (320px width)
- [ ] Test on tablet (768px width)
- [ ] Test on desktop (1024px+ width)
- [ ] Verify touch targets are 44px+ on mobile
- [ ] Verify text is readable without zooming

#### Error Handling
- [ ] Submit empty task title, verify validation error
- [ ] Stop backend, try creating task, verify error message
- [ ] Try accessing /dashboard without authentication
- [ ] Submit login with wrong password, verify error

---

## Project Structure Reference

```
frontend/
├── app/
│   ├── layout.tsx                    # Root layout with AuthProvider, Toaster
│   ├── page.tsx                      # Landing page (redirects to dashboard)
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
│       ├── Button.tsx                # Reusable button component
│       ├── Input.tsx                 # Reusable input component
│       ├── Modal.tsx                 # Reusable modal component
│       └── LoadingSpinner.tsx        # Reusable spinner component
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

---

## Common Issues & Troubleshooting

### Issue 1: "Cannot connect to backend API"

**Symptoms**: Network errors, 404 responses, CORS errors

**Solutions**:
1. Verify backend is running: `curl http://localhost:8001/health`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Ensure backend CORS is configured to allow `http://localhost:3000`
4. Restart both frontend and backend servers

### Issue 2: "Module not found" errors

**Symptoms**: Import errors, TypeScript errors

**Solutions**:
1. Verify all dependencies installed: `npm install`
2. Check file paths match project structure
3. Restart TypeScript server in VS Code: `Cmd+Shift+P` → "TypeScript: Restart TS Server"
4. Clear Next.js cache: `rm -rf .next` and restart dev server

### Issue 3: "Authentication not persisting"

**Symptoms**: User logged out after page refresh

**Solutions**:
1. Check browser localStorage for `token` key
2. Verify AuthContext is loading token from localStorage on mount
3. Check browser console for errors
4. Clear localStorage and try logging in again

### Issue 4: "Tailwind styles not applying"

**Symptoms**: Components have no styling

**Solutions**:
1. Verify `tailwind.config.js` exists and is configured
2. Check `globals.css` imports Tailwind directives
3. Restart dev server
4. Clear browser cache

### Issue 5: "Better Auth errors"

**Symptoms**: Authentication fails, JWT errors

**Solutions**:
1. Verify `BETTER_AUTH_SECRET` is set in `.env.local`
2. Check Better Auth API route is configured at `/api/auth/[...all]`
3. Ensure backend Better Auth is configured correctly
4. Check browser console and terminal for error messages

---

## Development Workflow

### Recommended Development Order

1. **Phase 2-3**: Set up Better Auth client and API routes
2. **Phase 4**: Implement AuthContext and useAuth hook
3. **Phase 5**: Add route protection middleware
4. **Phase 6-7**: Build authentication UI (login, signup)
5. **Phase 8-9**: Set up API client and task API functions
6. **Phase 10**: Create dashboard layout
7. **Phase 11-17**: Build task components (form, list, item, modals)
8. **Phase 18**: Add reusable UI components
9. **Phase 19**: Integrate toast notifications
10. **Phase 20-22**: Implement responsive design, loading states, error handling
11. **Phase 23-26**: Add TypeScript types, optimizations, logout, landing page

### Git Workflow

```bash
# Ensure you're on the feature branch
git checkout 002-nextjs-auth-frontend

# Commit frequently with descriptive messages
git add .
git commit -m "feat: implement authentication context and useAuth hook"

# Push to remote
git push origin 002-nextjs-auth-frontend
```

---

## Useful Commands

```bash
# Development
npm run dev              # Start development server
npm run build            # Build for production
npm run start            # Start production server
npm run lint             # Run ESLint
npm run lint:fix         # Fix ESLint errors

# Type Checking
npx tsc --noEmit         # Check TypeScript types without building

# Dependency Management
npm install <package>    # Install new package
npm update               # Update dependencies
npm outdated             # Check for outdated packages

# Cleanup
rm -rf .next             # Clear Next.js cache
rm -rf node_modules      # Remove dependencies
npm install              # Reinstall dependencies
```

---

## Next Steps

After completing the setup:

1. **Review Documentation**:
   - Read `plan.md` for implementation phases
   - Review `research.md` for technology decisions
   - Study `data-model.md` for entity definitions

2. **Start Implementation**:
   - Follow phases 2-26 in `plan.md`
   - Refer to `contracts/` for TypeScript types
   - Test frequently using the manual testing checklist

3. **Get Help**:
   - Check backend API documentation at `http://localhost:8001/docs`
   - Review Next.js documentation: https://nextjs.org/docs
   - Check Better Auth documentation: https://better-auth.com/docs

---

## Additional Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **React Documentation**: https://react.dev
- **Tailwind CSS Documentation**: https://tailwindcss.com/docs
- **Better Auth Documentation**: https://better-auth.com/docs
- **Axios Documentation**: https://axios-http.com/docs/intro
- **TypeScript Documentation**: https://www.typescriptlang.org/docs

---

**Setup Complete**: You're ready to start implementing the Next.js authenticated todo frontend!
