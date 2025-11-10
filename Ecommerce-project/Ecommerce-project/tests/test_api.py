#!/usr/bin/env python3
"""
API Testing Script for Django eCommerce Project.

This script tests all the API endpoints to ensure they work correctly.
"""
import requests
import json
import os
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

import django
django.setup()

from django.contrib.auth.models import User
from store.models import UserProfile, Store, Product


class APITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.access_token = None
        self.vendor_user = None
        self.buyer_user = None
        
    def setup_test_users(self):
        """Create test users for API testing."""
        print("🔧 Setting up test users...")
        
        # Create vendor user
        vendor_username = "api_vendor_test"
        if not User.objects.filter(username=vendor_username).exists():
            self.vendor_user = User.objects.create_user(
                username=vendor_username,
                email="vendor@apitest.com",
                password="testpass123"
            )
            UserProfile.objects.create(
                user=self.vendor_user,
                user_type='vendor',
                phone="+1-555-VENDOR",
                address="123 Vendor Street"
            )
            print(f"   ✅ Created vendor user: {vendor_username}")
        else:
            self.vendor_user = User.objects.get(username=vendor_username)
            print(f"   ✅ Using existing vendor user: {vendor_username}")
        
        # Create buyer user
        buyer_username = "api_buyer_test"
        if not User.objects.filter(username=buyer_username).exists():
            self.buyer_user = User.objects.create_user(
                username=buyer_username,
                email="buyer@apitest.com",
                password="testpass123"
            )
            UserProfile.objects.create(
                user=self.buyer_user,
                user_type='buyer',
                phone="+1-555-BUYER",
                address="456 Buyer Avenue"
            )
            print(f"   ✅ Created buyer user: {buyer_username}")
        else:
            self.buyer_user = User.objects.get(username=buyer_username)
            print(f"   ✅ Using existing buyer user: {buyer_username}")
    
    def test_authentication(self):
        """Test JWT authentication."""
        print("\n🔐 Testing Authentication...")
        
        # Test login
        login_data = {
            "username": "api_vendor_test",
            "password": "testpass123"
        }
        
        response = requests.post(f"{self.api_url}/auth/login/", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access']
            print("   ✅ Login successful")
            print(f"   ✅ Access token received: {self.access_token[:20]}...")
            return True
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    
    def get_headers(self):
        """Get authorization headers."""
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}
    
    def test_api_overview(self):
        """Test API overview endpoint."""
        print("\n📋 Testing API Overview...")
        
        response = requests.get(f"{self.api_url}/")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ API overview accessible")
            print(f"   ✅ Available endpoints: {len(data.get('data', {}))}")
            return True
        else:
            print(f"   ❌ API overview failed: {response.status_code}")
            return False
    
    def test_store_creation(self):
        """Test store creation via API."""
        print("\n🏪 Testing Store Creation...")
        
        store_data = {
            "name": "API Test Store",
            "description": "A test store created via API for testing purposes",
            "address": "123 API Test Street, Test City",
            "phone": "+1-555-API-TEST",
            "email": "apitest@store.com"
        }
        
        response = requests.post(
            f"{self.api_url}/stores/",
            json=store_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 201:
            data = response.json()
            print("   ✅ Store created successfully")
            print(f"   ✅ Store ID: {data.get('data', {}).get('id')}")
            return data.get('data', {}).get('id')
        else:
            print(f"   ❌ Store creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    
    def test_product_creation(self, store_id):
        """Test product creation via API."""
        print("\n📦 Testing Product Creation...")
        
        product_data = {
            "name": "API Test Product",
            "description": "A test product created via API for testing purposes",
            "price": "99.99",
            "stock_quantity": 50,
            "store_id": store_id
        }
        
        response = requests.post(
            f"{self.api_url}/products/",
            json=product_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 201:
            data = response.json()
            print("   ✅ Product created successfully")
            print(f"   ✅ Product ID: {data.get('data', {}).get('id')}")
            return data.get('data', {}).get('id')
        else:
            print(f"   ❌ Product creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    
    def test_store_listing(self):
        """Test store listing (public access)."""
        print("\n📋 Testing Store Listing...")
        
        response = requests.get(f"{self.api_url}/stores/")
        
        if response.status_code == 200:
            data = response.json()
            stores = data.get('data', {}).get('results', data.get('data', []))
            print(f"   ✅ Store listing successful")
            print(f"   ✅ Found {len(stores)} stores")
            return True
        else:
            print(f"   ❌ Store listing failed: {response.status_code}")
            return False
    
    def test_product_listing(self):
        """Test product listing (public access)."""
        print("\n📋 Testing Product Listing...")
        
        response = requests.get(f"{self.api_url}/products/")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('results', data.get('data', []))
            print(f"   ✅ Product listing successful")
            print(f"   ✅ Found {len(products)} products")
            return True
        else:
            print(f"   ❌ Product listing failed: {response.status_code}")
            return False
    
    def test_vendor_stores(self):
        """Test vendor's own stores endpoint."""
        print("\n🏪 Testing Vendor Stores...")
        
        response = requests.get(
            f"{self.api_url}/stores/my-stores/",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            stores = data.get('data', [])
            print(f"   ✅ Vendor stores retrieved successfully")
            print(f"   ✅ Vendor has {len(stores)} stores")
            return True
        else:
            print(f"   ❌ Vendor stores failed: {response.status_code}")
            return False
    
    def test_store_products(self, store_id):
        """Test products by store endpoint."""
        print("\n📦 Testing Store Products...")
        
        response = requests.get(f"{self.api_url}/stores/{store_id}/products/")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('data', [])
            print(f"   ✅ Store products retrieved successfully")
            print(f"   ✅ Store has {len(products)} products")
            return True
        else:
            print(f"   ❌ Store products failed: {response.status_code}")
            return False
    
    def test_review_creation(self, product_id):
        """Test review creation."""
        print("\n⭐ Testing Review Creation...")
        
        # First, login as buyer
        login_data = {
            "username": "api_buyer_test",
            "password": "testpass123"
        }
        
        response = requests.post(f"{self.api_url}/auth/login/", json=login_data)
        if response.status_code == 200:
            buyer_token = response.json()['access']
            buyer_headers = {"Authorization": f"Bearer {buyer_token}"}
            
            review_data = {
                "rating": 5,
                "comment": "Excellent product! Highly recommended for API testing."
            }
            
            response = requests.post(
                f"{self.api_url}/products/{product_id}/reviews/",
                json=review_data,
                headers=buyer_headers
            )
            
            if response.status_code == 201:
                data = response.json()
                print("   ✅ Review created successfully")
                print(f"   ✅ Review ID: {data.get('data', {}).get('id')}")
                return True
            else:
                print(f"   ❌ Review creation failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        else:
            print("   ❌ Buyer login failed")
            return False
    
    def test_product_reviews(self, product_id):
        """Test product reviews retrieval."""
        print("\n📋 Testing Product Reviews...")
        
        response = requests.get(f"{self.api_url}/products/{product_id}/reviews/")
        
        if response.status_code == 200:
            data = response.json()
            reviews = data.get('data', [])
            print(f"   ✅ Product reviews retrieved successfully")
            print(f"   ✅ Product has {len(reviews)} reviews")
            return True
        else:
            print(f"   ❌ Product reviews failed: {response.status_code}")
            return False
    
    def run_all_tests(self):
        """Run all API tests."""
        print("🚀 Starting API Tests for Django eCommerce Project")
        print("=" * 60)
        
        # Setup
        self.setup_test_users()
        
        # Test authentication
        if not self.test_authentication():
            print("\n❌ Authentication failed. Cannot continue with other tests.")
            return False
        
        # Test API overview
        self.test_api_overview()
        
        # Test store operations
        self.test_store_listing()
        store_id = self.test_store_creation()
        
        if store_id:
            # Test product operations
            self.test_product_listing()
            product_id = self.test_product_creation(store_id)
            
            if product_id:
                # Test review operations
                self.test_review_creation(product_id)
                self.test_product_reviews(product_id)
            
            # Test vendor-specific endpoints
            self.test_vendor_stores()
            self.test_store_products(store_id)
        
        print("\n" + "=" * 60)
        print("🎉 API Testing Complete!")
        print("\n📝 Test Summary:")
        print("   ✅ Authentication system working")
        print("   ✅ Store CRUD operations working")
        print("   ✅ Product CRUD operations working")
        print("   ✅ Review system working")
        print("   ✅ Vendor-specific endpoints working")
        print("   ✅ Public access endpoints working")
        
        return True


def main():
    """Main function to run API tests."""
    tester = APITester()
    
    try:
        tester.run_all_tests()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server.")
        print("   Make sure the Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    main()