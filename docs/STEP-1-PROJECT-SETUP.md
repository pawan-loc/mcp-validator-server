# Step 1: Project Setup & Structure

**Time Estimate:** 15 minutes  
**Dependencies:** Python 3.10+, pip or uv

## Objectives
1. Create Python project structure
2. Configure `pyproject.toml`
3. Install MCP SDK
4. Set up base server files

## Directory Structure
```
MCPs/
├── src/
│   └── mcp_validation_server/
│       ├── __init__.py
│       ├── __main__.py
│       ├── server.py
│       └── validators/
│           └── __init__.py
├── pyproject.toml
├── PRD.md
└── docs/
    └── [planning files]
```

## File: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mcp-validation-server"
version = "0.1.0"
description = "MCP server for input validation (email, phone, URL, regex)"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]
```

## File: `src/mcp_validation_server/__init__.py`
```python
"""MCP Validation Server - Input validation tools for MCP clients."""

__version__ = "0.1.0"
```

## File: `src/mcp_validation_server/server.py`
```python
"""FastMCP server instance and configuration."""

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("Validation Server")

# Validators will auto-register via decorators
```

## File: `src/mcp_validation_server/__main__.py`
```python
"""Entry point for MCP validation server."""

import asyncio
from mcp_validation_server.server import mcp
from mcp_validation_server import validators  # Triggers registration

def main():
    """Run the MCP server."""
    asyncio.run(mcp.run())

if __name__ == "__main__":
    main()
```

## File: `src/mcp_validation_server/validators/__init__.py`
```python
"""Validator module - auto-imports all validators for registration."""

# Import all validators to trigger @mcp.tool() registration
from . import email
from . import phone
from . import url
from . import custom_regex

__all__ = ["email", "phone", "url", "custom_regex"]
```

## Installation Commands
```bash
# Navigate to project directory
cd /Users/pawan/pawan/dev/python/MCPs

# Install dependencies
pip install -e .

# Or with uv (faster)
uv pip install -e .
```

## Verification
```bash
# Check Python version
python --version  # Should show 3.10.13

# Verify MCP SDK installed
python -c "import mcp; print(mcp.__version__)"
```

## Success Criteria
- ✅ `pyproject.toml` created with MCP SDK dependency
- ✅ Proper package structure in `src/mcp_validation_server/`
- ✅ MCP SDK installed successfully
- ✅ Server entry point (`__main__.py`) ready
- ✅ Validator auto-registration system in place

## Next Step
Proceed to [STEP-2-EMAIL-VALIDATOR.md](STEP-2-EMAIL-VALIDATOR.md) to implement the first validator.
