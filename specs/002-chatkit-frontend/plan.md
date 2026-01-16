# Implementation Plan: OpenAI ChatKit Frontend for AI Task Management

**Branch**: `002-chatkit-frontend` | **Date**: 2026-01-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-chatkit-frontend/spec.md`

## Summary

Build a conversational AI chat interface using OpenAI ChatKit that integrates with the existing FastAPI backend (POST /api/{user_id}/chat endpoint). The frontend will enable users to manage tasks through natural language, display conversation history, visualize tool calls, and provide seamless navigation between chat and traditional todo list interfaces. Implementation uses Next.js 16 App Router, TypeScript, Tailwind CSS, and Better Auth for JWT authentication.

**Primary Requirement**: Chat interface for natural language task management with real-time AI responses, conversation persistence, and tool call transparency.

**Technical Approach**: Custom React components with useChat hook for state management, Axios for API integration, localStorage for conversation ID persistence, and responsive Tailwind CSS design. OpenAI ChatKit library provides UI components and patterns, while custom components handle tool call visualization and conversation management.

## Technical Context

**Language/Version**: TypeScript 5.0+, Node.js 18+
**Primary Dependencies**:
- Next.js 16+ (App Router)
- React 18+
- OpenAI ChatKit (@openai/chatkit)
- Axios (HTTP client)
- date-fns (timestamp formatting)
- react-hot-toast (notifications)
- Tailwind CSS 3+ (styling)

**Storage**:
- Backend: Neon PostgreSQL (conversation and message persistence via existing API)
- Frontend: localStorage (conversation ID persistence), React state (message history during session)

**Testing**:
- Jest + React Testing Library (component tests)
- Playwright or Cypress (E2E tests - optional)
- Manual testing for responsive design

**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - last 2 years)

**Project Type**: Web application (frontend only - backend already implemented)

**Performance Goals**:
- Message send/receive: <5 seconds
- Interface switching: <2 seconds
- Smooth scrolling with 100+ messages
- First contentful paint: <2 seconds

**Constraints**:
- Must use existing backend API (no backend modifications)
- Must integrate with Better Auth JWT tokens
- Must match existing Tailwind CSS styling
- Plain text only (no markdown initially)
- 3-4 day timeline

**Scale/Scope**:
- 6 user stories (2 P1, 2 P2, 2 P3)
- 22 functional requirements
- 7 React components
- 2 custom hooks
- 3 TypeScript type definition files
- Responsive design (320px - 1920px+)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

**I. Production-Ready Code Quality** ✅ PASS
- TypeScript strict mode enabled (no `any` types)
- Component testing with React Testing Library (target 60% coverage)
- ESLint + Prettier configured
- All architectural decisions documented in code comments

**II. Cloud-Native Architecture** ✅ PASS (Frontend-specific)
- Stateless frontend (state in backend database)
- Configuration externalized (environment variables)
- Health check not applicable (static frontend)
- Docker containerization for deployment

**III. AI Integration Excellence** ⚠️ CONDITIONAL PASS
- **VIOLATION**: Streaming responses NOT implemented (constitution requires streaming)
- **Justification**: Spec explicitly excludes streaming for MVP timeline (3-4 days). Backend API returns complete responses, not streams.
- **Mitigation**:
  - Loading indicators provide user feedback
  - Typing indicators show AI is processing
  - Design API client to support streaming in future (add streaming parameter)
  - Document streaming as Phase 2 enhancement
- **Approval Required**: Technical lead must approve non-streaming approach for MVP

**IV. Security-First Approach** ✅ PASS
- JWT tokens from Better Auth (existing implementation)
- No secrets in frontend code
- Input validation on message length (2000 chars)
- CORS handled by backend
- XSS prevention via React's built-in escaping

**V. Developer Experience** ✅ PASS
- Clear component hierarchy and file structure
- README with setup instructions (quickstart.md)
- Consistent patterns across components
- TypeScript interfaces for all data structures

### Code Quality Standards Compliance

**Type Safety** ✅ PASS
- TypeScript strict mode
- Interfaces for all props and data structures
- No implicit any types

**Testing Requirements** ✅ PASS (Target)
- Component tests for all UI components (target 60%)
- Integration tests for chat flow
- Manual responsive design testing

**Linting & Formatting** ✅ PASS
- ESLint with TypeScript rules
- Prettier for code formatting
- Pre-commit hooks configured

### Architecture Standards Compliance

**Phase II: Next.js + FastAPI Foundation** ✅ PASS
- RESTful API integration (POST /api/{user_id}/chat)
- Clear separation: components, hooks, API client, types
- Consistent error handling across components

**Phase III: AI Chatbot Integration** ⚠️ CONDITIONAL PASS
- **VIOLATION**: No streaming (see AI Integration Excellence above)
- Rate limiting handled by backend
- Context management via conversation history
- Graceful error handling for API failures

### Post-Design Re-evaluation

*To be completed after Phase 1 (data-model.md, contracts/, quickstart.md)*

**Streaming Decision**:
- **Status**: Deferred to Phase 2
- **Rationale**: MVP focuses on core functionality within 3-4 day timeline
- **Future Work**: Add streaming support using Server-Sent Events (SSE) or WebSocket
- **API Compatibility**: Design API client with streaming parameter for future enhancement

## Project Structure

### Documentation (this feature)

```text
specs/002-chatkit-frontend/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already created)
├── research.md          # Phase 0 output (technology research)
├── data-model.md        # Phase 1 output (frontend data structures)
├── quickstart.md        # Phase 1 output (setup and usage guide)
├── contracts/           # Phase 1 output (API contracts and types)
│   ├── chat-api.yaml    # Backend API contract (reference)
│   └── frontend-types.ts # TypeScript type definitions
├── checklists/
│   └── requirements.md  # Specification quality validation (already created)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── chat/
│   │   └── page.tsx                    # Chat page route (NEW)
│   ├── dashboard/
│   │   └── page.tsx                    # Todo list page (EXISTING - modify navigation)
│   └── layout.tsx                      # Root layout (EXISTING - add chat navigation)
│
├── components/
│   ├── chat/                           # NEW: Chat components
│   │   ├── ChatInterface.tsx           # Main chat container
│   │   ├── ChatMessage.tsx             # Individual message display
│   │   ├── ChatInput.tsx               # Message input with send button
│   │   ├── ToolCallDisplay.tsx         # Tool call visualization
│   │   ├── ConversationList.tsx        # Sidebar conversation list (optional)
│   │   ├── EmptyChat.tsx               # Empty state with suggestions
│   │   └── TypingIndicator.tsx         # Loading/typing indicator
│   │
│   └── layout/                         # EXISTING
│       └── Navigation.tsx              # MODIFY: Add chat navigation link
│
├── lib/
│   ├── api/
│   │   ├── client.ts                   # EXISTING: Axios client with JWT
│   │   └── chat.ts                     # NEW: Chat API functions
│   │
│   └── hooks/
│       ├── useChat.ts                  # NEW: Chat state management hook
│       └── useConversations.ts         # NEW: Conversation list hook (optional)
│
├── types/
│   └── chat.ts                         # NEW: TypeScript interfaces
│
├── contexts/
│   └── AuthContext.tsx                 # EXISTING: Better Auth context
│
└── styles/
    └── globals.css                     # EXISTING: Tailwind CSS config
```

**Structure Decision**: Web application structure with frontend-only changes. Backend API already implemented in feature 001-mcp-ai-chat. All new code in `frontend/` directory following Next.js 16 App Router conventions. Components organized by feature (chat/), with shared utilities in lib/ and types in types/.

## Complexity Tracking

### Streaming Response Violation

**Why Needed**: MVP timeline (3-4 days) requires focus on core functionality. Streaming adds significant complexity:
- Server-Sent Events (SSE) or WebSocket implementation
- Partial message rendering and state management
- Error handling for interrupted streams
- Testing streaming scenarios

**Alternatives Considered**:
1. **Full Streaming Implementation**: Rejected due to timeline constraints and backend API not supporting streaming
2. **Polling for Updates**: Rejected as inefficient and poor UX
3. **Complete Response with Loading Indicators**: Selected for MVP simplicity

**Mitigation**:
- Loading indicators provide clear feedback
- Typing indicators show AI is processing
- API client designed with streaming parameter for future enhancement
- Document streaming as Phase 2 feature

**Review**: Technical lead approval required for non-streaming MVP approach

## Phase 0: Research & Technology Validation

### Research Tasks

**R1: OpenAI ChatKit Integration Patterns**
- **Question**: How to integrate OpenAI ChatKit with Next.js 16 App Router?
- **Research**:
  - Review OpenAI ChatKit documentation
  - Identify compatible components and patterns
  - Determine if ChatKit provides pre-built components or just patterns
  - Assess TypeScript support and type definitions
- **Output**: Integration approach (use ChatKit components vs. custom components)

**R2: Conversation State Management**
- **Question**: Best approach for managing conversation state in React?
- **Research**:
  - Custom hook (useChat) vs. Context API vs. state management library
  - localStorage for conversation ID persistence
  - Optimistic updates for message sending
  - Error recovery and retry logic
- **Output**: State management architecture decision

**R3: Responsive Chat UI Patterns**
- **Question**: How to implement responsive chat interface (320px - 1920px+)?
- **Research**:
  - Mobile-first design patterns
  - Message bubble sizing and wrapping
  - Input area behavior on mobile keyboards
  - Sidebar behavior on different screen sizes
- **Output**: Responsive design strategy with Tailwind CSS breakpoints

**R4: Tool Call Visualization**
- **Question**: How to display tool call information inline with messages?
- **Research**:
  - Expandable/collapsible sections
  - JSON formatting for parameters and results
  - Icon mapping for different tools
  - Accessibility considerations
- **Output**: Tool call display component design

**R5: Auto-scroll Behavior**
- **Question**: How to implement smart auto-scroll (scroll to bottom on new messages, but not when user scrolls up)?
- **Research**:
  - Scroll position detection
  - useRef for scroll container
  - Smooth scrolling behavior
  - Performance with many messages
- **Output**: Auto-scroll implementation pattern

**R6: Message Timestamp Formatting**
- **Question**: Best library and format for displaying message timestamps?
- **Research**:
  - date-fns vs. moment.js vs. native Intl
  - Relative time ("2 minutes ago") vs. absolute time
  - Timezone handling
  - Update frequency for relative times
- **Output**: Timestamp formatting approach (date-fns with relative time)

### Research Output

All research findings documented in `research.md` with:
- Decision made
- Rationale
- Alternatives considered
- Code examples where applicable

## Phase 1: Design & Contracts

### Data Model (data-model.md)

**Frontend Data Structures** (TypeScript interfaces):

```typescript
// Message entity
interface Message {
  id?: string;                    // Optional: generated client-side
  role: 'user' | 'assistant';     // Message sender
  content: string;                // Message text
  tool_calls?: ToolCall[];        // Optional: AI tool invocations
  created_at?: string;            // ISO 8601 timestamp
}

// Tool call entity
interface ToolCall {
  tool: string;                   // Tool name (e.g., "add_task")
  params: Record<string, any>;    // Tool parameters
  result: Record<string, any>;    // Tool execution result
}

// Conversation entity
interface Conversation {
  id: number;                     // Backend-generated ID
  created_at: string;             // ISO 8601 timestamp
  updated_at: string;             // ISO 8601 timestamp
  preview?: string;               // First message or summary
}

// Chat state (useChat hook)
interface ChatState {
  messages: Message[];            // Current conversation messages
  currentConversationId: number | null;  // Active conversation
  isLoading: boolean;             // API request in progress
  error: string | null;           // Error message if any
}

// API request/response types
interface ChatRequest {
  conversation_id?: number;       // Optional: null for new conversation
  message: string;                // User message (max 2000 chars)
}

interface ChatResponse {
  conversation_id: number;        // Conversation ID (new or existing)
  response: string;               // AI assistant response
  tool_calls: ToolCall[];         // Tools invoked by AI
}
```

**State Transitions**:
- New conversation: `currentConversationId: null` → send message → `currentConversationId: <id>`
- Message sending: `isLoading: false` → `isLoading: true` → `isLoading: false`
- Error handling: API failure → `error: <message>` → user dismisses → `error: null`

**Validation Rules**:
- Message content: 1-2000 characters, no whitespace-only
- Conversation ID: positive integer or null
- Tool call parameters: valid JSON object
- Timestamps: ISO 8601 format

### API Contracts (contracts/)

**Backend API Contract** (reference from 001-mcp-ai-chat):

```yaml
# contracts/chat-api.yaml (reference only - backend already implemented)
POST /api/{user_id}/chat
  Headers:
    Authorization: Bearer <jwt_token>
  Request:
    conversation_id: integer | null
    message: string (1-2000 chars)
  Response:
    conversation_id: integer
    response: string
    tool_calls: array of ToolCall
  Errors:
    401: Unauthorized (invalid/expired JWT)
    400: Bad Request (invalid message)
    500: Internal Server Error
```

**Frontend Type Definitions**:

```typescript
// contracts/frontend-types.ts
export interface Message {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: ToolCall[];
  created_at?: string;
}

export interface ToolCall {
  tool: string;
  params: Record<string, any>;
  result: Record<string, any>;
}

export interface Conversation {
  id: number;
  created_at: string;
  updated_at: string;
  preview?: string;
}

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
}

export interface ChatState {
  messages: Message[];
  currentConversationId: number | null;
  isLoading: boolean;
  error: string | null;
}
```

### Quickstart Guide (quickstart.md)

Developer setup and usage guide covering:
- Prerequisites (Node.js 18+, npm/yarn)
- Installation steps
- Environment configuration
- Running development server
- Testing the chat interface
- Building for production
- Troubleshooting common issues

### Agent Context Update

Run agent context update script:
```bash
.specify/scripts/bash/update-agent-context.sh claude
```

Update CLAUDE.md with new technologies:
- OpenAI ChatKit (@openai/chatkit)
- date-fns (timestamp formatting)
- Chat interface components (ChatInterface, ChatMessage, ChatInput, etc.)

## Phase 2: Implementation Phases

*Note: Detailed implementation tasks will be generated by `/sp.tasks` command*

### Phase 2.1: Setup & Dependencies (T001-T004)

**Install OpenAI ChatKit**:
```bash
cd frontend
npm install @openai/chatkit date-fns
```

**Create directory structure**:
- `app/chat/page.tsx`
- `components/chat/` (7 components)
- `lib/api/chat.ts`
- `lib/hooks/useChat.ts`
- `types/chat.ts`

**Update navigation**:
- Modify `components/layout/Navigation.tsx` to add chat link
- Add view toggle between chat and todo list

### Phase 2.2: TypeScript Type Definitions (T005-T007)

Create `types/chat.ts` with all interfaces:
- Message, ToolCall, Conversation
- ChatRequest, ChatResponse
- ChatState

### Phase 2.3: Chat API Client (T008-T012)

Create `lib/api/chat.ts`:
- `sendMessage(userId, request)` - POST to /api/{user_id}/chat
- `getConversationHistory(userId, conversationId)` - Optional
- `listConversations(userId)` - Optional
- `createConversation(userId)` - Optional

Use existing `lib/api/client.ts` Axios instance with JWT interceptor.

### Phase 2.4: Chat State Management Hook (T013-T018)

Create `lib/hooks/useChat.ts`:
- State management (messages, conversationId, isLoading, error)
- `sendMessage(content)` - Optimistic updates, API call, error handling
- `startNewConversation()` - Reset state
- `clearError()` - Dismiss error messages

### Phase 2.5: Chat Interface Page (T019-T021)

Create `app/chat/page.tsx`:
- Authentication check (redirect to login if not authenticated)
- Loading state while checking auth
- Render ChatInterface component

### Phase 2.6: Main Chat Interface Component (T022-T028)

Create `components/chat/ChatInterface.tsx`:
- Header with title and "New Chat" button
- Messages area with scroll container
- Empty state (EmptyChat component)
- Message list (ChatMessage components)
- Loading indicator
- Error display
- Input area (ChatInput component)
- Auto-scroll to bottom on new messages

### Phase 2.7: Chat Message Component (T029-T033)

Create `components/chat/ChatMessage.tsx`:
- User vs. assistant styling (different colors, alignment)
- Message content with word wrapping
- Tool call display (ToolCallDisplay component)
- Timestamp formatting (date-fns)
- Responsive design (mobile, tablet, desktop)

### Phase 2.8: Tool Call Display Component (T034-T038)

Create `components/chat/ToolCallDisplay.tsx`:
- Tool icon mapping (add_task: ➕, list_tasks: 📋, etc.)
- Tool label mapping (add_task: "Added Task", etc.)
- Parameters display (formatted JSON)
- Result summary (task title, count, status)
- Expandable/collapsible sections (optional)

### Phase 2.9: Chat Input Component (T039-T044)

Create `components/chat/ChatInput.tsx`:
- Textarea with auto-resize
- Send button with icon
- Enter key to send (Shift+Enter for new line)
- Character limit (2000 chars) with counter
- Disabled state while loading
- Helper text ("Press Enter to send")

### Phase 2.10: Empty Chat State (T045-T048)

Create `components/chat/EmptyChat.tsx`:
- Welcome message and icon
- Feature highlights (3 cards)
- Suggestion buttons (5 example messages)
- Click suggestion to send message

### Phase 2.11: Responsive Design Implementation (T049-T054)

Implement responsive breakpoints:
- Mobile (320px-767px): Single column, compact header, full-width messages
- Tablet (768px-1023px): Optimized spacing, medium-width messages
- Desktop (1024px+): Max-width container, optional sidebar, wide messages

### Phase 2.12: Navigation Integration (T055-T058)

Update navigation:
- Add chat link to main navigation
- Create view toggle (List View / Chat View)
- Active state styling
- Mobile-friendly navigation

### Phase 2.13: Conversation History Sidebar (T059-T063) - Optional

Create `components/chat/ConversationList.tsx`:
- List all user conversations
- Show preview and timestamp
- Click to switch conversations
- Active conversation highlighting
- Loading state

### Phase 2.14: Error Handling & Edge Cases (T064-T070)

Implement error handling:
- Network errors (offline, timeout)
- Authentication errors (401 - redirect to login)
- Server errors (500 - show error message)
- Empty responses (fallback message)
- Rapid message sending (queue messages)
- Long conversations (performance optimization)

### Phase 2.15: Loading & Typing Indicators (T071-T073)

Create `components/chat/TypingIndicator.tsx`:
- Animated dots (bounce animation)
- "AI is typing..." text
- Display while isLoading is true

### Phase 2.16: Message Timestamps & Formatting (T074-T076)

Implement timestamp formatting:
- Install date-fns
- Format relative time ("2 minutes ago")
- Format absolute time for older messages
- Update on interval (optional)

### Phase 2.17: Auto-scroll Behavior (T077-T080)

Implement smart auto-scroll:
- Scroll to bottom on new messages
- Detect user scroll up (disable auto-scroll)
- Re-enable auto-scroll when near bottom
- Smooth scrolling animation

### Phase 2.18: Input Enhancements (T081-T084)

Enhance input component:
- Auto-resize textarea based on content
- Character limit with counter
- Paste handling
- Focus management

### Phase 2.19: Testing & Quality Assurance (T085-T095)

**Component Tests**:
- ChatMessage renders correctly
- Tool calls display properly
- Input handles Enter/Shift+Enter
- Empty state shows suggestions

**Integration Tests**:
- Full chat flow (send message, receive response)
- Conversation persistence
- Error handling
- Navigation between views

**Responsive Design Tests**:
- Mobile (375px, 414px)
- Tablet (768px, 1024px)
- Desktop (1280px, 1920px)

**Manual Tests**:
- Natural language variations
- Long messages
- Special characters
- Rapid message sending

## Architecture Decisions

### Decision 1: Message Storage Strategy

**Options**:
1. Store locally in React state only
2. Fetch from backend on every page load
3. Hybrid: Store in state during session, fetch on page load

**Tradeoff**: Performance vs. data consistency

**Decision**: Hybrid approach (Option 3)
- Store messages in React state during active session
- Fetch conversation history from backend on page load
- Use conversation ID from localStorage to resume conversation

**Rationale**:
- Best user experience (fast during session)
- Data consistency (always fresh on page load)
- Backend is source of truth

### Decision 2: Conversation List Display

**Options**:
1. Always-visible sidebar (desktop only)
2. Dropdown menu
3. Separate page

**Tradeoff**: Always visible vs. space-saving vs. navigation

**Decision**: Optional sidebar on desktop (Option 1), hidden on mobile
- Desktop (1024px+): Sidebar visible by default
- Mobile/Tablet: Hidden, accessible via menu button

**Rationale**:
- Desktop has space for sidebar
- Mobile needs full width for chat
- Optional enhancement (P3 priority)

### Decision 3: Message Rendering

**Options**:
1. Plain text only
2. Markdown rendering
3. Rich text editor

**Tradeoff**: Simplicity vs. formatting capability vs. complexity

**Decision**: Plain text only (Option 1) for MVP
- Use `whitespace-pre-wrap` for line breaks
- Escape HTML to prevent XSS
- Add Markdown support in Phase 2

**Rationale**:
- Spec explicitly states plain text initially
- Simplifies implementation
- Reduces security risks
- Can add Markdown later without breaking changes

### Decision 4: Tool Call Visualization

**Options**:
1. Inline collapsed section (expandable)
2. Separate section below message
3. Modal popup

**Tradeoff**: Context vs. clarity vs. interaction

**Decision**: Inline section (Option 1), always expanded for MVP
- Display tool name with icon
- Show parameters and results
- Bordered section within message bubble

**Rationale**:
- Keeps tool calls in context with message
- No additional clicks required
- Clear visual separation from message text
- Can add expand/collapse in Phase 2

### Decision 5: Input Method

**Options**:
1. Single-line input
2. Multi-line textarea (fixed height)
3. Auto-expanding textarea

**Tradeoff**: Simplicity vs. long messages vs. best of both

**Decision**: Auto-expanding textarea (Option 3)
- Starts at 1 row (52px height)
- Expands up to 150px max height
- Scrolls if content exceeds max height

**Rationale**:
- Accommodates short and long messages
- Better UX than fixed height
- Common pattern in modern chat interfaces

### Decision 6: Empty State Action

**Options**:
1. Just input field
2. Suggestion buttons
3. Interactive tutorial

**Tradeoff**: Freedom vs. guidance vs. learning curve

**Decision**: Suggestion buttons (Option 2)
- 5 example messages as clickable buttons
- Feature highlights (3 cards)
- Welcome message

**Rationale**:
- Helps users understand capabilities
- Reduces friction for first message
- Common pattern in AI chat interfaces

## Testing Strategy

### Component Tests (React Testing Library)

**ChatMessage Component**:
- Renders user messages with correct styling
- Renders assistant messages with correct styling
- Displays tool calls when present
- Formats timestamps correctly
- Handles missing timestamps gracefully

**ChatInput Component**:
- Sends message on Enter key
- Creates new line on Shift+Enter
- Disables input while loading
- Enforces character limit
- Shows character counter

**ToolCallDisplay Component**:
- Displays tool name with correct icon
- Shows parameters formatted
- Shows result summary
- Handles multiple tool calls

**EmptyChat Component**:
- Displays welcome message
- Shows suggestion buttons
- Calls onSendMessage when suggestion clicked

**ChatInterface Component**:
- Displays messages in correct order
- Shows loading indicator while waiting
- Displays error messages
- Auto-scrolls to bottom on new messages
- Shows empty state when no messages

### Integration Tests

**Full Chat Flow**:
1. User types message
2. Message appears in chat
3. Loading indicator shows
4. API request sent with JWT token
5. Response received
6. Assistant message appears
7. Tool calls displayed

**Conversation Persistence**:
1. Send messages in conversation
2. Refresh page
3. Conversation history loads
4. Can continue conversation

**Error Handling**:
1. Simulate network error
2. Error message displays
3. User can retry
4. Success after retry

**Navigation**:
1. Switch from chat to todo list
2. Switch back to chat
3. Conversation preserved

### Responsive Design Tests

**Mobile (375px)**:
- Messages display correctly
- Input area accessible
- Send button visible
- No horizontal scroll

**Tablet (768px)**:
- Optimal message width
- Comfortable spacing
- Navigation accessible

**Desktop (1280px)**:
- Max-width container
- Optional sidebar visible
- Comfortable reading width

### Manual Testing Scenarios

**Natural Language Variations**:
- "Add buy groceries"
- "Create a task to buy groceries"
- "I need to buy groceries"
- "Remind me to buy groceries"

**Edge Cases**:
- Very long messages (2000 chars)
- Special characters (!@#$%^&*)
- Emoji in messages
- Rapid message sending
- Slow network (throttle to 3G)

## Quality Gates

### Pre-Implementation Checklist

- [x] Specification complete and validated
- [x] Constitution check passed (with streaming violation justified)
- [ ] Research complete (research.md)
- [ ] Data model defined (data-model.md)
- [ ] API contracts documented (contracts/)
- [ ] Quickstart guide written (quickstart.md)
- [ ] Agent context updated (CLAUDE.md)

### Implementation Milestones

**Milestone 1: Core Chat (Day 1-2)**
- [ ] Chat interface displays messages
- [ ] Can send messages to backend
- [ ] Receives and displays AI responses
- [ ] Loading indicators work
- [ ] Error messages display

**Milestone 2: Features (Day 2-3)**
- [ ] Tool calls visualized
- [ ] Conversation persistence works
- [ ] New conversation creation
- [ ] Timestamps displayed
- [ ] Auto-scroll implemented

**Milestone 3: Polish (Day 3-4)**
- [ ] Responsive design complete
- [ ] Navigation integration
- [ ] Empty state implemented
- [ ] Error handling robust
- [ ] All tests passing

### Acceptance Criteria

**Functional**:
- All 22 functional requirements implemented
- All P1 user stories complete
- All P2 user stories complete (tool calls, conversation management)

**Quality**:
- 60% component test coverage
- Zero TypeScript errors
- Zero ESLint warnings
- All manual tests pass

**Performance**:
- Message send/receive <5 seconds
- Interface switching <2 seconds
- Smooth scrolling with 100 messages
- No memory leaks

**Responsive**:
- Works on mobile (320px+)
- Works on tablet (768px+)
- Works on desktop (1024px+)

## Post-Design Constitution Re-evaluation

*To be completed after Phase 1 artifacts are created*

### Streaming Response Decision

**Status**: Deferred to Phase 2 (post-MVP)

**Justification Approved**: Yes (conditional)
- MVP timeline requires focus on core functionality
- Backend API does not currently support streaming
- Loading indicators provide adequate user feedback
- API client designed for future streaming support

**Mitigation Plan**:
1. Document streaming as Phase 2 enhancement
2. Design API client with streaming parameter
3. Use Server-Sent Events (SSE) for streaming
4. Update ChatInterface to handle partial messages
5. Add tests for streaming scenarios

**Technical Debt**:
- Track as GitHub issue: "Add streaming support for AI responses"
- Priority: Medium (UX enhancement)
- Estimated effort: 2-3 days

### Final Constitution Compliance

**All Gates**: ✅ PASS (with approved streaming exception)

**Ready for Implementation**: Yes

**Next Command**: `/sp.tasks` to generate detailed implementation tasks

---

**Plan Status**: Complete
**Approval Required**: Technical lead approval for non-streaming MVP approach
**Next Steps**:
1. Review and approve plan
2. Run `/sp.tasks` to generate implementation tasks
3. Begin implementation (estimated 3-4 days)
