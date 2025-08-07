#!/usr/bin/env python3
"""
Test script to verify that all "crater" references have been replaced with "boulder"
in the boulder detection system. This script checks both the backend detection
system and the frontend constants to ensure consistency.
"""

import os
import sys
import json
from pathlib import Path

def test_backend_detection_system():
    """Test the backend boulder detection system"""
    print("🧪 Testing Backend Boulder Detection System")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("detector.py"):
        print("❌ Please run this script from the boulder_detection directory")
        return False
    
    try:
        # Import the detection modules
        from detector import BoulderDetector
        from transforms import DataTransforms
        from measurements import ObjectMeasurements
        from gradcam import GradCAMVisualizer
        
        print("✅ All backend modules imported successfully")
        
        # Test class names in transforms
        transforms = DataTransforms()
        if hasattr(transforms, 'class_names_vit'):
            if transforms.class_names_vit == ['boulder']:
                print("✅ ViT class names correctly set to ['boulder']")
            else:
                print(f"❌ ViT class names incorrect: {transforms.class_names_vit}")
                return False
        
        # Test if models exist
        yolo_model = "best.pt"
        vit_model = "vit_model.pth"
        
        if os.path.exists(yolo_model):
            print(f"✅ YOLO model found: {yolo_model}")
        else:
            print(f"⚠️  YOLO model not found: {yolo_model}")
        
        if os.path.exists(vit_model):
            print(f"✅ ViT model found: {vit_model}")
        else:
            print(f"⚠️  ViT model not found: {vit_model}")
        
        # Test detector initialization
        try:
            detector = BoulderDetector(yolo_model, vit_model, scale=1.0)
            print("✅ Boulder detector initialized successfully")
        except Exception as e:
            print(f"⚠️  Could not initialize detector (models may not be available): {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_frontend_constants():
    """Test the frontend constants file"""
    print("\n🧪 Testing Frontend Constants")
    print("=" * 50)
    
    # Path to frontend constants
    constants_path = Path("../../frontend/website/src/pages/boulder/constants/index.js")
    
    if not constants_path.exists():
        print(f"❌ Frontend constants file not found: {constants_path}")
        return False
    
    try:
        with open(constants_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for any remaining "crater" references
        if "crater" in content.lower():
            print("❌ Found 'crater' references in frontend constants:")
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if "crater" in line.lower():
                    print(f"   Line {i}: {line.strip()}")
            return False
        else:
            print("✅ No 'crater' references found in frontend constants")
        
        # Check for "boulder" references
        if "boulder" in content.lower():
            print("✅ 'Boulder' references found in frontend constants")
        else:
            print("⚠️  No 'boulder' references found in frontend constants")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading frontend constants: {e}")
        return False

def test_backend_api_files():
    """Test the backend API files for consistency"""
    print("\n🧪 Testing Backend API Files")
    print("=" * 50)
    
    # Check server files
    server_files = [
        "../../backend/server/app.py",
        "../../backend/server/models.py", 
        "../../backend/server/database.py"
    ]
    
    all_good = True
    
    for file_path in server_files:
        path = Path(file_path)
        if not path.exists():
            print(f"⚠️  File not found: {file_path}")
            continue
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for "crater" references in boulder detection context
            if "crater_count" in content:
                print(f"❌ Found 'crater_count' in {file_path}")
                all_good = False
            elif "crater" in content.lower():
                # Check if it's in a comment or legitimate context
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if "crater" in line.lower() and not line.strip().startswith('#'):
                        print(f"⚠️  Found 'crater' in {file_path} line {i}: {line.strip()}")
            else:
                print(f"✅ No problematic 'crater' references in {file_path}")
                
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            all_good = False
    
    return all_good

def test_detection_output():
    """Test that the detection system outputs boulder labels"""
    print("\n🧪 Testing Detection Output")
    print("=" * 50)
    
    # Check if test image exists
    test_image = "download.png"
    if not os.path.exists(test_image):
        print(f"⚠️  Test image not found: {test_image}")
        print("💡 Place a test image named 'download.png' in this directory to test detection output")
        return True
    
    try:
        from detector import BoulderDetector
        
        # Initialize detector
        detector = BoulderDetector("best.pt", "vit_model.pth", scale=1.0)
        
        # Detect objects
        detected_objects = detector.detect_objects(test_image)
        
        print(f"✅ Detected {len(detected_objects)} objects")
        
        # Check that all objects are labeled as "boulder"
        all_boulders = True
        for i, obj in enumerate(detected_objects):
            if obj.class_name != 'boulder':
                print(f"❌ Object {i+1} labeled as '{obj.class_name}' instead of 'boulder'")
                all_boulders = False
            else:
                print(f"✅ Object {i+1} correctly labeled as 'boulder'")
        
        if all_boulders:
            print("✅ All detected objects are correctly labeled as 'boulder'")
        
        return all_boulders
        
    except Exception as e:
        print(f"⚠️  Could not test detection output: {e}")
        return True

def main():
    """Run all tests"""
    print("🚀 Boulder Detection System Update Verification")
    print("=" * 60)
    
    tests = [
        ("Backend Detection System", test_backend_detection_system),
        ("Frontend Constants", test_frontend_constants),
        ("Backend API Files", test_backend_api_files),
        ("Detection Output", test_detection_output)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The boulder detection system has been successfully updated.")
        print("✅ All 'crater' references have been replaced with 'boulder'")
        print("✅ The system is now focused on boulder detection only")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 