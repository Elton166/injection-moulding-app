#!/usr/bin/env python3
"""
Test script to verify admin login functionality.
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def test_admin_users():
    """Test admin user authentication."""
    print("🔍 Testing Admin Users")
    print("=" * 40)
    
    # Test credentials
    test_users = [
        {'username': 'admin', 'password': 'admin123'},  # Updated password
        {'username': 'testadmin', 'password': 'admin123'},
    ]
    
    for creds in test_users:
        username = creds['username']
        password = creds['password']
        
        try:
            # Check if user exists
            user = User.objects.get(username=username)
            print(f"\n👤 User: {username}")
            print(f"   Email: {user.email}")
            print(f"   Active: {user.is_active}")
            print(f"   Superuser: {user.is_superuser}")
            print(f"   Staff: {user.is_staff}")
            
            # Test authentication
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                print(f"   ✅ Authentication: SUCCESS")
            else:
                print(f"   ❌ Authentication: FAILED")
                
        except User.DoesNotExist:
            print(f"❌ User '{username}' does not exist")
    
    print("\n" + "=" * 40)
    print("📋 All Superusers:")
    superusers = User.objects.filter(is_superuser=True)
    for user in superusers:
        print(f"   - {user.username} ({user.email}) - Active: {user.is_active}")

if __name__ == "__main__":
    test_admin_users()