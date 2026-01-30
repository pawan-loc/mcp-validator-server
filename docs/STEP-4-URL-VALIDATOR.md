# Step 4: URL Validator

**Time Estimate:** 10 minutes  
**Dependencies:** Step 1 (project structure)

## Objectives
1. Create URL validation tool
2. Validate HTTP/HTTPS URLs only
3. Use `urllib.parse` for robust parsing
4. Register with MCP server via `@mcp.tool()` decorator

## File: `src/mcp_validation_server/validators/url.py`
```python
"""URL validation tool for HTTP/HTTPS URLs."""

from urllib.parse import urlparse
from mcp_validation_server.server import mcp


@mcp.tool()
def validate_url(url: str) -> dict:
    """
    Validate URL format (HTTP/HTTPS only).
    
    Checks if the URL is properly formatted and uses HTTP or HTTPS scheme.
    Uses urllib.parse for robust URL parsing.
    
    Args:
        url: URL to validate
        
    Returns:
        dict with 'valid' (bool), 'input' (str), 'message' (str), and 'details' (dict)
        
    Example:
        >>> validate_url("https://example.com/path")
        {
            'valid': True,
            'input': 'https://example.com/path',
            'message': 'Valid HTTP/HTTPS URL',
            'details': {
                'scheme': 'https',
                'netloc': 'example.com',
                'path': '/path'
            }
        }
        
        >>> validate_url("ftp://example.com")
        {
            'valid': False,
            'input': 'ftp://example.com',
            'message': 'Invalid URL scheme. Only HTTP/HTTPS allowed',
            'details': {'scheme': 'ftp'}
        }
    """
    try:
        parsed = urlparse(url)
        
        # Check if scheme is http or https
        is_valid = parsed.scheme in ["http", "https"]
        
        # Check if netloc (domain) exists
        has_domain = bool(parsed.netloc)
        
        if is_valid and has_domain:
            return {
                "valid": True,
                "input": url,
                "message": "Valid HTTP/HTTPS URL",
                "details": {
                    "scheme": parsed.scheme,
                    "netloc": parsed.netloc,
                    "path": parsed.path or "/"
                }
            }
        elif not has_domain:
            return {
                "valid": False,
                "input": url,
                "message": "Invalid URL: missing domain",
                "details": {"scheme": parsed.scheme or "none"}
            }
        else:
            return {
                "valid": False,
                "input": url,
                "message": "Invalid URL scheme. Only HTTP/HTTPS allowed",
                "details": {"scheme": parsed.scheme or "none"}
            }
            
    except Exception as e:
        return {
            "valid": False,
            "input": url,
            "message": f"URL parsing error: {str(e)}",
            "details": {}
        }
```

## URL Components
```
https://example.com:8080/path/to/resource?key=value#section
  ^       ^            ^     ^               ^         ^
  |       |            |     |               |         |
scheme  netloc       port  path            query    fragment
```

## Valid Examples
- `http://example.com`
- `https://www.example.com`
- `https://example.com/path`
- `https://example.com:8080/path`
- `https://sub.domain.example.com`
- `https://example.com/path?query=value`
- `https://example.com/path#section`

## Invalid Examples
- `ftp://example.com` (wrong scheme)
- `example.com` (no scheme)
- `http://` (no domain)
- `https:///path` (no domain)
- `file:///path/to/file` (file scheme)
- `javascript:alert(1)` (javascript scheme)

## Security Considerations
- Only allows `http` and `https` schemes
- Prevents `javascript:`, `data:`, `file:` URLs
- Validates domain presence
- Robust error handling for malformed URLs

## Testing
```bash
# Test via Python
python -c "
from src.mcp_validation_server.validators.url import validate_url
print(validate_url('https://example.com'))
print(validate_url('ftp://example.com'))
print(validate_url('example.com'))
"
```

## MCP Integration
Once the server is running, this tool will be available as:
- Tool name: `validate_url`
- Parameter: `url` (string)
- Returns: JSON object with validation result and parsed details

## Success Criteria
- ✅ URL validator function created
- ✅ Registered with `@mcp.tool()` decorator
- ✅ Validates HTTP/HTTPS URLs correctly
- ✅ Rejects non-HTTP(S) schemes
- ✅ Provides parsed URL details
- ✅ Handles malformed URLs gracefully

## Next Step
Proceed to [STEP-5-REGEX-VALIDATOR.md](STEP-5-REGEX-VALIDATOR.md) to implement custom regex validation.
