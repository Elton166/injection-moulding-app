"""Admin configuration for the store app."""
from django.contrib import admin

from .models import (
    Customer, Order, OrderItem, PasswordResetToken, Product, Review,
    ShippingAddress, Store, UserProfile
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """Admin interface for Store model."""
    list_display = ['name', 'vendor', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'vendor__username', 'email']
    ordering = ['-created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    list_display = ['name', 'store', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['is_active', 'digital', 'created_at', 'store']
    search_fields = ['name', 'store__name']
    ordering = ['-created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ['id', 'customer', 'status', 'complete', 'total_amount', 'date_ordered']
    list_filter = ['status', 'complete', 'date_ordered']
    search_fields = ['customer__username', 'transaction_id']
    ordering = ['-date_ordered']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""
    list_display = ['order', 'product', 'quantity', 'price', 'date_added']
    list_filter = ['date_added']
    ordering = ['-date_added']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review model."""
    list_display = ['product', 'user', 'rating', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['product__name', 'user__username']
    ordering = ['-created_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin interface for PasswordResetToken model."""
    list_display = ['user', 'token', 'created_at', 'expires_at', 'used']
    list_filter = ['used', 'created_at']
    ordering = ['-created_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model."""
    list_display = ['name', 'email', 'user']
    search_fields = ['name', 'email', 'user__username']


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    """Admin interface for ShippingAddress model."""
    list_display = ['customer', 'address', 'city', 'state', 'zipcode', 'date_added']
    list_filter = ['state', 'date_added']
    search_fields = ['customer__username', 'address', 'city']
    ordering = ['-date_added']