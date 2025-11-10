# 🚀 Start Here: Part 2 Fixes Implementation

## Quick Overview

You have a complete spec to fix all 5 feedback points from your Part 2 submission. This guide helps you get started quickly.

## 📋 What Needs to be Fixed

1. **Part 1 Verification** - Ensure all Part 1 features work
2. **Edit/Delete Missing** - Add edit and delete for stores and products
3. **Password Reset Missing** - Add "Forgot Password" functionality
4. **Twitter Only in API** - Add Twitter integration to web views too
5. **Twitter API Error** - Fix 403 error by using API v2

## 📁 Your Spec Files

```
.kiro/specs/ecommerce-fixes-part2/
├── requirements.md  ← Read this first (14 requirements)
├── design.md        ← Then read this (technical design)
└── tasks.md         ← Then follow this (implementation steps)
```

## 🎯 Implementation Order

### Step 1: Read the Spec (15 minutes)
1. Open `requirements.md` - understand what needs to be built
2. Open `design.md` - see how to build it
3. Open `tasks.md` - see the step-by-step plan

### Step 2: Start with Twitter Fix (30 minutes)
**Why first?** This fixes the immediate 403 error

- [ ] Task 2.1: Update `store/utils.py`
  - Replace `tweepy.API` with `tweepy.Client`
  - Replace `update_status()` with `create_tweet()`
  - Add Bearer Token authentication
  
- [ ] Task 2.2: Update `ecommerce/settings.py`
  - Add `TWITTER_BEARER_TOKEN` setting

**Test**: Create a store via API - should tweet without 403 error

### Step 3: Add Twitter to Web Views (20 minutes)
**Why next?** Ensures tweets work everywhere

- [ ] Task 3.1: Update `store/views.py` create_store
  - Import `send_store_tweet`
  - Call after store creation
  
- [ ] Task 3.2: Update `store/views.py` create_product
  - Import `send_product_tweet`
  - Call after product creation

**Test**: Create store via web form - should tweet

### Step 4: Add Store Edit/Delete (1 hour)
**Why next?** Core missing functionality

- [ ] Task 4: Store Edit
  - Create `edit_store` view
  - Create `edit_store.html` template
  - Add URL pattern
  - Add edit button to UI
  
- [ ] Task 5: Store Delete
  - Create `delete_store` view
  - Create `delete_store.html` template
  - Add URL pattern
  - Add delete button to UI

**Test**: Edit and delete your own store

### Step 5: Add Product Edit/Delete (1 hour)
**Why next?** Same as stores

- [ ] Task 6: Product Edit
- [ ] Task 7: Product Delete

**Test**: Edit and delete your own product

### Step 6: Add Password Reset (1.5 hours)
**Why next?** Important security feature

- [ ] Task 8: Password Reset
  - Verify/create PasswordResetToken model
  - Create request view
  - Create confirm view
  - Create templates
  - Add URLs
  - Update login page
  - Configure email

**Test**: Request password reset, receive email, reset password

### Step 7: Write Tests (2 hours)
**Why next?** Verify everything works

- [ ] Task 10: All tests
  - Store CRUD tests
  - Product CRUD tests
  - Password reset tests
  - Twitter tests
  - Form validation tests

**Test**: Run `python manage.py test`

### Step 8: Update Documentation (30 minutes)
**Why last?** Document what you built

- [ ] Task 11: Documentation
  - Update README
  - Create Twitter v2 guide
  - Update user guide
  - Update API docs

### Step 9: Final Verification (30 minutes)
**Why last?** Ensure all feedback addressed

- [ ] Task 12: Test everything
  - Complete vendor flow
  - Password reset flow
  - Twitter integration
  - Permission checks

## 🔧 Quick Code Examples

### Twitter API v2 (Task 2.1)

**File**: `store/utils.py`

```python
import tweepy
from django.conf import settings

def get_twitter_client():
    """Get Twitter API v2 client"""
    client = tweepy.Client(
        bearer_token=settings.TWITTER_BEARER_TOKEN,
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    return client

def send_store_tweet(store):
    """Send tweet using API v2"""
    try:
        client = get_twitter_client()
        tweet_text = f"🏪 New store: {store.name}!"
        response = client.create_tweet(text=tweet_text)
        print(f"Tweet sent: {response.data['id']}")
    except Exception as e:
        print(f"Tweet failed: {e}")
```

### Store Edit View (Task 4.1)

**File**: `store/views.py`

```python
@login_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    
    # Check ownership
    if store.vendor != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated!')
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm(instance=store)
    
    return render(request, 'store/edit_store.html', {'form': form})
```

### Password Reset Request (Task 8.2)

**File**: `store/views.py`

```python
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        
        # Create token
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
            'Password Reset',
            f'Reset link: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )
        
        messages.success(request, 'Email sent!')
        return redirect('login')
    
    return render(request, 'store/password_reset_request.html')
```

## ✅ Testing Checklist

After implementation, verify:

- [ ] Can edit own store (web)
- [ ] Cannot edit other's store (403)
- [ ] Can delete own store (web)
- [ ] Cannot delete other's store (403)
- [ ] Same for products
- [ ] Password reset link on login page
- [ ] Can request password reset
- [ ] Receive reset email
- [ ] Can reset password with link
- [ ] Expired link rejected
- [ ] Tweet sent when creating store (web)
- [ ] Tweet sent when creating product (web)
- [ ] Tweet sent when creating store (API)
- [ ] Tweet sent when creating product (API)
- [ ] No 403 error from Twitter
- [ ] App works without Twitter credentials

## 🆘 Common Issues

### Twitter 403 Error
**Problem**: Still getting 403 Forbidden
**Solution**: Make sure you're using `Client.create_tweet()` not `API.update_status()`

### Permission Denied
**Problem**: Can't edit/delete resources
**Solution**: Check ownership verification in views

### Email Not Sending
**Problem**: Password reset email not received
**Solution**: Check EMAIL_BACKEND in settings (use console for dev)

### Import Error
**Problem**: Cannot import send_store_tweet
**Solution**: Make sure it's in `store/utils.py` and imported correctly

## 📚 Resources

- **Tweepy Client Docs**: https://docs.tweepy.org/en/stable/client.html
- **Django Email**: https://docs.djangoproject.com/en/5.2/topics/email/
- **Django Forms**: https://docs.djangoproject.com/en/5.2/topics/forms/

## 🎓 Tips

1. **Test as you go** - Don't wait until the end
2. **Commit often** - After each task
3. **Read error messages** - They tell you what's wrong
4. **Use the design doc** - It has code examples
5. **Ask for help** - If stuck for more than 30 minutes

## 📊 Progress Tracking

Use the tasks.md file to track progress:
- `[ ]` = Not started
- `[x]` = Completed

Or use this checklist:
- [ ] Task 1: Verify Part 1
- [ ] Task 2: Twitter API v2
- [ ] Task 3: Twitter web integration
- [ ] Task 4: Store edit
- [ ] Task 5: Store delete
- [ ] Task 6: Product edit
- [ ] Task 7: Product delete
- [ ] Task 8: Password reset
- [ ] Task 9: API verification
- [ ] Task 10: Tests
- [ ] Task 11: Documentation
- [ ] Task 12: Final verification

---

**Ready to start?** Open `.kiro/specs/ecommerce-fixes-part2/tasks.md` and begin with Task 1!

**Estimated Time**: 8-12 hours total
**Difficulty**: Intermediate
**Status**: Spec complete, ready to implement
