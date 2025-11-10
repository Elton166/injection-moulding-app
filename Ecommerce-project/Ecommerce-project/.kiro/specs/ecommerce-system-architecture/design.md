# eCommerce Platform - System Architecture Design

## Overview

The Django eCommerce Platform is a multi-vendor marketplace that enables vendors to create stores and sell products while buyers can browse, purchase, and review items. The system is built on Django 5.2.6 with MariaDB as the database, Django REST Framework for API capabilities, and JWT for authentication. The architecture follows a layered approach with clear separation between presentation, business logic, and data layers.

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
├─────────────────────────────────────────────────────────────────┤
│  Web Browser  │  Mobile App  │  Third-Party API Clients         │
└────────┬──────────────┬────────────────────┬────────────────────┘
         │              │                    │
         │              │                    │
         ▼              ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Presentation Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  Django Templates  │  REST API Endpoints  │  JWT Auth           │
│  (HTML/CSS/JS)     │  (JSON Responses)    │  (Token Validation) │
└────────┬──────────────────┬────────────────────┬────────────────┘
         │                  │                    │
         │                  │                    │
         ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Business Logic Layer                         │
├─────────────────────────────────────────────────────────────────┤
│  Views & ViewSets  │  Serializers  │  Permissions  │  Utils     │
│  - Store Views     │  - Store      │  - IsVendor   │  - Twitter │
│  - Product Views   │  - Product    │  - IsOwner    │  - Email   │
│  - Order Views     │  - Review     │  - ReadOnly   │  - Payment │
│  - Review Views    │  - User       │               │            │
└────────┬──────────────────┬────────────────────┬────────────────┘
         │                  │                    │
         │                  │                    │
         ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Access Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  Django ORM  │  Models  │  Migrations  │  Query Optimization    │
└────────┬──────────────────┬────────────────────┬────────────────┘
         │                  │                    │
         │                  │                    │
         ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                              │
├─────────────────────────────────────────────────────────────────┤
│                    MariaDB 12.0.2                                │
│  - User Tables  │  - Store Tables  │  - Order Tables            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
├─────────────────────────────────────────────────────────────────┤
│  Twitter API  │  Email SMTP  │  Payment Gateway  │  File Storage│
└─────────────────────────────────────────────────────────────────┘
```

### System Component Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                     Django Application                            │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Web Views     │  │   API Views     │  │  Authentication │ │
│  │                 │  │                 │  │                 │ │
│  │ - store/        │  │ - /api/stores/  │  │ - Session Auth  │ │
│  │ - cart/         │  │ - /api/products/│  │ - JWT Auth      │ │
│  │ - checkout/     │  │ - /api/reviews/ │  │ - Permissions   │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                     │           │
│           └────────────────────┼─────────────────────┘           │
│                                │                                 │
│  ┌─────────────────────────────┴──────────────────────────────┐ │
│  │                    Business Logic                           │ │
│  │                                                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │ │
│  │  │  Store   │  │ Product  │  │  Order   │  │  Review  │  │ │
│  │  │ Manager  │  │ Manager  │  │ Manager  │  │ Manager  │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │ │
│  │                                                              │ │
│  └──────────────────────────┬───────────────────────────────┘  │
│                             │                                   │
│  ┌──────────────────────────┴───────────────────────────────┐  │
│  │                    Django ORM                             │  │
│  │                                                            │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐         │  │
│  │  │  User  │  │ Store  │  │Product │  │ Order  │         │  │
│  │  │ Models │  │ Models │  │ Models │  │ Models │         │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘         │  │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │    MariaDB      │
                   │   Database      │
                   └─────────────────┘
```

## Components and Interfaces

### 1. User Management Component

**Purpose**: Handle user registration, authentication, and profile management

**Models**:
- `User` (Django built-in): username, email, password, first_name, last_name
- `UserProfile`: user (FK), user_type (vendor/buyer), phone, address, created_at

**Interfaces**:
```python
# Web Views
/register/          # User registration form
/login/             # User login form
/logout/            # User logout
/profile/           # User profile management

# API Endpoints
POST /api/auth/login/       # JWT token generation
POST /api/auth/refresh/     # Token refresh
GET  /api/auth/profile/     # Get user profile
```

**Key Methods**:
- `create_user_profile()`: Automatically create profile on user registration
- `validate_user_type()`: Ensure user type is vendor or buyer
- `check_vendor_permissions()`: Verify user has vendor role

### 2. Store Management Component

**Purpose**: Enable vendors to create and manage their stores

**Models**:
- `Store`: vendor (FK to User), name, description, address, phone, email, is_active, created_at

**Interfaces**:
```python
# Web Views
/stores/                    # List all stores
/stores/<id>/               # Store detail page
/stores/create/             # Create new store (vendor only)
/stores/<id>/edit/          # Edit store (owner only)

# API Endpoints
GET    /api/stores/                 # List all active stores
POST   /api/stores/                 # Create store (vendor only)
GET    /api/stores/<id>/            # Get store details
PUT    /api/stores/<id>/            # Update store (owner only)
DELETE /api/stores/<id>/            # Delete store (owner only)
GET    /api/stores/my-stores/       # Get vendor's stores
GET    /api/vendors/<id>/stores/    # Get stores by vendor
```

**Key Methods**:
- `create_store()`: Create store and trigger Twitter announcement
- `validate_vendor_ownership()`: Verify vendor owns the store
- `get_product_count()`: Calculate number of products in store
- `send_store_tweet()`: Post store announcement to Twitter

### 3. Product Management Component

**Purpose**: Manage product catalog with images, pricing, and inventory

**Models**:
- `Product`: store (FK), name, description, price, stock_quantity, image, digital, is_active, created_at

**Interfaces**:
```python
# Web Views
/products/                  # List all products
/products/<id>/             # Product detail page
/products/create/           # Create product (vendor only)
/products/<id>/edit/        # Edit product (owner only)

# API Endpoints
GET    /api/products/                       # List all products
POST   /api/products/                       # Create product (vendor only)
GET    /api/products/<id>/                  # Get product details
PUT    /api/products/<id>/                  # Update product (owner only)
DELETE /api/products/<id>/                  # Delete product (owner only)
GET    /api/products/my-products/           # Get vendor's products
GET    /api/stores/<id>/products/           # Get products by store
GET    /api/vendors/<id>/products/          # Get products by vendor
```

**Key Methods**:
- `create_product()`: Create product and trigger Twitter announcement
- `validate_store_ownership()`: Verify vendor owns the product's store
- `calculate_average_rating()`: Compute average from all reviews
- `get_review_count()`: Count total reviews for product
- `send_product_tweet()`: Post product announcement to Twitter

### 4. Shopping Cart Component

**Purpose**: Manage shopping cart for guest and authenticated users

**Models**:
- `Order`: customer (FK to User), date_ordered, complete, transaction_id, status, total_amount
- `OrderItem`: product (FK), order (FK), quantity, price, date_added

**Interfaces**:
```python
# Web Views
/cart/                      # View shopping cart
/cart/add/<product_id>/     # Add item to cart
/cart/update/               # Update cart quantities
/cart/remove/<item_id>/     # Remove item from cart
/checkout/                  # Checkout process

# API Endpoints (Future)
GET    /api/cart/           # Get current cart
POST   /api/cart/items/     # Add item to cart
PUT    /api/cart/items/<id>/# Update cart item
DELETE /api/cart/items/<id>/# Remove cart item
```

**Key Methods**:
- `get_or_create_cart()`: Get existing cart or create new one
- `add_to_cart()`: Add product with quantity to cart
- `update_cart_item()`: Modify item quantity
- `calculate_cart_total()`: Sum all items in cart
- `create_order()`: Convert cart to order on checkout

### 5. Order Processing Component

**Purpose**: Handle order creation, tracking, and fulfillment

**Models**:
- `Order`: customer, date_ordered, complete, transaction_id, status, total_amount
- `OrderItem`: product, order, quantity, price, date_added
- `ShippingAddress`: customer, order, address, city, state, zipcode, date_added

**Interfaces**:
```python
# Web Views
/orders/                    # List user's orders
/orders/<id>/               # Order detail page
/checkout/                  # Checkout and create order

# API Endpoints (Future)
GET    /api/orders/         # List user's orders
POST   /api/orders/         # Create new order
GET    /api/orders/<id>/    # Get order details
PUT    /api/orders/<id>/    # Update order status
```

**Key Methods**:
- `create_order_from_cart()`: Convert cart items to order
- `calculate_order_total()`: Sum all order items
- `update_order_status()`: Change order status (pending → shipped → delivered)
- `get_shipping_required()`: Check if order contains physical products

### 6. Review System Component

**Purpose**: Enable vendors to review and rate products

**Models**:
- `Review`: product (FK), user (FK), rating (1-5), comment, is_verified, created_at

**Interfaces**:
```python
# Web Views
/products/<id>/reviews/     # View product reviews
/reviews/create/            # Create review (vendor only)
/reviews/<id>/edit/         # Edit review (author only)

# API Endpoints
GET    /api/products/<id>/reviews/  # List product reviews
POST   /api/products/<id>/reviews/  # Create review (vendor only)
GET    /api/reviews/<id>/           # Get review details
PUT    /api/reviews/<id>/           # Update review (author only)
DELETE /api/reviews/<id>/           # Delete review (author only)
```

**Key Methods**:
- `create_review()`: Create review and update product rating
- `validate_vendor_permission()`: Ensure only vendors can review
- `prevent_duplicate_review()`: Check user hasn't already reviewed product
- `update_product_rating()`: Recalculate average rating after review changes

### 7. Authentication & Authorization Component

**Purpose**: Secure access control with session and JWT authentication

**Components**:
- Session Authentication (Django built-in)
- JWT Authentication (djangorestframework-simplejwt)
- Custom Permission Classes

**Permission Classes**:
```python
IsVendorOrReadOnly          # Vendors can write, others read-only
IsOwnerOrReadOnly           # Resource owners can write, others read-only
IsStoreOwnerOrReadOnly      # Store owners can write, others read-only
IsReviewOwnerOrReadOnly     # Review authors can write, others read-only
IsVendor                    # Vendor-only access
IsAuthenticatedOrReadOnly   # Authenticated can write, others read-only
```

**JWT Configuration**:
- Access Token Lifetime: 24 hours
- Refresh Token Lifetime: 7 days
- Token Rotation: Enabled
- Algorithm: HS256

### 8. Social Media Integration Component

**Purpose**: Automatically promote stores and products on Twitter

**Utilities**:
- `send_store_tweet()`: Post store announcement
- `send_product_tweet()`: Post product announcement with optional image
- `upload_media()`: Upload product images to Twitter

**Twitter API Integration**:
- API v1.1: Media upload
- API v2: Tweet posting
- Error Handling: Graceful failure without blocking resource creation

**Tweet Templates**:
```
Store: "🏪 New store opened! {name} - {description} #ecommerce #newstore"
Product: "🆕 New product! {name} at {store} - ${price} #shopping #newproduct"
```

## Data Models

### Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
│─────────────────│
│ id (PK)         │
│ username        │
│ email           │
│ password        │
└────────┬────────┘
         │ 1
         │
         │ 1
┌────────┴────────┐
│  UserProfile    │
│─────────────────│
│ id (PK)         │
│ user_id (FK)    │
│ user_type       │
│ phone           │
│ address         │
└─────────────────┘

         │ 1
         │
         │ *
┌────────┴────────┐
│     Store       │
│─────────────────│
│ id (PK)         │
│ vendor_id (FK)  │
│ name            │
│ description     │
│ address         │
│ phone           │
│ email           │
│ is_active       │
│ created_at      │
└────────┬────────┘
         │ 1
         │
         │ *
┌────────┴────────┐
│    Product      │
│─────────────────│
│ id (PK)         │
│ store_id (FK)   │
│ name            │
│ description     │
│ price           │
│ stock_quantity  │
│ image           │
│ is_active       │
│ created_at      │
└────────┬────────┘
         │ 1
         │
         ├─────────────────┐
         │ *               │ *
┌────────┴────────┐ ┌──────┴──────┐
│     Review      │ │  OrderItem  │
│─────────────────│ │─────────────│
│ id (PK)         │ │ id (PK)     │
│ product_id (FK) │ │ product_id  │
│ user_id (FK)    │ │ order_id    │
│ rating          │ │ quantity    │
│ comment         │ │ price       │
│ created_at      │ │ date_added  │
└─────────────────┘ └──────┬──────┘
                           │ *
                           │
                           │ 1
                    ┌──────┴──────┐
                    │    Order    │
                    │─────────────│
                    │ id (PK)     │
                    │ customer_id │
                    │ date_ordered│
                    │ complete    │
                    │ status      │
                    │ total_amount│
                    └──────┬──────┘
                           │ 1
                           │
                           │ 1
                    ┌──────┴──────────┐
                    │ ShippingAddress │
                    │─────────────────│
                    │ id (PK)         │
                    │ order_id (FK)   │
                    │ address         │
                    │ city            │
                    │ state           │
                    │ zipcode         │
                    └─────────────────┘
```

### Database Indexes

**Optimized Queries**:
```sql
-- User lookups
CREATE INDEX idx_user_username ON auth_user(username);
CREATE INDEX idx_user_email ON auth_user(email);

-- Store queries
CREATE INDEX idx_store_vendor ON store_store(vendor_id);
CREATE INDEX idx_store_active ON store_store(is_active);

-- Product queries
CREATE INDEX idx_product_store ON store_product(store_id);
CREATE INDEX idx_product_active ON store_product(is_active);

-- Review queries
CREATE INDEX idx_review_product ON store_review(product_id);
CREATE INDEX idx_review_user ON store_review(user_id);

-- Order queries
CREATE INDEX idx_order_customer ON store_order(customer_id);
CREATE INDEX idx_order_status ON store_order(status);
```

## Error Handling

### API Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field_name": ["Specific field error"]
    }
  }
}
```

### Error Codes

- `AUTHENTICATION_REQUIRED`: User must be authenticated
- `PERMISSION_DENIED`: User lacks required permissions
- `VALIDATION_ERROR`: Input data validation failed
- `NOT_FOUND`: Requested resource doesn't exist
- `DUPLICATE_ENTRY`: Resource already exists
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `SERVER_ERROR`: Internal server error

### Error Handling Strategy

1. **Validation Errors**: Return 400 with field-specific errors
2. **Authentication Errors**: Return 401 with clear message
3. **Permission Errors**: Return 403 with permission requirement
4. **Not Found Errors**: Return 404 with resource type
5. **Server Errors**: Return 500 and log full traceback
6. **External Service Errors**: Log error, continue operation

## Testing Strategy

### Test Coverage Areas

1. **Unit Tests**
   - Model methods (average_rating, get_cart_total)
   - Utility functions (send_tweet, validate_permissions)
   - Serializer validation logic

2. **Integration Tests**
   - API endpoint responses
   - Authentication flows
   - Permission enforcement
   - Database transactions

3. **End-to-End Tests**
   - User registration → store creation → product creation
   - Product browsing → add to cart → checkout
   - Review creation → rating calculation

### Test Data Strategy

- Use Django fixtures for consistent test data
- Create factory functions for model instances
- Use separate test database
- Clean up test data after each test

### Performance Testing

- Load testing with 500 concurrent users
- Database query optimization verification
- API response time monitoring
- Memory usage profiling

## Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Django     │  │  Django     │  │  Django     │
│  Instance 1 │  │  Instance 2 │  │  Instance 3 │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │    MariaDB      │
              │   (Primary)     │
              └────────┬────────┘
                       │
                       │ Replication
                       │
              ┌────────┴────────┐
              │    MariaDB      │
              │   (Replica)     │
              └─────────────────┘
```

### Scalability Considerations

- Horizontal scaling with multiple Django instances
- Database read replicas for query distribution
- Redis caching for frequently accessed data
- CDN for static files and media
- Asynchronous task queue (Celery) for background jobs

This design provides a robust, scalable foundation for the eCommerce platform with clear separation of concerns and comprehensive error handling.
