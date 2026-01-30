# Step 2: Email Validator

**Time Estimate:** 10 minutes  
**Dependencies:** Step 1 (project structure)

## Objectives
1. Create email validation tool
2. Implement RFC 5322 pattern (simplified)
3. Register with MCP server via `@mcp.tool()` decorator (makes function callable by Claude/MCP clients)

## File: `src/mcp_validation_server/validators/email.py`
```python
"""Email validation tool using regex pattern."""

import re
from mcp_validation_server.server import mcp

# RFC 5322 Email Pattern (simplified)
EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


@mcp.tool()
def validate_email(email: str) -> dict:
    """
    Validate email address format.
    
    Checks if the email matches RFC 5322 standard (simplified).
    Validates format: username@domain.tld
    
    Args:
        email: Email address to validate
        
    Returns:
        dict with 'valid' (bool), 'input' (str), and 'message' (str)
        
    Example:
        >>> validate_email("user@example.com")
        {'valid': True, 'input': 'user@example.com', 'message': 'Valid email format'}
        
        >>> validate_email("invalid.email")
        {'valid': False, 'input': 'invalid.email', 'message': 'Invalid email format'}
    """
    is_valid = bool(EMAIL_PATTERN.match(email))
    
    return {
        "valid": is_valid,
        "input": email,
        "message": "Valid email format" if is_valid else "Invalid email format"
    }
```

## Pattern Breakdown
```
^[a-zA-Z0-9._%+-]+  # Username part (letters, numbers, ._%+-)
@                   # Required @ symbol
[a-zA-Z0-9.-]+      # Domain name (letters, numbers, .-)
\.                  # Required dot
[a-zA-Z]{2,}$       # TLD (minimum 2 letters)
```

## Valid Examples
- `user@example.com`
- `john.doe@company.co.uk`
- `test+tag@domain.org`
- `user123@test-server.com`

## Invalid Examples
- `plaintext` (no @ symbol)
- `@example.com` (no username)
- `user@` (no domain)
- `user@domain` (no TLD)
- `user @example.com` (space)

## Testing
```bash
# Test via Python
python -c "
from src.mcp_validation_server.validators.email import validate_email
print(validate_email('user@example.com'))
print(validate_email('invalid'))
"
```

## MCP Integration
Once the server is running, this tool will be available as:
- Tool name: `validate_email`
- Parameter: `email` (string)
- Returns: JSON object with validation result

## What @mcp.tool() Does
The decorator:
- ✅ Exposes the function to MCP clients (Claude Desktop, etc.)
- ✅ Handles JSON-RPC communication automatically
- ✅ Generates tool description from docstring
- ✅ Without it: just regular Python (MCP can't see it)

## Success Criteria
- ✅ Email validator function created
- ✅ Registered with `@mcp.tool()` decorator
- ✅ Validates common email formats correctly
- ✅ Returns consistent response structure
- ✅ Includes helpful error messages

## Next Step
Proceed to [STEP-3-PHONE-VALIDATOR.md](STEP-3-PHONE-VALIDATOR.md) to implement phone validation.
