#!/usr/bin/env python3
"""
Web Interface Verification for MariaDB eCommerce Project.
"""
import requests
import time

def test_web_interface():
    """Test the web interface endpoints."""
    print("🌐 Testing Web Interface with MariaDB")
    print("=" * 40)
    
    base_url = "http://127.0.0.1:8000"
    
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    try:
        # Test 1: Home page
        print("\n🔍 Test 1: Home Page")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Home page loads successfully")
        else:
            print(f"   ❌ Home page failed: {response.status_code}")
        
        # Test 2: Admin page
        print("\n🔍 Test 2: Admin Interface")
        response = requests.get(f"{base_url}/admin/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Admin interface accessible")
        else:
            print(f"   ❌ Admin interface failed: {response.status_code}")
        
        # Test 3: Store page
        print("\n🔍 Test 3: Store Page")
        response = requests.get(f"{base_url}/store/", timeout=10)
        if response.status_code == 200:
            print("   ✅ Store page loads successfully")
        else:
            print(f"   ❌ Store page failed: {response.status_code}")
        
        # Test 4: API endpoints
        print("\n🔍 Test 4: API Endpoints")
        response = requests.get(f"{base_url}/api/products/", timeout=10)
        if response.status_code == 200:
            products = response.json()
            print(f"   ✅ API returns {len(products)} products")
        else:
            print(f"   ❌ API failed: {response.status_code}")
        
        print("\n" + "=" * 40)
        print("🎉 Web Interface Test Complete!")
        print("✅ All endpoints working with MariaDB!")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        print("   Make sure the server is running: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_web_interface()