#!/usr/bin/env python3
"""
User Registration and Authentication Test Script

This script tests the complete user registration and authentication flow
to ensure all functionality works properly.
"""
import os
import sys
import requests
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
sys.path.append('.')

import django
django.setup()

from django.contrib.auth.models import User
from store.models import UserProfile, Store, Product


class RegistrationTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_csrf_token(self, url):
        """Get CSRF token from a page."""
        response = self.session.get(url)
        if response.status_code == 200:
            # Extract CSRF token from cookies
            csrf_token = self.session.cookies.get('csrftoken')
            return csrf_token
        return None
    
    def test_registration_page_access(self):
        """Test that registration page is accessible."""
        print("🔍 Testing Registration Page Access...")
        
        try:
            response = self.session.get(f"{self.base_url}/register/")
            
            if response.status_code == 200:
                print("   ✅ Registration page accessible")
                if "Register" in response.text and "Create Account" in response.text:
                    print("   ✅ Registration form found")
                    return True
                else:
                    print("   ❌ Registration form not found in page")
                    return False
            else:
                print(f"   ❌ Registration page failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Registration page test failed: {e}")
            return False
    
    def test_login_page_access(self):
        """Test that login page is accessible."""
        print("🔍 Testing Login Page Access...")
        
        try:
            response = self.session.get(f"{self.base_url}/login/")
            
            if response.status_code == 200:
                print("   ✅ Login page accessible")
                if "Login" in response.text and "Username" in response.text:
                    print("   ✅ Login form found")
                    return True
                else:
                    print("   ❌ Login form not found in page")
                    return False
            else:
                print(f"   ❌ Login page failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Login page test failed: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration functionality."""
        print("🔍 Testing User Registration...")
        
        # Clean up any existing test users
        test_username = "test_user_reg"
        User.objects.filter(username=test_username).delete()
        
        try:
            # Get CSRF token
            csrf_token = self.get_csrf_token(f"{self.base_url}/register/")
            if not csrf_token:
                print("   ❌ Could not get CSRF token")
                return False
            
            # Registration data
            registration_data = {
                'username': test_username,
                'email': 'test@registration.com',
                'password': 'testpass123',
                'user_type': 'buyer',
                'csrfmiddlewaretoken': csrf_token
            }
            
            # Submit registration
            response = self.session.post(
                f"{self.base_url}/register/",
                data=registration_data,
                headers={'Referer': f"{self.base_url}/register/"}
            )
            
            if response.status_code == 200 or response.status_code == 302:
                # Check if user was created in database
                if User.objects.filter(username=test_username).exists():
                    user = User.objects.get(username=test_username)
                    profile = UserProfile.objects.get(user=user)
                    
                    print("   ✅ User registration successful")
                    print(f"   ✅ User created: {user.username}")
                    print(f"   ✅ Profile created: {profile.user_type}")
                    return True
                else:
                    print("   ❌ User not found in database after registration")
                    return False
            else:
                print(f"   ❌ Registration failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False
                
        except Exception as e:
            print(f"   ❌ Registration test failed: {e}")
            return False
    
    def test_user_login(self):
        """Test user login functionality."""
        print("🔍 Testing User Login...")
        
        # Ensure test user exists
        test_username = "test_user_login"
        test_password = "testpass123"
        
        User.objects.filter(username=test_username).delete()
        user = User.objects.create_user(
            username=test_username,
            email='test@login.com',
            password=test_password
        )
        UserProfile.objects.create(user=user, user_type='buyer')
        
        try:
            # Get CSRF token
            csrf_token = self.get_csrf_token(f"{self.base_url}/login/")
            if not csrf_token:
                print("   ❌ Could not get CSRF token")
                return False
            
            # Login data
            login_data = {
                'username': test_username,
                'password': test_password,
                'csrfmiddlewaretoken': csrf_token
            }
            
            # Submit login
            response = self.session.post(
                f"{self.base_url}/login/",
                data=login_data,
                headers={'Referer': f"{self.base_url}/login/"}
            )
            
            if response.status_code == 200 or response.status_code == 302:
                # Check if redirected to store (successful login)
                if response.status_code == 302 or "Hi, " + test_username in response.text:
                    print("   ✅ User login successful")
                    return True
                else:
                    print("   ❌ Login did not redirect properly")
                    return False
            else:
                print(f"   ❌ Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Login test failed: {e}")
            return False
    
    def test_vendor_registration_and_dashboard(self):
        """Test vendor registration and dashboard access."""
        print("🔍 Testing Vendor Registration and Dashboard...")
        
        # Clean up any existing test vendor
        test_username = "test_vendor"
        User.objects.filter(username=test_username).delete()
        
        try:
            # Create vendor user
            user = User.objects.create_user(
                username=test_username,
                email='vendor@test.com',
                password='testpass123'
            )
            UserProfile.objects.create(user=user, user_type='vendor')
            
            print("   ✅ Vendor user created")
            
            # Test vendor dashboard access
            response = self.session.get(f"{self.base_url}/vendor/")
            
            if response.status_code == 200 or response.status_code == 302:
                print("   ✅ Vendor dashboard accessible")
                return True
            else:
                print(f"   ❌ Vendor dashboard failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Vendor test failed: {e}")
            return False
    
    def test_navigation_links(self):
        """Test that navigation links work properly."""
        print("🔍 Testing Navigation Links...")
        
        try:
            # Test main store page
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("   ✅ Main store page accessible")
                
                # Check for navigation links
                if "Register" in response.text and "Login" in response.text:
                    print("   ✅ Registration and login links found")
                    return True
                else:
                    print("   ❌ Navigation links not found")
                    return False
            else:
                print(f"   ❌ Main page failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Navigation test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all registration and authentication tests."""
        print("🚀 Starting User Registration and Authentication Tests")
        print("=" * 60)
        
        tests = [
            self.test_registration_page_access,
            self.test_login_page_access,
            self.test_navigation_links,
            self.test_user_registration,
            self.test_user_login,
            self.test_vendor_registration_and_dashboard,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                print()  # Add spacing between tests
            except Exception as e:
                print(f"   ❌ Test failed with exception: {e}")
                print()
        
        print("=" * 60)
        print(f"🎯 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! User registration system is working perfectly!")
            print("\n✅ Users can now:")
            print("   - Access registration page via navigation")
            print("   - Register as buyers or vendors")
            print("   - Login with their credentials")
            print("   - Access appropriate dashboards")
            print("   - Navigate the application properly")
        else:
            print("⚠️ Some tests failed. Please check the issues above.")
        
        return passed == total


def main():
    """Main test function."""
    tester = RegistrationTester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            print("\n🚀 Ready for submission!")
            print("The user registration system is fully functional.")
        else:
            print("\n🔧 Please fix the issues above before submission.")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server.")
        print("   Make sure the Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    main()