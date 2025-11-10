#!/usr/bin/env python
"""Test URL configuration"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.urls import get_resolver

print("🔍 Testing URL Configuration")
print("=" * 50)

resolver = get_resolver()
print("\n📋 Available URL Patterns:")

for pattern in resolver.url_patterns:
    print(f"  - {pattern.pattern}")
    
print("\n✅ URL configuration loaded successfully!")
print("\nTesting specific URLs:")

test_urls = [
    '/',
    '/register/',
    '/login/',
    '/vendor/',
    '/api/',
    '/admin/',
]

from django.urls import resolve
from django.urls.exceptions import Resolver404

for url in test_urls:
    try:
        match = resolve(url)
        print(f"  ✅ {url} → {match.view_name}")
    except Resolver404:
        print(f"  ❌ {url} → NOT FOUND")
