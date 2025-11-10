# Implementation Plan - eCommerce Part 2 Fixes

- [ ] 1. Verify and fix Part 1 functionality
  - Verify all user registration and authentication features work
  - Test store creation through web interface
  - Test product creation through web interface
  - Verify shopping cart functionality
  - Verify order processing
  - Check all database migrations are applied
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

- [x] 2. Update Twitter integration to API v2

  - [x] 2.1 Update store/utils.py with Twitter API v2 client

    - Create `get_twitter_client()` function using `tweepy.Client`
    - Update `send_store_tweet()` to use `client.create_tweet()`
    - Update `send_product_tweet()` to use `client.create_tweet()`
    - Implement media upload using API v1.1 for images
    - Add comprehensive error handling with try-except blocks
    - Add logging for successful tweets and errors
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_


  - [ ] 2.2 Update settings.py with Twitter API v2 configuration
    - Add `TWITTER_BEARER_TOKEN` setting
    - Ensure all Twitter credentials are in settings
    - Add fallback values for missing credentials


    - _Requirements: 10.1, 10.2_

- [x] 3. Add Twitter integration to web views

  - [ ] 3.1 Update create_store view in store/views.py
    - Import `send_store_tweet` from utils
    - Call `send_store_tweet(store)` after store creation
    - Wrap in try-except to handle errors gracefully
    - Log errors without failing store creation
    - _Requirements: 5.1, 5.3, 5.4, 5.5, 5.7_


  - [ ] 3.2 Update create_product view in store/views.py
    - Import `send_product_tweet` from utils
    - Call `send_product_tweet(product)` after product creation
    - Wrap in try-except to handle errors gracefully
    - Log errors without failing product creation
    - _Requirements: 5.2, 5.3, 5.4, 5.5, 5.7_

- [x] 4. Implement store edit functionality



  - [ ] 4.1 Create edit_store view in store/views.py
    - Add `@login_required` and `@require_vendor` decorators
    - Get store by ID using `get_object_or_404`
    - Verify ownership (store.vendor == request.user)
    - Return 403 if not owner
    - Handle GET request: display form with current data
    - Handle POST request: validate and save changes
    - Add success message and redirect to store detail
    - _Requirements: 2.2, 2.3, 2.4, 7.3, 7.4, 7.5, 7.6, 7.7_


  - [ ] 4.2 Create edit_store.html template
    - Create form with pre-filled store data
    - Include CSRF token
    - Add submit and cancel buttons
    - Display validation errors

    - _Requirements: 9.1, 9.5, 9.6_

  - [ ] 4.3 Add URL pattern for store edit
    - Add path: `stores/<int:store_id>/edit/`

    - Name: `edit_store`
    - _Requirements: 8.1, 8.7_


  - [x] 4.4 Update store list/detail templates with edit button

    - Add "Edit" button linking to edit_store URL
    - Show only for store owner
    - _Requirements: 2.1_

- [ ] 5. Implement store delete functionality
  - [ ] 5.1 Create delete_store view in store/views.py
    - Add `@login_required` and `@require_vendor` decorators
    - Get store by ID using `get_object_or_404`
    - Verify ownership (store.vendor == request.user)

    - Return 403 if not owner
    - Handle GET request: display confirmation page
    - Handle POST request: soft delete (set is_active=False)
    - Add success message and redirect to my_stores
    - _Requirements: 2.5, 2.6, 11.3, 11.4_


  - [ ] 5.2 Create delete_store.html template
    - Display store information
    - Show confirmation message
    - Include CSRF token

    - Add confirm and cancel buttons
    - _Requirements: 2.5_


  - [x] 5.3 Add URL pattern for store delete

    - Add path: `stores/<int:store_id>/delete/`
    - Name: `delete_store`
    - _Requirements: 8.2, 8.7_

  - [ ] 5.4 Update store list/detail templates with delete button
    - Add "Delete" button linking to delete_store URL
    - Show only for store owner
    - _Requirements: 2.1_


- [ ] 6. Implement product edit functionality
  - [ ] 6.1 Create edit_product view in store/views.py
    - Add `@login_required` and `@require_vendor` decorators
    - Get product by ID using `get_object_or_404`
    - Verify store ownership (product.store.vendor == request.user)
    - Return 403 if not owner
    - Handle GET request: display form with current data

    - Handle POST request: validate and save changes (including image)
    - Add success message and redirect to product detail
    - _Requirements: 3.2, 3.3, 3.4, 7.3, 7.4, 7.5, 7.6, 7.7_


  - [ ] 6.2 Create edit_product.html template
    - Create form with pre-filled product data
    - Include file upload for image


    - Include CSRF token

    - Add submit and cancel buttons
    - Display validation errors
    - _Requirements: 9.1, 9.5, 9.6_

  - [ ] 6.3 Add URL pattern for product edit
    - Add path: `products/<int:product_id>/edit/`
    - Name: `edit_product`
    - _Requirements: 8.3, 8.7_


  - [ ] 6.4 Update product list/detail templates with edit button
    - Add "Edit" button linking to edit_product URL
    - Show only for product owner
    - _Requirements: 3.1_

- [x] 7. Implement product delete functionality

  - [ ] 7.1 Create delete_product view in store/views.py
    - Add `@login_required` and `@require_vendor` decorators
    - Get product by ID using `get_object_or_404`
    - Verify store ownership (product.store.vendor == request.user)

    - Return 403 if not owner
    - Handle GET request: display confirmation page
    - Handle POST request: soft delete (set is_active=False)
    - Add success message and redirect to my_products
    - _Requirements: 3.5, 3.6, 11.3, 11.4_

  - [ ] 7.2 Create delete_product.html template
    - Display product information
    - Show confirmation message
    - Include CSRF token
    - Add confirm and cancel buttons
    - _Requirements: 3.5_

  - [ ] 7.3 Add URL pattern for product delete
    - Add path: `products/<int:product_id>/delete/`
    - Name: `delete_product`
    - _Requirements: 8.4, 8.7_

  - [ ] 7.4 Update product list/detail templates with delete button
    - Add "Delete" button linking to delete_product URL
    - Show only for product owner
    - _Requirements: 3.1_

- [ ] 8. Implement password reset functionality
  - [ ] 8.1 Verify PasswordResetToken model exists
    - Check if model exists in store/models.py
    - If not, create model with user, token, created_at, expires_at, used fields
    - Add `is_expired()` method
    - Run makemigrations and migrate
    - _Requirements: 4.3, 4.8_

  - [x] 8.2 Create password_reset_request view

    - Handle GET request: display email input form
    - Handle POST request: get email from form
    - Look up user by email
    - Create PasswordResetToken with UUID and 1-hour expiration
    - Build reset URL with token
    - Send email with reset link
    - Display success message
    - Handle user not found gracefully
    - _Requirements: 4.2, 4.3, 4.4, 12.4, 12.5, 12.7_

  - [x] 8.3 Create password_reset_confirm view


    - Get token from URL parameter
    - Look up PasswordResetToken
    - Check if token is expired or used
    - Handle GET request: display password reset form
    - Handle POST request: validate passwords match
    - Update user password using `set_password()`
    - Mark token as used
    - Display success message and redirect to login
    - _Requirements: 4.5, 4.6, 4.7_

  - [ ] 8.4 Create password reset templates
    - Create password_reset_request.html with email form
    - Create password_reset_confirm.html with password form
    - Include CSRF tokens
    - Display error and success messages
    - _Requirements: 4.2, 4.6, 9.1, 9.5, 9.6_

  - [ ] 8.5 Add URL patterns for password reset
    - Add path: `password-reset/` → password_reset_request
    - Add path: `password-reset/<uuid:token>/` → password_reset_confirm
    - _Requirements: 8.5, 8.6, 8.7_

  - [ ] 8.6 Update login template with "Forgot Password" link
    - Add link to password_reset_request view
    - Place below login form
    - _Requirements: 4.1_

  - [ ] 8.7 Configure email settings
    - Verify EMAIL_BACKEND is set in settings.py
    - Use console backend for development
    - Add SMTP settings for production (commented out)
    - Set DEFAULT_FROM_EMAIL
    - _Requirements: 12.1, 12.2, 12.3, 12.6_

- [ ] 9. Update API views to ensure Twitter integration
  - [ ] 9.1 Verify API store creation calls send_store_tweet
    - Check StoreListCreateView.perform_create()
    - Ensure send_store_tweet is called
    - Verify error handling is in place
    - _Requirements: 5.4, 5.5_

  - [ ] 9.2 Verify API product creation calls send_product_tweet
    - Check ProductListCreateView.perform_create()
    - Ensure send_product_tweet is called
    - Verify error handling is in place
    - _Requirements: 5.4, 5.5_

- [ ] 10. Create comprehensive tests
  - [ ] 10.1 Write tests for store CRUD operations
    - Test edit store with owner (should succeed)
    - Test edit store with non-owner (should return 403)
    - Test delete store with owner (should succeed)
    - Test delete store with non-owner (should return 403)
    - _Requirements: 13.1, 13.6_

  - [ ] 10.2 Write tests for product CRUD operations
    - Test edit product with store owner (should succeed)
    - Test edit product with non-owner (should return 403)
    - Test delete product with store owner (should succeed)
    - Test delete product with non-owner (should return 403)
    - _Requirements: 13.2, 13.6_

  - [ ] 10.3 Write tests for password reset flow
    - Test reset request with valid email
    - Test reset request with invalid email
    - Test reset confirm with valid token
    - Test reset confirm with expired token
    - Test reset confirm with used token
    - _Requirements: 13.3_

  - [ ] 10.4 Write tests for Twitter integration
    - Test send_store_tweet with valid credentials
    - Test send_store_tweet with missing credentials
    - Test send_product_tweet with image
    - Test send_product_tweet without image
    - Test error handling for API failures
    - _Requirements: 13.4, 13.5_

  - [ ] 10.5 Write tests for form validation
    - Test store form validation
    - Test product form validation
    - Test password reset form validation
    - _Requirements: 13.7_

- [ ] 11. Update documentation
  - [ ] 11.1 Update README with new features
    - Document edit/delete functionality
    - Document password reset setup
    - Document Twitter API v2 configuration
    - Add new dependencies (if any)
    - _Requirements: 14.7_

  - [ ] 11.2 Create Twitter API v2 setup guide
    - Document how to get Bearer Token
    - Document required credentials
    - Provide configuration examples
    - _Requirements: 14.2_

  - [ ] 11.3 Update user guide with CRUD operations
    - Document how to edit stores
    - Document how to delete stores
    - Document how to edit products
    - Document how to delete products
    - Document password reset process
    - _Requirements: 14.4_

  - [ ] 11.4 Update API documentation
    - Document edit/delete API endpoints
    - Provide request/response examples
    - _Requirements: 14.5, 14.6_

- [ ] 12. Final testing and verification
  - Test complete vendor flow: register → create store → create product → edit → delete
  - Test password reset flow end-to-end
  - Test Twitter integration for both web and API
  - Verify all Part 1 functionality still works
  - Test permission enforcement on all operations
  - Verify soft delete works correctly
  - Test with missing Twitter credentials
  - _Requirements: All_
