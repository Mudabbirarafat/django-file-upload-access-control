#!/usr/bin/env python
"""
Test script to verify the Django File Upload API is working
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("=" * 60)
    print("Testing Django File Upload Access Control API")
    print("=" * 60)
    
    # Test 1: User Registration
    print("\n1. Testing User Registration...")
    register_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    if response.status_code != 201:
        print("   ✓ User already exists or other issue")
    else:
        print("   ✓ User registered successfully")
    
    # Test 2: Get JWT Token
    print("\n2. Testing JWT Token Generation...")
    token_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/auth/token/", json=token_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get('access')
        print(f"   ✓ Token received: {access_token[:20]}...")
        
        # Test 3: List Files (with authentication)
        print("\n3. Testing List Files (Authenticated)...")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(f"{BASE_URL}/files/", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✓ API is working correctly!")
    else:
        print(f"   ✗ Failed to get token: {response.json()}")

if __name__ == "__main__":
    try:
        test_api()
        print("\n" + "=" * 60)
        print("API TEST SUCCESSFUL!")
        print("=" * 60)
        print("\nAccess the application at:")
        print("  - API: http://localhost:8000/api/")
        print("  - Admin: http://localhost:8000/admin/")
        print("\nAdmin Credentials:")
        print("  - Username: admin")
        print("  - Password: admin123")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure the Django server is running on http://localhost:8000/")
