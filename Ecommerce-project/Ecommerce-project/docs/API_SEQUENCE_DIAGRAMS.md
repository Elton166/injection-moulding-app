# API Sequence Diagrams

## 🔄 User Interaction Flows

### 1. Vendor Creates Store via API

```mermaid
sequenceDiagram
    participant V as Vendor
    participant API as Django API
    participant DB as MariaDB
    participant TW as Twitter API
    
    V->>API: POST /api/auth/login/ (credentials)
    API->>DB: Validate user credentials
    DB-->>API: User authenticated
    API-->>V: JWT tokens (access, refresh)
    
    V->>API: POST /api/stores/ (store data + JWT)
    API->>API: Validate JWT token
    API->>API: Check vendor permissions
    API->>DB: Create store record
    DB-->>API: Store created (ID: 123)
    
    API->>TW: Tweet about new store
    TW-->>API: Tweet sent (ID: xyz)
    
    API-->>V: Store created response
    
    Note over V,TW: Store is now live and announced on Twitter
```

### 2. Vendor Adds Product via API

```mermaid
sequenceDiagram
    participant V as Vendor
    participant API as Django API
    participant DB as MariaDB
    participant TW as Twitter API
    participant FS as File System
    
    V->>API: POST /api/products/ (product data + image + JWT)
    API->>API: Validate JWT token
    API->>API: Check store ownership
    API->>DB: Validate store exists
    DB-->>API: Store validated
    
    API->>FS: Save product image
    FS-->>API: Image saved
    
    API->>DB: Create product record
    DB-->>API: Product created (ID: 456)
    
    API->>TW: Upload product image
    TW-->>API: Media uploaded (media_id)
    
    API->>TW: Tweet about new product (with image)
    TW-->>API: Tweet sent (ID: abc)
    
    API-->>V: Product created response
    
    Note over V,TW: Product is now available and promoted on Twitter
```

### 3. Buyer Retrieves Stores and Products

```mermaid
sequenceDiagram
    participant B as Buyer
    participant API as Django API
    participant DB as MariaDB
    
    B->>API: GET /api/stores/
    API->>DB: Query active stores
    DB-->>API: Store list with vendor info
    API-->>B: Stores list (JSON)
    
    B->>API: GET /api/stores/123/products/
    API->>DB: Query products for store 123
    DB-->>API: Product list with details
    API-->>B: Products list (JSON)
    
    B->>API: GET /api/products/456/
    API->>DB: Query product details
    DB-->>API: Product with reviews, ratings
    API-->>B: Product details (JSON)
    
    Note over B,DB: Public access, no authentication required
```

### 4. Buyer Creates Product Review

```mermaid
sequenceDiagram
    participant B as Buyer
    participant API as Django API
    participant DB as MariaDB
    
    B->>API: POST /api/auth/login/ (credentials)
    API->>DB: Validate buyer credentials
    DB-->>API: User authenticated
    API-->>B: JWT tokens
    
    B->>API: POST /api/products/456/reviews/ (review data + JWT)
    API->>API: Validate JWT token
    API->>DB: Check product exists
    DB-->>API: Product validated
    
    API->>DB: Create review record
    DB-->>API: Review created (ID: 789)
    
    API-->>B: Review created response
    
    Note over B,DB: Review is now visible to all users
```

### 5. Vendor Retrieves Own Resources

```mermaid
sequenceDiagram
    participant V as Vendor
    participant API as Django API
    participant DB as MariaDB
    
    V->>API: GET /api/stores/my-stores/ (JWT)
    API->>API: Validate JWT token
    API->>API: Extract user from token
    API->>DB: Query stores by vendor
    DB-->>API: Vendor's stores with stats
    API-->>V: My stores list (JSON)
    
    V->>API: GET /api/products/my-products/ (JWT)
    API->>API: Validate JWT token
    API->>DB: Query products by vendor
    DB-->>API: Vendor's products with reviews
    API-->>V: My products list (JSON)
    
    Note over V,DB: Vendor-specific data with business metrics
```

### 6. Public Access to Vendor Resources

```mermaid
sequenceDiagram
    participant U as User (Public)
    participant API as Django API
    participant DB as MariaDB
    
    U->>API: GET /api/vendors/5/stores/
    API->>DB: Query stores for vendor ID 5
    DB-->>API: Public store information
    API-->>U: Vendor stores (JSON)
    
    U->>API: GET /api/vendors/5/products/
    API->>DB: Query products for vendor ID 5
    DB-->>API: Public product information
    API-->>U: Vendor products (JSON)
    
    Note over U,DB: Public marketplace browsing
```

## 🔐 Authentication Flow Details

### JWT Token Lifecycle

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Django API
    participant JWT as JWT Service
    participant DB as Database
    
    C->>API: POST /api/auth/login/ (username, password)
    API->>DB: Validate credentials
    DB-->>API: User data
    API->>JWT: Generate tokens
    JWT-->>API: Access + Refresh tokens
    API-->>C: Tokens (expires in 24h)
    
    Note over C,JWT: Client stores tokens securely
    
    C->>API: API Request + Access Token
    API->>JWT: Validate access token
    JWT-->>API: Token valid + User info
    API->>DB: Process request
    DB-->>API: Response data
    API-->>C: API Response
    
    Note over C,JWT: Token expires after 24 hours
    
    C->>API: POST /api/auth/refresh/ (refresh token)
    API->>JWT: Validate refresh token
    JWT-->>API: New access token
    API-->>C: New access token
    
    Note over C,JWT: Refresh tokens valid for 7 days
```

## 🐦 Twitter Integration Flow

### Store Tweet Process

```mermaid
sequenceDiagram
    participant API as Django API
    participant TW as Twitter Client
    participant TWA as Twitter API
    
    API->>TW: Initialize Twitter client
    TW->>TWA: Authenticate with API keys
    TWA-->>TW: Authentication successful
    
    API->>TW: send_store_tweet(store)
    TW->>TW: Format tweet text
    TW->>TWA: POST /2/tweets (tweet data)
    TWA-->>TW: Tweet created (ID: xyz)
    TW-->>API: Success response
    
    Note over API,TWA: Store announcement posted to Twitter
```

### Product Tweet with Media

```mermaid
sequenceDiagram
    participant API as Django API
    participant TW as Twitter Client
    participant TWA as Twitter API v1.1
    participant TW2 as Twitter API v2
    
    API->>TW: send_product_tweet(product)
    TW->>TW: Check if product has image
    
    alt Product has image
        TW->>TWA: POST /1.1/media/upload (image)
        TWA-->>TW: Media uploaded (media_id)
        TW->>TW2: POST /2/tweets (text + media_id)
        TW2-->>TW: Tweet with image created
    else No image
        TW->>TW2: POST /2/tweets (text only)
        TW2-->>TW: Tweet created
    end
    
    TW-->>API: Success response
    
    Note over API,TW2: Product promoted with visual content
```

## 🔄 Error Handling Flows

### API Error Response

```mermaid
sequenceDiagram
    participant C as Client
    participant API as Django API
    participant DB as Database
    
    C->>API: Invalid API request
    API->>API: Validate request
    API->>API: Validation fails
    
    API-->>C: Error Response
    Note right of API: {<br/>  "success": false,<br/>  "error": {<br/>    "code": "VALIDATION_ERROR",<br/>    "message": "Invalid data",<br/>    "details": {...}<br/>  }<br/>}
```

### Twitter Integration Error Handling

```mermaid
sequenceDiagram
    participant API as Django API
    participant TW as Twitter Client
    participant TWA as Twitter API
    participant DB as Database
    
    API->>DB: Create store/product
    DB-->>API: Resource created successfully
    
    API->>TW: Send tweet
    TW->>TWA: POST tweet
    TWA-->>TW: Error (rate limit/auth failure)
    TW-->>API: Tweet failed
    
    API->>API: Log error (don't fail creation)
    API-->>Client: Resource created (tweet failed silently)
    
    Note over API,TWA: Business operation succeeds even if social media fails
```

## 📊 Data Flow Summary

### Request/Response Patterns

1. **Authentication Required Endpoints**
   - All POST, PUT, DELETE operations
   - Vendor-specific endpoints (/my-stores/, /my-products/)
   - Review creation

2. **Public Access Endpoints**
   - GET /api/stores/
   - GET /api/products/
   - GET /api/vendors/{id}/stores/
   - GET /api/vendors/{id}/products/
   - GET /api/products/{id}/reviews/

3. **Permission-Based Access**
   - Store owners can edit their stores
   - Product owners can edit their products
   - Review authors can edit their reviews
   - Vendors can create stores and products

4. **Social Media Integration**
   - Automatic tweets on resource creation
   - Media upload for visual content
   - Graceful error handling
   - Rate limit compliance

This API design ensures secure, scalable, and user-friendly access to your eCommerce platform while maintaining proper separation of concerns and following REST best practices.