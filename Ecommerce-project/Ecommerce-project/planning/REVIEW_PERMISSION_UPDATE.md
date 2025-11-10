# Review Permission Update

## Change Summary
Updated the review creation permission to **allow only vendors** to create reviews.

## What Changed

### Before
- Any authenticated user (both vendors and buyers) could create reviews
- Permission class: `IsAuthenticatedOrReadOnly`

### After
- **Only vendors** can create reviews
- Buyers attempting to create reviews will receive a 403 Forbidden error
- Permission class: `IsVendorOrReadOnly`

## Files Modified

### 1. `store/api_views.py`
**ProductReviewsView** - Changed permission class from `IsAuthenticatedOrReadOnly` to `IsVendorOrReadOnly`

```python
class ProductReviewsView(generics.ListCreateAPIView):
    """
    List reviews for a product or create a new review.
    
    GET: Returns reviews for the product (public access)
    POST: Creates a new review (vendors only)  # Updated
    """
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendorOrReadOnly]  # Changed from IsAuthenticatedOrReadOnly
```

## Testing

### Test 1: Vendor Can Create Review ✓
```bash
# Login as vendor
POST /api/auth/login/
{"username": "vendor1", "password": "testpass123"}

# Create review (SUCCESS - 201 Created)
POST /api/products/7/reviews/
Authorization: Bearer <vendor_token>
{"rating": 5, "comment": "Great product from vendor!"}

Response: 201 Created
{"rating": 5, "comment": "Great product from vendor!"}
```

### Test 2: Buyer Cannot Create Review ✓
```bash
# Login as buyer
POST /api/auth/login/
{"username": "buyer1", "password": "testpass123"}

# Try to create review (FAIL - 403 Forbidden)
POST /api/products/7/reviews/
Authorization: Bearer <buyer_token>
{"rating": 5, "comment": "Test"}

Response: 403 Forbidden
{"detail": "You do not have permission to perform this action."}
```

### Test 3: Public Can View Reviews ✓
```bash
# No authentication needed
GET /api/products/7/reviews/

Response: 200 OK
{
  "count": 1,
  "results": [...]
}
```

## Updated Test Suite
The comprehensive test suite (`test_all_endpoints.py`) has been updated to include:
- Test 17: Vendor creates review (expects 201)
- Test 21: Buyer attempts to create review (expects 403)

All 26 tests pass successfully.

## API Endpoints Affected

### Review Creation (Vendor Only)
- `POST /api/products/{product_id}/reviews/` - Create review (vendors only)

### Review Management (Owner Only)
- `PUT/PATCH /api/reviews/{id}/` - Update own review
- `DELETE /api/reviews/{id}/` - Delete own review

### Public Access (No Authentication)
- `GET /api/products/{product_id}/reviews/` - List reviews
- `GET /api/reviews/{id}/` - Get review detail

## Verification
Run the test suite to verify:
```bash
python manage.py runserver
# In another terminal:
python test_all_endpoints.py
```

Expected: All 26 tests pass, including the new buyer rejection test.

## Status: ✓ VERIFIED
- Vendors can create reviews: ✓
- Buyers are blocked from creating reviews (403): ✓
- Public can view reviews: ✓
- All tests passing: ✓
