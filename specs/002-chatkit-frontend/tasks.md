---
description: "Implementation tasks for OpenAI ChatKit Frontend feature"
---

# Tasks: OpenAI ChatKit Frontend for AI Task Management

**Input**: Design documents from `/specs/002-chatkit-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification - focusing on implementation tasks only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `frontend/` directory at repository root
- All new code in `frontend/app/`, `frontend/components/`, `frontend/lib/`, `frontend/types/`
- Follows Next.js 16 App Router conventions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 Install OpenAI ChatKit and date-fns dependencies in frontend/package.json
- [x] T002 [P] Create directory structure: frontend/app/chat/, frontend/components/chat/, frontend/lib/api/, frontend/lib/hooks/, frontend/types/
- [x] T003 [P] Verify TypeScript configuration in frontend/tsconfig.json (strict mode enabled)
- [x] T004 [P] Verify Tailwind CSS configuration in frontend/tailwind.config.js includes chat components

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create TypeScript type definitions in frontend/types/chat.ts (Message, ToolCall, Conversation, ChatState, ChatRequest, ChatResponse interfaces)
- [x] T006 [P] Add type guards and validation functions to frontend/types/chat.ts (isUserMessage, isAssistantMessage, hasToolCalls, validateMessage)
- [x] T007 [P] Add helper functions to frontend/types/chat.ts (generateTempMessageId, formatToolName, getToolIcon)
- [x] T008 Create chat API client in frontend/lib/api/chat.ts with sendMessage function using existing Axios client
- [x] T009 [P] Add error handling and response transformation to frontend/lib/api/chat.ts
- [x] T010 Create useChat custom hook in frontend/lib/hooks/useChat.ts with state management (messages, conversationId, isLoading, error)
- [x] T011 Add sendMessage function to useChat hook with optimistic updates and error recovery
- [x] T012 [P] Add startNewConversation and clearError functions to useChat hook
- [x] T013 [P] Add localStorage persistence for conversation ID in useChat hook

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Send Messages and Receive AI Responses (Priority: P1) 🎯 MVP

**Goal**: Users can type natural language messages to manage tasks and receive conversational responses from the AI assistant

**Independent Test**: Login, type "Add a task to buy groceries", send message, verify AI responds with confirmation

### Implementation for User Story 1

- [x] T014 [P] [US1] Create chat page route in frontend/app/chat/page.tsx with authentication check
- [x] T015 [P] [US1] Create ChatInterface component in frontend/components/chat/ChatInterface.tsx with header and layout structure
- [x] T016 [US1] Add message list rendering to ChatInterface component with scroll container
- [x] T017 [US1] Integrate useChat hook into ChatInterface component
- [x] T018 [P] [US1] Create ChatMessage component in frontend/components/chat/ChatMessage.tsx with user/assistant styling
- [x] T019 [US1] Add message content rendering with word wrapping to ChatMessage component
- [x] T020 [P] [US1] Create ChatInput component in frontend/components/chat/ChatInput.tsx with textarea and send button
- [x] T021 [US1] Add Enter key handler to ChatInput (Enter sends, Shift+Enter new line)
- [x] T022 [US1] Add character limit validation (2000 chars) to ChatInput with counter display
- [x] T023 [US1] Connect ChatInput to useChat sendMessage function
- [x] T024 [P] [US1] Create TypingIndicator component in frontend/components/chat/TypingIndicator.tsx with animated dots
- [x] T025 [US1] Add loading state display to ChatInterface (show TypingIndicator when isLoading)
- [x] T026 [US1] Add error message display to ChatInterface with dismiss functionality
- [x] T027 [US1] Disable input and send button while isLoading in ChatInput component
- [x] T028 [US1] Add network error handling with retry capability in useChat hook

**Checkpoint**: At this point, User Story 1 should be fully functional - users can send messages and receive AI responses

---

## Phase 4: User Story 2 - View Conversation History (Priority: P1)

**Goal**: Users can see complete conversation history that persists across page refreshes

**Independent Test**: Send multiple messages, refresh page, verify all messages are still visible in correct order

### Implementation for User Story 2

- [x] T029 [P] [US2] Add message timestamp display to ChatMessage component using date-fns
- [x] T030 [US2] Implement relative time formatting ("2 minutes ago") for recent messages in ChatMessage
- [x] T031 [US2] Implement absolute time formatting for older messages in ChatMessage
- [x] T032 [P] [US2] Add auto-scroll behavior to ChatInterface (scroll to bottom on new messages)
- [x] T033 [US2] Implement smart auto-scroll detection (disable when user scrolls up, re-enable when near bottom)
- [x] T034 [US2] Add smooth scrolling animation to auto-scroll behavior
- [x] T035 [US2] Load conversation ID from localStorage on page mount in useChat hook
- [x] T036 [US2] Fetch conversation history from backend when conversation ID exists (optional - backend may not support this yet)
- [x] T037 [US2] Ensure messages persist in state during active session
- [x] T038 [US2] Test conversation persistence across page refresh

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can send messages and view persistent history

---

## Phase 5: User Story 3 - Create and Resume Conversations (Priority: P2)

**Goal**: Users can start new conversations and resume existing conversations independently

**Independent Test**: Create new conversation, send messages, create another new conversation, verify both exist independently

### Implementation for User Story 3

- [x] T039 [P] [US3] Add "New Chat" button to ChatInterface header
- [x] T040 [US3] Connect "New Chat" button to startNewConversation function from useChat hook
- [x] T041 [US3] Clear localStorage conversation ID when starting new conversation
- [x] T042 [US3] Reset messages array when starting new conversation
- [x] T043 [US3] Update conversation ID in localStorage when backend returns new conversation ID
- [x] T044 [US3] Ensure new conversation creates fresh context (no message history)
- [x] T045 [P] [US3] Create EmptyChat component in frontend/components/chat/EmptyChat.tsx with welcome message
- [x] T046 [US3] Add feature highlights (3 cards) to EmptyChat component
- [x] T047 [US3] Add suggestion buttons (5 example messages) to EmptyChat component
- [x] T048 [US3] Connect suggestion buttons to sendMessage function (click suggestion to send)
- [x] T049 [US3] Display EmptyChat component when messages array is empty in ChatInterface

**Checkpoint**: All P1 and P2 core stories complete - users can manage conversations independently

---

## Phase 6: User Story 4 - View Tool Call Details (Priority: P2)

**Goal**: Users can see which task management tools the AI invoked and what actions were performed

**Independent Test**: Send "Add a task to buy groceries", verify response shows add_task tool was called with title parameter

### Implementation for User Story 4

- [x] T050 [P] [US4] Create ToolCallDisplay component in frontend/components/chat/ToolCallDisplay.tsx
- [x] T051 [US4] Add tool icon mapping to ToolCallDisplay (add_task: ➕, list_tasks: 📋, complete_task: ✅, delete_task: 🗑️, update_task: ✏️)
- [x] T052 [US4] Add tool label mapping to ToolCallDisplay (add_task: "Added Task", etc.)
- [x] T053 [US4] Implement tool call section rendering with tool name and icon
- [x] T054 [US4] Add parameters display to ToolCallDisplay (formatted as readable text)
- [x] T055 [US4] Add result summary display to ToolCallDisplay (task title, count, status)
- [x] T056 [US4] Style ToolCallDisplay with bordered section and background color
- [x] T057 [US4] Integrate ToolCallDisplay into ChatMessage component (display when tool_calls present)
- [x] T058 [US4] Handle multiple tool calls in single message (render all tool calls)

**Checkpoint**: Tool call transparency complete - users can see all AI actions

---

## Phase 7: User Story 5 - Switch Between Chat and Todo List UI (Priority: P3)

**Goal**: Users can navigate between conversational chat interface and traditional todo list interface

**Independent Test**: Add task via chat, switch to todo list view, verify task appears in list

### Implementation for User Story 5

- [x] T059 [P] [US5] Add chat navigation link to frontend/components/layout/Navigation.tsx
- [x] T060 [US5] Add active state styling for chat link in Navigation component
- [x] T061 [US5] Create view toggle component (List View / Chat View) in Navigation
- [x] T062 [US5] Ensure navigation is mobile-friendly (responsive design)
- [x] T063 [US5] Test navigation between chat page and dashboard page
- [x] T064 [US5] Verify conversation state is preserved when switching views

**Checkpoint**: Navigation complete - users can switch between interfaces seamlessly

---

## Phase 8: User Story 6 - Browse Conversation History Sidebar (Priority: P3)

**Goal**: Users can view list of previous conversations in sidebar and quickly switch between them

**Independent Test**: Create multiple conversations, view sidebar, click different conversations to switch between them

### Implementation for User Story 6

- [ ] T065 [P] [US6] Create ConversationList component in frontend/components/chat/ConversationList.tsx
- [ ] T066 [US6] Create useConversations hook in frontend/lib/hooks/useConversations.ts for fetching conversation list
- [ ] T067 [US6] Add API function to fetch user conversations in frontend/lib/api/chat.ts
- [ ] T068 [US6] Implement conversation list rendering with preview and timestamp
- [ ] T069 [US6] Add click handler to switch conversations (load conversation history)
- [ ] T070 [US6] Add active conversation highlighting in ConversationList
- [ ] T071 [US6] Add loading state to ConversationList while fetching conversations
- [ ] T072 [US6] Integrate ConversationList into ChatInterface as sidebar (desktop only)
- [ ] T073 [US6] Hide sidebar on mobile/tablet (< 1024px width)
- [ ] T074 [US6] Add menu button to show/hide sidebar on mobile

**Checkpoint**: All user stories complete - full feature functionality delivered

---

## Phase 9: Responsive Design Implementation

**Purpose**: Ensure chat interface works across all device sizes

- [x] T075 [P] Implement mobile layout (320px-767px) with single column and compact header
- [x] T076 [P] Implement tablet layout (768px-1023px) with optimized spacing
- [x] T077 [P] Implement desktop layout (1024px+) with max-width container and optional sidebar
- [x] T078 [P] Add responsive message bubble widths (full on mobile, 85% on tablet, 70% on desktop)
- [x] T079 [P] Ensure input area is accessible on mobile keyboards (fixed positioning)
- [x] T080 Test responsive design on multiple screen sizes (375px, 768px, 1280px, 1920px)

---

## Phase 10: Input Enhancements

**Purpose**: Improve input component usability

- [x] T081 [P] Implement auto-resize textarea in ChatInput (starts at 1 row, expands to 150px max)
- [x] T082 [P] Add paste handling to ChatInput component
- [x] T083 [P] Add focus management to ChatInput (auto-focus after sending message)
- [x] T084 Add helper text to ChatInput ("Press Enter to send, Shift+Enter for new line")

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [x] T085 [P] Add aria-labels for accessibility to all interactive elements
- [x] T086 [P] Ensure keyboard navigation works for all components
- [x] T087 [P] Add proper error boundaries to catch React errors
- [x] T088 [P] Optimize re-renders with React.memo for ChatMessage component
- [x] T089 [P] Add loading skeleton for conversation history loading (TypingIndicator serves this purpose)
- [x] T090 Verify all TypeScript types are correct (no any types)
- [x] T091 Run ESLint and fix all warnings
- [x] T092 Run Prettier to format all code
- [ ] T093 Test full chat flow end-to-end (send message, receive response, tool calls display)
- [ ] T094 Test error scenarios (network error, auth error, server error)
- [ ] T095 Test responsive design on real devices (mobile, tablet, desktop)
- [ ] T096 Validate against quickstart.md manual testing checklist
- [ ] T097 Update documentation with any implementation notes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Responsive Design (Phase 9)**: Can start after US1 is complete
- **Input Enhancements (Phase 10)**: Can start after US1 is complete
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Builds on US1/US2 but independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 5 (P3)**: Can start after US1 is complete - Requires chat interface to exist
- **User Story 6 (P3)**: Can start after US3 is complete - Requires conversation management to exist

### Within Each User Story

- Core components before integration
- Layout before content
- State management before UI updates
- Error handling after happy path
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, US1, US2, US3, US4 can start in parallel (if team capacity allows)
- All responsive design tasks marked [P] can run in parallel
- All input enhancement tasks marked [P] can run in parallel
- All polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch foundational tasks together:
Task: "Create TypeScript type definitions in frontend/types/chat.ts"
Task: "Add type guards and validation functions to frontend/types/chat.ts"
Task: "Add helper functions to frontend/types/chat.ts"

# Launch component creation tasks together:
Task: "Create chat page route in frontend/app/chat/page.tsx"
Task: "Create ChatInterface component in frontend/components/chat/ChatInterface.tsx"
Task: "Create ChatMessage component in frontend/components/chat/ChatMessage.tsx"
Task: "Create ChatInput component in frontend/components/chat/ChatInput.tsx"
Task: "Create TypingIndicator component in frontend/components/chat/TypingIndicator.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Send/Receive Messages)
4. Complete Phase 4: User Story 2 (View History)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo if ready

**MVP Delivers**: Core chat functionality with message sending, AI responses, and persistent conversation history

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Basic chat!)
3. Add User Story 2 → Test independently → Deploy/Demo (Persistent history!)
4. Add User Story 3 → Test independently → Deploy/Demo (Conversation management!)
5. Add User Story 4 → Test independently → Deploy/Demo (Tool transparency!)
6. Add User Story 5 → Test independently → Deploy/Demo (Navigation!)
7. Add User Story 6 → Test independently → Deploy/Demo (Full feature!)
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 + User Story 2 (P1 stories)
   - Developer B: User Story 3 + User Story 4 (P2 stories)
   - Developer C: User Story 5 + User Story 6 (P3 stories)
3. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 97
- Setup: 4 tasks
- Foundational: 9 tasks (BLOCKING)
- User Story 1 (P1): 15 tasks
- User Story 2 (P1): 10 tasks
- User Story 3 (P2): 11 tasks
- User Story 4 (P2): 9 tasks
- User Story 5 (P3): 6 tasks
- User Story 6 (P3): 10 tasks
- Responsive Design: 6 tasks
- Input Enhancements: 4 tasks
- Polish: 13 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phases

**Independent Test Criteria**:
- US1: Send "Add a task to buy groceries", verify AI responds
- US2: Send messages, refresh page, verify history persists
- US3: Create new conversation, verify fresh context
- US4: Send message, verify tool calls display
- US5: Switch between chat and todo list, verify navigation works
- US6: View sidebar, switch conversations, verify switching works

**Suggested MVP Scope**: User Stories 1 & 2 (25 tasks + Setup + Foundational = 38 tasks)

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests not included as not explicitly requested in specification
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
