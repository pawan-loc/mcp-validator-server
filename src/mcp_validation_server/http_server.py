"""
http_server.py - HTTP/SSE transport for MCP validation server

Copyright (c) 2025, Footfallz LLC

modification history
--------------------
01a,30jan26,pwn  written.

DESCRIPTION
Provides HTTP/SSE endpoint for remote MCP client connections.
Allows the validation server to be accessed over HTTP instead of
just local STDIO transport.
"""

# Standard library imports
import asyncio
import logging
import json
from typing import Any

# Third-party imports
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from sse_starlette import EventSourceResponse

# Local imports
from mcp_validation_server.server import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_sse(request):
    """
    Handle SSE connections for MCP clients.
    
    Args:
        request: Starlette request object
        
    Returns:
        EventSourceResponse with MCP server messages
    """
    async def event_generator():
        """Generate SSE events from MCP server."""
        try:
            logger.info("New SSE connection established")
            
            # Send initial connection message
            yield {
                "event": "connected",
                "data": json.dumps({
                    "status": "connected",
                    "service": "mcp-validation-server"
                })
            }
            
            # Keep connection alive
            while True:
                await asyncio.sleep(30)
                yield {
                    "event": "heartbeat",
                    "data": json.dumps({"status": "alive"})
                }
                    
        except Exception as e:
            logger.error(f"SSE connection error: {e}")
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


async def health_check(request):
    """Health check endpoint."""
    return Response(
        content='{"status": "healthy", "service": "mcp-validation-server"}',
        media_type="application/json"
    )


async def mcp_info(request):
    """MCP server information endpoint."""
    return Response(
        content=json.dumps({
            "service": "MCP Validation Server",
            "transport": "HTTP/SSE",
            "version": "1.0.0",
            "tools": [
                "validate_email",
                "validate_phone",
                "validate_url",
                "validate_regex"
            ],
            "endpoints": {
                "sse": "/sse",
                "health": "/health",
                "info": "/info"
            }
        }),
        media_type="application/json"
    )


# Create Starlette app
app = Starlette(
    debug=True,
    routes=[
        Route("/", endpoint=mcp_info),
        Route("/sse", endpoint=handle_sse),
        Route("/health", endpoint=health_check),
        Route("/info", endpoint=mcp_info),
    ]
)


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting MCP Validation Server (HTTP/SSE)")
    logger.info("SSE endpoint: http://localhost:8080/sse")
    logger.info("Health check: http://localhost:8080/health")
    logger.info("Info: http://localhost:8080/info")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
