"""
FastAPI HTTP API for MCP Validation Server
Standalone REST API - no MCP dependencies needed for clients
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import validators directly (no MCP needed)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url
from mcp_validation_server.validators.custom_regex import validate_regex

app = FastAPI(
    title="MCP Validation API",
    description="Standalone HTTP API for input validation",
    version="0.1.0"
)

# Enable CORS for all origins (customize as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Models
class EmailRequest(BaseModel):
    email: str


class PhoneRequest(BaseModel):
    phone_number: str


class URLRequest(BaseModel):
    url: str


class RegexRequest(BaseModel):
    text: str
    pattern: str
    flags: Optional[str] = ""


# Health Check
@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "MCP Validation API",
        "status": "running",
        "version": "0.1.0",
        "endpoints": [
            "/validate/email",
            "/validate/phone",
            "/validate/url",
            "/validate/regex"
        ]
    }


# Email Validation Endpoint
@app.post("/validate/email")
def api_validate_email(request: EmailRequest):
    """
    Validate email address format
    
    Example:
        POST /validate/email
        {"email": "user@example.com"}
    """
    result = validate_email(request.email)
    if not result['valid']:
        raise HTTPException(status_code=400, detail=result)
    return result


# Phone Validation Endpoint
@app.post("/validate/phone")
def api_validate_phone(request: PhoneRequest):
    """
    Validate phone number in E.164 format
    
    Example:
        POST /validate/phone
        {"phone_number": "+12025551234"}
    """
    result = validate_phone(request.phone_number)
    if not result['valid']:
        raise HTTPException(status_code=400, detail=result)
    return result


# URL Validation Endpoint
@app.post("/validate/url")
def api_validate_url(request: URLRequest):
    """
    Validate HTTP/HTTPS URL
    
    Example:
        POST /validate/url
        {"url": "https://example.com"}
    """
    result = validate_url(request.url)
    if not result['valid']:
        raise HTTPException(status_code=400, detail=result)
    return result


# Regex Validation Endpoint
@app.post("/validate/regex")
def api_validate_regex(request: RegexRequest):
    """
    Validate text against custom regex pattern
    
    Example:
        POST /validate/regex
        {"text": "ABC123", "pattern": "^[A-Z]{3}\\d{3}$", "flags": ""}
    """
    result = validate_regex(request.text, request.pattern, request.flags)
    if not result['valid']:
        raise HTTPException(status_code=400, detail=result)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
