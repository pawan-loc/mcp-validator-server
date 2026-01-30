"""
rest_api.py - REST API wrapper for MCP validators

Copyright (c) 2025, Footfallz LLC

modification history
--------------------
01a,30jan26,pwn  written.

DESCRIPTION
Provides REST API endpoints for validation functions.
This is a simpler alternative to SSE for remote access.
"""

# Standard library imports
from typing import Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Local imports
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url
from mcp_validation_server.validators.custom_regex import validate_regex


# Request models
class EmailRequest(BaseModel):
    """Email validation request."""
    email: str = Field(..., description="Email address to validate")


class PhoneRequest(BaseModel):
    """Phone validation request."""
    phone: str = Field(..., description="Phone number to validate (E.164 format)")


class URLRequest(BaseModel):
    """URL validation request."""
    url: str = Field(..., description="URL to validate")


class RegexRequest(BaseModel):
    """Regex validation request."""
    text: str = Field(..., description="Text to validate")
    pattern: str = Field(..., description="Regex pattern")
    description: Optional[str] = Field(None, description="Pattern description")
    flags: Optional[int] = Field(0, description="Regex flags")


# Response model
class ValidationResponse(BaseModel):
    """Validation response."""
    valid: bool
    input: str
    message: str
    details: Optional[dict] = None


# Create FastAPI app
app = FastAPI(
    title="MCP Validation Server API",
    description="REST API for email, phone, URL, and regex validation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "service": "MCP Validation Server",
        "version": "1.0.0",
        "endpoints": {
            "email": "/validate/email",
            "phone": "/validate/phone",
            "url": "/validate/url",
            "regex": "/validate/regex",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mcp-validation-server"}


@app.post("/validate/email", response_model=ValidationResponse)
def validate_email_endpoint(request: EmailRequest):
    """
    Validate email address.
    
    Validates according to RFC 5322 standards (simplified).
    
    Example:
        POST /validate/email
        {"email": "user@example.com"}
        
    Returns:
        {"valid": true, "input": "user@example.com", "message": "Valid email format"}
    """
    try:
        result = validate_email(request.email)
        return ValidationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/phone", response_model=ValidationResponse)
def validate_phone_endpoint(request: PhoneRequest):
    """
    Validate phone number.
    
    Expects E.164 format: +[country code][number]
    
    Example:
        POST /validate/phone
        {"phone": "+14155552671"}
        
    Returns:
        {"valid": true, "input": "+14155552671", "message": "Valid E.164 phone number"}
    """
    try:
        result = validate_phone(request.phone)
        return ValidationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/url", response_model=ValidationResponse)
def validate_url_endpoint(request: URLRequest):
    """
    Validate HTTP/HTTPS URL.
    
    Only accepts http:// and https:// schemes.
    
    Example:
        POST /validate/url
        {"url": "https://example.com"}
        
    Returns:
        {"valid": true, "input": "https://example.com", "message": "Valid URL"}
    """
    try:
        result = validate_url(request.url)
        return ValidationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/regex", response_model=ValidationResponse)
def validate_regex_endpoint(request: RegexRequest):
    """
    Validate text against regex pattern.
    
    Supports custom patterns with optional flags.
    
    Example:
        POST /validate/regex
        {
            "text": "username123",
            "pattern": "^[a-zA-Z0-9_]{3,20}$",
            "description": "Username format"
        }
        
    Returns:
        {"valid": true, "input": "username123", "message": "Pattern matched"}
    """
    try:
        result = validate_regex(
            text=request.text,
            pattern=request.pattern,
            description=request.description,
            flags=request.flags
        )
        return ValidationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting MCP Validation REST API")
    print("📍 API docs: http://localhost:8000/docs")
    print("📍 Health check: http://localhost:8000/health")
    print("📍 Root: http://localhost:8000/")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
