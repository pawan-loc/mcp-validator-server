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
# For library usage (import validators)
pip install git+https://github.com/pawan-loc/mcp-validator-server.git

# For MCP server usage
pip install "git+https://github.com/pawan-loc/mcp-validator-server.git#egg=mcp-validation-server[mcp]"

# For standalone HTTP API
pip install "git+https://github.com/pawan-loc/mcp-validator-server.git#egg=mcp-validation-server[api]"

# Install everything
pip install "git+https://github.com/pawan-loc/mcp-validator-server.git#egg=mcp-validation-server[all]"
```

## Usage

You can use this project in **two ways**:

### Option 1: As a Python Library (No AI/MCP Required)

Use the validators directly in your Python projects (Django, Flask, FastAPI, etc.):

#### Installation
```bash
# Install from GitHub
pip install git+https://github.com/pawan-loc/mcp-validator-server.git

# Or install locally
pip install -e /path/to/mcp-validator-server
```

#### Usage in Your Code
```python
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url
from mcp_validation_server.validators.custom_regex import validate_regex

# Validate email
result = validate_email("user@example.com")
print(result)  # {'valid': True, 'input': 'user@example.com', 'message': 'Valid email format'}

# Validate phone
phone_result = validate_phone("+12025551234")
print(phone_result)  # {'valid': True, ...}

# Validate URL
url_result = validate_url("https://example.com")
print(url_result)  # {'valid': True, 'details': {...}}

# Custom regex
regex_result = validate_regex("ABC123", r"^[A-Z]{3}\d{3}$", "")
print(regex_result)  # {'valid': True, 'match': 'ABC123'}
```

#### Django Example
```python
# In your Django views.py or forms.py
from mcp_validation_server.validators.email import validate_email
from django.http import JsonResponse

def register_user(request):
    email = request.POST.get('email')
    
    result = validate_email(email)
    if not result['valid']:
        return JsonResponse({'error': result['message']}, status=400)
    
    # Continue with registration...
    return JsonResponse({'success': True})
```

#### FastAPI Example
```python
from fastapi import FastAPI, HTTPException
from mcp_validation_server.validators.email import validate_email

app = FastAPI()

@app.post("/validate-email")
def validate_email_endpoint(email: str):
    result = validate_email(email)
    if not result['valid']:
        raise HTTPException(status_code=400, detail=result['message'])
    return result
```

---

### Option 3: As Standalone HTTP API (Recommended for Production)

Run the validation server as a standalone HTTP service - **no installation needed** in your client projects!

#### Start the API Server

```bash
# In the MCP validator project
cd /path/to/mcp-validator-server
pip install ".[api]"
python -m uvicorn mcp_validation_server.api:app --host 0.0.0.0 --port 8000
```

Server runs at `http://localhost:8000`

#### Use from Django (No Installation Required!)

Copy `clients/django_client.py` to your Django project, then:

```python
# In your Django views.py - just copy the client file, no pip install!
from .django_client import validate_email, validate_phone, validate_url

def register_user(request):
    email = request.POST.get('email')
    
    # Calls HTTP API - no dependencies needed!
    result = validate_email(email)
    if not result['valid']:
        return JsonResponse({'error': result['message']}, status=400)
    
    return JsonResponse({'success': True})
```

#### Or Use Requests Directly

```python
import requests

# Call the API directly
response = requests.post(
    "http://localhost:8000/validate/email",
    json={"email": "test@example.com"}
)
result = response.json()
# {'valid': True, 'input': 'test@example.com', 'message': 'Valid email format'}
```

#### API Endpoints

- `GET /` - Health check
- `POST /validate/email` - Validate email
- `POST /validate/phone` - Validate phone
- `POST /validate/url` - Validate URL
- `POST /validate/regex` - Validate with custom regex

**Advantages:**
- ✅ No dependencies in client projects
- ✅ Works with any language (Python, JavaScript, PHP, etc.)
- ✅ Easy to scale and deploy
- ✅ Centralized validation logic

---

### Option 2: As an MCP Server (For AI Clients)

Use with AI assistants like Claude Desktop:

#### With Claude Desktop

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

#### Standalone MCP Testing

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
