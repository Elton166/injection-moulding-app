"""
API views for the eCommerce store application.

This module contains all the API view classes for handling REST API requests
for stores, products, and reviews.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Store, Product, Review, UserProfile
from .serializers import (
    StoreListSerializer, StoreDetailSerializer, StoreCreateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer,
    ReviewSerializer, ReviewCreateSerializer, VendorStoreSerializer,
    UserProfileSerializer
)
from .permissions import (
    IsVendorOrReadOnly, IsOwnerOrReadOnly, IsStoreOwnerOrReadOnly,
    IsReviewOwnerOrReadOnly, IsVendor, IsAuthenticatedOrReadOnly
)
from .utils import send_store_tweet, send_product_tweet


class StoreListCreateView(generics.ListCreateAPIView):
    """
    List all stores or create a new store.
    
    GET: Returns a list of all active stores (public access)
    POST: Creates a new store (vendor only)
    """
    queryset = Store.objects.filter(is_active=True)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendorOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StoreCreateSerializer
        return StoreListSerializer
    
    def perform_create(self, serializer):
        """Create a new store and send a tweet."""
        store = serializer.save()
        
        # Send tweet about new store
        try:
            send_store_tweet(store)
        except Exception as e:
            # Log the error but don't fail the store creation
            print(f"Failed to send store tweet: {e}")
    
    def create(self, request, *args, **kwargs):
        """Override create to return standardized response."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get the created store with full details
        store = serializer.instance
        response_serializer = StoreListSerializer(store, context={'request': request})
        
        return Response({
            'success': True,
            'message': 'Store created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a store.
    
    GET: Returns store details (public access)
    PUT/PATCH: Updates store (owner only)
    DELETE: Deletes store (owner only)
    """
    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    
    GET: Returns a list of all active products (public access)
    POST: Creates a new product (vendor only)
    """
    queryset = Product.objects.filter(is_active=True)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendorOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        """Filter products by store if store_id is provided."""
        queryset = Product.objects.filter(is_active=True)
        store_id = self.request.query_params.get('store_id')
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset
    
    def perform_create(self, serializer):
        """Create a new product and send a tweet."""
        product = serializer.save()
        
        # Send tweet about new product
        try:
            send_product_tweet(product)
        except Exception as e:
            # Log the error but don't fail the product creation
            print(f"Failed to send product tweet: {e}")
    
    def create(self, request, *args, **kwargs):
        """Override create to return standardized response."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get the created product with full details
        product = serializer.instance
        response_serializer = ProductListSerializer(product, context={'request': request})
        
        return Response({
            'success': True,
            'message': 'Product created successfully',
            'data': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product.
    
    GET: Returns product details (public access)
    PUT/PATCH: Updates product (store owner only)
    DELETE: Deletes product (store owner only)
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStoreOwnerOrReadOnly]


class StoreProductsView(generics.ListAPIView):
    """
    List all products for a specific store.
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        store_id = self.kwargs['store_id']
        return Product.objects.filter(store_id=store_id, is_active=True)


class ProductReviewsView(generics.ListCreateAPIView):
    """
    List reviews for a product or create a new review.
    
    GET: Returns reviews for the product (public access)
    POST: Creates a new review (vendors only)
    """
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendorOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id).order_by('-created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def perform_create(self, serializer):
        """Create a new review for the product."""
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        serializer.save(user=self.request.user, product=product)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a review.
    
    GET: Returns review details (public access)
    PUT/PATCH: Updates review (author only)
    DELETE: Deletes review (author only)
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsReviewOwnerOrReadOnly]


class VendorStoresView(generics.ListAPIView):
    """
    List all stores for a specific vendor.
    """
    serializer_class = StoreListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return Store.objects.filter(vendor_id=vendor_id, is_active=True)


class VendorProductsView(generics.ListAPIView):
    """
    List all products for a specific vendor.
    """
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        vendor_id = self.kwargs['vendor_id']
        return Product.objects.filter(
            store__vendor_id=vendor_id, 
            is_active=True
        )


class MyStoresView(generics.ListAPIView):
    """
    List current vendor's stores.
    """
    serializer_class = VendorStoreSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendor]
    
    def get_queryset(self):
        return Store.objects.filter(vendor=self.request.user)


class MyProductsView(generics.ListAPIView):
    """
    List current vendor's products.
    """
    serializer_class = ProductListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsVendor]
    
    def get_queryset(self):
        return Product.objects.filter(store__vendor=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile_view(request):
    """
    Get current user's profile information.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response({
            'success': True,
            'data': serializer.data
        })
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'error': {
                'code': 'PROFILE_NOT_FOUND',
                'message': 'User profile not found'
            }
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def api_overview(request):
    """
    API overview with available endpoints.
    """
    api_urls = {
        'Authentication': {
            'Login': '/api/auth/login/',
            'Refresh Token': '/api/auth/refresh/',
            'User Profile': '/api/auth/profile/',
        },
        'Stores': {
            'List/Create Stores': '/api/stores/',
            'Store Detail': '/api/stores/{id}/',
            'My Stores': '/api/stores/my-stores/',
            'Store Products': '/api/stores/{store_id}/products/',
        },
        'Products': {
            'List/Create Products': '/api/products/',
            'Product Detail': '/api/products/{id}/',
            'My Products': '/api/products/my-products/',
            'Product Reviews': '/api/products/{product_id}/reviews/',
        },
        'Reviews': {
            'Review Detail': '/api/reviews/{id}/',
        },
        'Vendors': {
            'Vendor Stores': '/api/vendors/{vendor_id}/stores/',
            'Vendor Products': '/api/vendors/{vendor_id}/products/',
        }
    }
    
    return Response({
        'success': True,
        'message': 'eCommerce API Overview',
        'data': api_urls
    })


class APIResponseMixin:
    """
    Mixin to standardize API responses.
    """
    
    def finalize_response(self, request, response, *args, **kwargs):
        """Wrap response data in standard format."""
        response = super().finalize_response(request, response, *args, **kwargs)
        
        if response.status_code >= 200 and response.status_code < 300:
            if isinstance(response.data, dict) and 'success' not in response.data:
                response.data = {
                    'success': True,
                    'data': response.data
                }
        else:
            if isinstance(response.data, dict) and 'success' not in response.data:
                response.data = {
                    'success': False,
                    'error': {
                        'code': 'API_ERROR',
                        'message': 'An error occurred',
                        'details': response.data
                    }
                }
        
        return response