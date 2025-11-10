import requests
import json

# Test API overview
response = requests.get("http://127.0.0.1:8000/api/")
print("API Overview:")
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

# Test authentication
login_data = {
    "username": "api_vendor_test",
    "password": "testpass123"
}

response = requests.post("http://127.0.0.1:8000/api/auth/login/", json=login_data)
print(f"\nLogin:")
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    token = response.json()['access']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test store creation
    store_data = {
        "name": "Quick Test Store",
        "description": "A quick test store",
        "address": "123 Test St",
        "phone": "+1-555-TEST",
        "email": "test@store.com"
    }
    
    response = requests.post("http://127.0.0.1:8000/api/stores/", json=store_data, headers=headers)
    print(f"\nStore Creation:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")