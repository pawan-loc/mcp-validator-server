"""Custom regex pattern validation tool."""

import re
from mcp_validation_server.server import mcp


@mcp.tool()
def validate_regex(text: str, pattern: str, flags: str = "") -> dict:
    """
    Validate text against a custom regex pattern.
    
    Allows users to test their own regex patterns with optional flags.
    Safe compilation with error handling for invalid patterns.
    
    Args:
        text: Text to validate against the pattern
        pattern: Regular expression pattern to match
        flags: Optional regex flags as string (i, m, s, x, a)
               i = ignore case
               m = multiline
               s = dotall (. matches newline)
               x = verbose (ignore whitespace in pattern)
               a = ASCII-only matching
        
    Returns:
        dict with 'valid' (bool), 'input' (str), 'pattern' (str), 
        'message' (str), and optional 'match' (str)
        
    Example:
        >>> validate_regex("Hello123", r"\\d+", "")
        {
            'valid': True,
            'input': 'Hello123',
            'pattern': '\\\\d+',
            'message': 'Pattern matched',
            'match': '123'
        }
        
        >>> validate_regex("hello", "HELLO", "i")
        {
            'valid': True,
            'input': 'hello',
            'pattern': 'HELLO',
            'message': 'Pattern matched (case-insensitive)',
            'match': 'hello'
        }
    """
    # Parse flags
    regex_flags = 0
    flag_descriptions = []
    
    if "i" in flags.lower():
        regex_flags |= re.IGNORECASE
        flag_descriptions.append("case-insensitive")
    if "m" in flags.lower():
        regex_flags |= re.MULTILINE
        flag_descriptions.append("multiline")
    if "s" in flags.lower():
        regex_flags |= re.DOTALL
        flag_descriptions.append("dotall")
    if "x" in flags.lower():
        regex_flags |= re.VERBOSE
        flag_descriptions.append("verbose")
    if "a" in flags.lower():
        regex_flags |= re.ASCII
        flag_descriptions.append("ASCII-only")
    
    # Try to compile and match pattern
    try:
        compiled_pattern = re.compile(pattern, regex_flags)
        match = compiled_pattern.search(text)
        
        if match:
            flag_note = f" ({', '.join(flag_descriptions)})" if flag_descriptions else ""
            return {
                "valid": True,
                "input": text,
                "pattern": pattern,
                "message": f"Pattern matched{flag_note}",
                "match": match.group(0)
            }
        else:
            return {
                "valid": False,
                "input": text,
                "pattern": pattern,
                "message": "Pattern did not match",
            }
            
    except re.error as e:
        return {
            "valid": False,
            "input": text,
            "pattern": pattern,
            "message": f"Invalid regex pattern: {str(e)}",
        }
    except Exception as e:
        return {
            "valid": False,
            "input": text,
            "pattern": pattern,
            "message": f"Error: {str(e)}",
        }
