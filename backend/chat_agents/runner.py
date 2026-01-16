"""Agent runner for executing conversations with OpenAI Agents SDK.

This module handles the execution of AI agent conversations using OpenAI Agents SDK,
including tool invocation and response generation.
"""

from typing import Dict, Any, List, Tuple
import json
import logging
from agents import Runner
from .agent import set_user_context, todoChatAgent

# Configure logging
logger = logging.getLogger(__name__)


async def run_agent_conversation(
    user_id: int,
    messages: List[Dict[str, str]],
    new_message: str
) -> Tuple[str, List[Dict[str, Any]]]:
    """Run agent conversation with OpenAI Agents SDK.

    Args:
        user_id: ID of the user
        messages: Conversation history (list of {role, content} dicts)
        new_message: New user message

    Returns:
        Tuple of (assistant_response, tool_calls)
        - assistant_response: The AI's text response
        - tool_calls: List of tool calls made (each with tool, params, result)

    Raises:
        Exception: If agent execution fails
    """
    # Set user context for function tools
    set_user_context(user_id)

    try:
        agent = todoChatAgent

        # Build conversation messages for Runner
        # According to OpenAI Agents SDK docs, input can be a string or list of input items
        conversation_messages = []

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

        logger.info(f"Running agent for user {user_id} with {len(conversation_messages)} messages")

        # Run agent with Runner
        # According to official docs: Runner.run() returns a RunResult
        result = await Runner.run(
            agent,            
            input=conversation_messages
        )

        logger.info(f"Agent run completed. Final output type: {type(result.final_output)}")

        # Extract assistant response from RunResult
        # According to OpenAI Agents SDK docs, use final_output for the response
        assistant_response = ""
        
        if result.final_output:
            # final_output can be a string or TextOutput object
            if isinstance(result.final_output, str):
                assistant_response = result.final_output
            elif hasattr(result.final_output, 'text'):
                assistant_response = result.final_output.text
            elif hasattr(result.final_output, 'content'):
                assistant_response = result.final_output.content
            else:
                assistant_response = str(result.final_output)
        
        logger.info(f"Assistant response: {assistant_response[:100]}...")

        # Extract tool calls from new_items
        # According to OpenAI Agents SDK docs, new_items contains the new items generated during the run
        tool_calls_made = []
        
        logger.info(f"Processing {len(result.new_items)} new items")
        
        for item in result.new_items:
            logger.info(f"Item type: {type(item)}, has type attr: {hasattr(item, 'type')}")
            
            # Check if this is a tool call item
            # RunItem wraps the raw item, check the raw item type
            if hasattr(item, 'raw'):
                raw_item = item.raw
                logger.info(f"Raw item type: {type(raw_item)}, role: {getattr(raw_item, 'role', None)}")
                
                # Check if this is a tool call in the raw item
                if hasattr(raw_item, 'role') and raw_item.role == 'assistant':
                    if hasattr(raw_item, 'tool_calls') and raw_item.tool_calls:
                        for tool_call in raw_item.tool_calls:
                            tool_name = tool_call.function.name if hasattr(tool_call, 'function') else None
                            tool_args_str = tool_call.function.arguments if hasattr(tool_call, 'function') else "{}"
                            
                            # Parse arguments
                            tool_params = {}
                            try:
                                tool_params = json.loads(tool_args_str)
                            except:
                                tool_params = {}
                            
                            # Inject user_id into params for frontend display
                            if isinstance(tool_params, dict):
                                tool_params["user_id"] = user_id
                            
                            if tool_name:
                                tool_calls_made.append({
                                    "tool": tool_name,
                                    "params": tool_params,
                                    "result": {}  # Result will be in a separate tool response item
                                })
                                logger.info(f"Found tool call: {tool_name}")
                
                # Check if this is a tool response
                elif hasattr(raw_item, 'role') and raw_item.role == 'tool':
                    # Match this result with the corresponding tool call
                    tool_call_id = getattr(raw_item, 'tool_call_id', None)
                    content = getattr(raw_item, 'content', '{}')
                    
                    # Try to parse the content as JSON
                    try:
                        result_data = json.loads(content) if isinstance(content, str) else content
                    except:
                        result_data = {"result": content}
                    
                    # Update the last tool call with this result
                    if tool_calls_made:
                        tool_calls_made[-1]["result"] = result_data
                        logger.info(f"Added result to tool call: {result_data}")

        logger.info(f"Extracted {len(tool_calls_made)} tool calls")

        return assistant_response, tool_calls_made

    except Exception as e:
        logger.error(f"Agent execution error: {str(e)}", exc_info=True)
        raise Exception(f"OpenAI Agents SDK execution error: {str(e)}")
    finally:
        # Clean up context
        set_user_context(None)
