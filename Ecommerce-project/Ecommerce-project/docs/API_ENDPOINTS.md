# API Endpoints Documentation

## Base URL
```
http://127.0.0.1:8000/api
```

## Authentication

All authenticated endpoints require JWT token in the Authorization header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## 🔐 Authentication Endpoints

### 1. Login (Get JWT Token)
**Endpoint:** `POST /api/auth/login/`

**Request:**
```json
{
    "username": "testuser",
    "password": "password123"
}
```

**Response:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Status Codes:**
- `200 OK` - Login successful
- `401 Unauthorized` - Invalid credentials

---

### 2. Refresh Token
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
    "access": "new_access_token"
}
```

---

### 3. Get User Profile
**Endpoint:** `GET /api/auth/profile/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Response:**
```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        },
        "user_type": "vendor",
        "phone": "+27-123-456-7890",
        "address": "123 Main St"
    }
}
```

---

## 🏪 Store Endpoints

### 1. List All Stores (Public)
**Endpoint:** `GET /api/stores/`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Tech Store",
            "description": "Electronics and gadgets",
            "address": "123 Tech Street",
            "phone": "+27-123-456-7890",
            "email": "contact@techstore.com",
            "vendor": {
                "id": 2,
                "username": "vendor1",
                "email": "vendor@example.com"
            },
            "is_active": true,
            "created_at": "2025-01-01T10:00:00Z",
            "product_count": 15
        }
    ]
}
```

---

### 2. Create Store (Vendor Only)
**Endpoint:** `POST /api/stores/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Request:**
```json
{
    "name": "My Amazing Store",
    "description": "Best products in town",
    "address": "123 Main Street, Cape Town",
    "phone": "+27-123-456-7890",
    "email": "store@example.com"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Store created successfully",
    "data": {
        "id": 2,
        "name": "My Amazing Store",
        "description": "Best products in town",
        "vendor": {
            "id": 2,
            "username": "vendor1"
        },
        "is_active": true,
        "created_at": "2025-01-15T14:30:00Z",
        "product_count": 0
    }
}
```

**Status Codes:**
- `201 Created` - Store created successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not a vendor

**Note:** Automatically sends a tweet about the new store!

---

### 3. Get Store Details
**Endpoint:** `GET /api/stores/{store_id}/`

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Tech Store",
        "description": "Electronics and gadgets",
        "address": "123 Tech Street",
        "phone": "+27-123-456-7890",
        "email": "contact@techstore.com",
        "vendor": {
            "id": 2,
            "username": "vendor1"
        },
        "is_active": true,
        "created_at": "2025-01-01T10:00:00Z",
        "products": [
            {
                "id": 1,
                "name": "Laptop",
                "price": "18999.99",
                "stock_quantity": 10
            }
        ]
    }
}
```

---

### 4. Update Store (Owner Only)
**Endpoint:** `PUT /api/stores/{store_id}/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Request:**
```json
{
    "name": "Updated Store Name",
    "description": "Updated description",
    "address": "New address",
    "phone": "+27-987-654-3210",
    "email": "newemail@example.com"
}
```

---

### 5. Get My Stores (Vendor Only)
**Endpoint:** `GET /api/stores/my-stores/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "My Store",
            "product_count": 25,
            "total_revenue": 125000.00
        }
    ]
}
```

---

## 📦 Product Endpoints

### 1. List All Products (Public)
**Endpoint:** `GET /api/products/`

**Query Parameters:**
- `store_id` (optional) - Filter by store

**Example:** `GET /api/products/?store_id=1`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": "18999.99",
            "stock_quantity": 10,
            "image": "http://localhost:8000/media/products/laptop.jpg",
            "store": {
                "id": 1,
                "name": "Tech Store",
                "vendor": "vendor1"
            },
            "is_active": true,
            "created_at": "2025-01-01T10:00:00Z",
            "average_rating": 4.5,
            "review_count": 12
        }
    ]
}
```

---

### 2. Create Product (Vendor Only)
**Endpoint:** `POST /api/products/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Request:**
```json
{
    "name": "Smartphone X",
    "description": "Latest smartphone with advanced features",
    "price": "12999.99",
    "stock_quantity": 50,
    "store_id": 1
}
```

**Response:**
```json
{
    "success": true,
    "message": "Product created successfully",
    "data": {
        "id": 2,
        "name": "Smartphone X",
        "description": "Latest smartphone with advanced features",
        "price": "12999.99",
        "stock_quantity": 50,
        "store": {
            "id": 1,
            "name": "Tech Store"
        },
        "is_active": true,
        "created_at": "2025-01-15T15:00:00Z"
    }
}
```

**Status Codes:**
- `201 Created` - Product created successfully
- `400 Bad Request` - Invalid data
- `401 Unauthorized` - Not authenticated
- `403 Forbidden` - Not the store owner

**Note:** Automatically sends a tweet about the new product!

---

### 3. Get Product Details
**Endpoint:** `GET /api/products/{product_id}/`

**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop for professionals",
        "price": "18999.99",
        "stock_quantity": 10,
        "image": "http://localhost:8000/media/products/laptop.jpg",
        "store": {
            "id": 1,
            "name": "Tech Store",
            "vendor": {
                "id": 2,
                "username": "vendor1"
            }
        },
        "is_active": true,
        "created_at": "2025-01-01T10:00:00Z",
        "reviews": [
            {
                "id": 1,
                "customer": {
                    "id": 3,
                    "username": "buyer1"
                },
                "rating": 5,
                "comment": "Excellent product!",
                "created_at": "2025-01-10T12:00:00Z"
            }
        ],
        "average_rating": 4.5
    }
}
```

---

### 4. Update Product (Owner Only)
**Endpoint:** `PUT /api/products/{product_id}/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Request:**
```json
{
    "name": "Updated Product Name",
    "description": "Updated description",
    "price": "19999.99",
    "stock_quantity": 15
}
```

---

### 5. Get Store Products
**Endpoint:** `GET /api/stores/{store_id}/products/`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Laptop",
            "price": "18999.99",
            "stock_quantity": 10
        }
    ]
}
```

---

### 6. Get My Products (Vendor Only)
**Endpoint:** `GET /api/products/my-products/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

---

## ⭐ Review Endpoints

### 1. Get Product Reviews (Public)
**Endpoint:** `GET /api/products/{product_id}/reviews/`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "name": "Laptop"
            },
            "customer": {
                "id": 3,
                "username": "buyer1",
                "email": "buyer@example.com"
            },
            "rating": 5,
            "comment": "Excellent product! Highly recommended.",
            "created_at": "2025-01-10T12:00:00Z"
        }
    ]
}
```

---

### 2. Create Review (Authenticated)
**Endpoint:** `POST /api/products/{product_id}/reviews/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Request:**
```json
{
    "rating": 5,
    "comment": "Excellent product! Highly recommended."
}
```

**Response:**
```json
{
    "success": true,
    "message": "Review created successfully",
    "data": {
        "id": 2,
        "product": {
            "id": 1,
            "name": "Laptop"
        },
        "customer": {
            "id": 3,
            "username": "buyer1"
        },
        "rating": 5,
        "comment": "Excellent product!",
        "created_at": "2025-01-15T16:00:00Z"
    }
}
```

**Validation:**
- Rating must be between 1 and 5
- Comment is optional but recommended

---

### 3. Update Review (Owner Only)
**Endpoint:** `PUT /api/reviews/{review_id}/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Request:**
```json
{
    "rating": 4,
    "comment": "Updated review comment"
}
```

---

### 4. Delete Review (Owner Only)
**Endpoint:** `DELETE /api/reviews/{review_id}/`

**Headers:** `Authorization: Bearer YOUR_ACCESS_TOKEN`

**Response:**
```json
{
    "success": true,
    "message": "Review deleted successfully"
}
```

---

## 👤 Vendor Endpoints

### 1. Get Vendor Stores
**Endpoint:** `GET /api/vendors/{vendor_id}/stores/`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Tech Store",
            "description": "Electronics and gadgets",
            "product_count": 15
        }
    ]
}
```

---

### 2. Get Vendor Products
**Endpoint:** `GET /api/vendors/{vendor_id}/products/`

**Response:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Laptop",
            "price": "18999.99",
            "store": {
                "id": 1,
                "name": "Tech Store"
            }
        }
    ]
}
```

---

## 📊 Response Format

### Success Response
```json
{
    "success": true,
    "data": { /* resource data */ },
    "message": "Operation completed successfully"
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "name": ["This field is required"]
        }
    }
}
```

---

## 🔒 Authentication & Permissions

### Permission Levels

1. **Public** - No authentication required
   - List stores
   - List products
   - View product details
   - View reviews

2. **Authenticated** - JWT token required
   - Create reviews
   - View profile
   - Update profile

3. **Vendor** - Must be vendor user type
   - Create stores
   - Create products
   - Update own stores
   - Update own products

4. **Owner** - Must own the resource
   - Update specific store
   - Update specific product
   - Delete own reviews

---

## 🧪 Testing with Postman

### 1. Setup Environment

Create environment variables:
- `base_url`: `http://127.0.0.1:8000`
- `access_token`: (will be set after login)

### 2. Test Workflow

1. **Login**
   ```
   POST {{base_url}}/api/auth/login/
   ```
   Save `access` token to `access_token` variable

2. **Create Store**
   ```
   POST {{base_url}}/api/stores/
   Authorization: Bearer {{access_token}}
   ```

3. **Create Product**
   ```
   POST {{base_url}}/api/products/
   Authorization: Bearer {{access_token}}
   ```

4. **Browse Products**
   ```
   GET {{base_url}}/api/products/
   ```

5. **Create Review**
   ```
   POST {{base_url}}/api/products/1/reviews/
   Authorization: Bearer {{access_token}}
   ```

---

## 🐦 Twitter Integration

When creating stores or products via API, the system automatically:

1. **New Store Tweet**
   ```
   🏪 New store opened on our platform!
   
   Store: Tech Store
   Description: Electronics and gadgets...
   
   Visit us to explore amazing products!
   
   #ecommerce #newstore #shopping
   ```

2. **New Product Tweet**
   ```
   🆕 New product available!
   
   Product: Smartphone X
   Store: Tech Store
   Price: R12999.99
   
   Description: Latest smartphone...
   
   #newproduct #shopping #techstore
   ```

**Note:** Tweets include product images when available!

---

## 📝 Rate Limiting

- **Free Tier**: 300 tweets per month
- **API Requests**: No limit (local development)
- **Production**: Implement rate limiting as needed

---

## 🆘 Common Issues

### 401 Unauthorized
- Check if token is valid
- Token expires after 24 hours
- Use refresh token to get new access token

### 403 Forbidden
- Check user permissions
- Vendors can't access buyer-only endpoints
- Users can only edit their own resources

### 404 Not Found
- Check endpoint URL
- Verify resource ID exists
- Ensure resource is active

---

**For more details, see the main README.md file**