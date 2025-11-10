# eCommerce Application - Part 2 Fixes Design

## Overview

This design document addresses the feedback for eCommerce Part 2 submission by implementing missing CRUD operations, password reset functionality, Twitter integration for web views, and migrating to Twitter API v2 for free-tier compatibility. The design ensures all Part 1 functionality is complete and working before adding Part 2 features.

## Architecture

### Component Updates

```
┌─────────────────────────────────────────────────────────────────┐
│                    UPDATED ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  WEB VIEWS (store/views.py)                                    │
│  ├─ Store CRUD: list, create, edit, delete                     │
│  ├─ Product CRUD: list, create, edit, delete                   │
│  ├─ Password Reset: request, confirm, complete                 │
│  └─ Twitter Integration: send_store_tweet, send_product_tweet  │
│                                                                  │
│  API VIEWS (store/api_views.py)                                │
│  ├─ Store CRUD: GET, POST, PUT, DELETE                         │
│  ├─ Product CRUD: GET, POST, PUT, DELETE                       │
│  └─ Twitter Integration: send_store_tweet, send_product_tweet  │
│                                                                  │
│  UTILITIES (store/utils.py)                                    │
│  ├─ Twitter API v2 Client                                      │
│  ├─ send_store_tweet(store) → uses Client.create_tweet        │
│  ├─ send_product_tweet(product) → uses Client.create_tweet    │
│  └─ Error handling for all Twitter operations                  │
│                                                                  │
│  MODELS (store/models.py)                                      │
│  ├─ Store: is_active field for soft delete                     │
│  ├─ Product: is_active field for soft delete                   │
│  └─ PasswordResetToken: token, expires_at, used               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Store CRUD Web Views

**File**: `store/views.py`

**New/Updated Views**:

```python
@login_required
@require_vendor
def edit_store(request, store_id):
    """Edit existing store (owner only)"""
    store = get_object_or_404(Store, id=store_id)
    
    # Verify ownership
    if store.vendor != request.user:
        return HttpResponseForbidden("You don't own this store")
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully')
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm(instance=store)
    
    return render(request, 'store/edit_store.html', {'form': form, 'store': store})


@login_required
@require_vendor
def delete_store(request, store_id):
    """Delete store (soft delete - owner only)"""
    store = get_object_or_404(Store, id=store_id)
    
    # Verify ownership
    if store.vendor != request.user:
        return HttpResponseForbidden("You don't own this store")
    
    if request.method == 'POST':
        # Soft delete
        store.is_active = False
        store.save()
        messages.success(request, 'Store deleted successfully')
        return redirect('my_stores')
    
    return render(request, 'store/delete_store.html', {'store': store})
```

**Updated Create Store View**:

```python
@login_required
@require_vendor
def create_store(request):
    """Create new store with Twitter integration"""
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user
            store.save()
            
            # Send tweet (imported from utils)
            try:
                from .utils import send_store_tweet
                send_store_tweet(store)
            except Exception as e:
                # Log error but don't fail store creation
                logger.error(f"Failed to send store tweet: {e}")
            
            messages.success(request, 'Store created successfully')
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm()
    
    return render(request, 'store/create_store.html', {'form': form})
```

### 2. Product CRUD Web Views

**File**: `store/views.py`

**New/Updated Views**:

```python
@login_required
@require_vendor
def edit_product(request, product_id):
    """Edit existing product (store owner only)"""
    product = get_object_or_404(Product, id=product_id)
    
    # Verify store ownership
    if product.store.vendor != request.user:
        return HttpResponseForbidden("You don't own this product's store")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})


@login_required
@require_vendor
def delete_product(request, product_id):
    """Delete product (soft delete - store owner only)"""
    product = get_object_or_404(Product, id=product_id)
    
    # Verify store ownership
    if product.store.vendor != request.user:
        return HttpResponseForbidden("You don't own this product's store")
    
    if request.method == 'POST':
        # Soft delete
        product.is_active = False
        product.save()
        messages.success(request, 'Product deleted successfully')
        return redirect('my_products')
    
    return render(request, 'store/delete_product.html', {'product': product})
```

**Updated Create Product View**:

```python
@login_required
@require_vendor
def create_product(request):
    """Create new product with Twitter integration"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            # Verify user owns the store
            if product.store.vendor != request.user:
                return HttpResponseForbidden("You don't own this store")
            product.save()
            
            # Send tweet (imported from utils)
            try:
                from .utils import send_product_tweet
                send_product_tweet(product)
            except Exception as e:
                # Log error but don't fail product creation
                logger.error(f"Failed to send product tweet: {e}")
            
            messages.success(request, 'Product created successfully')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    
    return render(request, 'store/create_product.html', {'form': form})
```

### 3. Password Reset Views

**File**: `store/views.py`

**New Views**:

```python
def password_reset_request(request):
    """Request password reset"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Create reset token
            token = PasswordResetToken.objects.create(
                user=user,
                token=uuid.uuid4(),
                expires_at=timezone.now() + timedelta(hours=1)
            )
            
            # Send email
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[token.token])
            )
            send_mail(
                'Password Reset Request',
                f'Click here to reset your password: {reset_url}\nThis link expires in 1 hour.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email sent')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email')
    
    return render(request, 'store/password_reset_request.html')


def password_reset_confirm(request, token):
    """Confirm password reset with token"""
    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            used=False
        )
        
        # Check if expired
        if reset_token.is_expired():
            messages.error(request, 'Reset link has expired')
            return redirect('password_reset_request')
        
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match')
            else:
                # Update password
                user = reset_token.user
                user.set_password(password)
                user.save()
                
                # Mark token as used
                reset_token.used = True
                reset_token.save()
                
                messages.success(request, 'Password reset successfully')
                return redirect('login')
        
        return render(request, 'store/password_reset_confirm.html', {'token': token})
    
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset link')
        return redirect('password_reset_request')
```

### 4. Twitter API v2 Integration

**File**: `store/utils.py`

**Updated Implementation**:

```python
import tweepy
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_twitter_client():
    """Get Twitter API v2 client"""
    try:
        # Use Bearer Token for API v2
        client = tweepy.Client(
            bearer_token=settings.TWITTER_BEARER_TOKEN,
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Twitter client: {e}")
        return None


def send_store_tweet(store):
    """
    Send tweet about new store using API v2
    """
    try:
        client = get_twitter_client()
        if not client:
            logger.warning("Twitter client not available")
            return
        
        # Format tweet text
        tweet_text = f"🏪 New store opened on our platform!\n\n"
        tweet_text += f"Store: {store.name}\n"
        tweet_text += f"Description: {store.description[:100]}\n"
        tweet_text += f"\n#ecommerce #newstore #shopping"
        
        # Send tweet using API v2
        response = client.create_tweet(text=tweet_text)
        
        logger.info(f"Store tweet sent successfully. Tweet ID: {response.data['id']}")
        
    except tweepy.TweepyException as e:
        logger.error(f"Failed to send store tweet: {e}")
    except Exception as e:
        logger.error(f"Unexpected error sending store tweet: {e}")


def send_product_tweet(product):
    """
    Send tweet about new product using API v2 with optional image
    """
    try:
        client = get_twitter_client()
        if not client:
            logger.warning("Twitter client not available")
            return
        
        # Format tweet text
        tweet_text = f"🆕 New product available!\n\n"
        tweet_text += f"Product: {product.name}\n"
        tweet_text += f"Store: {product.store.name}\n"
        tweet_text += f"Price: ${product.price}\n"
        tweet_text += f"\n#newproduct #shopping #ecommerce"
        
        media_ids = None
        
        # Upload image if available (using API v1.1)
        if product.image:
            try:
                # Create API v1.1 instance for media upload
                auth = tweepy.OAuth1UserHandler(
                    settings.TWITTER_API_KEY,
                    settings.TWITTER_API_SECRET,
                    settings.TWITTER_ACCESS_TOKEN,
                    settings.TWITTER_ACCESS_TOKEN_SECRET
                )
                api = tweepy.API(auth)
                
                # Upload media
                media = api.media_upload(product.image.path)
                media_ids = [media.media_id]
                logger.info(f"Product image uploaded. Media ID: {media.media_id}")
            except Exception as e:
                logger.error(f"Failed to upload product image: {e}")
        
        # Send tweet using API v2
        response = client.create_tweet(text=tweet_text, media_ids=media_ids)
        
        logger.info(f"Product tweet sent successfully. Tweet ID: {response.data['id']}")
        
    except tweepy.TweepyException as e:
        logger.error(f"Failed to send product tweet: {e}")
    except Exception as e:
        logger.error(f"Unexpected error sending product tweet: {e}")
```

### 5. URL Routing

**File**: `store/urls.py`

**Updated URL Patterns**:

```python
from django.urls import path
from . import views

urlpatterns = [
    # Store URLs
    path('stores/', views.store_list, name='store_list'),
    path('stores/create/', views.create_store, name='create_store'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('stores/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('stores/<int:store_id>/delete/', views.delete_store, name='delete_store'),
    path('my-stores/', views.my_stores, name='my_stores'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('my-products/', views.my_products, name='my_products'),
    
    # Password Reset URLs
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<uuid:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Other URLs...
]
```

## Data Models

### Updated Models

**File**: `store/models.py`

No changes needed - `is_active` fields already exist on Store and Product models.

**PasswordResetToken Model** (if not exists):

```python
class PasswordResetToken(models.Model):
    """Token for password reset"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    def is_expired(self):
        """Check if token has expired"""
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
```

## Error Handling

### Twitter Integration Error Handling

All Twitter functions use try-except blocks:
- Catch `tweepy.TweepyException` for Twitter-specific errors
- Catch general `Exception` for unexpected errors
- Log all errors with descriptive messages
- Never raise exceptions that would break store/product creation
- Return gracefully when Twitter client is unavailable

### Permission Error Handling

- Use `@login_required` decorator for authentication
- Check ownership before allowing edit/delete
- Return `HttpResponseForbidden` for unauthorized access
- Display user-friendly error messages

### Form Validation Error Handling

- Display field-specific errors on forms
- Preserve form data on validation failure
- Show success messages after successful operations
- Redirect to appropriate pages after operations

## Testing Strategy

### Unit Tests

1. **Store CRUD Tests**
   - Test edit store with owner
   - Test edit store with non-owner (should fail)
   - Test delete store with owner
   - Test delete store with non-owner (should fail)

2. **Product CRUD Tests**
   - Test edit product with store owner
   - Test edit product with non-owner (should fail)
   - Test delete product with store owner
   - Test delete product with non-owner (should fail)

3. **Password Reset Tests**
   - Test reset request with valid email
   - Test reset request with invalid email
   - Test reset confirm with valid token
   - Test reset confirm with expired token
   - Test reset confirm with used token

4. **Twitter Integration Tests**
   - Test send_store_tweet with valid credentials
   - Test send_store_tweet with missing credentials
   - Test send_product_tweet with image
   - Test send_product_tweet without image
   - Test error handling for API failures

### Integration Tests

1. Test complete store creation flow with tweet
2. Test complete product creation flow with tweet
3. Test complete password reset flow
4. Test edit/delete operations through web interface
5. Test permission enforcement across all operations

## Deployment Considerations

### Environment Variables

Add to settings or environment:

```python
# Twitter API v2 Configuration
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN', '')
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', '')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET', '')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', '')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Development
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Production
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
```

### Database Migrations

Run migrations for PasswordResetToken model if new:

```bash
python manage.py makemigrations
python manage.py migrate
```

This design addresses all feedback points and provides a complete, working solution for Part 2 requirements.
