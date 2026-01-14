"""MCP server initialization and configuration.

This module initializes the MCP server with all task management tools.
"""

from typing import Dict, Any, List
from .tools import ALL_TOOLS
from .handlers import TOOL_HANDLERS


class MCPServer:
    """MCP Server for task management tools.

    Provides tool definitions and invocation interface for AI agents.
    """

    def __init__(self, name: str = "todo-mcp-server", version: str = "1.0.0"):
        """Initialize MCP server.

        Args:
            name: Server name
            version: Server version
        """
        self.name = name
        self.version = version
        self.tools = ALL_TOOLS
        self.handlers = TOOL_HANDLERS

    def get_tools(self) -> List[Dict[str, Any]]:
        """Get all available tools.

        Returns:
            List of tool definitions
        """
        return self.tools

    async def invoke_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a tool by name.

        Args:
            tool_name: Name of the tool to invoke
            params: Parameters for the tool

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool does not exist
        """
        if tool_name not in self.handlers:
            raise ValueError(f"Tool '{tool_name}' not found")

        handler = self.handlers[tool_name]
        return await handler(params)


# Global MCP server instance
mcp_server = MCPServer()
