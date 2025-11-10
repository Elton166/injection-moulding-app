# Quick Token Authentication Test

## Quick Test (Copy & Paste)

### 1. Start Server
```bash
python manage.py runserver
```

### 2. Test in Another Terminal

#### Using cURL (Windows CMD):
```bash
# Get token
curl -X POST http://127.0.0.1:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"username\": \"vendor1\", \"password\": \"testpass123\"}"

# Use token (replace YOUR_TOKEN with the access token from above)
curl -X GET http://127.0.0.1:8000/api/stores/my-stores/ -H "Authorization: Bearer YOUR_TOKEN"
```

#### Using Python:
```python
import requests

# Get token
response = requests.post(
    'http://127.0.0.1:8000/api/auth/login/',
    json={'username': 'vendor1', 'password': 'testpass123'}
)
token = response.json()['access']
print(f"Token: {token[:50]}...")

# Use token
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://127.0.0.1:8000/api/stores/my-stores/', headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### 3. Run Automated Tests
```bash
# Basic token test
python test_token_auth.py

# Comprehensive test (all 25 endpoints)
python test_all_endpoints.py
```

## Expected Results
- Login returns `access` and `refresh` tokens
- Using the token returns 200 OK with data
- Without token returns 401 Unauthorized
- Invalid token returns 401 with "Token is invalid or expired"

## Test Users
- **Vendor:** `vendor1` / `testpass123`
- **Buyer:** `buyer1` / `testpass123`

## Status: ✓ VERIFIED
All token authentication is working correctly. All 25 endpoint tests passed.
