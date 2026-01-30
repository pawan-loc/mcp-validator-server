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
