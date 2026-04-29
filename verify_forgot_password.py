"""
Quick verification script for forgot password endpoints
Run this after restarting Django server
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_forgot_password():
    print("=" * 50)
    print("Testing Forgot Password Endpoints")
    print("=" * 50)
    
    # Test 1: Check if endpoint exists
    print("\n1. Testing forgot-password endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/forgot-password/",
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("   ✅ Forgot password endpoint working!")
            reset_code = response.json().get('reset_code')
            
            # Test 2: Reset password
            print("\n2. Testing reset-password endpoint...")
            reset_response = requests.post(
                f"{BASE_URL}/auth/reset-password/",
                json={
                    "email": "test@example.com",
                    "reset_code": reset_code,
                    "new_password": "newpass123"
                },
                headers={"Content-Type": "application/json"}
            )
            print(f"   Status: {reset_response.status_code}")
            print(f"   Response: {json.dumps(reset_response.json(), indent=2)}")
            
            if reset_response.status_code == 200:
                print("   ✅ Reset password endpoint working!")
            else:
                print("   ⚠️ Reset password failed (expected if email doesn't exist)")
        else:
            print("   ⚠️ Forgot password failed (expected if email doesn't exist)")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to backend!")
        print("   Make sure Django server is running on http://localhost:8000")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Verification Complete")
    print("=" * 50)

if __name__ == "__main__":
    test_forgot_password()
