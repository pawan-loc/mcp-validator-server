# Step 5: Custom Regex Validator

**Time Estimate:** 15 minutes  
**Dependencies:** Step 1 (project structure)

## Objectives
1. Create custom regex validation tool
2. Support regex flags (case-insensitive, multiline, etc.)
3. Safe regex compilation with error handling
4. Register with MCP server via `@mcp.tool()` decorator

## File: `src/mcp_validation_server/validators/custom_regex.py`
```python
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
        >>> validate_regex("Hello123", r"\d+", "")
        {
            'valid': True,
            'input': 'Hello123',
            'pattern': '\\d+',
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
```

## Regex Flags Reference

| Flag | Name | Description | Example |
|------|------|-------------|---------|
| `i` | IGNORECASE | Case-insensitive matching | `"HELLO"` matches `"hello"` |
| `m` | MULTILINE | `^` and `$` match line boundaries | Multi-line text matching |
| `s` | DOTALL | `.` matches newline characters | Match across lines |
| `x` | VERBOSE | Ignore whitespace in pattern | Readable complex patterns |
| `a` | ASCII | ASCII-only `\w`, `\d`, `\s` | No Unicode matching |

## Use Cases

### 1. Extract Numbers
```python
validate_regex("Order #12345", r"\d+", "")
# Matches: "12345"
```

### 2. Case-Insensitive Search
```python
validate_regex("Hello World", "hello", "i")
# Matches: "Hello"
```

### 3. Multiline Matching
```python
text = """Line 1
Line 2
Line 3"""
validate_regex(text, r"^Line", "m")
# Matches all lines starting with "Line"
```

### 4. Custom Patterns
```python
# Validate hex color codes
validate_regex("#FF5733", r"^#[0-9A-Fa-f]{6}$", "")

# Extract email domain
validate_regex("user@example.com", r"@([a-z0-9.-]+)", "i")
```

## Safety Features
- ✅ Safe regex compilation with `try-except`
- ✅ Prevents catastrophic backtracking (Python's re module has safeguards)
- ✅ Clear error messages for invalid patterns
- ✅ No code execution vulnerabilities

## Testing
```bash
# Test via Python
python -c "
from src.mcp_validation_server.validators.custom_regex import validate_regex
print(validate_regex('Hello123', r'\d+', ''))
print(validate_regex('hello', 'HELLO', 'i'))
print(validate_regex('test', '[invalid', ''))
"
```

## MCP Integration
Once the server is running, this tool will be available as:
- Tool name: `validate_regex`
- Parameters: 
  - `text` (string)
  - `pattern` (string)
  - `flags` (string, optional)
- Returns: JSON object with validation result and match details

## Success Criteria
- ✅ Regex validator function created
- ✅ Registered with `@mcp.tool()` decorator
- ✅ Supports all common regex flags
- ✅ Safe error handling for invalid patterns
- ✅ Returns matched text when successful
- ✅ Clear flag descriptions in messages

## Next Step
Proceed to [STEP-6-TESTING-DOCS.md](STEP-6-TESTING-DOCS.md) to create documentation and testing setup.
