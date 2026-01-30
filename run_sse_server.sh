#!/bin/bash
# run_sse_server.sh - Start MCP server with SSE transport

cd /Users/pawan/pawan/dev/python/MCPs
source .venv/bin/activate

echo "🚀 Starting MCP Validation Server (SSE)"
echo "📍 SSE endpoint: http://localhost:8080/sse"
echo "📍 Health check: http://localhost:8080/health"
echo "📍 Info: http://localhost:8080/info"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python src/mcp_validation_server/http_server.py
