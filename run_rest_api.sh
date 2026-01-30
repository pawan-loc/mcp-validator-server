#!/bin/bash
# run_rest_api.sh - Start MCP validators as REST API

cd /Users/pawan/pawan/dev/python/MCPs
source .venv/bin/activate

echo "🚀 Starting MCP Validation REST API"
echo "📍 API docs: http://localhost:8000/docs"
echo "📍 Health check: http://localhost:8000/health"
echo "📍 Root endpoint: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python src/mcp_validation_server/rest_api.py
