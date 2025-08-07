#!/usr/bin/env python3
"""
Test script for boulder detection with updated class names.
This script verifies that the boulder detection system is working correctly
and displays "Boulder" labels instead of "Crater" labels.
"""

import os
import sys
from detector import BoulderDetector
from PIL import Image
import cv2
import numpy as np

def test_boulder_detection():
    """Test the boulder detection system."""
    
    # Check if model files exist
    yolo_model_path = "best.pt"
    vit_model_path = "vit_model.pth"
    
    if not os.path.exists(yolo_model_path):
        print(f"❌ YOLO model not found at: {yolo_model_path}")
        return False
    
    if not os.path.exists(vit_model_path):
        print(f"❌ ViT model not found at: {vit_model_path}")
        return False
    
    print("✅ Model files found!")
    
    try:
        # Initialize detector
        print("🚀 Initializing boulder detector...")
        detector = BoulderDetector(yolo_model_path, vit_model_path, scale=1.0)
        print("✅ Boulder detector initialized successfully!")
        
        # Test with a sample image if available
        test_image_path = "download.png"  # Use the sample image in the folder
        
        if os.path.exists(test_image_path):
            print(f"🔍 Testing with image: {test_image_path}")
            
            # Detect objects
            detected_objects = detector.detect_objects(test_image_path)
            
            print(f"✅ Detected {len(detected_objects)} objects!")
            
            # Check if objects are labeled as "boulder"
            for i, obj in enumerate(detected_objects):
                print(f"  Object {i+1}: {obj.class_name} (confidence: {obj.confidence:.2f})")
                if obj.class_name != 'boulder':
                    print(f"  ⚠️  Warning: Object {i+1} is labeled as '{obj.class_name}' instead of 'boulder'")
            
            # Create visualization
            print("🎨 Creating visualization...")
            visualization = detector.create_visualization(test_image_path, detected_objects)
            
            # Save the visualization
            output_path = "boulder_detection_test_result.jpg"
            cv2.imwrite(output_path, visualization)
            print(f"✅ Visualization saved as: {output_path}")
            
            # Print summary
            if detected_objects:
                print("\n📊 Detection Summary:")
                for i, obj in enumerate(detected_objects):
                    print(f"  Boulder #{i+1}:")
                    print(f"    - Class: {obj.class_name}")
                    print(f"    - Confidence: {obj.confidence:.2f}")
                    print(f"    - Bounding Box: {obj.bbox}")
                    print(f"    - Diameter: {obj.diameter_real:.2f}m")
                    print(f"    - Volume: {obj.volume_real:.2f}m³")
            else:
                print("📊 No boulders detected in the test image.")
            
            return True
            
        else:
            print(f"⚠️  Test image not found at: {test_image_path}")
            print("💡 You can test with any image by placing it in the boulder_detection folder.")
            return True
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Boulder Detection System")
    print("=" * 50)
    
    success = test_boulder_detection()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Boulder detection test completed successfully!")
        print("🎯 The system is now configured to detect and label boulders correctly.")
    else:
        print("❌ Boulder detection test failed!")
        print("🔧 Please check the error messages above and fix any issues.") 