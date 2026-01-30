"""Entry point for MCP validation server."""

import asyncio
from mcp_validation_server.server import mcp
from mcp_validation_server import validators  # Triggers registration

def main():
    """Run the MCP server."""
    asyncio.run(mcp.run())

if __name__ == "__main__":
    main()
