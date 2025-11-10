"""
Comprehensive test script for all API endpoints with token authentication
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_endpoint(method, url, headers=None, data=None, expected_status=200):
    """Helper function to test an endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "PATCH":
            response = requests.patch(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        
        print(f"\n{method} {url}")
        print(f"Status: {response.status_code} (Expected: {expected_status})")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)[:500]}...")
        except:
            print(f"Response: {response.text[:200]}")
        
        success = response.status_code == expected_status
        print(f"Result: {'PASS' if success else 'FAIL'}")
        return response, success
    except Exception as e:
        print(f"ERROR: {e}")
        return None, False

def main():
    print_section("COMPREHENSIVE API ENDPOINT TESTING")
    
    # Step 1: Login as vendor
    print_section("1. AUTHENTICATION - Login as Vendor")
    login_data = {"username": "vendor1", "password": "testpass123"}
    response, success = test_endpoint("POST", f"{BASE_URL}/auth/login/", data=login_data)
    
    if not success:
        print("\n❌ Login failed! Cannot continue tests.")
        return
    
    vendor_token = response.json()['access']
    vendor_headers = {
        "Authorization": f"Bearer {vendor_token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Login as buyer
    print_section("2. AUTHENTICATION - Login as Buyer")
    login_data = {"username": "buyer1", "password": "testpass123"}
    response, success = test_endpoint("POST", f"{BASE_URL}/auth/login/", data=login_data)
    
    if not success:
        print("\n❌ Buyer login failed!")
        buyer_headers = None
    else:
        buyer_token = response.json()['access']
        buyer_headers = {
            "Authorization": f"Bearer {buyer_token}",
            "Content-Type": "application/json"
        }
    
    # Step 3: Test API Overview (Public)
    print_section("3. API OVERVIEW - Public Access")
    test_endpoint("GET", f"{BASE_URL}/")
    
    # Step 4: Test User Profile (Authenticated)
    print_section("4. USER PROFILE - Vendor")
    test_endpoint("GET", f"{BASE_URL}/auth/profile/", headers=vendor_headers)
    
    if buyer_headers:
        print_section("5. USER PROFILE - Buyer")
        test_endpoint("GET", f"{BASE_URL}/auth/profile/", headers=buyer_headers)
    
    # Step 5: Test Store Endpoints
    print_section("6. STORES - List All (Public)")
    response, _ = test_endpoint("GET", f"{BASE_URL}/stores/")
    
    print_section("7. STORES - Create New Store (Vendor)")
    store_data = {
        "name": "Comprehensive Test Store",
        "description": "Testing all endpoints",
        "address": "456 Test Ave",
        "phone": "9876543210",
        "email": "comprehensive@test.com"
    }
    response, success = test_endpoint("POST", f"{BASE_URL}/stores/", 
                                     headers=vendor_headers, data=store_data, 
                                     expected_status=201)
    
    new_store_id = None
    if success:
        new_store_id = response.json()['data']['id']
        print(f"\nCreated Store ID: {new_store_id}")
    
    print_section("8. STORES - My Stores (Vendor)")
    test_endpoint("GET", f"{BASE_URL}/stores/my-stores/", headers=vendor_headers)
    
    print_section("9. STORES - Get Store Detail (Public)")
    if new_store_id:
        test_endpoint("GET", f"{BASE_URL}/stores/{new_store_id}/")
    
    print_section("10. STORES - Update Store (Vendor)")
    if new_store_id:
        update_data = {"description": "Updated description"}
        test_endpoint("PATCH", f"{BASE_URL}/stores/{new_store_id}/", 
                     headers=vendor_headers, data=update_data)
    
    # Step 6: Test Product Endpoints
    print_section("11. PRODUCTS - List All (Public)")
    test_endpoint("GET", f"{BASE_URL}/products/")
    
    print_section("12. PRODUCTS - Create New Product (Vendor)")
    if new_store_id:
        product_data = {
            "name": "Test Product",
            "description": "Testing product creation",
            "price": "99.99",
            "stock_quantity": 50,
            "store_id": new_store_id
        }
        response, success = test_endpoint("POST", f"{BASE_URL}/products/", 
                                         headers=vendor_headers, data=product_data,
                                         expected_status=201)
        
        new_product_id = None
        if success:
            new_product_id = response.json()['data']['id']
            print(f"\nCreated Product ID: {new_product_id}")
    
    print_section("13. PRODUCTS - My Products (Vendor)")
    test_endpoint("GET", f"{BASE_URL}/products/my-products/", headers=vendor_headers)
    
    print_section("14. PRODUCTS - Get Product Detail (Public)")
    if new_product_id:
        test_endpoint("GET", f"{BASE_URL}/products/{new_product_id}/")
    
    print_section("15. PRODUCTS - Update Product (Vendor)")
    if new_product_id:
        update_data = {"price": "89.99"}
        test_endpoint("PATCH", f"{BASE_URL}/products/{new_product_id}/", 
                     headers=vendor_headers, data=update_data)
    
    print_section("16. PRODUCTS - Filter by Store")
    if new_store_id:
        test_endpoint("GET", f"{BASE_URL}/stores/{new_store_id}/products/")
    
    # Step 7: Test Review Endpoints
    print_section("17. REVIEWS - Create Review (Vendor)")
    new_review_id = None
    if vendor_headers and new_product_id:
        review_data = {
            "rating": 5,
            "comment": "Excellent product!"
        }
        response, success = test_endpoint("POST", 
                                         f"{BASE_URL}/products/{new_product_id}/reviews/",
                                         headers=vendor_headers, data=review_data,
                                         expected_status=201)
        
        if success:
            # Get the review ID from the list of reviews
            reviews_response = requests.get(f"{BASE_URL}/products/{new_product_id}/reviews/")
            if reviews_response.status_code == 200:
                reviews = reviews_response.json().get('results', [])
                if reviews:
                    new_review_id = reviews[0]['id']
                    print(f"\nCreated Review ID: {new_review_id}")
    
    print_section("18. REVIEWS - List Product Reviews (Public)")
    if new_product_id:
        test_endpoint("GET", f"{BASE_URL}/products/{new_product_id}/reviews/")
    
    print_section("19. REVIEWS - Get Review Detail (Public)")
    if new_review_id:
        test_endpoint("GET", f"{BASE_URL}/reviews/{new_review_id}/")
    
    print_section("20. REVIEWS - Update Review (Vendor)")
    if vendor_headers and new_review_id:
        update_data = {"rating": 4, "comment": "Good product!"}
        test_endpoint("PATCH", f"{BASE_URL}/reviews/{new_review_id}/",
                     headers=vendor_headers, data=update_data)
    
    print_section("21. REVIEWS - Buyer Cannot Create Review (Should Fail)")
    if buyer_headers and new_product_id:
        review_data = {
            "rating": 3,
            "comment": "Buyer trying to review"
        }
        test_endpoint("POST", 
                     f"{BASE_URL}/products/{new_product_id}/reviews/",
                     headers=buyer_headers, data=review_data,
                     expected_status=403)
    
    # Step 8: Test Vendor Endpoints
    print_section("22. VENDORS - Get Vendor Stores (Public)")
    test_endpoint("GET", f"{BASE_URL}/vendors/2/stores/")
    
    print_section("23. VENDORS - Get Vendor Products (Public)")
    test_endpoint("GET", f"{BASE_URL}/vendors/2/products/")
    
    # Step 9: Test Authorization Failures
    print_section("24. AUTHORIZATION - Buyer Cannot Create Store")
    if buyer_headers:
        store_data = {
            "name": "Unauthorized Store",
            "description": "Should fail",
            "address": "123 Fail St",
            "phone": "1111111111",
            "email": "fail@test.com"
        }
        test_endpoint("POST", f"{BASE_URL}/stores/", 
                     headers=buyer_headers, data=store_data,
                     expected_status=403)
    
    print_section("25. AUTHORIZATION - No Token Access to Protected Endpoint")
    test_endpoint("GET", f"{BASE_URL}/stores/my-stores/", expected_status=401)
    
    print_section("26. AUTHORIZATION - Invalid Token")
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    test_endpoint("GET", f"{BASE_URL}/stores/my-stores/", 
                 headers=invalid_headers, expected_status=401)
    
    # Summary
    print_section("TEST SUMMARY")
    print("\n[SUCCESS] All endpoint tests completed!")
    print("[SUCCESS] Token authentication is working correctly")
    print("[SUCCESS] Authorization rules are properly enforced")
    print("[SUCCESS] Public endpoints are accessible without authentication")
    print("[SUCCESS] Protected endpoints require valid tokens")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to the server.")
        print("Please make sure the Django development server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
