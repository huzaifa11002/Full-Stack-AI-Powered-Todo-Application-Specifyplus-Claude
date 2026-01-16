# Quickstart Guide: OpenAI ChatKit Frontend

**Feature**: 002-chatkit-frontend
**Date**: 2026-01-14
**Audience**: Frontend developers

## Overview

This guide provides step-by-step instructions for setting up and running the OpenAI ChatKit frontend for AI task management. The chat interface integrates with the existing FastAPI backend to enable natural language task management.

---

## Prerequisites

### Required Software

- **Node.js**: 18.0.0 or higher
- **npm**: 9.0.0 or higher (or yarn 1.22.0+)
- **Git**: For version control
- **Code Editor**: VS Code recommended (with TypeScript and Tailwind CSS extensions)

### Required Knowledge

- React 18+ and Next.js 16 App Router
- TypeScript basics
- Tailwind CSS
- REST API integration
- JWT authentication concepts

### Backend Requirements

- Backend API must be running (feature 001-mcp-ai-chat)
- Backend endpoint: `POST /api/{user_id}/chat`
- Better Auth authentication configured
- OpenAI API key configured in backend

---

## Installation

### 1. Clone Repository

```bash
# If not already cloned
git clone <repository-url>
cd todo-app

# Switch to feature branch
git checkout 002-chatkit-frontend
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install

# Install new dependencies for chat feature
npm install @openai/chatkit date-fns
```

### 3. Verify Installation

```bash
# Check Node.js version
node --version  # Should be 18.0.0 or higher

# Check npm version
npm --version   # Should be 9.0.0 or higher

# Verify dependencies installed
npm list @openai/chatkit date-fns
```

---

## Configuration

### Environment Variables

The frontend uses environment variables for configuration. These should already be set up from previous features.

**File**: `frontend/.env.local`

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration (already configured)
NEXT_PUBLIC_AUTH_URL=http://localhost:3000/api/auth
```

**Note**: No additional environment variables needed for chat feature. Backend handles OpenAI API key.

### TypeScript Configuration

Verify TypeScript is configured correctly:

**File**: `frontend/tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    // ... other options
  }
}
```

### Tailwind CSS Configuration

Verify Tailwind CSS is configured:

**File**: `frontend/tailwind.config.js`

```javascript
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  // ... other config
};
```

---

## Development Workflow

### 1. Start Backend Server

**Terminal 1** (Backend):
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Verify backend is running:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 2. Start Frontend Development Server

**Terminal 2** (Frontend):
```bash
cd frontend
npm run dev
```

Frontend will start on `http://localhost:3000`

### 3. Access Chat Interface

1. Open browser: `http://localhost:3000`
2. Login with test credentials (if not already logged in)
3. Navigate to chat interface: `http://localhost:3000/chat`

---

## Project Structure

### New Files Created

```
frontend/
├── app/
│   └── chat/
│       └── page.tsx                    # Chat page route
│
├── components/
│   └── chat/
│       ├── ChatInterface.tsx           # Main chat container
│       ├── ChatMessage.tsx             # Message display
│       ├── ChatInput.tsx               # Message input
│       ├── ToolCallDisplay.tsx         # Tool call visualization
│       ├── ConversationList.tsx        # Conversation sidebar (optional)
│       ├── EmptyChat.tsx               # Empty state
│       └── TypingIndicator.tsx         # Loading indicator
│
├── lib/
│   ├── api/
│   │   └── chat.ts                     # Chat API client
│   └── hooks/
│       ├── useChat.ts                  # Chat state management
│       └── useConversations.ts         # Conversation list (optional)
│
└── types/
    └── chat.ts                         # TypeScript interfaces
```

### Modified Files

```
frontend/
├── app/
│   └── layout.tsx                      # Added chat navigation
│
└── components/
    └── layout/
        └── Navigation.tsx              # Added chat link
```

---

## Testing the Chat Interface

### Manual Testing Checklist

**1. Basic Chat Flow**:
- [ ] Navigate to `/chat`
- [ ] See empty state with suggestions
- [ ] Click a suggestion or type a message
- [ ] Press Enter to send
- [ ] See loading indicator
- [ ] Receive AI response
- [ ] See tool call visualization (if applicable)

**2. Message Sending**:
- [ ] Type "Add a task to buy groceries"
- [ ] Press Enter (message sends)
- [ ] Try Shift+Enter (creates new line)
- [ ] Click Send button (message sends)
- [ ] Verify message appears in chat
- [ ] Verify AI response appears

**3. Tool Call Visualization**:
- [ ] Send "Add a task to buy groceries"
- [ ] Verify tool call section appears
- [ ] See "Added Task" label with ➕ icon
- [ ] See task title in result

**4. Conversation Persistence**:
- [ ] Send multiple messages
- [ ] Refresh page (F5)
- [ ] Verify conversation history loads
- [ ] Continue conversation

**5. New Conversation**:
- [ ] Click "New Chat" button
- [ ] Verify messages clear
- [ ] Send new message
- [ ] Verify new conversation created

**6. Navigation**:
- [ ] Switch to "List View" (todo list)
- [ ] Switch back to "Chat View"
- [ ] Verify conversation preserved

**7. Responsive Design**:
- [ ] Resize browser to mobile width (375px)
- [ ] Verify layout adapts
- [ ] Verify input area accessible
- [ ] Test on tablet width (768px)
- [ ] Test on desktop width (1280px)

**8. Error Handling**:
- [ ] Stop backend server
- [ ] Try sending message
- [ ] Verify error message displays
- [ ] Restart backend
- [ ] Retry sending message
- [ ] Verify success

### Example Test Messages

**Task Creation**:
- "Add a task to buy groceries"
- "Create a task to call mom"
- "I need to finish the report"

**Task Querying**:
- "Show me my tasks"
- "What tasks do I have?"
- "List all pending tasks"

**Task Completion**:
- "Mark task 1 as complete"
- "Complete the grocery task"
- "I finished task 3"

**Task Modification**:
- "Update task 2 title to 'Buy groceries and cook dinner'"
- "Change the description of task 1"

**Task Deletion**:
- "Delete task 5"
- "Remove the meeting task"

---

## Running Tests

### Component Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Test Coverage Goals

- Component tests: 60% coverage minimum
- Critical paths: 100% coverage (ChatInterface, useChat hook)

### Example Test

```typescript
// components/chat/__tests__/ChatMessage.test.tsx
import { render, screen } from '@testing-library/react';
import ChatMessage from '../ChatMessage';

test('renders user message correctly', () => {
  const message = {
    role: 'user',
    content: 'Hello',
    created_at: new Date().toISOString(),
  };

  render(<ChatMessage message={message} />);
  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

---

## Building for Production

### 1. Build Frontend

```bash
cd frontend
npm run build
```

### 2. Verify Build

```bash
# Check build output
ls -la .next/

# Test production build locally
npm start
```

### 3. Production Checklist

- [ ] All tests passing
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Environment variables configured
- [ ] Backend API accessible
- [ ] Authentication working
- [ ] Chat interface functional

---

## Troubleshooting

### Common Issues

**Issue**: "Cannot find module '@openai/chatkit'"
```bash
# Solution: Install dependencies
cd frontend
npm install @openai/chatkit date-fns
```

**Issue**: "API request failed with 401 Unauthorized"
```bash
# Solution: Check authentication
# 1. Verify you're logged in
# 2. Check JWT token in browser DevTools (Application > Local Storage)
# 3. Try logging out and back in
```

**Issue**: "Backend API not responding"
```bash
# Solution: Verify backend is running
curl http://localhost:8000/health

# If not running, start backend:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Issue**: "Messages not persisting after refresh"
```bash
# Solution: Check localStorage
# 1. Open browser DevTools (F12)
# 2. Go to Application > Local Storage
# 3. Verify 'chatkit_conversation_id' exists
# 4. If missing, conversation ID not being saved
```

**Issue**: "Tool calls not displaying"
```bash
# Solution: Check backend response
# 1. Open browser DevTools (F12)
# 2. Go to Network tab
# 3. Send a message
# 4. Check response for 'tool_calls' array
# 5. Verify backend is invoking tools correctly
```

**Issue**: "TypeScript errors in IDE"
```bash
# Solution: Restart TypeScript server
# VS Code: Cmd/Ctrl + Shift + P > "TypeScript: Restart TS Server"
```

**Issue**: "Tailwind CSS styles not applying"
```bash
# Solution: Verify Tailwind is configured
# 1. Check tailwind.config.js includes chat components
# 2. Restart dev server
npm run dev
```

---

## Development Tips

### Hot Reload

- Frontend hot reloads automatically on file changes
- No need to restart dev server for most changes
- Restart required for:
  - Environment variable changes
  - Next.js config changes
  - New dependencies installed

### Browser DevTools

**Useful Tabs**:
- **Console**: View logs and errors
- **Network**: Inspect API requests/responses
- **Application**: Check localStorage, cookies
- **React DevTools**: Inspect component state

### Debugging

**Add console logs**:
```typescript
// In useChat hook
console.log('Sending message:', message);
console.log('API response:', response);
console.log('Current state:', state);
```

**Use React DevTools**:
- Install React DevTools browser extension
- Inspect component props and state
- Track re-renders

**Network Debugging**:
- Open Network tab in DevTools
- Filter by "Fetch/XHR"
- Inspect request/response for `/chat` endpoint

---

## Performance Optimization

### Development Mode

- Hot reload enabled
- Source maps included
- Unminified code

### Production Mode

- Code minified
- Tree-shaking applied
- Source maps optional
- Optimized bundle size

### Performance Tips

1. **Lazy Loading**: Components loaded on demand
2. **Memoization**: Use React.memo for expensive components
3. **Code Splitting**: Automatic with Next.js App Router
4. **Image Optimization**: Use Next.js Image component

---

## Next Steps

### After Setup

1. ✅ Frontend running locally
2. ✅ Chat interface accessible
3. ✅ Can send/receive messages
4. ⏭️ Run component tests
5. ⏭️ Test responsive design
6. ⏭️ Test error scenarios
7. ⏭️ Review code for improvements

### Phase 2 Enhancements

- Streaming responses (SSE)
- Collapsible tool calls
- Conversation sidebar
- Markdown rendering
- Message search
- Conversation export

---

## Additional Resources

### Documentation

- **Next.js**: https://nextjs.org/docs
- **React**: https://react.dev
- **TypeScript**: https://www.typescriptlang.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **date-fns**: https://date-fns.org/docs

### Project Documentation

- **Feature Spec**: `specs/002-chatkit-frontend/spec.md`
- **Implementation Plan**: `specs/002-chatkit-frontend/plan.md`
- **Data Model**: `specs/002-chatkit-frontend/data-model.md`
- **API Contracts**: `specs/002-chatkit-frontend/contracts/`

### Getting Help

- Check troubleshooting section above
- Review error messages in console
- Inspect network requests in DevTools
- Check backend logs for API errors

---

## Summary

**Setup Time**: ~15 minutes
**Prerequisites**: Node.js 18+, Backend running
**Key Commands**:
- `npm install` - Install dependencies
- `npm run dev` - Start development server
- `npm test` - Run tests
- `npm run build` - Build for production

**Access Points**:
- Frontend: http://localhost:3000
- Chat Interface: http://localhost:3000/chat
- Backend API: http://localhost:8000

**Ready to Code**: Yes ✅
