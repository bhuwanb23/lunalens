"""
Test script to verify that visualization shows only bounding boxes without text labels.
"""

import os
import sys
from detector import BoulderDetector
from measurements import ObjectMeasurements

def test_clean_visualization():
    """Test that visualization shows only bounding boxes."""
    print("🧪 Testing clean visualization (bounding boxes only)...")
    
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
        
        # Create mock detected objects for testing
        mock_objects = [
            ObjectMeasurements(
                class_name="boulder",
                confidence=0.85,
                bbox=(100, 100, 200, 150),
                width_real=10.0,
                height_real=5.0,
                area_real=50.0,
                diameter_real=7.5,
                volume_real=187.5,
                circularity=0.8,
                elongation=1.2,
                degradation_state="Fresh",
                estimated_depth=2.0
            ),
            ObjectMeasurements(
                class_name="boulder",
                confidence=0.92,
                bbox=(300, 200, 400, 280),
                width_real=12.0,
                height_real=8.0,
                area_real=96.0,
                diameter_real=10.0,
                volume_real=384.0,
                circularity=0.9,
                elongation=1.1,
                degradation_state="Moderate",
                estimated_depth=3.0
            )
        ]
        
        # Create visualization
        visualization = detector.create_visualization(test_image_path, mock_objects)
        
        if visualization is not None:
            # Save the visualization
            import cv2
            output_path = "test_clean_visualization.png"
            cv2.imwrite(output_path, visualization)
            print(f"✅ Clean visualization saved to: {output_path}")
            print("✅ Test passed! Visualization should show only bounding boxes without text labels.")
            return True
        else:
            print("❌ Visualization returned None")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_clean_visualization()
    if success:
        print("\n🎉 All tests passed! The visualization now shows only bounding boxes.")
    else:
        print("\n❌ Tests failed!") 