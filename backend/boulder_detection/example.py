"""
Example script demonstrating how to use the boulder detection system.
This script shows different usage scenarios and configurations.
"""

import os
import sys
from detector import BoulderDetector


def example_basic_detection():
    """Example of basic object detection."""
    print("=== Example 1: Basic Detection ===")
    
    # Initialize detector
    detector = BoulderDetector(
        yolo_model_path="models/best.pt",
        vit_model_path="models/vit_model.pth",
        scale=1.0
    )
    
    # Detect objects
    detected_objects = detector.detect_objects("path/to/your/image.jpg")
    
    # Print results
    for i, obj in enumerate(detected_objects):
        print(f"Object {i+1}: {obj.class_name}, Confidence: {obj.confidence:.2f}")
        print(f"  Size: {obj.width_real:.2f}m x {obj.height_real:.2f}m")
        print(f"  Volume: {obj.volume_real:.2f}m³")


def example_vit_fallback():
    """Example of detection with ViT fallback for low confidence."""
    print("\n=== Example 2: ViT Fallback Detection ===")
    
    detector = BoulderDetector(
        yolo_model_path="models/best.pt",
        vit_model_path="models/vit_model.pth",
        scale=1.0
    )
    
    # Detect with ViT fallback
    detected_objects = detector.detect_with_vit_fallback(
        image_path="path/to/your/image.jpg",
        confidence_threshold=0.6
    )
    
    # Calculate and print density analysis
    density_analysis = detector.calculate_density_analysis(
        detected_objects, "path/to/your/image.jpg"
    )
    detector.print_detection_summary(detected_objects, density_analysis)


def example_depth_estimation():
    """Example of detection with depth estimation."""
    print("\n=== Example 3: Depth Estimation ===")
    
    detector = BoulderDetector(
        yolo_model_path="models/best.pt",
        vit_model_path="models/vit_model.pth",
        scale=1.0
    )
    
    # Detect with depth estimation
    detected_objects = detector.detect_with_depth_estimation(
        image_path="path/to/your/image.jpg",
        solar_incidence_angle=45.0  # degrees
    )
    
    # Print results with depth information
    for obj in detected_objects:
        if obj.class_name == 'crater' and obj.estimated_depth is not None:
            print(f"Crater depth: {obj.estimated_depth:.2f}m")


def example_visualization():
    """Example of creating visualizations."""
    print("\n=== Example 4: Visualization ===")
    
    detector = BoulderDetector(
        yolo_model_path="models/best.pt",
        vit_model_path="models/vit_model.pth",
        scale=1.0
    )
    
    # Detect objects
    detected_objects = detector.detect_objects("path/to/your/image.jpg")
    
    # Create visualization
    visualization = detector.create_visualization(
        "path/to/your/image.jpg", 
        detected_objects
    )
    
    # Save visualization
    import cv2
    cv2.imwrite("output_detection.jpg", visualization)
    print("Visualization saved as 'output_detection.jpg'")


def example_custom_scale():
    """Example with custom scale for different image resolutions."""
    print("\n=== Example 5: Custom Scale ===")
    
    # For high-resolution images, you might need a different scale
    # Example: 0.1 meters per pixel for high-res satellite imagery
    detector = BoulderDetector(
        yolo_model_path="models/best.pt",
        vit_model_path="models/vit_model.pth",
        scale=0.1  # 0.1 meters per pixel
    )
    
    detected_objects = detector.detect_objects("path/to/high_res_image.jpg")
    
    for obj in detected_objects:
        print(f"{obj.class_name}: {obj.diameter_real:.2f}m diameter")


def example_batch_processing():
    """Example of processing multiple images."""
    print("\n=== Example 6: Batch Processing ===")
    
    detector = BoulderDetector(
        yolo_model_path="models/best.pt",
        vit_model_path="models/vit_model.pth",
        scale=1.0
    )
    
    # List of images to process
    image_paths = [
        "path/to/image1.jpg",
        "path/to/image2.jpg",
        "path/to/image3.jpg"
    ]
    
    results = {}
    
    for image_path in image_paths:
        if os.path.exists(image_path):
            print(f"Processing: {image_path}")
            detected_objects = detector.detect_objects(image_path)
            density_analysis = detector.calculate_density_analysis(detected_objects, image_path)
            results[image_path] = {
                'objects': detected_objects,
                'density': density_analysis
            }
        else:
            print(f"Image not found: {image_path}")
    
    # Print summary
    for image_path, result in results.items():
        print(f"\n{image_path}:")
        print(f"  Objects detected: {len(result['objects'])}")
        print(f"  Crater density: {result['density']['crater_density']:.6f}")
        print(f"  Boulder density: {result['density']['boulder_density']:.6f}")


def main():
    """Run all examples."""
    print("Boulder Detection System - Examples")
    print("=" * 50)
    
    # Check if models exist
    if not os.path.exists("models/best.pt"):
        print("❌ YOLO model not found at 'models/best.pt'")
        print("Please ensure your models are in the correct location.")
        return
    
    if not os.path.exists("models/vit_model.pth"):
        print("❌ ViT model not found at 'models/vit_model.pth'")
        print("Please ensure your models are in the correct location.")
        return
    
    # Run examples (commented out to avoid errors without actual images)
    print("Examples are provided for reference.")
    print("To run them, uncomment the function calls below and provide valid image paths.")
    
    # Uncomment these lines to run the examples:
    # example_basic_detection()
    # example_vit_fallback()
    # example_depth_estimation()
    # example_visualization()
    # example_custom_scale()
    # example_batch_processing()
    
    print("\nTo run the interactive version, use:")
    print("python -m boulder_detection.main")


if __name__ == "__main__":
    main() 