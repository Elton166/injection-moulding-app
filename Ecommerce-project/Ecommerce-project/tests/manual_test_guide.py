#!/usr/bin/env python3
"""
Manual Test Guide for User Registration System

This script provides a step-by-step guide for manually testing
the user registration and authentication system.
"""

def print_manual_test_guide():
    """Print manual testing instructions."""
    print("🧪 Manual Testing Guide for User Registration System")
    print("=" * 60)
    
    print("\n📋 Pre-Test Setup:")
    print("1. Make sure Django server is running: python manage.py runserver")
    print("2. Open your web browser")
    print("3. Navigate to: http://127.0.0.1:8000/")
    
    print("\n🔍 Test 1: Navigation and UI")
    print("✅ Check that the main page loads properly")
    print("✅ Verify 'Register' and 'Login' buttons are visible in navigation")
    print("✅ Click 'Register' button - should go to registration page")
    print("✅ Click 'Login' button - should go to login page")
    
    print("\n🔍 Test 2: User Registration (Buyer)")
    print("1. Go to: http://127.0.0.1:8000/register/")
    print("2. Fill out the form:")
    print("   - Username: testbuyer")
    print("   - Email: buyer@test.com")
    print("   - Password: testpass123")
    print("   - Account Type: Buyer")
    print("3. Click 'Create Account'")
    print("✅ Should redirect to login page with success message")
    
    print("\n🔍 Test 3: User Login (Buyer)")
    print("1. Go to: http://127.0.0.1:8000/login/")
    print("2. Enter credentials:")
    print("   - Username: testbuyer")
    print("   - Password: testpass123")
    print("3. Click 'Login'")
    print("✅ Should redirect to store page")
    print("✅ Navigation should show 'Hi, testbuyer (Buyer)' and 'Logout' button")
    
    print("\n🔍 Test 4: User Registration (Vendor)")
    print("1. Logout first (click 'Logout' button)")
    print("2. Go to: http://127.0.0.1:8000/register/")
    print("3. Fill out the form:")
    print("   - Username: testvendor")
    print("   - Email: vendor@test.com")
    print("   - Password: testpass123")
    print("   - Account Type: Vendor")
    print("4. Click 'Create Account'")
    print("✅ Should redirect to login page with success message")
    
    print("\n🔍 Test 5: Vendor Login and Dashboard")
    print("1. Login with vendor credentials:")
    print("   - Username: testvendor")
    print("   - Password: testpass123")
    print("2. After login, navigation should show 'Vendor Dashboard' link")
    print("3. Click 'Vendor Dashboard'")
    print("✅ Should show vendor dashboard with 'Create New Store' button")
    
    print("\n🔍 Test 6: Store Creation")
    print("1. In vendor dashboard, click 'Create New Store'")
    print("2. Fill out store form:")
    print("   - Store Name: Test Store")
    print("   - Description: A test store for verification")
    print("   - Address: 123 Test Street, Test City")
    print("   - Phone: +1-555-TEST")
    print("   - Email: test@store.com")
    print("3. Check the terms checkbox")
    print("4. Click 'Create Store'")
    print("✅ Should redirect to vendor dashboard showing the new store")
    
    print("\n🔍 Test 7: API Integration")
    print("1. Test API endpoints:")
    print("   - GET http://127.0.0.1:8000/api/ (API overview)")
    print("   - GET http://127.0.0.1:8000/api/stores/ (list stores)")
    print("   - GET http://127.0.0.1:8000/api/products/ (list products)")
    print("✅ All should return JSON responses")
    
    print("\n🔍 Test 8: Error Handling")
    print("1. Try registering with existing username")
    print("2. Try logging in with wrong password")
    print("3. Try accessing vendor dashboard as buyer")
    print("✅ Should show appropriate error messages")
    
    print("\n" + "=" * 60)
    print("🎉 If all tests pass, the system is ready for submission!")
    
    print("\n📊 Expected Results Summary:")
    print("✅ Users can register as buyers or vendors")
    print("✅ Users can login and logout properly")
    print("✅ Navigation shows appropriate options based on user type")
    print("✅ Vendors can access dashboard and create stores")
    print("✅ API endpoints are accessible")
    print("✅ Error handling works correctly")
    print("✅ All templates render without errors")

if __name__ == "__main__":
    print_manual_test_guide()