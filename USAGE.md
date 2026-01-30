# Usage Examples

## Email Validation

### Valid Emails
```python
validate_email("user@example.com")
validate_email("john.doe@company.co.uk")
validate_email("test+tag@domain.org")
```

### Invalid Emails
```python
validate_email("plaintext")        # No @ symbol
validate_email("@example.com")     # No username
validate_email("user@domain")      # No TLD
```

## Phone Validation

### Valid Phone Numbers (E.164)
```python
validate_phone("+12025551234")     # USA
validate_phone("+442071838750")    # UK
validate_phone("+919876543210")    # India
```

### Invalid Phone Numbers
```python
validate_phone("2025551234")       # Missing + prefix
validate_phone("+0123456789")      # Can't start with 0
validate_phone("+1 202 555 1234")  # Contains spaces
```

## URL Validation

### Valid URLs
```python
validate_url("https://example.com")
validate_url("http://sub.domain.com/path")
validate_url("https://example.com:8080")
```

### Invalid URLs
```python
validate_url("ftp://example.com")      # Wrong scheme
validate_url("example.com")            # No scheme
validate_url("javascript:alert(1)")    # Unsafe scheme
```

## Custom Regex

### Extract Numbers
```python
validate_regex("Order #12345", r"\d+", "")
# → {"valid": true, "match": "12345"}
```

### Case-Insensitive Match
```python
validate_regex("Hello World", "hello", "i")
# → {"valid": true, "match": "Hello"}
```

### Hex Color Validation
```python
validate_regex("#FF5733", r"^#[0-9A-Fa-f]{6}$", "")
# → {"valid": true, "match": "#FF5733"}
```

### Invalid Pattern
```python
validate_regex("test", "[invalid", "")
# → {"valid": false, "message": "Invalid regex pattern: ..."}
```
