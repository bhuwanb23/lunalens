#!/usr/bin/env python3
"""
Test script for LunaLens Backend Server
"""


import requests


def test_server():
    """Test basic server functionality"""
    base_url = "http://localhost:5000"

    print("🧪 Testing LunaLens Backend Server...")

    # Test 1: Server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server with: python app.py")
        return False

    # Test 2: Boulder status endpoint
    try:
        response = requests.get(f"{base_url}/api/boulder/status")
        data = response.json()
        print(f"✅ Boulder status endpoint working: {data}")
    except Exception as e:
        print(f"⚠️ Boulder status endpoint error: {e}")

    # Test 3: Analytics endpoint
    try:
        response = requests.get(f"{base_url}/api/analytics/summary")
        data = response.json()
        print(f"✅ Analytics endpoint working: {data}")
    except Exception as e:
        print(f"⚠️ Analytics endpoint error: {e}")

    # Test 4: Login endpoint
    try:
        login_data = {
            "missionId": "test001",
            "accessCode": "test001@2024"
        }
        response = requests.post(f"{base_url}/login", json=login_data)
        data = response.json()
        if data.get("success"):
            print("✅ Login endpoint working")
            token = data.get("token")

            # Test 5: Token verification
            verify_data = {"token": token}
            response = requests.post(f"{base_url}/verify-token", json=verify_data)
            verify_data = response.json()
            if verify_data.get("valid"):
                print("✅ Token verification working")
            else:
                print("❌ Token verification failed")
        else:
            print("❌ Login failed")
    except Exception as e:
        print(f"⚠️ Login endpoint error: {e}")

    print("\n🎉 Server test completed!")
    return True

if __name__ == "__main__":
    test_server()
