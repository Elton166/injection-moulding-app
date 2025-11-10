#!/usr/bin/env python3
"""
Twitter API v1.1 Test Script (Free Tier Compatible)

This script tests the Twitter integration using only API v1.1 features
that are available with the free tier.
"""
import os
import sys
import tweepy
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
sys.path.append('.')
import django
django.setup()

def test_twitter_free_tier():
    """Test Twitter API v1.1 connection (free tier)."""
    print("🐦 Testing Twitter API v1.1 (Free Tier)")
    print("=" * 50)
    
    try:
        # Check if credentials are configured
        if (settings.TWITTER_API_KEY == '[your_twitter_api_key]' or 
            not settings.TWITTER_API_KEY):
            print("❌ Twitter credentials not configured!")
            print("   Please set your Twitter API credentials in environment variables:")
            print("   set TWITTER_API_KEY=your_api_key")
            print("   set TWITTER_API_SECRET=your_api_secret")
            print("   set TWITTER_ACCESS_TOKEN=your_access_token")
            print("   set TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret")
            return False
        
        # Initialize Twitter API v1.1 (free tier)
        print("🔑 Initializing Twitter API v1.1...")
        auth = tweepy.OAuth1UserHandler(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        
        api = tweepy.API(auth, wait_on_rate_limit=True)
        
        # Verify credentials
        print("🔍 Verifying credentials...")
        user = api.verify_credentials()
        print(f"   ✅ Authenticated as: @{user.screen_name}")
        print(f"   ✅ Account: {user.name}")
        print(f"   ✅ Followers: {user.followers_count}")
        
        # Check rate limits
        print("\n📊 Checking rate limits...")
        rate_limit = api.get_rate_limit_status()
        statuses_limit = rate_limit['resources']['statuses']['/statuses/update']
        
        print(f"   ✅ Tweet limit: {statuses_limit['remaining']}/{statuses_limit['limit']}")
        print(f"   ✅ Reset time: {statuses_limit['reset']}")
        
        # Test tweet (optional - uncomment to actually send a test tweet)
        send_test_tweet = input("\n🧪 Send a test tweet? (y/n): ").lower()
        
        if send_test_tweet == 'y':
            test_message = "🧪 Testing Twitter API v1.1 integration for Django eCommerce project! #test #django #ecommerce"
            
            try:
                status = api.update_status(test_message)
                print(f"   ✅ Test tweet sent successfully!")
                print(f"   ✅ Tweet ID: {status.id}")
                print(f"   ✅ Tweet URL: https://twitter.com/{user.screen_name}/status/{status.id}")
                
                # Delete the test tweet after 5 seconds (cleanup)
                import time
                print("   🧹 Cleaning up test tweet in 5 seconds...")
                time.sleep(5)
                api.destroy_status(status.id)
                print("   ✅ Test tweet deleted")
                
            except Exception as tweet_error:
                print(f"   ❌ Failed to send test tweet: {tweet_error}")
        
        print("\n" + "=" * 50)
        print("🎉 Twitter API v1.1 Test Complete!")
        print("✅ Your Twitter integration is ready for the free tier!")
        
        return True
        
    except tweepy.Unauthorized:
        print("❌ Twitter authentication failed!")
        print("   Check your API keys and make sure they're correct")
        print("   Make sure your app has 'Read and Write' permissions")
        return False
        
    except tweepy.Forbidden:
        print("❌ Twitter access forbidden!")
        print("   Your app might not have the required permissions")
        print("   Make sure your app has 'Read and Write' permissions")
        return False
        
    except Exception as e:
        print(f"❌ Twitter test failed: {e}")
        return False

def test_store_tweet_format():
    """Test the store tweet format without actually sending."""
    print("\n📝 Testing Store Tweet Format...")
    
    # Mock store data
    class MockStore:
        name = "Amazing Tech Store"
        description = "We sell the latest and greatest technology products including smartphones, laptops, tablets, and accessories for all your tech needs."
    
    store = MockStore()
    
    # Create tweet text (same logic as in utils.py)
    tweet_text = f"""🏪 New store opened on our platform!

Store: {store.name}
Description: {store.description[:120]}{'...' if len(store.description) > 120 else ''}

Visit us to explore amazing products!

#ecommerce #newstore #shopping"""
    
    print(f"   Tweet length: {len(tweet_text)} characters")
    print(f"   Within limit: {'✅ Yes' if len(tweet_text) <= 280 else '❌ No'}")
    print(f"\n   Preview:")
    print(f"   {'-' * 40}")
    print(f"   {tweet_text}")
    print(f"   {'-' * 40}")

def test_product_tweet_format():
    """Test the product tweet format without actually sending."""
    print("\n📝 Testing Product Tweet Format...")
    
    # Mock product data
    class MockProduct:
        name = "iPhone 15 Pro Max with Advanced Camera System"
        price = 1199.99
        description = "The most advanced iPhone ever with titanium design, A17 Pro chip, and professional camera system for stunning photos and videos."
        
        class store:
            name = "Tech Gadgets Store"
    
    product = MockProduct()
    
    # Create tweet text (same logic as in utils.py)
    store_hashtag = product.store.name.replace(' ', '').replace('-', '').lower()[:15]
    
    tweet_text = f"""🆕 New product available!

Product: {product.name[:50]}{'...' if len(product.name) > 50 else ''}
Store: {product.store.name}
Price: ${product.price}

Description: {product.description[:60]}{'...' if len(product.description) > 60 else ''}

#newproduct #shopping #{store_hashtag}"""
    
    print(f"   Tweet length: {len(tweet_text)} characters")
    print(f"   Within limit: {'✅ Yes' if len(tweet_text) <= 280 else '❌ No'}")
    print(f"\n   Preview:")
    print(f"   {'-' * 40}")
    print(f"   {tweet_text}")
    print(f"   {'-' * 40}")

def main():
    """Main test function."""
    print("🚀 Twitter Free Tier Integration Test")
    print("=" * 50)
    
    # Test API connection
    if test_twitter_free_tier():
        # Test tweet formats
        test_store_tweet_format()
        test_product_tweet_format()
        
        print("\n🎯 Free Tier Benefits:")
        print("   ✅ 300 tweets per month (perfect for testing)")
        print("   ✅ API v1.1 compatibility")
        print("   ✅ Media upload support")
        print("   ✅ No elevated access required")
        
        print("\n📝 Next Steps:")
        print("   1. Create stores and products via API")
        print("   2. Watch automatic tweets being sent")
        print("   3. Monitor your monthly usage")
        
    else:
        print("\n💡 Troubleshooting:")
        print("   1. Make sure you have a Twitter Developer account")
        print("   2. Create an app with 'Read and Write' permissions")
        print("   3. Generate API keys and access tokens")
        print("   4. Set environment variables with your credentials")

if __name__ == "__main__":
    main()