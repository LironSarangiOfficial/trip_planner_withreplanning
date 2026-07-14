"""
MCP server for the Trip Planner project.

Wraps the existing data-fetching functions in `services/` as MCP tools, so
any MCP client (Claude, an MCP-aware agent, mcp-cli, etc.) can call them
over the Model Context Protocol instead of importing them directly.

No other part of the project is changed - this file only imports from
services/*.py, it doesn't modify them.

Run directly:
    python mcp/server.py
"""

import os
import sys

# Import the real MCP SDK BEFORE touching sys.path below. This project has a
# folder literally named "mcp" (the one this file lives in) - if the project
# root were already on sys.path when Python resolves `import mcp`, that
# folder could shadow the real, pip-installed "mcp" package. Importing it
# first avoids that entirely.
from mcp.server.fastmcp import FastMCP

# Make the project root importable so we can reuse the existing services/
# modules unchanged, regardless of the working directory this is launched
# from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from services.weather_service import get_weather
from services.serper_service import search_serper
from services.foursquare_service import get_hotels
from services.opentripmap_service import get_destination_places

mcp = FastMCP("trip-planner-mcp")


@mcp.tool()
def weather(city: str) -> dict:
    """Get current weather (temp, description, humidity) for a city via OpenWeatherMap."""
    return get_weather(city)


@mcp.tool()
def web_search(query: str, num_results: int = 5) -> dict:
    """Run a live Google search via Serper. Used for destination/transport/best-time research."""
    return search_serper(query, num_results=num_results)


@mcp.tool()
def hotels(city: str) -> list:
    """Find hotels near a city via Foursquare Places."""
    return get_hotels(city)


@mcp.tool()
def destination_places(place_name: str, limit: int = 8) -> dict:
    """Get top tourist places (attractions, beaches, landmarks, etc.) for a destination via OpenTripMap."""
    return get_destination_places(place_name, limit=limit)


if __name__ == "__main__":
    # stdio transport - standard for local MCP servers spawned by a client
    mcp.run()
