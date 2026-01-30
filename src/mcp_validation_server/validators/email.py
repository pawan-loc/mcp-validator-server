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
