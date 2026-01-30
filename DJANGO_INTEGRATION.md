# Django Integration Guide - MCP Validation Server

This guide shows you how to integrate the MCP Validation Server with your Django project.

## 📋 Table of Contents
- [Installation](#installation)
- [Using Validators in Django](#using-validators-in-django)
- [Django Forms Integration](#django-forms-integration)
- [Django REST Framework Integration](#django-rest-framework-integration)
- [Claude Desktop MCP Configuration](#claude-desktop-mcp-configuration)

---

## Installation

### Option 1: Install from Source (Recommended for Development)
```bash
# Navigate to your Django project
cd /path/to/your/django-project

# Activate your Django virtual environment
source venv/bin/activate  # or your venv path

# Install the MCP validation server in editable mode
pip install -e /Users/pawan/pawan/dev/python/MCPs
```

### Option 2: Install from GitHub (Production)
```bash
pip install git+https://github.com/pawan-loc/mcp-validator-server.git
```

### Option 3: Add to requirements.txt
```txt
# requirements.txt
# For development (editable install)
-e /Users/pawan/pawan/dev/python/MCPs

# OR for production (from GitHub)
git+https://github.com/pawan-loc/mcp-validator-server.git
```

---

## Using Validators in Django

### 1. Basic Usage in Django Views

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url

@require_http_methods(["POST"])
def validate_user_input(request):
    """Validate user input using MCP validators."""
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    website = request.POST.get('website')
    
    results = {
        'email': validate_email(email) if email else None,
        'phone': validate_phone(phone) if phone else None,
        'url': validate_url(website) if website else None,
    }
    
    return JsonResponse(results)
```

### 2. Using in Django Models

```python
# models.py
from django.db import models
from django.core.exceptions import ValidationError
from mcp_validation_server.validators.email import validate_email as mcp_validate_email
from mcp_validation_server.validators.phone import validate_phone as mcp_validate_phone

def validate_email_field(value):
    """Custom Django validator using MCP email validator."""
    result = mcp_validate_email(value)
    if not result['valid']:
        raise ValidationError(result['message'])

def validate_phone_field(value):
    """Custom Django validator using MCP phone validator."""
    result = mcp_validate_phone(value)
    if not result['valid']:
        raise ValidationError(result['message'])

class User(models.Model):
    email = models.EmailField(
        validators=[validate_email_field],
        help_text="Email validated using MCP validator"
    )
    phone = models.CharField(
        max_length=20,
        validators=[validate_phone_field],
        help_text="E.164 format: +[country][number]"
    )
    website = models.URLField(blank=True, null=True)
    
    def clean(self):
        """Additional validation at model level."""
        super().clean()
        
        # Validate email
        email_result = mcp_validate_email(self.email)
        if not email_result['valid']:
            raise ValidationError({'email': email_result['message']})
        
        # Validate phone
        phone_result = mcp_validate_phone(self.phone)
        if not phone_result['valid']:
            raise ValidationError({'phone': phone_result['message']})
```

---

## Django Forms Integration

### 1. Custom Form Validators

```python
# forms.py
from django import forms
from django.core.exceptions import ValidationError
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url
from mcp_validation_server.validators.custom_regex import validate_regex

class ContactForm(forms.Form):
    """Contact form with MCP validation."""
    
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    website = forms.URLField(required=False)
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_email(self):
        """Validate email using MCP validator."""
        email = self.cleaned_data.get('email')
        result = validate_email(email)
        
        if not result['valid']:
            raise ValidationError(result['message'])
        
        return email
    
    def clean_phone(self):
        """Validate phone using MCP validator."""
        phone = self.cleaned_data.get('phone')
        result = validate_phone(phone)
        
        if not result['valid']:
            raise ValidationError(f"{result['message']}. Expected format: +[country][number]")
        
        return phone
    
    def clean_website(self):
        """Validate URL using MCP validator."""
        website = self.cleaned_data.get('website')
        if not website:
            return website
            
        result = validate_url(website)
        
        if not result['valid']:
            raise ValidationError(result['message'])
        
        return website

class RegistrationForm(forms.Form):
    """User registration with custom regex validation."""
    
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    
    def clean_username(self):
        """Validate username: 3-20 chars, alphanumeric + underscore."""
        username = self.cleaned_data.get('username')
        
        result = validate_regex(
            text=username,
            pattern=r'^[a-zA-Z0-9_]{3,20}$',
            description="Username must be 3-20 characters, alphanumeric or underscore"
        )
        
        if not result['valid']:
            raise ValidationError(result['message'])
        
        return username
    
    def clean_password(self):
        """Validate password strength."""
        password = self.cleaned_data.get('password')
        
        # At least 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char
        result = validate_regex(
            text=password,
            pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            description="Password must have 8+ chars with uppercase, lowercase, digit, and special character"
        )
        
        if not result['valid']:
            raise ValidationError(result['message'])
        
        return password
```

### 2. ModelForm Integration

```python
# forms.py
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    """ModelForm with MCP validators."""
    
    class Meta:
        model = User
        fields = ['email', 'phone', 'website']
    
    def clean_email(self):
        from mcp_validation_server.validators.email import validate_email
        
        email = self.cleaned_data.get('email')
        result = validate_email(email)
        
        if not result['valid']:
            raise forms.ValidationError(result['message'])
        
        return email
```

---

## Django REST Framework Integration

### 1. Custom DRF Validators

```python
# validators.py
from rest_framework import serializers
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url

def drf_email_validator(value):
    """DRF validator for email."""
    result = validate_email(value)
    if not result['valid']:
        raise serializers.ValidationError(result['message'])

def drf_phone_validator(value):
    """DRF validator for phone."""
    result = validate_phone(value)
    if not result['valid']:
        raise serializers.ValidationError(result['message'])

def drf_url_validator(value):
    """DRF validator for URL."""
    result = validate_url(value)
    if not result['valid']:
        raise serializers.ValidationError(result['message'])
```

### 2. Serializer Integration

```python
# serializers.py
from rest_framework import serializers
from .models import User
from .validators import drf_email_validator, drf_phone_validator, drf_url_validator

class UserSerializer(serializers.ModelSerializer):
    """User serializer with MCP validators."""
    
    email = serializers.EmailField(validators=[drf_email_validator])
    phone = serializers.CharField(validators=[drf_phone_validator])
    website = serializers.URLField(
        required=False,
        allow_blank=True,
        validators=[drf_url_validator]
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'website']

class ContactSerializer(serializers.Serializer):
    """Contact form serializer."""
    
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(validators=[drf_email_validator])
    phone = serializers.CharField(validators=[drf_phone_validator])
    message = serializers.CharField()
    
    def create(self, validated_data):
        # Your creation logic here
        pass
```

### 3. API View Example

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone

class ValidateInputView(APIView):
    """API endpoint to validate various inputs."""
    
    def post(self, request):
        """
        POST /api/validate/
        Body: {
            "email": "user@example.com",
            "phone": "+14155552671"
        }
        """
        email = request.data.get('email')
        phone = request.data.get('phone')
        
        results = {}
        
        if email:
            results['email'] = validate_email(email)
        
        if phone:
            results['phone'] = validate_phone(phone)
        
        # Check if all validations passed
        all_valid = all(
            result['valid'] 
            for result in results.values()
        )
        
        return Response(
            {
                'all_valid': all_valid,
                'results': results
            },
            status=status.HTTP_200_OK
        )
```

---

## Claude Desktop MCP Configuration

### Configuration File

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "validation": {
      "command": "/Users/pawan/pawan/dev/python/MCPs/.venv/bin/python",
      "args": ["-m", "mcp_validation_server"],
      "env": {}
    }
  }
}
```

### Available MCP Tools

Once configured, Claude Desktop will have access to these tools:

1. **validate_email** - Validate email addresses (RFC 5322)
2. **validate_phone** - Validate phone numbers (E.164 format)
3. **validate_url** - Validate HTTP/HTTPS URLs
4. **validate_regex** - Test custom regex patterns with flags

### Example Claude Usage

Ask Claude:
- "Validate this email: user@example.com"
- "Check if +14155552671 is a valid phone number"
- "Is https://example.com a valid URL?"
- "Test if 'username123' matches pattern ^[a-zA-Z0-9_]{3,20}$"

---

## Complete Django Example

Here's a complete example combining everything:

### models.py
```python
from django.db import models
from django.core.exceptions import ValidationError
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        super().clean()
        
        # Validate email
        email_result = validate_email(self.email)
        if not email_result['valid']:
            raise ValidationError({'email': email_result['message']})
        
        # Validate phone
        phone_result = validate_phone(self.phone)
        if not phone_result['valid']:
            raise ValidationError({'phone': phone_result['message']})
    
    def __str__(self):
        return f"{self.name} ({self.email})"
```

### forms.py
```python
from django import forms
from .models import Customer
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'website']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        result = validate_email(email)
        if not result['valid']:
            raise forms.ValidationError(result['message'])
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        result = validate_phone(phone)
        if not result['valid']:
            raise forms.ValidationError(f"{result['message']}. Use E.164 format: +[country][number]")
        return phone
```

### views.py
```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerForm

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'customers/create.html', {'form': form})
```

### urls.py
```python
from django.urls import path
from . import views

urlpatterns = [
    path('customers/create/', views.create_customer, name='customer_create'),
]
```

### Template (templates/customers/create.html)
```html
{% extends 'base.html' %}

{% block content %}
<h1>Create Customer</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Customer</button>
</form>

<div class="help-text">
    <p><strong>Email:</strong> Standard email format (e.g., user@example.com)</p>
    <p><strong>Phone:</strong> E.164 format (e.g., +14155552671)</p>
    <p><strong>Website:</strong> HTTP/HTTPS URL (e.g., https://example.com)</p>
</div>
{% endblock %}
```

---

## Testing

### Unit Tests

```python
# tests/test_validators.py
from django.test import TestCase
from mcp_validation_server.validators.email import validate_email
from mcp_validation_server.validators.phone import validate_phone
from mcp_validation_server.validators.url import validate_url

class ValidatorTests(TestCase):
    
    def test_email_validation(self):
        """Test email validator."""
        # Valid emails
        self.assertTrue(validate_email('user@example.com')['valid'])
        self.assertTrue(validate_email('test.user@domain.co.uk')['valid'])
        
        # Invalid emails
        self.assertFalse(validate_email('invalid.email')['valid'])
        self.assertFalse(validate_email('@example.com')['valid'])
    
    def test_phone_validation(self):
        """Test phone validator."""
        # Valid phones
        self.assertTrue(validate_phone('+14155552671')['valid'])
        self.assertTrue(validate_phone('+442071234567')['valid'])
        
        # Invalid phones
        self.assertFalse(validate_phone('1234567890')['valid'])
        self.assertFalse(validate_phone('+1')['valid'])
    
    def test_url_validation(self):
        """Test URL validator."""
        # Valid URLs
        self.assertTrue(validate_url('https://example.com')['valid'])
        self.assertTrue(validate_url('http://localhost:8000')['valid'])
        
        # Invalid URLs
        self.assertFalse(validate_url('ftp://example.com')['valid'])
        self.assertFalse(validate_url('not-a-url')['valid'])
```

### Model Tests

```python
# tests/test_models.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Customer

class CustomerModelTests(TestCase):
    
    def test_valid_customer(self):
        """Test creating valid customer."""
        customer = Customer(
            name='John Doe',
            email='john@example.com',
            phone='+14155552671'
        )
        customer.full_clean()  # Should not raise
        customer.save()
        self.assertIsNotNone(customer.id)
    
    def test_invalid_email(self):
        """Test invalid email raises error."""
        customer = Customer(
            name='Jane Doe',
            email='invalid.email',
            phone='+14155552671'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()
    
    def test_invalid_phone(self):
        """Test invalid phone raises error."""
        customer = Customer(
            name='Bob Smith',
            email='bob@example.com',
            phone='1234567890'
        )
        with self.assertRaises(ValidationError):
            customer.full_clean()
```

---

## Troubleshooting

### Import Errors
```bash
# Ensure the package is installed
pip list | grep mcp-validation-server

# Reinstall if needed
pip install -e /Users/pawan/pawan/dev/python/MCPs
```

### Validation Not Working
```python
# Test validators directly in Django shell
python manage.py shell

from mcp_validation_server.validators.email import validate_email
result = validate_email('test@example.com')
print(result)
```

### MCP Server Not Connecting
1. Check Claude Desktop config path is correct
2. Verify Python path: `/Users/pawan/pawan/dev/python/MCPs/.venv/bin/python`
3. Restart Claude Desktop after config changes
4. Check Claude Desktop logs for errors

---

## Resources

- **MCP Server Repo**: https://github.com/pawan-loc/mcp-validator-server
- **Django Docs**: https://docs.djangoproject.com/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Regex Tester**: https://regex101.com/

---

## Support

For issues or questions:
1. Check the [GitHub Issues](https://github.com/pawan-loc/mcp-validator-server/issues)
2. Review the [USAGE.md](USAGE.md) documentation
3. Test validators in Django shell before using in production

---

**Happy Validating! 🚀**
