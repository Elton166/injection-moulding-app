import json
from .models import *

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']

				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				'digital':product.digital,'get_total':total,
				}
				items.append(item)

				if product.digital == False:
					order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		# Ensure a Customer exists for the authenticated user; create one if missing.
		try:
			customer = request.user.customer
		except Exception:
			customer, _ = Customer.objects.get_or_create(
				user=request.user,
				defaults={
					'name': getattr(request.user, 'username', '') or '',
					'email': getattr(request.user, 'email', '') or '',
				}
			)

		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			email=email,
			)
	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return customer, order


# Twitter Integration Functions
import tweepy
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_twitter_client():
    """
    Initialize and return Twitter API v2 Client (free tier compatible).
    Uses Client.create_tweet() which is available on free tier.
    """
    try:
        # Check if Twitter credentials are configured
        if not hasattr(settings, 'TWITTER_API_KEY') or not settings.TWITTER_API_KEY:
            logger.warning("Twitter API credentials not configured")
            return None
        
        # Twitter API v2 Client (free tier compatible)
        client = tweepy.Client(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        
        logger.info("Twitter API v2 client initialized successfully")
        return client
        
    except Exception as e:
        logger.error(f"Failed to initialize Twitter API v2 client: {e}")
        return None


def get_twitter_api_v1():
    """
    Initialize Twitter API v1.1 for media upload (still available on free tier).
    """
    try:
        if not hasattr(settings, 'TWITTER_API_KEY') or not settings.TWITTER_API_KEY:
            return None
            
        auth = tweepy.OAuth1UserHandler(
            consumer_key=settings.TWITTER_API_KEY,
            consumer_secret=settings.TWITTER_API_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        
        api = tweepy.API(auth)
        return api
        
    except Exception as e:
        logger.error(f"Failed to initialize Twitter API v1.1: {e}")
        return None


def send_store_tweet(store):
    """
    Send a tweet when a new store is created using Twitter API v2 (free tier compatible).
    
    Args:
        store: Store model instance
    
    Returns:
        bool: True if tweet sent successfully, False otherwise
    """
    try:
        client = get_twitter_client()
        if not client:
            logger.warning("Twitter client not available, skipping store tweet")
            return False
        
        # Create tweet text (280 character limit)
        tweet_text = f"""🏪 New store opened on our platform!

Store: {store.name}
Description: {store.description[:120]}{'...' if len(store.description) > 120 else ''}

Visit us to explore amazing products!

#ecommerce #newstore #shopping"""
        
        # Ensure tweet is within character limit
        if len(tweet_text) > 280:
            max_desc_length = 80
            tweet_text = f"""🏪 New store opened!

{store.name}
{store.description[:max_desc_length]}{'...' if len(store.description) > max_desc_length else ''}

#ecommerce #newstore #shopping"""
        
        # Send tweet using API v2 Client.create_tweet()
        response = client.create_tweet(text=tweet_text)
        logger.info(f"Store tweet sent successfully. Tweet ID: {response.data['id']}")
        return True
        
    except tweepy.TweepyException as e:
        logger.error(f"Failed to send store tweet (Tweepy error): {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to send store tweet: {e}")
        return False


def send_product_tweet(product):
    """
    Send a tweet when a new product is added using Twitter API v2 (free tier compatible).
    
    Args:
        product: Product model instance
    
    Returns:
        bool: True if tweet sent successfully, False otherwise
    """
    try:
        client = get_twitter_client()
        if not client:
            logger.warning("Twitter client not available, skipping product tweet")
            return False
        
        # Create tweet text
        store_hashtag = product.store.name.replace(' ', '').replace('-', '').lower()[:15]
        
        tweet_text = f"""🆕 New product available!

Product: {product.name[:50]}{'...' if len(product.name) > 50 else ''}
Store: {product.store.name}
Price: R{product.price}

{product.description[:60]}{'...' if len(product.description) > 60 else ''}

#newproduct #shopping #{store_hashtag}"""
        
        # Ensure tweet is within character limit
        if len(tweet_text) > 280:
            tweet_text = f"""🆕 {product.name[:40]}{'...' if len(product.name) > 40 else ''}

Store: {product.store.name}
Price: R{product.price}

{product.description[:80]}{'...' if len(product.description) > 80 else ''}

#newproduct #shopping"""
        
        # Handle media upload if product has an image
        media_ids = None
        if product.image:
            try:
                api_v1 = get_twitter_api_v1()
                if api_v1:
                    image_path = product.image.path
                    if os.path.exists(image_path):
                        # Upload media using API v1.1 (still available on free tier)
                        media = api_v1.media_upload(image_path)
                        media_ids = [media.media_id]
                        logger.info(f"Media uploaded successfully: {media.media_id}")
            except Exception as media_error:
                logger.warning(f"Failed to upload media: {media_error}")
                # Continue without media
        
        # Send tweet using API v2 Client.create_tweet()
        if media_ids:
            response = client.create_tweet(text=tweet_text, media_ids=media_ids)
        else:
            response = client.create_tweet(text=tweet_text)
        
        logger.info(f"Product tweet sent successfully. Tweet ID: {response.data['id']}")
        return True
        
    except tweepy.TweepyException as e:
        logger.error(f"Failed to send product tweet (Tweepy error): {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to send product tweet: {e}")
        return False


def format_currency(amount):
    """
    Format currency amount for display.
    """
    return f"${amount:.2f}"


def generate_order_number():
    """
    Generate a unique order number.
    """
    import uuid
    import time
    
    timestamp = str(int(time.time()))
    unique_id = str(uuid.uuid4())[:8]
    return f"ORD-{timestamp}-{unique_id}".upper()