"""MCP tool definitions for task management operations.

This module defines the MCP tools that the AI agent can invoke:
- add_task: Create a new task
- list_tasks: Query tasks with filters
- complete_task: Mark a task as complete
- delete_task: Delete a task
- update_task: Update task properties
"""

from typing import Dict, Any

# Tool definitions following MCP specification
# Each tool has: name, description, input_schema (JSON Schema), output_schema

ADD_TASK_TOOL = {
    "name": "add_task",
    "description": "Create a new task for the user",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user creating the task"
            },
            "title": {
                "type": "string",
                "description": "Title of the task",
                "minLength": 1,
                "maxLength": 200
            },
            "description": {
                "type": "string",
                "description": "Optional description of the task",
                "maxLength": 2000
            }
        },
        "required": ["user_id", "title"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": ["string", "null"]},
            "is_completed": {"type": "boolean"},
            "created_at": {"type": "string", "format": "date-time"}
        }
    }
}

LIST_TASKS_TOOL = {
    "name": "list_tasks",
    "description": "List tasks for the user with optional filters",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user whose tasks to list"
            },
            "is_completed": {
                "type": "boolean",
                "description": "Filter by completion status (optional)"
            }
        },
        "required": ["user_id"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": ["string", "null"]},
                        "is_completed": {"type": "boolean"}
                    }
                }
            },
            "count": {"type": "integer"}
        }
    }
}

COMPLETE_TASK_TOOL = {
    "name": "complete_task",
    "description": "Mark a task as complete",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user who owns the task"
            },
            "task_id": {
                "type": "integer",
                "description": "ID of the task to complete"
            }
        },
        "required": ["user_id", "task_id"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "is_completed": {"type": "boolean"}
        }
    }
}

DELETE_TASK_TOOL = {
    "name": "delete_task",
    "description": "Delete a task",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user who owns the task"
            },
            "task_id": {
                "type": "integer",
                "description": "ID of the task to delete"
            }
        },
        "required": ["user_id", "task_id"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "message": {"type": "string"}
        }
    }
}

UPDATE_TASK_TOOL = {
    "name": "update_task",
    "description": "Update task properties (title, description, completion status)",
    "input_schema": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user who owns the task"
            },
            "task_id": {
                "type": "integer",
                "description": "ID of the task to update"
            },
            "title": {
                "type": "string",
                "description": "New title for the task (optional)",
                "minLength": 1,
                "maxLength": 200
            },
            "description": {
                "type": "string",
                "description": "New description for the task (optional)",
                "maxLength": 2000
            },
            "is_completed": {
                "type": "boolean",
                "description": "New completion status (optional)"
            }
        },
        "required": ["user_id", "task_id"]
    },
    "output_schema": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": ["string", "null"]},
            "is_completed": {"type": "boolean"}
        }
    }
}

# All tools registry
ALL_TOOLS = [
    ADD_TASK_TOOL,
    LIST_TASKS_TOOL,
    COMPLETE_TASK_TOOL,
    DELETE_TASK_TOOL,
    UPDATE_TASK_TOOL
]
