"""
Models for the eCommerce store application.

This module defines the database models for users, stores, products,
orders, reviews, and other core entities of the eCommerce platform.
"""
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


USER_TYPE_CHOICES = [
    ('buyer', 'Buyer'),
    ('vendor', 'Vendor'),
]


class UserProfile(models.Model):
    """
    Extended user profile with additional fields for eCommerce functionality.
    
    Attributes:
        user: One-to-one relationship with Django User model
        user_type: Type of user (buyer or vendor)
        phone: User's phone number
        address: User's address
        created_at: Timestamp when profile was created
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        help_text="Associated Django user account"
    )
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='buyer',
        help_text="Type of user account"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="User's phone number"
    )
    address = models.TextField(
        blank=True, 
        null=True,
        help_text="User's address"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        null=True,
        help_text="When the profile was created"
    )

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class Customer(models.Model):
    """Legacy customer model for backward compatibility."""
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Store(models.Model):
    """
    Store model representing vendor stores.
    
    Each vendor can have multiple stores.
    """
    vendor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'userprofile__user_type': 'vendor'}
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model with enhanced fields for eCommerce functionality.
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        """Return the image URL or empty string if no image."""
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def average_rating(self):
        """Calculate the average rating for this product."""
        reviews = self.review_set.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0

    def total_reviews(self):
        """Return the total number of reviews for this product."""
        return self.review_set.count()

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class Order(models.Model):
    """
    Order model for managing customer orders.
    """
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date_ordered']

    def __str__(self):
        return f"Order {self.id} - {self.customer.username if self.customer else 'Anonymous'}"

    @property
    def get_cart_total(self):
        """Calculate the total cost of all items in the order."""
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        """Calculate the total number of items in the order."""
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 


class OrderItem(models.Model):
    """
    Individual items within an order.
    """
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    @property
    def get_total(self):
        """Calculate the total cost for this order item."""
        return self.price * self.quantity


class ShippingAddress(models.Model):
    """
    Shipping address information for orders.
    """
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Shipping Addresses"
        ordering = ['-date_added']

    def __str__(self):
        return self.address


class Review(models.Model):
    """
    Product review model with rating and comments.
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating} stars"


class PasswordResetToken(models.Model):
    """
    Token model for secure password reset functionality.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_expired(self):
        """Check if the token has expired."""
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Reset token for {self.user.username}"