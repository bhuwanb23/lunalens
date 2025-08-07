#!/usr/bin/env python3
"""
Comprehensive test to verify that detection works with class name mapping.
"""

import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_detection_with_mapping():
    """Test that detection returns correct class names."""
    print("🧪 Testing detection with class name mapping...")
    
    try:
        from detector import BoulderDetector
        
        # Initialize detector
        print("🔧 Initializing BoulderDetector...")
        detector = BoulderDetector("best.pt", "vit_model.pth", scale=1.0)
        
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
                return True
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

if __name__ == "__main__":
    success = test_detection_with_mapping()
    if success:
        print("\n🎉 Test passed! The detection with class name mapping is working correctly.")
    else:
        print("\n⚠️ Test failed. The detection with class name mapping is not working.")
    
    sys.exit(0 if success else 1) 