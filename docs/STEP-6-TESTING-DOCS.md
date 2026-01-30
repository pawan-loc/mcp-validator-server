# Step 6: Testing & Documentation

**Time Estimate:** 20 minutes  
**Dependencies:** Steps 1-5 (all validators implemented)

## Objectives
1. Create comprehensive README
2. Write usage documentation
3. Set up VS Code MCP debugging
4. Optional: Add unit tests

## File: `README.md`
```markdown
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

\`\`\`bash
# Clone or navigate to project
cd /Users/pawan/pawan/dev/python/MCPs

# Install with pip
pip install -e .

# Or with uv (recommended)
uv pip install -e .
\`\`\`

## Usage

### With Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

\`\`\`json
{
  "mcpServers": {
    "validation": {
      "command": "python",
      "args": ["-m", "mcp_validation_server"],
      "cwd": "/Users/pawan/pawan/dev/python/MCPs"
    }
  }
}
\`\`\`

Restart Claude Desktop, then use validation tools in your conversations!

### Standalone Testing

\`\`\`bash
# Run the server
python -m mcp_validation_server

# Or use MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector python -m mcp_validation_server
\`\`\`

## Available Tools

### 1. validate_email
Validates email addresses.

**Parameters:**
- `email` (string): Email address to validate

**Example:**
\`\`\`
validate_email("user@example.com")
→ {"valid": true, "message": "Valid email format"}
\`\`\`

### 2. validate_phone
Validates phone numbers in E.164 format.

**Parameters:**
- `phone_number` (string): Phone number with country code (+12025551234)

**Example:**
\`\`\`
validate_phone("+12025551234")
→ {"valid": true, "message": "Valid E.164 phone format"}
\`\`\`

### 3. validate_url
Validates HTTP/HTTPS URLs.

**Parameters:**
- `url` (string): URL to validate

**Example:**
\`\`\`
validate_url("https://example.com")
→ {"valid": true, "details": {"scheme": "https", "netloc": "example.com"}}
\`\`\`

### 4. validate_regex
Tests text against custom regex patterns.

**Parameters:**
- `text` (string): Text to validate
- `pattern` (string): Regex pattern
- `flags` (string, optional): Flags (i, m, s, x, a)

**Example:**
\`\`\`
validate_regex("Hello123", r"\d+", "")
→ {"valid": true, "match": "123"}
\`\`\`

## Architecture

Modular design with self-registering validators:

\`\`\`
src/mcp_validation_server/
├── server.py           # FastMCP instance
├── __main__.py         # Entry point
└── validators/
    ├── email.py        # @mcp.tool()
    ├── phone.py        # @mcp.tool()
    ├── url.py          # @mcp.tool()
    └── custom_regex.py # @mcp.tool()
\`\`\`

**Add new validator:** Create new file in `validators/`, import in `__init__.py`  
**Remove validator:** Comment out import in `validators/__init__.py`

## Development

\`\`\`bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests (optional)
pytest tests/

# Type checking
python -m mypy src/
\`\`\`

## License

MIT
\`\`\`

## File: `USAGE.md`
```markdown
# Usage Examples

## Email Validation

### Valid Emails
\`\`\`python
validate_email("user@example.com")
validate_email("john.doe@company.co.uk")
validate_email("test+tag@domain.org")
\`\`\`

### Invalid Emails
\`\`\`python
validate_email("plaintext")        # No @ symbol
validate_email("@example.com")     # No username
validate_email("user@domain")      # No TLD
\`\`\`

## Phone Validation

### Valid Phone Numbers (E.164)
\`\`\`python
validate_phone("+12025551234")     # USA
validate_phone("+442071838750")    # UK
validate_phone("+919876543210")    # India
\`\`\`

### Invalid Phone Numbers
\`\`\`python
validate_phone("2025551234")       # Missing + prefix
validate_phone("+0123456789")      # Can't start with 0
validate_phone("+1 202 555 1234")  # Contains spaces
\`\`\`

## URL Validation

### Valid URLs
\`\`\`python
validate_url("https://example.com")
validate_url("http://sub.domain.com/path")
validate_url("https://example.com:8080")
\`\`\`

### Invalid URLs
\`\`\`python
validate_url("ftp://example.com")      # Wrong scheme
validate_url("example.com")            # No scheme
validate_url("javascript:alert(1)")    # Unsafe scheme
\`\`\`

## Custom Regex

### Extract Numbers
\`\`\`python
validate_regex("Order #12345", r"\d+", "")
# → {"valid": true, "match": "12345"}
\`\`\`

### Case-Insensitive Match
\`\`\`python
validate_regex("Hello World", "hello", "i")
# → {"valid": true, "match": "Hello"}
\`\`\`

### Hex Color Validation
\`\`\`python
validate_regex("#FF5733", r"^#[0-9A-Fa-f]{6}$", "")
# → {"valid": true, "match": "#FF5733"}
\`\`\`

### Invalid Pattern
\`\`\`python
validate_regex("test", "[invalid", "")
# → {"valid": false, "message": "Invalid regex pattern: ..."}
\`\`\`
\`\`\`

## File: `.vscode/mcp.json`
```json
{
  "mcpServers": {
    "validation": {
      "command": "python",
      "args": ["-m", "mcp_validation_server"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  }
}
```

## File: `tests/test_validators.py` (Optional)
```python
"""Unit tests for validators."""

import pytest
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url
from mcp_validation_server.validators.custom_regex import validate_regex


class TestEmailValidator:
    """Test email validation."""
    
    def test_valid_emails(self):
        """Test valid email formats."""
        assert validate_email("user@example.com")["valid"]
        assert validate_email("test+tag@domain.org")["valid"]
        
    def test_invalid_emails(self):
        """Test invalid email formats."""
        assert not validate_email("plaintext")["valid"]
        assert not validate_email("@example.com")["valid"]


class TestPhoneValidator:
    """Test phone validation."""
    
    def test_valid_phones(self):
        """Test valid E.164 phone numbers."""
        assert validate_phone("+12025551234")["valid"]
        assert validate_phone("+442071838750")["valid"]
        
    def test_invalid_phones(self):
        """Test invalid phone numbers."""
        assert not validate_phone("2025551234")["valid"]
        assert not validate_phone("+0123")["valid"]


class TestURLValidator:
    """Test URL validation."""
    
    def test_valid_urls(self):
        """Test valid HTTP/HTTPS URLs."""
        assert validate_url("https://example.com")["valid"]
        assert validate_url("http://sub.domain.com/path")["valid"]
        
    def test_invalid_urls(self):
        """Test invalid URLs."""
        assert not validate_url("ftp://example.com")["valid"]
        assert not validate_url("example.com")["valid"]


class TestRegexValidator:
    """Test custom regex validation."""
    
    def test_simple_pattern(self):
        """Test simple regex pattern."""
        result = validate_regex("Hello123", r"\d+", "")
        assert result["valid"]
        assert result["match"] == "123"
        
    def test_case_insensitive(self):
        """Test case-insensitive flag."""
        result = validate_regex("hello", "HELLO", "i")
        assert result["valid"]
        
    def test_invalid_pattern(self):
        """Test invalid regex pattern."""
        result = validate_regex("test", "[invalid", "")
        assert not result["valid"]
```

## Testing Checklist

### Manual Testing
- [ ] Install server: `pip install -e .`
- [ ] Run server: `python -m mcp_validation_server`
- [ ] Test with MCP Inspector
- [ ] Add to Claude Desktop config
- [ ] Restart Claude Desktop
- [ ] Test all 4 validators in Claude

### Unit Tests (Optional)
```bash
pytest tests/ -v
```

### Integration Testing
1. Open VS Code with `.vscode/mcp.json`
2. Use MCP debugging features
3. Verify all tools are registered
4. Test error handling

## Documentation Checklist
- [ ] README.md with installation & usage
- [ ] USAGE.md with examples for all validators
- [ ] .vscode/mcp.json for debugging
- [ ] Inline docstrings in all validators
- [ ] Claude Desktop config example
- [ ] Optional: pytest tests

## Success Criteria
- ✅ Complete README with setup instructions
- ✅ USAGE.md with examples for all 4 validators
- ✅ VS Code MCP configuration
- ✅ Works with Claude Desktop
- ✅ All validators tested and working
- ✅ Clear error messages
- ✅ Optional: Unit tests passing

## Final Steps
1. Test server standalone
2. Test with MCP Inspector
3. Configure Claude Desktop
4. Verify all tools work in Claude
5. Share project or deploy!

🎉 **Project Complete!**
