"""
Test script to verify JWT token authentication
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_authentication():
    print("=" * 60)
    print("Testing JWT Token Authentication")
    print("=" * 60)
    
    # Step 1: Login to get token
    print("\n1. Testing Login...")
    login_data = {
        "username": "vendor1",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 200:
        print("\n❌ Login failed!")
        return
    
    # Extract tokens
    tokens = response.json()
    access_token = tokens.get('access')
    refresh_token = tokens.get('refresh')
    
    print(f"\n✓ Login successful!")
    print(f"Access Token: {access_token[:50]}...")
    print(f"Refresh Token: {refresh_token[:50]}...")
    
    # Step 2: Test authenticated endpoint with token
    print("\n" + "=" * 60)
    print("2. Testing Authenticated Endpoint (My Stores)...")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/stores/my-stores/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✓ Token authentication successful!")
    else:
        print("\n❌ Token authentication failed!")
    
    # Step 3: Test user profile endpoint
    print("\n" + "=" * 60)
    print("3. Testing User Profile Endpoint...")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✓ Profile endpoint successful!")
    else:
        print("\n❌ Profile endpoint failed!")
    
    # Step 4: Test creating a store
    print("\n" + "=" * 60)
    print("4. Testing Create Store (Authenticated)...")
    print("=" * 60)
    
    store_data = {
        "name": "Test Store via API",
        "description": "Testing token authentication",
        "address": "123 Test St",
        "phone": "1234567890",
        "email": "teststore@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/stores/", json=store_data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("\n✓ Store creation successful!")
    else:
        print("\n❌ Store creation failed!")
    
    # Step 5: Test without token (should fail for authenticated endpoints)
    print("\n" + "=" * 60)
    print("5. Testing Without Token (Should Fail)...")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/stores/my-stores/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("\n✓ Correctly rejected unauthenticated request!")
    else:
        print("\n❌ Should have rejected unauthenticated request!")
    
    # Step 6: Test with invalid token
    print("\n" + "=" * 60)
    print("6. Testing With Invalid Token (Should Fail)...")
    print("=" * 60)
    
    invalid_headers = {
        "Authorization": "Bearer invalid_token_here",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/stores/my-stores/", headers=invalid_headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("\n✓ Correctly rejected invalid token!")
    else:
        print("\n❌ Should have rejected invalid token!")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_authentication()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Please make sure the Django development server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")
