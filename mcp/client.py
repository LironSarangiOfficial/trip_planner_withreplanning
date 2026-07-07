import asyncio

from mcp import Client
from server import server

async def main() -> None:
    async with Client(server) as client:
        result = await client.call_tool("",{})
        print(result.structured_content)


