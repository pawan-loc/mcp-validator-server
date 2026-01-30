#!/bin/bash
# test_rest_api.sh - Test REST API endpoints

echo "🧪 Testing MCP Validation REST API"
echo ""

# Health check
echo "1️⃣ Testing health endpoint..."
curl -s http://localhost:8000/health | python -m json.tool
echo ""

# Root endpoint
echo "2️⃣ Testing root endpoint..."
curl -s http://localhost:8000/ | python -m json.tool
echo ""

# Email validation
echo "3️⃣ Testing email validation..."
echo "Valid email (test@example.com):"
curl -s -X POST http://localhost:8000/validate/email \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}' | python -m json.tool
echo ""

echo "Invalid email (invalid.email):"
curl -s -X POST http://localhost:8000/validate/email \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid.email"}' | python -m json.tool
echo ""

# Phone validation
echo "4️⃣ Testing phone validation..."
echo "Valid phone (+14155552671):"
curl -s -X POST http://localhost:8000/validate/phone \
  -H "Content-Type: application/json" \
  -d '{"phone": "+14155552671"}' | python -m json.tool
echo ""

echo "Invalid phone (1234567890):"
curl -s -X POST http://localhost:8000/validate/phone \
  -H "Content-Type: application/json" \
  -d '{"phone": "1234567890"}' | python -m json.tool
echo ""

# URL validation
echo "5️⃣ Testing URL validation..."
echo "Valid URL (https://example.com):"
curl -s -X POST http://localhost:8000/validate/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' | python -m json.tool
echo ""

echo "Invalid URL (ftp://example.com):"
curl -s -X POST http://localhost:8000/validate/url \
  -H "Content-Type: application/json" \
  -d '{"url": "ftp://example.com"}' | python -m json.tool
echo ""

# Regex validation
echo "6️⃣ Testing regex validation..."
echo "Username format (username123 vs abc!):"
curl -s -X POST http://localhost:8000/validate/regex \
  -H "Content-Type: application/json" \
  -d '{"text": "username123", "pattern": "^[a-zA-Z0-9_]{3,20}$", "description": "Username format"}' | python -m json.tool
echo ""

curl -s -X POST http://localhost:8000/validate/regex \
  -H "Content-Type: application/json" \
  -d '{"text": "abc!", "pattern": "^[a-zA-Z0-9_]{3,20}$", "description": "Username format"}' | python -m json.tool
echo ""

echo "✅ All tests complete!"
echo "📍 View API docs at: http://localhost:8000/docs"
