# Quick Test: Vendor-Only Reviews

## Test That Only Vendors Can Create Reviews

### Start Server
```bash
python manage.py runserver
```

### Test 1: Vendor Creates Review (Should Work)
```python
import requests

# Login as vendor
response = requests.post(
    'http://127.0.0.1:8000/api/auth/login/',
    json={'username': 'vendor1', 'password': 'testpass123'}
)
vendor_token = response.json()['access']

# Create review
response = requests.post(
    'http://127.0.0.1:8000/api/products/7/reviews/',
    json={'rating': 5, 'comment': 'Great product!'},
    headers={'Authorization': f'Bearer {vendor_token}'}
)
print(f"Vendor Status: {response.status_code}")  # Should be 201
print(f"Response: {response.json()}")
```

### Test 2: Buyer Tries to Create Review (Should Fail)
```python
import requests

# Login as buyer
response = requests.post(
    'http://127.0.0.1:8000/api/auth/login/',
    json={'username': 'buyer1', 'password': 'testpass123'}
)
buyer_token = response.json()['access']

# Try to create review
response = requests.post(
    'http://127.0.0.1:8000/api/products/7/reviews/',
    json={'rating': 5, 'comment': 'Test'},
    headers={'Authorization': f'Bearer {buyer_token}'}
)
print(f"Buyer Status: {response.status_code}")  # Should be 403
print(f"Response: {response.json()}")  # Should say "You do not have permission"
```

### Test 3: Run Full Test Suite
```bash
python test_all_endpoints.py
```

## Expected Results

### Vendor (vendor1)
- ✓ Can create reviews (201 Created)
- ✓ Can update own reviews
- ✓ Can delete own reviews

### Buyer (buyer1)
- ✗ Cannot create reviews (403 Forbidden)
- ✗ Cannot update reviews
- ✗ Cannot delete reviews

### Public (No Auth)
- ✓ Can view all reviews (200 OK)
- ✓ Can view review details (200 OK)

## Quick One-Liner Tests

### Vendor Success
```bash
python -c "import requests; r1 = requests.post('http://127.0.0.1:8000/api/auth/login/', json={'username': 'vendor1', 'password': 'testpass123'}); token = r1.json()['access']; r2 = requests.post('http://127.0.0.1:8000/api/products/7/reviews/', json={'rating': 5, 'comment': 'Vendor review'}, headers={'Authorization': f'Bearer {token}'}); print(f'Status: {r2.status_code} (Expected: 201)')"
```

### Buyer Rejection
```bash
python -c "import requests; r1 = requests.post('http://127.0.0.1:8000/api/auth/login/', json={'username': 'buyer1', 'password': 'testpass123'}); token = r1.json()['access']; r2 = requests.post('http://127.0.0.1:8000/api/products/7/reviews/', json={'rating': 5, 'comment': 'Buyer review'}, headers={'Authorization': f'Bearer {token}'}); print(f'Status: {r2.status_code} (Expected: 403)')"
```

## Status: ✓ IMPLEMENTED & TESTED
Only vendors can now create reviews. Buyers are correctly blocked with 403 Forbidden.
