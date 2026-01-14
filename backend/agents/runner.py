"""Agent runner for executing conversations with tool calling.

This module handles the execution of AI agent conversations, including
tool invocation and response generation.
"""

from typing import Dict, Any, List, Tuple
import json
from openai import OpenAI, APIError, RateLimitError
from .config import openai_client, SYSTEM_PROMPT
from .agent import create_agent_config
from mcp.server import mcp_server


async def run_agent_conversation(
    user_id: int,
    messages: List[Dict[str, str]],
    new_message: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """Run agent conversation with tool calling support.

    Args:
        user_id: ID of the user
        messages: Conversation history (list of {role, content} dicts)
        new_message: New user message

    Returns:
        Tuple of (assistant_response, tool_calls)
        - assistant_response: The AI's text response
        - tool_calls: List of tool calls made (each with tool, params, result)

    Raises:
        APIError: If OpenAI API call fails
        RateLimitError: If rate limit is exceeded
    """
    # Get agent configuration
    agent_config = create_agent_config(user_id)

    # Build conversation messages
    conversation_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # Add conversation history
    for msg in messages:
        conversation_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # Add new user message
    conversation_messages.append({
        "role": "user",
        "content": new_message
    })

    # Track tool calls
    tool_calls_made = []

    try:
        # Call OpenAI API with function calling
        response = openai_client.chat.completions.create(
            model=agent_config["model"],
            messages=conversation_messages,
            tools=agent_config["tools"],
            temperature=agent_config["temperature"],
            max_tokens=agent_config["max_tokens"]
        )

        # Get the assistant's response
        assistant_message = response.choices[0].message

        # Check if the assistant wants to call tools
        if assistant_message.tool_calls:
            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_params = json.loads(tool_call.function.arguments)

                # Inject user_id into tool parameters for user isolation
                tool_params["user_id"] = user_id

                # Invoke the tool via MCP server
                try:
                    tool_result = await mcp_server.invoke_tool(tool_name, tool_params)

                    # Record the tool call
                    tool_calls_made.append({
                        "tool": tool_name,
                        "params": tool_params,
                        "result": tool_result
                    })

                    # Add tool result to conversation
                    conversation_messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call.model_dump()]
                    })
                    conversation_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })

                except Exception as e:
                    # Record failed tool call
                    tool_calls_made.append({
                        "tool": tool_name,
                        "params": tool_params,
                        "result": {"error": str(e)}
                    })

            # Get final response after tool execution
            final_response = openai_client.chat.completions.create(
                model=agent_config["model"],
                messages=conversation_messages,
                temperature=agent_config["temperature"],
                max_tokens=agent_config["max_tokens"]
            )

            assistant_response = final_response.choices[0].message.content

        else:
            # No tool calls, just return the response
            assistant_response = assistant_message.content

        return assistant_response, tool_calls_made

    except RateLimitError as e:
        raise RateLimitError(f"OpenAI rate limit exceeded: {str(e)}")
    except APIError as e:
        raise APIError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise Exception(f"Agent execution error: {str(e)}")
