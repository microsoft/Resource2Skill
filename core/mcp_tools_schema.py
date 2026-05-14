"""
core/mcp_tools_schema.py
Convert MCP tool definitions to OpenAI function-calling schema.

Provides:
  - mcp_tool_to_openai_schema(tool) — dynamic conversion from MCP SDK Tool
  - get_tools_from_mcp(session) — async: list_tools() + convert
  - load_tools_fallback(path) — load tool schemas from a JSON file (for dry-run)
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

log = logging.getLogger("mcp_tools_schema")


def mcp_tool_to_openai_schema(tool) -> dict:
    """Convert an MCP SDK Tool object to OpenAI function calling format.

    The MCP SDK Tool has .name, .description, and .inputSchema (JSON Schema dict).
    """
    schema = tool.inputSchema or {"type": "object", "properties": {}}
    # Ensure 'type' is present (OpenAI requires it)
    if "type" not in schema:
        schema["type"] = "object"
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": schema,
        },
    }


async def get_tools_from_mcp(session) -> list[dict]:
    """Fetch tool definitions from an MCP session and convert to OpenAI format."""
    result = await session.list_tools()
    tools = []
    for t in result.tools:
        try:
            tools.append(mcp_tool_to_openai_schema(t))
        except Exception as e:
            log.warning("Failed to convert MCP tool '%s': %s", t.name, e)
    log.info("Loaded %d tools from MCP server", len(tools))
    return tools


def load_tools_fallback(path: Path) -> list[dict]:
    """Load tool schemas from a JSON file for dry-run / offline testing.

    Args:
        path: Path to a JSON file containing a list of OpenAI tool schemas.

    Returns:
        List of OpenAI function-calling tool dicts.
    """
    with open(path, encoding="utf-8") as f:
        tools = json.load(f)
    log.info("Loaded %d fallback tools from %s", len(tools), path)
    return tools
