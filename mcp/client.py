"""
MCP client for the Trip Planner project.

Spawns mcp/server.py as a subprocess over stdio, lists the tools it exposes,
and calls each one so you can confirm the MCP wiring works end to end.

Run directly:
    python mcp/client.py
"""

import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")

server_params = StdioServerParameters(
    command=sys.executable,
    args=[SERVER_SCRIPT],
)


def _print_result(label: str, result) -> None:
    print(f"\n--- {label} ---")
    if result.isError:
        print("Tool reported an error:")
    for block in result.content:
        if hasattr(block, "text"):
            text = block.text
            print(text[:800] + ("..." if len(text) > 800 else ""))


async def main() -> None:
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Connected. Available tools:", [t.name for t in tools.tools])

            result = await session.call_tool("weather", {"city": "Goa"})
            _print_result("weather(city='Goa')", result)

            result = await session.call_tool(
                "web_search", {"query": "best time to visit Goa", "num_results": 3}
            )
            _print_result("web_search(query='best time to visit Goa')", result)

            result = await session.call_tool("hotels", {"city": "Goa"})
            _print_result("hotels(city='Goa')", result)

            result = await session.call_tool(
                "destination_places", {"place_name": "Goa", "limit": 3}
            )
            _print_result("destination_places(place_name='Goa')", result)


if __name__ == "__main__":
    asyncio.run(main())
