# Data Model: MCP AI Chat

**Feature**: 001-mcp-ai-chat
**Date**: 2026-01-13
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the database schema extensions required for the MCP AI Chat feature. Two new models are introduced: `Conversation` and `Message`, which work together to store conversation history for stateless AI chat interactions.

---

## Entity Relationship Diagram

```
User (existing)
  ↓ 1:N
Conversation (new)
  ↓ 1:N
Message (new)

Task (existing) - referenced by tool operations but no direct relationship
```

---

## Model Definitions

### Conversation Model

**Purpose**: Represents a chat session between a user and the AI assistant. A user can have multiple conversations over time.

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Conversation(SQLModel, table=True):
    """
    Conversation model for AI chat sessions

    A conversation represents a continuous chat session between a user
    and the AI assistant. All messages within a conversation share context.
    """
    __tablename__ = "conversations"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Field Descriptions**:
- `id`: Auto-incrementing primary key
- `user_id`: Reference to the user who owns this conversation (indexed for fast user isolation queries)
- `created_at`: Timestamp when conversation was created
- `updated_at`: Timestamp when conversation was last updated (updated on new messages)
- `messages`: Relationship to all messages in this conversation (cascade delete)

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` for user isolation queries

**Constraints**:
- `user_id` must reference existing user (foreign key constraint)
- `created_at` and `updated_at` cannot be null

**State Transitions**:
- Created: When user sends first message without conversation_id
- Updated: When new message is added to conversation
- Deleted: When user explicitly deletes conversation (future feature)

---

### Message Model

**Purpose**: Represents a single message within a conversation. Messages can be from the user or the AI assistant.

**SQLModel Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class Message(SQLModel, table=True):
    """
    Message model for conversation messages

    A message represents a single turn in a conversation, either from
    the user or the AI assistant. Messages are immutable after creation.
    """
    __tablename__ = "messages"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign Keys
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        nullable=False
    )
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        nullable=False
    )

    # Message Data
    role: str = Field(nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls

    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

**Field Descriptions**:
- `id`: Auto-incrementing primary key
- `conversation_id`: Reference to the conversation this message belongs to (indexed for fast history retrieval)
- `user_id`: Reference to the user (for user isolation, even though it's redundant with conversation.user_id)
- `role`: Message role - either "user" or "assistant"
- `content`: The actual message text
- `tool_calls`: JSON string containing tool invocation details (only for assistant messages)
- `created_at`: Timestamp when message was created
- `conversation`: Relationship to parent conversation

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `conversation_id` for conversation history queries
- Index on `user_id` for user isolation queries
- Composite index on `(conversation_id, created_at)` for ordered history retrieval (recommended)

**Constraints**:
- `conversation_id` must reference existing conversation (foreign key constraint)
- `user_id` must reference existing user (foreign key constraint)
- `role` must be "user" or "assistant" (application-level validation)
- `content` cannot be empty (application-level validation)
- `tool_calls` must be valid JSON if present (application-level validation)

**State Transitions**:
- Created: When message is stored in database
- Immutable: Messages are never updated or deleted individually (only via conversation cascade)

---

## Validation Rules

### Conversation Validation

**Creation**:
- `user_id` must reference existing user
- `created_at` and `updated_at` set automatically

**Update**:
- Only `updated_at` can be modified (automatically on new messages)
- Cannot change `user_id` after creation

**Deletion**:
- Cascade deletes all associated messages
- Requires user authorization (user_id must match)

### Message Validation

**Role Validation**:
```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

# In Message model
role: MessageRole = Field(nullable=False)
```

**Content Validation**:
```python
from pydantic import validator

class Message(SQLModel, table=True):
    # ... fields ...

    @validator('content')
    def content_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Message content cannot be empty')
        return v.strip()
```

**Tool Calls Validation**:
```python
import json
from pydantic import validator

class Message(SQLModel, table=True):
    # ... fields ...

    @validator('tool_calls')
    def tool_calls_valid_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('tool_calls must be valid JSON')
        return v
```

---

## Database Migration

### Alembic Migration Script

**File**: `backend/alembic/versions/xxx_add_conversation_message_models.py`

```python
"""Add Conversation and Message models for AI chat

Revision ID: xxx
Revises: yyy
Create Date: 2026-01-13

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'xxx'
down_revision = 'yyy'  # Previous migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index on user_id for user isolation queries
    op.create_index(
        'ix_conversations_user_id',
        'conversations',
        ['user_id']
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for efficient queries
    op.create_index(
        'ix_messages_conversation_id',
        'messages',
        ['conversation_id']
    )

    op.create_index(
        'ix_messages_user_id',
        'messages',
        ['user_id']
    )

    # Create composite index for ordered history retrieval
    op.create_index(
        'ix_messages_conversation_created',
        'messages',
        ['conversation_id', 'created_at']
    )


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_messages_conversation_created', table_name='messages')
    op.drop_index('ix_messages_user_id', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')

    # Drop tables (cascade will handle foreign keys)
    op.drop_table('messages')

    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
```

**Migration Commands**:
```bash
# Generate migration (if using autogenerate)
alembic revision --autogenerate -m "Add Conversation and Message models"

# Apply migration
alembic upgrade head

# Rollback migration (if needed)
alembic downgrade -1
```

---

## Query Patterns

### Common Queries

**1. Get User's Conversations**:
```python
from sqlmodel import select

# Get all conversations for a user
conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
).all()
```

**2. Get Conversation History**:
```python
# Get messages for a conversation (ordered chronologically)
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at)
    .limit(50)  # Limit to recent messages
).all()
```

**3. Get Conversation with Messages (Eager Loading)**:
```python
from sqlmodel import select
from sqlalchemy.orm import selectinload

# Get conversation with all messages loaded
conversation = session.exec(
    select(Conversation)
    .where(Conversation.id == conversation_id)
    .options(selectinload(Conversation.messages))
).first()
```

**4. Create Conversation and First Message**:
```python
# Create conversation
conversation = Conversation(user_id=user_id)
session.add(conversation)
session.commit()
session.refresh(conversation)

# Create first message
message = Message(
    conversation_id=conversation.id,
    user_id=user_id,
    role="user",
    content="Hello!"
)
session.add(message)
session.commit()
```

**5. Add Message to Existing Conversation**:
```python
# Add message
message = Message(
    conversation_id=conversation_id,
    user_id=user_id,
    role="assistant",
    content="Hello! How can I help you?",
    tool_calls=json.dumps([...])  # Optional
)
session.add(message)

# Update conversation timestamp
conversation.updated_at = datetime.utcnow()
session.add(conversation)

session.commit()
```

---

## Performance Considerations

### Index Strategy

**Primary Indexes** (created in migration):
- `conversations.id` (primary key, automatic)
- `conversations.user_id` (for user isolation)
- `messages.id` (primary key, automatic)
- `messages.conversation_id` (for history retrieval)
- `messages.user_id` (for user isolation)
- `(messages.conversation_id, messages.created_at)` (composite, for ordered retrieval)

**Query Performance**:
- User isolation queries: O(log n) with user_id index
- Conversation history: O(log n) with composite index
- Message insertion: O(log n) for index updates

### Storage Estimates

**Conversation**:
- Fixed size: ~40 bytes per row
- 1000 conversations: ~40 KB

**Message**:
- Variable size: ~100-500 bytes per message (depends on content length)
- Average: ~250 bytes per message
- 10,000 messages: ~2.5 MB

**Growth Rate**:
- Assuming 100 users, 10 conversations per user, 20 messages per conversation
- Total: 1,000 conversations, 20,000 messages
- Storage: ~5 MB (negligible)

### Optimization Opportunities

**Future Optimizations** (if needed):
1. **Message Pagination**: Limit history retrieval to recent N messages
2. **Conversation Archiving**: Move old conversations to archive table
3. **Message Summarization**: Summarize old messages to reduce token costs
4. **Read Replicas**: Use read replicas for conversation history queries
5. **Caching**: Cache recent conversation history in Redis

---

## Security Considerations

### User Isolation

**Enforcement Points**:
1. All conversation queries must filter by `user_id`
2. All message queries must filter by `user_id` or `conversation.user_id`
3. API endpoints must validate user owns conversation before access

**Example Secure Query**:
```python
# SECURE: Filters by user_id
conversation = session.exec(
    select(Conversation)
    .where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id  # User isolation
    )
).first()

if not conversation:
    raise HTTPException(404, "Conversation not found")
```

**Example Insecure Query** (DO NOT USE):
```python
# INSECURE: No user_id filter
conversation = session.get(Conversation, conversation_id)
# Anyone can access any conversation!
```

### Data Protection

**Sensitive Data**:
- Message content may contain PII (personally identifiable information)
- Tool calls may contain task details
- Conversation history reveals user behavior

**Protection Measures**:
- Database encryption at rest (Neon DB default)
- TLS encryption in transit (HTTPS)
- Access control via JWT authentication
- Audit logging for conversation access

---

## Testing Strategy

### Unit Tests

**Model Validation Tests**:
```python
def test_conversation_creation():
    conversation = Conversation(user_id=1)
    assert conversation.user_id == 1
    assert conversation.created_at is not None
    assert conversation.updated_at is not None

def test_message_role_validation():
    with pytest.raises(ValueError):
        Message(
            conversation_id=1,
            user_id=1,
            role="invalid",  # Should fail
            content="Test"
        )

def test_message_content_not_empty():
    with pytest.raises(ValueError):
        Message(
            conversation_id=1,
            user_id=1,
            role="user",
            content=""  # Should fail
        )
```

### Integration Tests

**Database Operations**:
```python
def test_create_conversation_and_messages(session):
    # Create conversation
    conversation = Conversation(user_id=1)
    session.add(conversation)
    session.commit()

    # Create messages
    msg1 = Message(
        conversation_id=conversation.id,
        user_id=1,
        role="user",
        content="Hello"
    )
    msg2 = Message(
        conversation_id=conversation.id,
        user_id=1,
        role="assistant",
        content="Hi there!"
    )
    session.add_all([msg1, msg2])
    session.commit()

    # Verify
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
    ).all()
    assert len(messages) == 2

def test_cascade_delete(session):
    # Create conversation with messages
    conversation = Conversation(user_id=1)
    session.add(conversation)
    session.commit()

    message = Message(
        conversation_id=conversation.id,
        user_id=1,
        role="user",
        content="Test"
    )
    session.add(message)
    session.commit()

    # Delete conversation
    session.delete(conversation)
    session.commit()

    # Verify messages are deleted
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
    ).all()
    assert len(messages) == 0
```

---

## Summary

**New Models**: 2 (Conversation, Message)
**New Tables**: 2 (conversations, messages)
**New Indexes**: 5 (user_id, conversation_id, composite)
**Foreign Keys**: 3 (conversation→user, message→conversation, message→user)
**Cascade Deletes**: 1 (conversation deletes messages)

**Key Design Decisions**:
1. Separate Conversation and Message models for clear separation of concerns
2. Redundant user_id in Message for efficient user isolation queries
3. Immutable messages (no updates after creation)
4. Cascade delete for data consistency
5. Composite index for efficient ordered history retrieval
6. JSON string for tool_calls (flexible, no schema changes needed)

**Ready for Implementation**: ✅
- Models defined with complete validation
- Migration script ready
- Query patterns documented
- Performance considerations addressed
- Security measures defined
- Testing strategy established
