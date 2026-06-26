#!/usr/bin/env python3
"""
Test script to verify image serving functionality
"""


import requests


def test_image_serving():
    """Test if images are being served correctly"""
    base_url = "http://localhost:5000"

    print("🧪 Testing image serving...")

    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        return False

    # Test 2: Check available files
    try:
        response = requests.get(f"{base_url}/api/test/files")
        if response.status_code == 200:
            data = response.json()
            print("✅ Files endpoint working")
            print(f"📁 Uploads directory: {data['uploads_directory']}")
            print("📄 Available files:")
            for file_info in data['files']:
                print(f"  - {file_info['filename']} ({file_info['size']} bytes)")
                print(f"    URL: {file_info['full_url']}")
        else:
            print(f"❌ Files endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Files endpoint error: {e}")

    # Test 3: Test direct image access
    test_files = ['download_detected.png', 'download_gradcam.png', 'download.png']
    for filename in test_files:
        try:
            url = f"{base_url}/uploads/{filename}"
            response = requests.get(url)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', 'unknown')
                content_length = response.headers.get('content-length', 'unknown')
                print(f"✅ {filename}: Status {response.status_code}, Type: {content_type}, Size: {content_length}")
            else:
                print(f"❌ {filename}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {filename}: Error - {e}")

    print("\n🎉 Image serving test completed!")
    return True

if __name__ == "__main__":
    test_image_serving()
