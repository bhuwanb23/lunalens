#!/usr/bin/env python3
"""
Quick test to verify YOLO model names override is working.
"""

import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_yolo_names():
    """Test that YOLO model names are correctly mapped."""
    print("🧪 Testing YOLO model names mapping...")
    
    try:
        from detector import BoulderDetector
        
        # Initialize detector
        print("🔧 Initializing BoulderDetector...")
        detector = BoulderDetector("best.pt", "vit_model.pth", scale=1.0)
        
        # Check if class name mapping is set up
        print(f"🔍 Class name mapping: {detector.class_name_mapping}")
        
        # Test the mapping function
        test_class_name = detector._get_class_name(0)
        print(f"🔍 Mapped class name for ID 0: '{test_class_name}'")
        
        if test_class_name == 'boulder':
            print("✅ Class name mapping is working correctly")
            return True
        else:
            print("❌ Class name mapping is not working correctly")
            print(f"   Expected: 'boulder'")
            print(f"   Got: '{test_class_name}'")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_yolo_names()
    if success:
        print("\n🎉 Test passed! The class name mapping is working correctly.")
    else:
        print("\n⚠️ Test failed. The class name mapping is not working.")
    
    sys.exit(0 if success else 1) 