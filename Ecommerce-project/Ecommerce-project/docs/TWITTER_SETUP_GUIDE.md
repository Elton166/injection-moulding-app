# Twitter API Integration Setup Guide (Free Tier Compatible)

## 🐦 Twitter Developer Account Setup (Free Tier)

### Step 1: Create Twitter Developer Account

1. **Visit Twitter Developer Portal**
   - Go to https://developer.twitter.com/
   - Click "Apply for a developer account"

2. **Complete Application**
   - Use your existing Twitter account or create a new one
   - Select "Making a bot" or "Hobbyist" as use case
   - Describe your eCommerce project integration
   - **Important**: Mention it's for educational/learning purposes

3. **Wait for Approval**
   - Twitter typically approves within 24-48 hours
   - You'll receive an email confirmation

### Step 2: Create a Twitter App (Free Tier)

1. **Access Developer Dashboard**
   - Login to https://developer.twitter.com/en/portal/dashboard
   - Click "Create App" (you get 1 app with free tier)

2. **App Configuration**
   - **App Name**: "eCommerce Learning Bot" (or similar)
   - **Description**: "Educational project for learning API integration"
   - **Website URL**: Your GitHub repo or localhost URL
   - **Use Case**: "Learning to integrate social media with eCommerce"

3. **App Permissions (Free Tier)**
   - Set permissions to "Read and Write"
   - **Note**: Free tier allows basic read/write operations

### Step 3: Generate API Keys (Free Tier - API v1.1)

1. **API Keys and Tokens (v1.1 Compatible)**
   - Go to your app's "Keys and Tokens" tab
   - Generate the following (only these 4 are needed for free tier):
     - ✅ **API Key** (Consumer Key)
     - ✅ **API Secret Key** (Consumer Secret)  
     - ✅ **Access Token**
     - ✅ **Access Token Secret**
     - ❌ ~~Bearer Token~~ (Not needed for v1.1)

2. **Save Your Credentials**
   ```
   API Key: [your_api_key]
   API Secret: [your_api_secret]
   Access Token: [your_access_token]
   Access Token Secret: [your_access_token_secret]
   ```

### 🆓 Free Tier Limitations
- **300 tweets per month** (perfect for testing)
- **API v1.1 only** (no v2 features)
- **1 app maximum**
- **Basic authentication** (OAuth 1.0a)

## 🔧 Environment Configuration

### Step 1: Set Environment Variables (Recommended)

**Windows (Command Prompt):**
```cmd
set TWITTER_API_KEY=your_actual_api_key
set TWITTER_API_SECRET=your_actual_api_secret
set TWITTER_ACCESS_TOKEN=your_actual_access_token
set TWITTER_ACCESS_TOKEN_SECRET=your_actual_access_token_secret
```

**Windows (PowerShell):**
```powershell
$env:TWITTER_API_KEY="your_actual_api_key"
$env:TWITTER_API_SECRET="your_actual_api_secret"
$env:TWITTER_ACCESS_TOKEN="your_actual_access_token"
$env:TWITTER_ACCESS_TOKEN_SECRET="your_actual_access_token_secret"
```

### Step 2: Alternative - Direct Settings Update

If you prefer not to use environment variables, you can directly update `ecommerce/settings.py`:

```python
# Twitter API Settings (v1.1 - Free Tier)
TWITTER_API_KEY = 'your_actual_api_key'
TWITTER_API_SECRET = 'your_actual_api_secret'
TWITTER_ACCESS_TOKEN = 'your_actual_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_actual_access_token_secret'
```

**⚠️ Security Warning**: Never commit real API keys to version control!

## 🧪 Testing Twitter Integration

### Step 1: Test Twitter Connection (Free Tier)

Use the provided test script to verify your Twitter setup:

```bash
python test_twitter_free_tier.py
```

This script will:
- ✅ Test API v1.1 authentication
- ✅ Check your rate limits
- ✅ Verify tweet format compatibility
- ✅ Optionally send a test tweet

### Step 2: Manual Test (Alternative)

You can also test manually:

```python
# Quick test in Django shell
python manage.py shell

>>> import tweepy
>>> from django.conf import settings
>>> 
>>> # Test authentication
>>> auth = tweepy.OAuth1UserHandler(
...     settings.TWITTER_API_KEY,
...     settings.TWITTER_API_SECRET,
...     settings.TWITTER_ACCESS_TOKEN,
...     settings.TWITTER_ACCESS_TOKEN_SECRET
... )
>>> api = tweepy.API(auth)
>>> user = api.verify_credentials()
>>> print(f"Authenticated as: @{user.screen_name}")
```

## 📝 Twitter Integration Features

### Automatic Tweets

The system automatically sends tweets when:

1. **New Store Created**
   ```
   🏪 New store opened on our platform!
   
   Store: Tech Gadgets Store
   Description: Latest electronics and gadgets for tech enthusiasts...
   
   Visit us to explore amazing products!
   
   #ecommerce #newstore #shopping #marketplace
   ```

2. **New Product Added**
   ```
   🆕 New product available!
   
   Product: iPhone 15 Pro
   Store: Tech Gadgets Store
   Price: $999.99
   
   Description: Latest iPhone with advanced camera system...
   
   #newproduct #shopping #ecommerce #techgadgetsstore
   ```

### Media Upload

- Store logos (if available) are included in store tweets
- Product images (if available) are included in product tweets
- Graceful fallback if media upload fails

## 🔍 Troubleshooting

### Common Issues

1. **"Forbidden" Error (403)**
   - Check if your app has "Read and Write" permissions
   - Regenerate access tokens after changing permissions

2. **"Unauthorized" Error (401)**
   - Verify all API keys are correct
   - Check if tokens haven't expired

3. **"Rate Limit Exceeded" (429)**
   - Twitter has rate limits (300 tweets per 15 minutes)
   - The integration includes `wait_on_rate_limit=True`

4. **Media Upload Fails**
   - Check if image file exists and is accessible
   - Verify image format (JPEG, PNG, GIF, WebP)
   - Check file size (max 5MB for images)

### Debug Mode

To enable debug output, add this to your Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'store.utils': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📊 Rate Limits

### Twitter API v1.1 Limits (Free Tier)

- **Tweets**: 300 per month (perfect for testing!)
- **Tweet Creation**: 300 per 15-minute window
- **Media Upload**: Included in tweet limit
- **Character Limit**: 280 characters per tweet

### Best Practices

1. **Monitor Usage**: Keep track of your monthly tweet count
2. **Error Handling**: The integration gracefully handles failures
3. **Batch Operations**: Avoid creating many stores/products rapidly
4. **Testing**: Use a test Twitter account for development

## 🚀 Going Live

### Production Checklist

- [ ] Twitter Developer Account approved
- [ ] App created with proper permissions
- [ ] API keys generated and secured
- [ ] Environment variables configured
- [ ] Twitter connection tested
- [ ] Sample tweets sent successfully
- [ ] Error handling verified
- [ ] Rate limiting considered

### Monitoring

Monitor your Twitter integration by:

1. **Checking Django Logs**: Look for Twitter-related messages
2. **Twitter Analytics**: Monitor tweet performance
3. **API Usage**: Track your monthly limits
4. **Error Rates**: Monitor failed tweet attempts

## 📞 Support

If you encounter issues:

1. **Twitter Developer Forums**: https://twittercommunity.com/
2. **Tweepy Documentation**: https://docs.tweepy.org/
3. **Django Logs**: Check your application logs for errors

---

**Note**: This integration is designed to enhance your eCommerce platform's social media presence by automatically announcing new stores and products to your Twitter followers.