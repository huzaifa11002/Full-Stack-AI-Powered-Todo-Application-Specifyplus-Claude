"""MCP server initialization using Official MCP SDK.

This module initializes the MCP server with all task management tools
using the official MCP SDK patterns.
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any
import logging

from .handlers import (
    handle_add_task,
    handle_list_tasks,
    handle_complete_task,
    handle_delete_task,
    handle_update_task
)
from .tools import ALL_TOOLS

# Configure logging
logger = logging.getLogger(__name__)

# Initialize MCP server using official SDK
app = Server("todo-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools.

    Returns:
        List of tool definitions
    """
    return [
        Tool(
            name=tool["name"],
            description=tool["description"],
            inputSchema=tool["input_schema"]
        )
        for tool in ALL_TOOLS
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute an MCP tool by name.

    Args:
        name: Name of the tool to execute
        arguments: Tool parameters

    Returns:
        List of text content with tool execution result

    Raises:
        ValueError: If tool does not exist or execution fails
    """
    # Map tool names to handlers
    handlers = {
        "add_task": handle_add_task,
        "list_tasks": handle_list_tasks,
        "complete_task": handle_complete_task,
        "delete_task": handle_delete_task,
        "update_task": handle_update_task
    }

    if name not in handlers:
        raise ValueError(f"Tool '{name}' not found")

    try:
        # Execute handler
        handler = handlers[name]
        result = await handler(arguments)

        # Return result as TextContent
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result)
        )]

    except ValueError as e:
        # Return structured error for validation/not found errors
        logger.error(f"Tool '{name}' validation error: {str(e)}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": str(e),
                "type": "validation_error"
            })
        )]

    except Exception as e:
        # Return structured error for unexpected errors
        logger.error(f"Tool '{name}' execution error: {str(e)}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": f"Tool execution failed: {str(e)}",
                "type": "execution_error"
            })
        )]


# Legacy compatibility: provide a simple wrapper for existing code
class MCPServerWrapper:
    """Wrapper for backward compatibility with existing code.

    This allows existing code that uses mcp_server.invoke_tool() to continue working
    while we transition to the official MCP SDK patterns.
    """

    async def invoke_tool(self, tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
        """Invoke a tool by name (legacy interface).

        Args:
            tool_name: Name of the tool to invoke
            params: Parameters for the tool

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool does not exist or execution fails
        """
        result = await call_tool(tool_name, params)

        # Parse the TextContent result back to dict
        import json
        if result and len(result) > 0:
            return json.loads(result[0].text)

        raise ValueError(f"Tool '{tool_name}' returned no result")


# Global instance for backward compatibility
mcp_server = MCPServerWrapper()

