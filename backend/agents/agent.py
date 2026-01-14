"""Agent creation and tool conversion utilities.

This module provides functions to create AI agents and convert MCP tools
to OpenAI function calling format.
"""

from typing import Dict, Any, List
from mcp.tools import ALL_TOOLS


def mcp_tool_to_openai_function(mcp_tool: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MCP tool definition to OpenAI function calling format.

    Args:
        mcp_tool: MCP tool definition with name, description, input_schema

    Returns:
        OpenAI function definition
    """
    return {
        "type": "function",
        "function": {
            "name": mcp_tool["name"],
            "description": mcp_tool["description"],
            "parameters": mcp_tool["input_schema"]
        }
    }


def get_openai_tools() -> List[Dict[str, Any]]:
    """Get all MCP tools in OpenAI function calling format.

    Returns:
        List of OpenAI function definitions
    """
    return [mcp_tool_to_openai_function(tool) for tool in ALL_TOOLS]


def create_agent_config(user_id: int) -> Dict[str, Any]:
    """Create agent configuration with user context.

    Args:
        user_id: ID of the user for this conversation

    Returns:
        Agent configuration dictionary
    """
    from .config import AGENT_MODEL, AGENT_TEMPERATURE, AGENT_MAX_TOKENS, SYSTEM_PROMPT

    return {
        "model": AGENT_MODEL,
        "temperature": AGENT_TEMPERATURE,
        "max_tokens": AGENT_MAX_TOKENS,
        "system_prompt": SYSTEM_PROMPT,
        "tools": get_openai_tools(),
        "user_id": user_id
    }
