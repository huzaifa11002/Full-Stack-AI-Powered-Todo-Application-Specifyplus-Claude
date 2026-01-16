# Research: OpenAI ChatKit Frontend Technology Validation

**Feature**: 002-chatkit-frontend
**Date**: 2026-01-14
**Phase**: Phase 0 - Research & Technology Validation

## Overview

This document contains research findings for implementing the OpenAI ChatKit frontend for AI task management. Research covers integration patterns, state management, responsive design, tool visualization, auto-scroll behavior, and timestamp formatting.

---

## R1: OpenAI ChatKit Integration Patterns

### Question
How to integrate OpenAI ChatKit with Next.js 16 App Router?

### Research Findings

**OpenAI ChatKit Library Investigation**:
- **Status**: OpenAI ChatKit (@openai/chatkit) is a UI component library for building chat interfaces
- **Compatibility**: Designed for React applications, compatible with Next.js 16 App Router
- **TypeScript Support**: Full TypeScript support with type definitions included
- **Components Provided**: Pre-built chat components (ChatWindow, MessageList, MessageInput, etc.)

**Integration Approaches**:

1. **Use ChatKit Pre-built Components** (Option A)
   - Pros: Faster development, consistent UI patterns, maintained by OpenAI
   - Cons: Less customization, may not match existing Tailwind CSS styling, learning curve for ChatKit API
   - Verdict: Not recommended - requires matching existing UI design

2. **Use ChatKit Patterns with Custom Components** (Option B)
   - Pros: Full control over styling, matches existing Tailwind CSS, follows ChatKit best practices
   - Cons: More development time, need to implement all components
   - Verdict: **RECOMMENDED** - provides flexibility while following proven patterns

3. **Hybrid Approach** (Option C)
   - Pros: Use ChatKit for complex components, custom for simple ones
   - Cons: Inconsistent patterns, harder to maintain
   - Verdict: Not recommended - adds complexity

### Decision

**Selected Approach**: Custom components following ChatKit patterns (Option B)

**Rationale**:
- Spec requires matching existing Tailwind CSS styling
- Need full control over responsive design (320px - 1920px+)
- Custom tool call visualization not provided by ChatKit
- Better integration with existing Better Auth authentication
- Follows React best practices and Next.js 16 App Router conventions

**Implementation Strategy**:
- Study ChatKit documentation for patterns and best practices
- Implement custom React components with TypeScript
- Use Tailwind CSS for all styling
- Follow ChatKit's state management patterns (useChat hook)
- Adopt ChatKit's message structure and API contracts

**Code Example**:
```typescript
// Custom ChatInterface component following ChatKit patterns
import { useChat } from '@/lib/hooks/useChat';

export default function ChatInterface() {
  const { messages, isLoading, sendMessage } = useChat();

  return (
    <div className="flex flex-col h-full">
      <MessageList messages={messages} />
      {isLoading && <TypingIndicator />}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}
```

---

## R2: Conversation State Management

### Question
Best approach for managing conversation state in React?

### Research Findings

**State Management Options**:

1. **Custom Hook (useChat)** (Option A)
   - Pros: Simple, no external dependencies, co-located with component logic
   - Cons: State not shared across components (unless lifted)
   - Use case: Single chat interface, state doesn't need global access

2. **Context API** (Option B)
   - Pros: Global state access, no external dependencies, React built-in
   - Cons: Can cause unnecessary re-renders, more boilerplate
   - Use case: Multiple components need chat state

3. **State Management Library (Zustand/Redux)** (Option C)
   - Pros: Advanced features (middleware, devtools), optimized re-renders
   - Cons: Additional dependency, learning curve, overkill for simple state
   - Use case: Complex state with many interactions

### Decision

**Selected Approach**: Custom Hook (useChat) with localStorage persistence (Option A)

**Rationale**:
- Chat state is localized to chat interface (no global access needed)
- Simpler implementation (no external state library)
- Follows React hooks best practices
- localStorage provides conversation ID persistence across sessions
- Optimistic updates for better UX

**State Structure**:
```typescript
interface ChatState {
  messages: Message[];              // Current conversation messages
  currentConversationId: number | null;  // Active conversation
  isLoading: boolean;               // API request in progress
  error: string | null;             // Error message if any
}
```

**Persistence Strategy**:
- **Conversation ID**: Store in localStorage to resume conversation on page refresh
- **Messages**: Fetch from backend on page load (backend is source of truth)
- **Session State**: Keep messages in React state during active session for performance

**Optimistic Updates**:
```typescript
// Add user message immediately (optimistic)
setState(prev => ({
  ...prev,
  messages: [...prev.messages, userMessage],
  isLoading: true
}));

// Send to backend
const response = await sendMessage(userMessage);

// Add assistant response
setState(prev => ({
  ...prev,
  messages: [...prev.messages, assistantMessage],
  isLoading: false
}));
```

**Error Recovery**:
```typescript
// On error, remove optimistic message
setState(prev => ({
  ...prev,
  messages: prev.messages.filter(m => m.id !== userMessage.id),
  isLoading: false,
  error: 'Failed to send message'
}));
```

---

## R3: Responsive Chat UI Patterns

### Question
How to implement responsive chat interface (320px - 1920px+)?

### Research Findings

**Responsive Design Strategies**:

1. **Mobile-First Approach**
   - Start with mobile layout (320px)
   - Add complexity for larger screens
   - Use Tailwind CSS breakpoints (sm, md, lg, xl)

2. **Breakpoint Strategy**:
   - **Mobile (320px - 767px)**: Single column, full-width messages, compact header
   - **Tablet (768px - 1023px)**: Optimized spacing, medium-width messages
   - **Desktop (1024px+)**: Max-width container, optional sidebar, wide messages

3. **Key Responsive Elements**:
   - **Message Bubbles**: Scale width based on screen size
   - **Input Area**: Fixed at bottom, adjusts height on mobile keyboards
   - **Sidebar**: Hidden on mobile, visible on desktop (optional)
   - **Navigation**: Hamburger menu on mobile, full nav on desktop

### Decision

**Selected Approach**: Mobile-first with Tailwind CSS breakpoints

**Tailwind CSS Breakpoints**:
```typescript
// Message bubble responsive width
<div className={`
  max-w-full           // Mobile: full width
  sm:max-w-[85%]       // Small: 85% width
  md:max-w-[75%]       // Medium: 75% width
  lg:max-w-[70%]       // Large: 70% width
`}>
  {message.content}
</div>
```

**Layout Patterns**:

**Mobile (320px - 767px)**:
```typescript
<div className="flex flex-col h-full">
  <header className="px-3 py-2">
    <h1 className="text-lg">AI Assistant</h1>
  </header>

  <div className="flex-1 overflow-y-auto px-3">
    {/* Full-width messages */}
  </div>

  <div className="px-3 py-3">
    {/* Compact input */}
  </div>
</div>
```

**Desktop (1024px+)**:
```typescript
<div className="flex h-screen">
  {/* Optional sidebar */}
  <aside className="hidden lg:block w-64 border-r">
    <ConversationList />
  </aside>

  <main className="flex-1">
    <div className="max-w-4xl mx-auto">
      <ChatInterface />
    </div>
  </main>
</div>
```

**Input Area Mobile Keyboard Handling**:
- Use `position: sticky` or `position: fixed` for input area
- Account for mobile keyboard height (viewport units)
- Prevent body scroll when keyboard is open

---

## R4: Tool Call Visualization

### Question
How to display tool call information inline with messages?

### Research Findings

**Visualization Approaches**:

1. **Inline Collapsed Section** (Option A)
   - Expandable/collapsible with click
   - Shows summary by default, details on expand
   - Pros: Saves space, progressive disclosure
   - Cons: Requires interaction, more complex

2. **Inline Always-Expanded Section** (Option B)
   - Always shows tool call details
   - Bordered section within message bubble
   - Pros: No interaction needed, transparent
   - Cons: Takes more space

3. **Separate Section Below Message** (Option C)
   - Tool calls in separate container
   - Pros: Clear separation
   - Cons: Loses context with message

### Decision

**Selected Approach**: Inline always-expanded section (Option B) for MVP

**Rationale**:
- Transparency is priority (users should see what AI did)
- No additional clicks required
- Simpler implementation (no expand/collapse state)
- Can add collapse functionality in Phase 2

**Tool Call Display Structure**:
```typescript
<div className="mt-3 pt-3 border-t border-gray-200">
  <div className="text-xs font-medium text-gray-600 uppercase">
    Actions Performed
  </div>

  {toolCalls.map(toolCall => (
    <div className="bg-gray-50 rounded p-2 text-sm border">
      {/* Tool icon and name */}
      <div className="flex items-center gap-2">
        <span>{getToolIcon(toolCall.tool)}</span>
        <span>{getToolLabel(toolCall.tool)}</span>
      </div>

      {/* Result summary */}
      <div className="mt-1 text-xs text-gray-600">
        {formatToolResult(toolCall.result)}
      </div>
    </div>
  ))}
</div>
```

**Tool Icon Mapping**:
```typescript
const toolIcons = {
  add_task: '➕',
  list_tasks: '📋',
  complete_task: '✅',
  delete_task: '🗑️',
  update_task: '✏️',
};
```

**Tool Label Mapping**:
```typescript
const toolLabels = {
  add_task: 'Added Task',
  list_tasks: 'Listed Tasks',
  complete_task: 'Completed Task',
  delete_task: 'Deleted Task',
  update_task: 'Updated Task',
};
```

**Accessibility Considerations**:
- Use semantic HTML (section, heading)
- Provide aria-labels for icons
- Ensure sufficient color contrast
- Support keyboard navigation

---

## R5: Auto-scroll Behavior

### Question
How to implement smart auto-scroll (scroll to bottom on new messages, but not when user scrolls up)?

### Research Findings

**Auto-scroll Patterns**:

1. **Always Scroll to Bottom**
   - Pros: Simple implementation
   - Cons: Interrupts user if they scrolled up to read history

2. **Smart Auto-scroll** (Recommended)
   - Scroll to bottom only if user is near bottom
   - Detect user scroll position
   - Disable auto-scroll when user scrolls up

3. **Manual Scroll Button**
   - Show "Scroll to bottom" button when not at bottom
   - Pros: User control
   - Cons: Extra interaction required

### Decision

**Selected Approach**: Smart auto-scroll (Option 2)

**Implementation Pattern**:
```typescript
const messagesContainerRef = useRef<HTMLDivElement>(null);
const messagesEndRef = useRef<HTMLDivElement>(null);
const [shouldAutoScroll, setShouldAutoScroll] = useState(true);

// Detect user scroll
const handleScroll = () => {
  if (!messagesContainerRef.current) return;

  const { scrollTop, scrollHeight, clientHeight } = messagesContainerRef.current;
  const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;

  setShouldAutoScroll(isNearBottom);
};

// Auto-scroll on new messages
useEffect(() => {
  if (shouldAutoScroll) {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }
}, [messages, shouldAutoScroll]);
```

**Scroll Threshold**:
- Consider "near bottom" if within 100px of bottom
- Allows for small scroll movements without disabling auto-scroll

**Smooth Scrolling**:
- Use `behavior: 'smooth'` for better UX
- Fallback to instant scroll if smooth not supported

**Performance Optimization**:
- Debounce scroll event handler
- Use `requestAnimationFrame` for scroll calculations
- Avoid unnecessary re-renders

---

## R6: Message Timestamp Formatting

### Question
Best library and format for displaying message timestamps?

### Research Findings

**Library Options**:

1. **date-fns** (Option A)
   - Pros: Modular (tree-shakeable), modern API, TypeScript support, actively maintained
   - Cons: Larger bundle than native Intl
   - Bundle size: ~2-3KB per function

2. **moment.js** (Option B)
   - Pros: Feature-rich, widely used
   - Cons: Large bundle size (~70KB), deprecated, not tree-shakeable
   - Verdict: Not recommended (deprecated)

3. **Native Intl.DateTimeFormat** (Option C)
   - Pros: No dependencies, built-in browser API
   - Cons: Limited formatting options, no relative time
   - Verdict: Not sufficient for relative time formatting

### Decision

**Selected Library**: date-fns (Option A)

**Rationale**:
- Modern, actively maintained
- Tree-shakeable (only import needed functions)
- Excellent TypeScript support
- Provides relative time formatting (`formatDistanceToNow`)
- Small bundle impact (~2-3KB)

**Timestamp Format Strategy**:

**Relative Time** (for recent messages):
```typescript
import { formatDistanceToNow } from 'date-fns';

// "2 minutes ago", "1 hour ago", "3 days ago"
formatDistanceToNow(new Date(message.created_at), { addSuffix: true });
```

**Absolute Time** (for older messages):
```typescript
import { format, isToday, isYesterday } from 'date-fns';

function formatMessageTime(timestamp: string) {
  const date = new Date(timestamp);

  if (isToday(date)) {
    return format(date, 'h:mm a');  // "2:30 PM"
  } else if (isYesterday(date)) {
    return `Yesterday ${format(date, 'h:mm a')}`;  // "Yesterday 2:30 PM"
  } else {
    return format(date, 'MMM d, h:mm a');  // "Jan 14, 2:30 PM"
  }
}
```

**Update Frequency**:
- No automatic updates for MVP (static timestamps)
- Can add interval-based updates in Phase 2 if needed
- Update on new messages (re-render triggers recalculation)

**Timezone Handling**:
- Use user's local timezone (browser default)
- Backend sends ISO 8601 timestamps (UTC)
- date-fns automatically converts to local time

---

## Summary of Decisions

### Technology Stack Confirmed

**Frontend Framework**:
- Next.js 16 App Router
- React 18+
- TypeScript 5.0+ (strict mode)

**UI Components**:
- Custom React components (not using ChatKit pre-built components)
- Tailwind CSS for styling
- Responsive design (mobile-first)

**State Management**:
- Custom useChat hook
- localStorage for conversation ID persistence
- Optimistic updates for better UX

**Dependencies**:
- date-fns (timestamp formatting)
- Axios (HTTP client - existing)
- react-hot-toast (notifications - existing)

**Design Patterns**:
- Smart auto-scroll (scroll to bottom when near bottom)
- Inline tool call visualization (always expanded for MVP)
- Hybrid message storage (state during session, fetch on load)

### Implementation Approach

**Phase 1 Priorities**:
1. Core chat interface (send/receive messages)
2. Tool call visualization
3. Responsive design
4. Conversation persistence

**Phase 2 Enhancements** (post-MVP):
1. Streaming responses (SSE)
2. Collapsible tool calls
3. Conversation sidebar
4. Markdown rendering
5. Message search

### Risk Mitigation

**Identified Risks**:
1. **Streaming not implemented**: Mitigated with loading indicators and typing animation
2. **Performance with many messages**: Mitigated with virtualization if needed (Phase 2)
3. **Mobile keyboard handling**: Test on real devices, adjust input positioning
4. **Tool call complexity**: Start with simple display, enhance in Phase 2

**Testing Strategy**:
- Component tests for all UI components (60% coverage target)
- Integration tests for chat flow
- Manual responsive design testing (multiple devices)
- Performance testing with 100+ messages

---

## Next Steps

1. ✅ Research complete
2. ⏭️ Create data-model.md (Phase 1)
3. ⏭️ Create contracts/ (Phase 1)
4. ⏭️ Create quickstart.md (Phase 1)
5. ⏭️ Update agent context (CLAUDE.md)
6. ⏭️ Generate implementation tasks (/sp.tasks)

**Research Status**: Complete
**Ready for Phase 1**: Yes
