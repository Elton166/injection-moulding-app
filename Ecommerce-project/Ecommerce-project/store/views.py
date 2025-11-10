"""
Views for the eCommerce store application.

This module contains all the view functions for handling user requests,
including product display, cart management, user authentication, and
order processing.
"""
import json
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Customer, Order, OrderItem, PasswordResetToken, Product, Review,
    ShippingAddress, Store, UserProfile
)


def store(request):
    """Display all active products and stores."""
    products = Product.objects.filter(is_active=True)
    stores = Store.objects.filter(is_active=True)
    
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cartItems = sum([cart[key]['quantity'] for key in cart]) if cart else 0
    
    context = {'products': products, 'stores': stores, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def product_detail(request, product_id):
    """Display detailed product information with reviews."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    
    # Check if user has purchased this product for verified reviews
    user_purchased = False
    if request.user.is_authenticated:
        user_purchased = OrderItem.objects.filter(
            order__customer=request.user,
            order__complete=True,
            product=product
        ).exists()
    
    context = {
        'product': product,
        'reviews': reviews,
        'user_purchased': user_purchased
    }
    return render(request, 'store/product_detail.html', context)


@login_required
def add_review(request, product_id):
    """Add a review for a product."""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        
        # Check if user has purchased this product
        user_purchased = OrderItem.objects.filter(
            order__customer=request.user,
            order__complete=True,
            product=product
        ).exists()
        
        review, created = Review.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'comment': comment,
                'is_verified': user_purchased
            }
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.is_verified = user_purchased
            review.save()
        
        messages.success(request, 'Review added successfully')
        return redirect('product_detail', product_id=product_id)
    
    context = {'product': product}
    return render(request, 'store/add_review.html', context)


def register_view(request):
    """Handle user registration with proper validation."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', '')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists')
            
        if not email:
            errors.append('Email is required')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already registered')
            
        if not password:
            errors.append('Password is required')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long')
            
        if not user_type or user_type not in ['buyer', 'vendor']:
            errors.append('Please select a valid account type')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'store/register.html', {
                'username': username,
                'email': email,
                'user_type': user_type
            })
        
        try:
            # Create user and profile
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name='',
                last_name=''
            )
            UserProfile.objects.create(user=user, user_type=user_type)
            
            messages.success(request, f'Registration successful! Welcome {username}. You can now login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, 'Registration failed. Please try again.')
            return render(request, 'store/register.html')
    
    return render(request, 'store/register.html')


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'store/login.html')


def logout_view(request):
    """Handle user logout - POST method only for security."""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('store')
    else:
        # If GET request, show confirmation page or redirect
        messages.warning(request, 'Please use the logout button to log out.')
        return redirect('store')


def cart(request):
    """Display shopping cart contents."""
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Handle cart in cookies for non-logged in users
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
        
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                
                item = {
                    'id': product.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'digital': product.digital,
                    'get_total': total,
                }
                items.append(item)
                
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@csrf_exempt
def updateItem(request):
    """Update cart items via AJAX."""
    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        
        print('Action:', action)
        print('Product:', productId)
        
        if request.user.is_authenticated:
            product = Product.objects.get(id=productId)
            order, created = Order.objects.get_or_create(customer=request.user, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(
                order=order, 
                product=product,
                defaults={'price': product.price}
            )
            
            if action == 'add':
                orderItem.quantity = (orderItem.quantity + 1)
            elif action == 'remove':
                orderItem.quantity = (orderItem.quantity - 1)
            
            orderItem.save()
            
            if orderItem.quantity <= 0:
                orderItem.delete()
                
        return JsonResponse('Item was added', safe=False)
        
    except Exception as e:
        print('Error:', str(e))
        return JsonResponse({'error': str(e)}, status=400)


def checkout(request):
    """Handle checkout process."""
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Handle cart in cookies for non-logged in users
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
            
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        
        for i in cart:
            try:
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                
                item = {
                    'id': product.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                    },
                    'quantity': cart[i]['quantity'],
                    'digital': product.digital,
                    'get_total': total,
                }
                items.append(item)
                
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    
    if request.method == 'POST' and request.user.is_authenticated:
        with transaction.atomic():
            if order.orderitem_set.exists():
                # Calculate total
                total = order.get_cart_total
                order.total_amount = total
                order.complete = True
                order.transaction_id = str(uuid.uuid4())
                order.save()
                
                # Create shipping address
                ShippingAddress.objects.create(
                    customer=request.user,
                    order=order,
                    address=request.POST['address'],
                    city=request.POST['city'],
                    state=request.POST['state'],
                    zipcode=request.POST['zipcode']
                )
                
                # Send invoice email
                send_invoice_email(request.user, order)
                
                messages.success(request, 'Order placed successfully! Check your email for the invoice.')
                return redirect('store')
            else:
                messages.error(request, 'Your cart is empty.')

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def send_invoice_email(user, order):
    """Send invoice email to customer."""
    subject = f'Invoice for Order #{order.id}'
    
    message = f"""
    Dear {user.username},
    
    Thank you for your order! Here's your invoice:
    
    Order ID: {order.transaction_id}
    Date: {order.date_ordered.strftime('%Y-%m-%d %H:%M')}
    
    Items:
    """
    
    for item in order.orderitem_set.all():
        message += f"- {item.product.name} x {item.quantity} = R{item.get_total}\n"
    
    message += f"\nTotal: R{order.total_amount}"
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")


def forgot_password(request):
    """Handle password reset requests."""
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            
            # Create password reset token
            token = PasswordResetToken.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            
            # Send reset email
            reset_url = request.build_absolute_uri(f'/reset-password/{token.token}/')
            subject = 'Password Reset Request'
            message = f"""
            Hi {user.username},
            
            You requested a password reset. Click the link below to reset your password:
            {reset_url}
            
            This link will expire in 24 hours.
            
            If you didn't request this, please ignore this email.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email sent! Check your inbox.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email address.')
    
    return render(request, 'store/forgot_password.html')


def reset_password(request, token):
    """Handle password reset with token."""
    try:
        reset_token = PasswordResetToken.objects.get(token=token, used=False)
        
        if reset_token.is_expired():
            messages.error(request, 'This reset link has expired.')
            return redirect('forgot_password')
        
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'store/reset_password.html', {'token': token})
            
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            reset_token.used = True
            reset_token.save()
            
            messages.success(request, 'Password reset successfully! You can now log in.')
            return redirect('login')
        
        return render(request, 'store/reset_password.html', {'token': token})
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset link.')
        return redirect('forgot_password')


# Vendor-specific views
@login_required
def vendor_dashboard(request):
    """Vendor dashboard for managing stores and products."""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('store')
    
    stores = Store.objects.filter(vendor=request.user)
    products = Product.objects.filter(store__vendor=request.user)
    
    # Calculate statistics
    total_stores = stores.count()
    total_products = products.count()
    total_orders = OrderItem.objects.filter(product__store__vendor=request.user).count()
    total_revenue = sum(item.get_total for item in OrderItem.objects.filter(
        product__store__vendor=request.user,
        order__complete=True
    ))
    
    context = {
        'stores': stores,
        'products': products,
        'total_stores': total_stores,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'store/vendor_dashboard.html', context)


@login_required
def create_store(request):
    """Create a new store."""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('store')
    
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        
        store = Store.objects.create(
            vendor=request.user,
            name=name,
            description=description,
            address=address,
            phone=phone,
            email=email
        )
        
        # Send tweet about new store
        try:
            from .utils import send_store_tweet
            send_store_tweet(store)
        except Exception as e:
            # Log error but don't fail store creation
            print(f"Failed to send store tweet: {e}")
        
        messages.success(request, 'Store created successfully')
        return redirect('vendor_dashboard')
    
    return render(request, 'store/create_store.html')


@login_required
def add_product(request):
    """Add a product to a store."""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('store')
    
    # Get user's stores
    user_stores = Store.objects.filter(vendor=request.user)
    
    if request.method == 'POST':
        try:
            store_id = request.POST.get('store')
            store = get_object_or_404(Store, id=store_id, vendor=request.user)
            
            name = request.POST.get('name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock_quantity = request.POST.get('stock_quantity')
            is_active = request.POST.get('is_active') == 'on'
            image = request.FILES.get('image')
            
            product = Product.objects.create(
                store=store,
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity,
                is_active=is_active,
                image=image
            )
            
            # Send tweet about new product
            try:
                from .utils import send_product_tweet
                send_product_tweet(product)
            except Exception as e:
                # Log error but don't fail product creation
                print(f"Failed to send product tweet: {e}")
            
            messages.success(request, f'Product "{name}" added successfully to {store.name}!')
            return redirect('vendor_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
    
    context = {'user_stores': user_stores}
    return render(request, 'store/add_product.html', context)



@login_required
def store_detail(request, store_id):
    """View store details and products."""
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store, is_active=True)
    
    context = {
        'store': store,
        'products': products
    }
    return render(request, 'store/store_detail.html', context)


@login_required
def edit_store(request, store_id):
    """Edit store details."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        store.name = request.POST.get('name')
        store.description = request.POST.get('description')
        store.address = request.POST.get('address')
        store.phone = request.POST.get('phone')
        store.email = request.POST.get('email')
        store.is_active = request.POST.get('is_active') == 'on'
        store.save()
        
        messages.success(request, 'Store updated successfully!')
        return redirect('vendor_dashboard')
    
    context = {'store': store}
    return render(request, 'store/edit_store.html', context)


@login_required
def edit_product(request, product_id):
    """Edit product details."""
    product = get_object_or_404(Product, id=product_id, store__vendor=request.user)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.stock_quantity = request.POST.get('stock_quantity')
        product.is_active = request.POST.get('is_active') == 'on'
        
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        
        product.save()
        
        messages.success(request, 'Product updated successfully!')
        return redirect('vendor_dashboard')
    
    context = {'product': product}
    return render(request, 'store/edit_product.html', context)


@login_required
def delete_store(request, store_id):
    """Delete a store (soft delete)."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    
    if request.method == 'POST':
        # Soft delete - set is_active to False
        store.is_active = False
        store.save()
        messages.success(request, f'Store "{store.name}" has been deleted successfully!')
        return redirect('vendor_dashboard')
    
    context = {'store': store}
    return render(request, 'store/delete_store.html', context)


@login_required
def delete_product(request, product_id):
    """Delete a product (soft delete)."""
    product = get_object_or_404(Product, id=product_id, store__vendor=request.user)
    
    if request.method == 'POST':
        # Soft delete - set is_active to False
        product.is_active = False
        product.save()
        messages.success(request, f'Product "{product.name}" has been deleted successfully!')
        return redirect('vendor_dashboard')
    
    context = {'product': product}
    return render(request, 'store/delete_product.html', context)


@login_required
def manage_products(request):
    """Manage all vendor products."""
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'vendor':
        messages.error(request, 'Access denied. Vendors only.')
        return redirect('store')
    
    products = Product.objects.filter(store__vendor=request.user)
    
    context = {'products': products}
    return render(request, 'store/manage_products.html', context)


@login_required
def profile(request):
    """User profile page."""
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user, user_type='buyer')
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        user_profile.phone = request.POST.get('phone', '')
        user_profile.address = request.POST.get('address', '')
        user_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {'user_profile': user_profile}
    return render(request, 'store/profile.html', context)


@csrf_exempt
def process_order(request):
    """Process order from checkout."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if request.user.is_authenticated:
                customer = request.user
                order, created = Order.objects.get_or_create(customer=customer, complete=False)
            else:
                # Handle guest checkout
                customer_data = data['form']
                email = customer_data['email']
                name = customer_data['name']
                
                customer, created = Customer.objects.get_or_create(email=email)
                customer.name = name
                customer.save()
                
                order = Order.objects.create(customer=customer, complete=False)
            
            # Mark order as complete
            total = float(data['form']['total'])
            order.transaction_id = str(uuid.uuid4())
            order.complete = True
            order.save()
            
            # Create shipping address if needed
            if order.shipping:
                ShippingAddress.objects.create(
                    customer=customer,
                    order=order,
                    address=data['shipping']['address'],
                    city=data['shipping']['city'],
                    state=data['shipping']['state'],
                    zipcode=data['shipping']['zipcode'],
                )
            
            return JsonResponse({'message': 'Order processed successfully'}, status=200)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
