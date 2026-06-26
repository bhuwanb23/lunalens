"""
Test script to compare original detection with enhanced detection.
"""

import os

from detector import BoulderDetector
from main import BoulderDetectionController


def test_enhanced_detection():
    """Test enhanced detection vs original detection."""
    print("🧪 Testing enhanced detection vs original detection...")

    # Check if model files exist
    yolo_model_path = "best.pt"
    vit_model_path = "vit_model.pth"

    if not os.path.exists(yolo_model_path):
        print(f"❌ YOLO model not found at: {yolo_model_path}")
        return False

    if not os.path.exists(vit_model_path):
        print(f"❌ ViT model not found at: {vit_model_path}")
        return False

    try:
        # Initialize detector
        detector = BoulderDetector(yolo_model_path, vit_model_path, scale=1.0)
        print("✅ Detector initialized successfully!")

        # Test image path
        test_image_path = "download.png"

        if not os.path.exists(test_image_path):
            print(f"❌ Test image not found at: {test_image_path}")
            return False

        print("\n" + "="*60)
        print("🔍 TESTING ORIGINAL DETECTION")
        print("="*60)

        # Test original detection (high confidence threshold)
        original_objects = detector.detect_objects(test_image_path, confidence_threshold=0.5)
        print(f"✅ Original detection found: {len(original_objects)} objects")

        print("\n" + "="*60)
        print("🚀 TESTING ENHANCED DETECTION")
        print("="*60)

        # Test enhanced detection
        enhanced_objects = detector.detect_with_enhanced_sensitivity(test_image_path)
        print(f"✅ Enhanced detection found: {len(enhanced_objects)} objects")

        print("\n" + "="*60)
        print("📊 COMPARISON RESULTS")
        print("="*60)
        print(f"Original detection: {len(original_objects)} objects")
        print(f"Enhanced detection: {len(enhanced_objects)} objects")
        print(f"Improvement: {len(enhanced_objects) - len(original_objects)} additional objects detected")

        if len(enhanced_objects) > len(original_objects):
            print("🎉 Enhanced detection successfully detected more boulders!")

            # Create visualizations for comparison
            print("\n🎨 Creating comparison visualizations...")

            # Original detection visualization
            if original_objects:
                original_viz = detector.create_visualization(test_image_path, original_objects)
                import cv2
                cv2.imwrite("original_detection.png", original_viz)
                print("✅ Original detection visualization saved to: original_detection.png")

            # Enhanced detection visualization
            if enhanced_objects:
                enhanced_viz = detector.create_visualization(test_image_path, enhanced_objects)
                import cv2
                cv2.imwrite("enhanced_detection.png", enhanced_viz)
                print("✅ Enhanced detection visualization saved to: enhanced_detection.png")

            return True
        else:
            print("⚠️ No improvement detected. This might be due to the specific image content.")
            return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_controller_enhanced():
    """Test the controller with enhanced detection."""
    print("\n🧪 Testing controller with enhanced detection...")

    try:
        # Initialize controller
        controller = BoulderDetectionController()

        # Test image path
        test_image_path = "download.png"

        if not os.path.exists(test_image_path):
            print(f"❌ Test image not found at: {test_image_path}")
            return False

        # Test with enhanced detection (default)
        enhanced_objects = controller.detect_boulders(test_image_path, use_enhanced=True)
        print(f"✅ Controller enhanced detection found: {len(enhanced_objects)} objects")

        # Test with original detection
        original_objects = controller.detect_boulders(test_image_path, use_enhanced=False, use_vit_fallback=False)
        print(f"✅ Controller original detection found: {len(original_objects)} objects")

        print("\n📊 Controller comparison:")
        print(f"Enhanced: {len(enhanced_objects)} objects")
        print(f"Original: {len(original_objects)} objects")
        print(f"Improvement: {len(enhanced_objects) - len(original_objects)} additional objects")

        return True

    except Exception as e:
        print(f"❌ Controller test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting enhanced detection tests...")

    # Test 1: Direct detector comparison
    success1 = test_enhanced_detection()

    # Test 2: Controller comparison
    success2 = test_controller_enhanced()

    if success1 and success2:
        print("\n🎉 All tests passed! Enhanced detection is working correctly.")
    else:
        print("\n❌ Some tests failed!")
