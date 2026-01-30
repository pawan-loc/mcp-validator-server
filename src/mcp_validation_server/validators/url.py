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
