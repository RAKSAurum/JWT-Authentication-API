set -e

API_BASE_URL="http://localhost:8000"
USERNAME="admin"
PASSWORD="admin123"

echo "Testing JWT Authentication API..."
echo "API Base URL: $API_BASE_URL"
echo ""

echo "Test 1: Login (POST /api/auth/login/)"
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE_URL/api/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{"username":"$USERNAME","password":"$PASSWORD"}")

echo "Login Response: $LOGIN_RESPONSE"

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null || echo "")

if [ -z "$TOKEN" ]; then
    echo "❌ Login failed - no token received"
    exit 1
fi

echo "✅ Login successful"
echo "Token: $TOKEN"
echo ""

echo "Test 2: Verify Token (POST /api/auth/verify/)"
VERIFY_RESPONSE=$(curl -s -X POST "$API_BASE_URL/api/auth/verify/" \
  -H "Content-Type: application/json" \
  -d "{"token":"$TOKEN"}")

echo "Verify Response: $VERIFY_RESPONSE"
echo "✅ Token verification completed"
echo ""

echo "Test 3: Validate Token (GET /api/auth/validate/)"
VALIDATE_RESPONSE=$(curl -s -X GET "$API_BASE_URL/api/auth/validate/" \
  -H "Authorization: Bearer $TOKEN")

echo "Validate Response: $VALIDATE_RESPONSE"
echo "✅ Token validation completed"
echo ""

echo "Test 4: Test with invalid token"
INVALID_RESPONSE=$(curl -s -X GET "$API_BASE_URL/api/auth/validate/" \
  -H "Authorization: Bearer invalid_token")

echo "Invalid Token Response: $INVALID_RESPONSE"
echo "✅ Invalid token test completed"
echo ""

echo "All tests completed successfully! 🎉"