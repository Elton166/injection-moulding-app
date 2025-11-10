# API Token Authentication Guide

## Overview
The eCommerce API uses JWT (JSON Web Token) authentication. All tests have been completed successfully, and token authentication is working correctly.

## Authentication Flow

### 1. Login to Get Token
**Endpoint:** `POST /api/auth/login/`

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Use the Access Token
Include the access token in the `Authorization` header for all protected endpoints:

```
Authorization: Bearer <your_access_token>
```

### 3. Example with cURL
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "vendor1", "password": "testpass123"}'

# Use the token
curl -X GET http://127.0.0.1:8000/api/stores/my-stores/ \
  -H "Authorization: Bearer <your_access_token>"
```

### 4. Example with Python Requests
```python
import requests

# Login
response = requests.post(
    'http://127.0.0.1:8000/api/auth/login/',
    json={'username': 'vendor1', 'password': 'testpass123'}
)
token = response.json()['access']

# Use the token
headers = {'Authorization': f'Bearer {token}'}
response = requests.get(
    'http://127.0.0.1:8000/api/stores/my-stores/',
    headers=headers
)
print(response.json())
```

### 5. Example with JavaScript/Fetch
```javascript
// Login
const loginResponse = await fetch('http://127.0.0.1:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'vendor1',
    password: 'testpass123'
  })
});
const { access } = await loginResponse.json();

// Use the token
const response = await fetch('http://127.0.0.1:8000/api/stores/my-stores/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
const data = await response.json();
console.log(data);
```

## Token Lifetime
- **Access Token:** 24 hours
- **Refresh Token:** 7 days

## Refresh Token
When your access token expires, use the refresh token to get a new one:

**Endpoint:** `POST /api/auth/refresh/`

**Request:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_access_token",
  "refresh": "new_refresh_token"
}
```

## Protected Endpoints
The following endpoints require authentication:

### Vendor Only
- `POST /api/stores/` - Create store
- `PUT/PATCH /api/stores/{id}/` - Update own store
- `DELETE /api/stores/{id}/` - Delete own store
- `GET /api/stores/my-stores/` - List own stores
- `POST /api/products/` - Create product
- `PUT/PATCH /api/products/{id}/` - Update own product
- `DELETE /api/products/{id}/` - Delete own product
- `GET /api/products/my-products/` - List own products

### Authenticated Users
- `GET /api/auth/profile/` - Get user profile

### Vendor Only (Reviews)
- `POST /api/products/{id}/reviews/` - Create review (vendors only)
- `PUT/PATCH /api/reviews/{id}/` - Update own review
- `DELETE /api/reviews/{id}/` - Delete own review

## Public Endpoints (No Authentication Required)
- `GET /api/` - API overview
- `GET /api/stores/` - List all stores
- `GET /api/stores/{id}/` - Get store details
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `GET /api/products/{id}/reviews/` - List product reviews
- `GET /api/vendors/{id}/stores/` - List vendor stores
- `GET /api/vendors/{id}/products/` - List vendor products

## Error Responses

### 401 Unauthorized - No Token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 401 Unauthorized - Invalid Token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### 403 Forbidden - Insufficient Permissions
```json
{
  "detail": "You do not have permission to perform this action."
}
```

## Testing
Run the comprehensive test suite to verify all endpoints:
```bash
python test_all_endpoints.py
```

## Test Users
- **Vendor:** username: `vendor1`, password: `testpass123`
- **Buyer:** username: `buyer1`, password: `testpass123`

## Verification Results
✓ All 26 endpoint tests passed successfully
✓ Token authentication is working correctly
✓ Authorization rules are properly enforced
✓ Public endpoints are accessible without authentication
✓ Protected endpoints require valid tokens
✓ Invalid tokens are correctly rejected
✓ Unauthenticated requests to protected endpoints are correctly rejected
✓ Only vendors can create reviews (buyers are correctly rejected with 403)
