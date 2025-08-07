#!/usr/bin/env python3
"""
Test script to verify YOLO model names override is working correctly.
This script tests that the YOLO model returns "boulder" instead of "crater".
"""

import os
import sys
import numpy as np
from PIL import Image

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_yolo_names_override():
    """Test that class name mapping is working correctly."""
    print("🧪 Testing class name mapping...")
    
    try:
        from detector import BoulderDetector
        
        # Initialize detector
        print("🔧 Initializing BoulderDetector...")
        detector = BoulderDetector("best.pt", "vit_model.pth", scale=1.0)
        
        # Check if class name mapping is set up correctly
        print("🔍 Checking class name mapping...")
        print(f"   Class name mapping: {detector.class_name_mapping}")
        
        # Test the mapping function
        test_class_name = detector._get_class_name(0)
        print(f"   Mapped class name for ID 0: '{test_class_name}'")
        
        if test_class_name == 'boulder':
            print("✅ Class name mapping is working correctly")
        else:
            print("❌ Class name mapping is not working correctly")
            print(f"   Expected: 'boulder'")
            print(f"   Got: '{test_class_name}'")
            return False
        
        # Test with a sample image if available
        test_image_path = "download.png"  # Use the sample image if available
        if os.path.exists(test_image_path):
            print(f"🔍 Testing with sample image: {test_image_path}")
            
            # Run detection
            detected_objects = detector.detect_objects(test_image_path)
            
            print(f"✅ Detection completed. Found {len(detected_objects)} objects")
            
            # Check class names
            all_correct = True
            for i, obj in enumerate(detected_objects):
                print(f"   Object {i+1}: class_name = '{obj.class_name}'")
                if obj.class_name != 'boulder':
                    print(f"   ❌ Object {i+1} has incorrect class_name: '{obj.class_name}' (expected 'boulder')")
                    all_correct = False
                else:
                    print(f"   ✅ Object {i+1} has correct class_name: '{obj.class_name}'")
            
            if all_correct:
                print("✅ All objects have correct class_name 'boulder'")
            else:
                print("❌ Some objects have incorrect class_name")
                return False
        else:
            print("⚠️ No test image found, skipping detection test")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_vit_class_names():
    """Test that ViT class names are correct."""
    print("\n🧪 Testing ViT class names...")
    
    try:
        from transforms import DataTransforms
        
        transforms = DataTransforms()
        class_names = transforms.get_class_names()
        
        print(f"   ViT class names: {class_names}")
        
        if class_names == ['boulder']:
            print("✅ ViT class names are correct: ['boulder']")
            return True
        else:
            print(f"❌ ViT class names are incorrect: {class_names}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing ViT class names: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting YOLO names override tests...\n")
    
    # Test YOLO names override
    yolo_test_passed = test_yolo_names_override()
    
    # Test ViT class names
    vit_test_passed = test_vit_class_names()
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS:")
    print(f"   Class Name Mapping: {'✅ PASSED' if yolo_test_passed else '❌ FAILED'}")
    print(f"   ViT Class Names: {'✅ PASSED' if vit_test_passed else '❌ FAILED'}")
    
    if yolo_test_passed and vit_test_passed:
        print("\n🎉 All tests passed! The boulder detection system should now correctly label objects as 'boulder'.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
    
    return yolo_test_passed and vit_test_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 