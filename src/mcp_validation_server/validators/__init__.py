"""Validator module - auto-imports all validators for registration."""

# Import all validators to trigger @mcp.tool() registration
from . import email
from . import phone
from . import url
from . import custom_regex

__all__ = ["email", "phone", "url", "custom_regex"]
