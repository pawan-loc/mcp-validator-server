"""
Django client for MCP Validation API
Use this in your Django project to call the standalone validation API
"""

import requests
from typing import Dict, Optional


class ValidationAPIClient:
    """Client for calling MCP Validation API from Django"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the API client
        
        Args:
            base_url: Base URL of the validation API server
        """
        self.base_url = base_url.rstrip('/')
    
    def validate_email(self, email: str) -> Dict:
        """
        Validate email address
        
        Args:
            email: Email address to validate
            
        Returns:
            dict: {'valid': bool, 'input': str, 'message': str}
        """
        try:
            response = requests.post(
                f"{self.base_url}/validate/email",
                json={"email": email}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()['detail']
        except requests.RequestException as e:
            return {
                'valid': False,
                'input': email,
                'message': f'API Error: {str(e)}'
            }
    
    def validate_phone(self, phone_number: str) -> Dict:
        """
        Validate phone number
        
        Args:
            phone_number: Phone number to validate (E.164 format)
            
        Returns:
            dict: {'valid': bool, 'input': str, 'message': str}
        """
        try:
            response = requests.post(
                f"{self.base_url}/validate/phone",
                json={"phone_number": phone_number}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()['detail']
        except requests.RequestException as e:
            return {
                'valid': False,
                'input': phone_number,
                'message': f'API Error: {str(e)}'
            }
    
    def validate_url(self, url: str) -> Dict:
        """
        Validate URL
        
        Args:
            url: URL to validate
            
        Returns:
            dict: {'valid': bool, 'input': str, 'message': str, 'details': dict}
        """
        try:
            response = requests.post(
                f"{self.base_url}/validate/url",
                json={"url": url}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()['detail']
        except requests.RequestException as e:
            return {
                'valid': False,
                'input': url,
                'message': f'API Error: {str(e)}',
                'details': {}
            }
    
    def validate_regex(self, text: str, pattern: str, flags: str = "") -> Dict:
        """
        Validate text against regex pattern
        
        Args:
            text: Text to validate
            pattern: Regex pattern
            flags: Optional regex flags (i, m, s, x, a)
            
        Returns:
            dict: {'valid': bool, 'input': str, 'pattern': str, 'message': str}
        """
        try:
            response = requests.post(
                f"{self.base_url}/validate/regex",
                json={"text": text, "pattern": pattern, "flags": flags}
            )
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()['detail']
        except requests.RequestException as e:
            return {
                'valid': False,
                'input': text,
                'pattern': pattern,
                'message': f'API Error: {str(e)}'
            }


# Singleton instance
_client = None

def get_validator_client(base_url: str = "http://localhost:8000") -> ValidationAPIClient:
    """Get or create singleton validation API client"""
    global _client
    if _client is None:
        _client = ValidationAPIClient(base_url)
    return _client


# Convenience functions
def validate_email(email: str) -> Dict:
    """Validate email via API"""
    return get_validator_client().validate_email(email)


def validate_phone(phone_number: str) -> Dict:
    """Validate phone via API"""
    return get_validator_client().validate_phone(phone_number)


def validate_url(url: str) -> Dict:
    """Validate URL via API"""
    return get_validator_client().validate_url(url)


def validate_regex(text: str, pattern: str, flags: str = "") -> Dict:
    """Validate regex via API"""
    return get_validator_client().validate_regex(text, pattern, flags)
