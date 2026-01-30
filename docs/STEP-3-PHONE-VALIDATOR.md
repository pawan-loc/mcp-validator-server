# Step 3: Phone Validator

**Time Estimate:** 10 minutes  
**Dependencies:** Step 1 (project structure)

## Objectives
1. Create phone number validation tool
2. Implement E.164 format validation
3. Register with MCP server via `@mcp.tool()` decorator (exposes function to MCP clients)

## File: `src/mcp_validation_server/validators/phone.py`
```python
"""Phone number validation tool using E.164 format."""

import re
from mcp_validation_server.server import mcp

# E.164 Phone Number Pattern
# Format: +[country code][number] (10-15 digits total)
PHONE_PATTERN = re.compile(
    r"^\+[1-9]\d{9,14}$"
)


@mcp.tool()
def validate_phone(phone_number: str) -> dict:
    """
    Validate phone number in E.164 format.
    
    E.164 is the international standard for phone numbers.
    Format: +[country code][subscriber number]
    Total length: 10-15 digits (including country code)
    
    Args:
        phone_number: Phone number to validate (must start with +)
        
    Returns:
        dict with 'valid' (bool), 'input' (str), and 'message' (str)
        
    Example:
        >>> validate_phone("+12025551234")
        {'valid': True, 'input': '+12025551234', 'message': 'Valid E.164 phone format'}
        
        >>> validate_phone("5551234")
        {'valid': False, 'input': '5551234', 'message': 'Invalid phone format. Use E.164: +[country][number]'}
    """
    is_valid = bool(PHONE_PATTERN.match(phone_number))
    
    return {
        "valid": is_valid,
        "input": phone_number,
        "message": (
            "Valid E.164 phone format" if is_valid 
            else "Invalid phone format. Use E.164: +[country][number]"
        )
    }
```

## Pattern Breakdown
```
^           # Start of string
\+          # Required + prefix
[1-9]       # Country code first digit (1-9, no leading 0)
\d{9,14}    # Remaining digits (9-14 more digits)
$           # End of string

Total: 10-15 digits (including country code)
```

## Valid Examples
- `+12025551234` (USA: +1 202-555-1234)
- `+442071838750` (UK: +44 20 7183 8750)
- `+919876543210` (India: +91 98765 43210)
- `+861234567890` (China: +86 123 4567 8900)
- `+33123456789` (France: +33 1 23 45 67 89)

## Invalid Examples
- `2025551234` (missing + prefix)
- `+0123456789` (country code can't start with 0)
- `+1234` (too short, < 10 digits)
- `+12345678901234567` (too long, > 15 digits)
- `+1 202 555 1234` (contains spaces)

## Country Code Reference
| Country | Code | Example |
|---------|------|---------|
| USA/Canada | +1 | +12025551234 |
| UK | +44 | +442071234567 |
| India | +91 | +919876543210 |
| China | +86 | +861234567890 |
| France | +33 | +33123456789 |

## Testing
```bash
# Test via Python
python -c "
from src.mcp_validation_server.validators.phone import validate_phone
print(validate_phone('+12025551234'))
print(validate_phone('5551234'))
"
```

## MCP Integration
Once the server is running, this tool will be available as:
- Tool name: `validate_phone`
- Parameter: `phone_number` (string)
- Returns: JSON object with validation result

## Success Criteria
- ✅ Phone validator function created
- ✅ Registered with `@mcp.tool()` decorator
- ✅ Validates E.164 format correctly
- ✅ Rejects invalid formats with clear messages
- ✅ Returns consistent response structure

## Next Step
Proceed to [STEP-4-URL-VALIDATOR.md](STEP-4-URL-VALIDATOR.md) to implement URL validation.
