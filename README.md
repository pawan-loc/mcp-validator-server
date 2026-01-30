# MCP Validation Server

A modular Model Context Protocol (MCP) server providing input validation tools for Claude Desktop and other MCP clients.

## Features

- ✅ **Email Validation** - RFC 5322 format validation
- ✅ **Phone Validation** - E.164 international format
- ✅ **URL Validation** - HTTP/HTTPS URLs only
- ✅ **Custom Regex** - Test your own patterns with flags

## Requirements

- Python 3.10+
- MCP SDK (`mcp>=1.0.0`)

## Installation

```bash
# Clone or navigate to project
cd /Users/pawan/pawan/dev/python/MCPs

# Install with pip
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

## Usage

### With Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "validation": {
      "command": "python",
      "args": ["-m", "mcp_validation_server"],
      "cwd": "/Users/pawan/pawan/dev/python/MCPs"
    }
  }
}
```

Restart Claude Desktop, then use validation tools in your conversations!

### Standalone Testing

```bash
# Run the server
python -m mcp_validation_server

# Or use MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector python -m mcp_validation_server
```

## Available Tools

### 1. validate_email
Validates email addresses.

**Parameters:**
- `email` (string): Email address to validate

**Example:**
```
validate_email("user@example.com")
→ {"valid": true, "message": "Valid email format"}
```

### 2. validate_phone
Validates phone numbers in E.164 format.

**Parameters:**
- `phone_number` (string): Phone number with country code (+12025551234)

**Example:**
```
validate_phone("+12025551234")
→ {"valid": true, "message": "Valid E.164 phone format"}
```

### 3. validate_url
Validates HTTP/HTTPS URLs.

**Parameters:**
- `url` (string): URL to validate

**Example:**
```
validate_url("https://example.com")
→ {"valid": true, "details": {"scheme": "https", "netloc": "example.com"}}
```

### 4. validate_regex
Tests text against custom regex patterns.

**Parameters:**
- `text` (string): Text to validate
- `pattern` (string): Regex pattern
- `flags` (string, optional): Flags (i, m, s, x, a)

**Example:**
```
validate_regex("Hello123", r"\d+", "")
→ {"valid": true, "match": "123"}
```

## Architecture

Modular design with self-registering validators:

```
src/mcp_validation_server/
├── server.py           # FastMCP instance
├── __main__.py         # Entry point
└── validators/
    ├── email.py        # @mcp.tool()
    ├── phone.py        # @mcp.tool()
    ├── url.py          # @mcp.tool()
    └── custom_regex.py # @mcp.tool()
```

**Add new validator:** Create new file in `validators/`, import in `__init__.py`  
**Remove validator:** Comment out import in `validators/__init__.py`

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests (optional)
pytest tests/

# Type checking
python -m mypy src/
```

## Testing

### MCP Inspector (Recommended)
```bash
npx @modelcontextprotocol/inspector python -m mcp_validation_server
```

Opens browser interface to test all tools interactively.

### Direct Python Testing
```bash
python -c "from src.mcp_validation_server.validators.email import validate_email; print(validate_email('test@example.com'))"
```

## License

MIT
