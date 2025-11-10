"""
Custom permissions for the eCommerce store API.

This module defines custom permission classes for controlling access
to API endpoints based on user roles and ownership.
"""
from rest_framework import permissions
from .models import UserProfile


class IsVendorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow vendors to create/edit resources.
    Read permissions are allowed for any request.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed for authenticated vendors
        if not request.user.is_authenticated:
            return False
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return user_profile.user_type == 'vendor'
        except UserProfile.DoesNotExist:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed for any request.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object
        if hasattr(obj, 'vendor'):
            return obj.vendor == request.user
        elif hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'store'):
            return obj.store.vendor == request.user
        
        return False


class IsStoreOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow store owners to edit their products.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the store owner
        return obj.store.vendor == request.user


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow review authors to edit their reviews.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the review author
        return obj.user == request.user


class IsVendor(permissions.BasePermission):
    """
    Permission class to check if user is a vendor.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return user_profile.user_type == 'vendor'
        except UserProfile.DoesNotExist:
            return False


class IsBuyer(permissions.BasePermission):
    """
    Permission class to check if user is a buyer.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return user_profile.user_type == 'buyer'
        except UserProfile.DoesNotExist:
            return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read access to everyone,
    but write access only to authenticated users.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed for authenticated users
        return request.user.is_authenticated