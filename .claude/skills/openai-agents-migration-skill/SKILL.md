---
name: openai-agents-migration-skill
description: Convert Swarm-based or legacy agent systems into OpenAI Agents SDK using Agent, Runner, and tool-based execution. Use when upgrading to openai-agents.
---

# Swarm → OpenAI Agents SDK Migration Guide

## Instructions

### 1. **Install & Use OpenAI Agents SDK**
```bash
pip install openai-agents
````

All agent logic must use:

* `Agent`
* `Runner`
* `@function_tool`

No legacy Swarm APIs allowed.

---

### 2. **Agent Definition**

* Define a single primary agent for orchestration
* Move behavior rules into `instructions`
* Avoid conditional routing in code
* Let the agent decide tool usage

Example:

```python
agent = Agent(
    name="Todo Chat Agent",
    instructions="You manage todos via MCP tools..."
)
```

---

### 3. **Tool Conversion**

Swarm actions → Agents SDK tools:

```python
@function_tool
def add_task(user_id: str, title: str, description: str | None = None):
    ...
```

Rules:

* Tools must be stateless
* Tools persist data via Neon DB
* Tools must match MCP specification

---

### 4. **Runner Execution**

* Replace Swarm loop with `Runner.run()`
* Provide full conversation context per request
* No agent memory between runs

Example:

```python
result = Runner.run(
    agent,
    messages=conversation_history
)
```

---

### 5. **Context Injection**

* Inject `user_id`, `conversation_id` via run context
* Do NOT store context globally
* Do NOT mutate agent instructions at runtime

---

### 6. **What to Remove from Swarm**

* Shared state objects
* Agent-to-agent messaging
* Manual tool routing
* In-memory task lists
* Persistent agent instances

---

## Successful Migration Criteria

* Swarm code fully removed
* Only OpenAI Agents SDK used
* Tools invoked by agent reasoning
* Stateless API behavior achieved
* MCP server remains independent

```

---

