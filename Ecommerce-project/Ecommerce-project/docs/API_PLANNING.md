# Django eCommerce API - Planning Document

## 🎯 API Design Overview

### Models Serialization Strategy

#### 1. Store Model Serialization
```json
{
    "id": 1,
    "name": "Tech Store",
    "description": "Electronics and gadgets",
    "address": "123 Tech Street",
    "phone": "+1-555-TECH",
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
```

#### 2. Product Model Serialization
```json
{
    "id": 1,
    "name": "Smartphone X",
    "description": "Latest smartphone with advanced features",
    "price": "999.99",
    "stock_quantity": 50,
    "image": "http://localhost:8000/media/products/phone.jpg",
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
```

#### 3. Review Model Serialization
```json
{
    "id": 1,
    "product": {
        "id": 1,
        "name": "Smartphone X"
    },
    "customer": {
        "id": 3,
        "username": "buyer1"
    },
    "rating": 5,
    "comment": "Excellent product, highly recommended!",
    "created_at": "2025-01-01T10:00:00Z"
}
```

## 🛣️ API Endpoints Design

### Authentication Endpoints
- `POST /api/auth/login/` - User login (JWT token)
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout

### Store Management (Vendor Only)
- `GET /api/stores/` - List all stores (public)
- `POST /api/stores/` - Create new store (vendor only)
- `GET /api/stores/{id}/` - Retrieve specific store
- `PUT /api/stores/{id}/` - Update store (owner only)
- `DELETE /api/stores/{id}/` - Delete store (owner only)
- `GET /api/stores/my-stores/` - Get vendor's stores

### Product Management
- `GET /api/products/` - List all products (public)
- `POST /api/products/` - Create new product (vendor only)
- `GET /api/products/{id}/` - Retrieve specific product
- `PUT /api/products/{id}/` - Update product (owner only)
- `DELETE /api/products/{id}/` - Delete product (owner only)
- `GET /api/stores/{store_id}/products/` - Get products by store

### Review Management
- `GET /api/products/{product_id}/reviews/` - Get product reviews
- `POST /api/products/{product_id}/reviews/` - Create review (authenticated)
- `GET /api/reviews/{id}/` - Get specific review
- `PUT /api/reviews/{id}/` - Update review (owner only)
- `DELETE /api/reviews/{id}/` - Delete review (owner only)

### Vendor-Specific Endpoints
- `GET /api/vendors/{vendor_id}/stores/` - Get stores by vendor
- `GET /api/vendors/{vendor_id}/products/` - Get all products by vendor

## 🔐 Authentication & Permissions

### Permission Classes
1. **IsVendorOrReadOnly** - Vendors can create/edit, others read-only
2. **IsOwnerOrReadOnly** - Only resource owner can edit
3. **IsAuthenticatedOrReadOnly** - Authenticated users can create, others read-only

### JWT Authentication Flow
1. User logs in with credentials
2. Server returns JWT access and refresh tokens
3. Client includes access token in Authorization header
4. Server validates token for protected endpoints

## 📊 API Response Format

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

### Pagination Response
```json
{
    "success": true,
    "data": {
        "count": 100,
        "next": "http://localhost:8000/api/products/?page=3",
        "previous": "http://localhost:8000/api/products/?page=1",
        "results": [ /* paginated data */ ]
    }
}
```

## 🔄 API Sequence Diagrams

### 1. Vendor Creates Store
```
Vendor -> API: POST /api/auth/login/ (credentials)
API -> Vendor: JWT tokens
Vendor -> API: POST /api/stores/ (store data + JWT)
API -> Database: Create store record
API -> Twitter: Tweet about new store
API -> Vendor: Store created response
```

### 2. Vendor Adds Product
```
Vendor -> API: POST /api/products/ (product data + JWT)
API -> Database: Create product record
API -> Twitter: Tweet about new product
API -> Vendor: Product created response
```

### 3. Buyer Retrieves Stores/Products
```
Buyer -> API: GET /api/stores/
API -> Database: Query stores
API -> Buyer: Stores list

Buyer -> API: GET /api/stores/{id}/products/
API -> Database: Query products by store
API -> Buyer: Products list
```

### 4. Buyer Retrieves Reviews
```
Buyer -> API: GET /api/products/{id}/reviews/
API -> Database: Query reviews by product
API -> Buyer: Reviews list
```

## 🐦 Twitter Integration Plan

### Tweet Templates

#### New Store Tweet
```
🏪 New store opened on our platform!
Store: {store_name}
Description: {store_description}
Visit us at: {website_url}
#ecommerce #newstore #shopping
```

#### New Product Tweet
```
🆕 New product available!
Product: {product_name}
Store: {store_name}
Description: {product_description}
Price: ${product_price}
#newproduct #shopping #ecommerce
```

### Twitter API Integration Points
1. **Store Creation**: Trigger tweet when store is created via API
2. **Product Creation**: Trigger tweet when product is added via API
3. **Media Upload**: Include store logo and product images when available
4. **Error Handling**: Graceful fallback if Twitter API fails

## 📝 Implementation Checklist

### Phase 1: API Foundation
- [ ] Install Django REST Framework
- [ ] Configure JWT authentication
- [ ] Create base serializers
- [ ] Set up API routing

### Phase 2: Core API Endpoints
- [ ] Store CRUD endpoints
- [ ] Product CRUD endpoints
- [ ] Review endpoints
- [ ] Authentication endpoints

### Phase 3: Permissions & Security
- [ ] Custom permission classes
- [ ] API rate limiting
- [ ] Input validation
- [ ] Error handling

### Phase 4: Twitter Integration
- [ ] Twitter developer account setup
- [ ] Twitter API client configuration
- [ ] Tweet functionality for stores
- [ ] Tweet functionality for products
- [ ] Media upload handling

### Phase 5: Testing & Documentation
- [ ] API endpoint testing
- [ ] Twitter integration testing
- [ ] API documentation
- [ ] Postman collection

## 🔧 Technical Requirements

### Dependencies
```
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
tweepy==4.14.0
Pillow==10.0.0
django-cors-headers==4.3.1
```

### Environment Variables
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

This planning document provides a comprehensive roadmap for implementing the RESTful API and Twitter integration while maintaining Django best practices and security standards.