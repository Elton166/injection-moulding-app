"""
URL configuration for the eCommerce store API.

This module defines all the URL patterns for the REST API endpoints.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import api_views

app_name = 'store_api'

urlpatterns = [
    # API Overview
    path('', api_views.api_overview, name='api_overview'),
    
    # Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', api_views.user_profile_view, name='user_profile'),
    
    # Store endpoints
    path('stores/', api_views.StoreListCreateView.as_view(), name='store_list_create'),
    path('stores/<int:pk>/', api_views.StoreDetailView.as_view(), name='store_detail'),
    path('stores/my-stores/', api_views.MyStoresView.as_view(), name='my_stores'),
    path('stores/<int:store_id>/products/', api_views.StoreProductsView.as_view(), name='store_products'),
    
    # Product endpoints
    path('products/', api_views.ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', api_views.ProductDetailView.as_view(), name='product_detail'),
    path('products/my-products/', api_views.MyProductsView.as_view(), name='my_products'),
    path('products/<int:product_id>/reviews/', api_views.ProductReviewsView.as_view(), name='product_reviews'),
    
    # Review endpoints
    path('reviews/<int:pk>/', api_views.ReviewDetailView.as_view(), name='review_detail'),
    
    # Vendor endpoints
    path('vendors/<int:vendor_id>/stores/', api_views.VendorStoresView.as_view(), name='vendor_stores'),
    path('vendors/<int:vendor_id>/products/', api_views.VendorProductsView.as_view(), name='vendor_products'),
]