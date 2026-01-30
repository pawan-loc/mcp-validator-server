"""FastMCP server instance and configuration."""

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("Validation Server")

# Validators will auto-register via decorators
