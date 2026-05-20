"""
Main module for boulder and crater detection.
Provides a user-friendly interface to run the detection system.
"""

import os
import sys
import numpy as np
from typing import Optional, List
from detector import BoulderDetector
from gradcam import GradCAMVisualizer
from measurements import PhysicalCalculator, ObjectMeasurements


class BoulderDetectionController:
    """Main controller class for boulder detection system."""
    
    def __init__(self):
        """Initialize the controller with models from the boulder_detection folder."""
        # Model paths in the boulder_detection folder
        self.yolo_model_path = "best.pt"
        self.vit_model_path = "vit_model.pth"
        
        self.is_ready = False
        self.detector = None

        # Validate model paths
        if not self._validate_model_paths():
            print("⚠️ Model files not found. Boulder detection is disabled until best.pt and vit_model.pth are placed in the boulder_detection folder.")
            return

        print("🚀 Loading models...")
        try:
            self.detector = BoulderDetector(self.yolo_model_path, self.vit_model_path, scale=1.0)
            self.is_ready = True
            print("✅ Models loaded successfully!")
        except Exception as e:
            print(f"⚠️ Error loading models: {e}. Boulder detection is disabled.")
            self.detector = None
            self.is_ready = False
    
    def _validate_model_paths(self) -> bool:
        """Validate that model files exist."""
        if not os.path.exists(self.yolo_model_path):
            print(f"❌ YOLO model not found at: {self.yolo_model_path}")
            return False
        
        if not os.path.exists(self.vit_model_path):
            print(f"❌ ViT model not found at: {self.vit_model_path}")
            return False
        
        return True
    
    def detect_boulders(self, image_path: str, use_vit_fallback: bool = True, 
                       confidence_threshold: float = 0.6, use_enhanced: bool = True) -> List[ObjectMeasurements]:
        """Detect boulders in the image with enhanced sensitivity."""
        print(f"🔍 Detecting boulders in: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found at: {image_path}")
            return []
        
        try:
            if use_enhanced:
                print("🚀 Using enhanced detection with multiple strategies...")
                detected_objects = self.detector.detect_with_enhanced_sensitivity(image_path)
            elif use_vit_fallback:
                detected_objects = self.detector.detect_with_vit_fallback(
                    image_path, confidence_threshold
                )
            else:
                detected_objects = self.detector.detect_objects(image_path)
            
            print(f"✅ Detected {len(detected_objects)} objects!")
            return detected_objects
            
        except Exception as e:
            print(f"❌ Error during detection: {e}")
            return []
    
    def calculate_measurements(self, detected_objects: List[ObjectMeasurements], 
                             scale: float = 1.0, solar_incidence_angle: Optional[float] = None) -> List[ObjectMeasurements]:
        """Calculate physical measurements for detected objects."""
        print("📏 Calculating measurements...")
        
        # The measurements are already calculated in the detector
        # This method is kept for compatibility but doesn't need to recalculate
        print("✅ Measurements already calculated by detector!")
        return detected_objects
    
    def generate_gradcam(self, image_path: str, detected_objects: List[ObjectMeasurements]) -> str:
        """Generate Grad-CAM visualizations for detected objects."""
        print("🎨 Generating Grad-CAM visualizations...")
        print(f"🔍 Image path: {image_path}")
        print(f"🔍 Number of detected objects: {len(detected_objects)}")
        
        try:
            # Create Grad-CAM visualizations
            gradcam_image = self.detector.gradcam_visualizer.create_gradcam_visualization_for_objects(
                image_path, detected_objects
            )
            
            if gradcam_image is None:
                print("❌ Grad-CAM visualization returned None")
                return ""
            
            print(f"✅ Grad-CAM image created, shape: {gradcam_image.shape}")
            
            # Save visualization
            import os
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_gradcam.png"
            print(f"🔍 Output path: {output_path}")
            import cv2
            # Convert RGB to BGR for OpenCV
            gradcam_bgr = cv2.cvtColor(gradcam_image, cv2.COLOR_RGB2BGR)
            success = cv2.imwrite(output_path, gradcam_bgr)
            print(f"🔍 cv2.imwrite success: {success}")
            print(f"💾 Grad-CAM visualization saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating Grad-CAM: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def create_visualization(self, image_path: str, detected_objects: List[ObjectMeasurements]) -> str:
        """Create detection visualization with bounding boxes and measurements."""
        print("🎨 Creating detection visualization...")
        
        try:
            visualization = self.detector.create_visualization(image_path, detected_objects)
            
            # Save visualization
            import os
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_detected.png"
            import cv2
            # The visualization is already in BGR format from the detector
            cv2.imwrite(output_path, visualization)
            print(f"💾 Detection visualization saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            return ""
    
    def calculate_density_analysis(self, detected_objects: List[ObjectMeasurements], image_path: str) -> dict:
        """Calculate density analysis for detected objects."""
        print("📊 Calculating density analysis...")
        
        try:
            density_analysis = self.detector.calculate_density_analysis(detected_objects, image_path)
            print("✅ Density analysis completed!")
            return density_analysis
            
        except Exception as e:
            print(f"❌ Error calculating density analysis: {e}")
            return {}
    
    def print_summary(self, detected_objects: List[ObjectMeasurements], density_analysis: dict):
        """Print comprehensive summary of detection results."""
        print("\n" + "="*60)
        print("📋 DETECTION SUMMARY")
        print("="*60)
        
        self.detector.print_detection_summary(detected_objects, density_analysis)
        
        print("\n" + "="*60)
        print("📏 DETAILED MEASUREMENTS")
        print("="*60)
        
        for i, obj in enumerate(detected_objects):
            print(f"\nObject {i+1}:")
            print(f"  Class: {obj.class_name}")
            print(f"  Confidence: {obj.confidence:.3f}")
            print(f"  Width: {obj.width_real:.2f} m")
            print(f"  Height: {obj.height_real:.2f} m")
            print(f"  Diameter: {obj.diameter_real:.2f} m")
            print(f"  Area: {obj.area_real:.2f} m²")
            print(f"  Volume: {obj.volume_real:.2f} m³")
            print(f"  Circularity: {obj.circularity:.3f}")
            print(f"  Elongation: {obj.elongation:.3f}")
            print(f"  Degradation State: {obj.degradation_state}")
            if obj.estimated_depth is not None:
                print(f"  Estimated Depth: {obj.estimated_depth:.2f} m")


def get_user_inputs() -> tuple:
    """Get user inputs for scale and solar incidence angle."""
    print("\n=== Configuration ===")
    
    # Get scale
    scale_input = input("Enter the scale (meters per pixel), or press Enter to use default (1.0): ")
    scale = float(scale_input) if scale_input.strip() else 1.0
    
    # Get solar incidence angle
    solar_incidence_angle_input = input("Enter the solar incidence angle in degrees, or press Enter to skip depth calculation: ")
    solar_incidence_angle = float(solar_incidence_angle_input) if solar_incidence_angle_input.strip() else None
    
    return scale, solar_incidence_angle


def show_menu() -> str:
    """Show the main menu and get user choice."""
    print("\n" + "="*60)
    print("🌙 BOULDER & CRATER DETECTION SYSTEM")
    print("="*60)
    print("📁 Using default image: download.png")
    print("="*60)
    print("1. Detect boulders only")
    print("2. Detect boulders + Calculate measurements")
    print("3. Detect boulders + Generate Grad-CAM")
    print("4. Detect boulders + Create visualization")
    print("5. Full analysis (detect + measure + Grad-CAM + visualize)")
    print("6. Custom analysis")
    print("0. Exit")
    print("="*60)
    
    return input("Enter your choice (0-6): ").strip()


def main():
    """Main function to run the detection system."""
    print("🚀 Initializing Boulder Detection System...")
    print("📁 Default image: download.png (place this file in the current directory)")
    
    # Initialize controller
    controller = BoulderDetectionController()
    
    while True:
        choice = show_menu()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        
        elif choice in ["1", "2", "3", "4", "5", "6"]:
            # Use default image path
            image_path = "download.png"
            print(f"🔍 Using default image: {image_path}")
            
            if not os.path.exists(image_path):
                print(f"❌ Default image not found at: {image_path}")
                print("Please ensure 'download.png' is in the current directory.")
                continue
            
            # Get configuration
            scale, solar_incidence_angle = get_user_inputs()
            
            # Get detection parameters
            use_vit_fallback_input = input("Use ViT fallback for low confidence detections? (y/n, default: y): ").strip().lower()
            use_vit_fallback = use_vit_fallback_input != 'n'
            
            confidence_threshold = 0.6
            if use_vit_fallback:
                threshold_input = input(f"Enter confidence threshold for ViT fallback (default: {confidence_threshold}): ").strip()
                if threshold_input:
                    try:
                        confidence_threshold = float(threshold_input)
                    except ValueError:
                        print(f"Invalid threshold, using default: {confidence_threshold}")
            
            # Run detection
            detected_objects = controller.detect_boulders(image_path, use_vit_fallback, confidence_threshold)
            
            if not detected_objects:
                print("❌ No objects detected. Please try with a different image or parameters.")
                continue
            
            # Process based on choice
            if choice == "1":
                # Detection only
                pass
                
            elif choice == "2":
                # Detection + Measurements
                detected_objects = controller.calculate_measurements(
                    detected_objects, scale, solar_incidence_angle
                )
                
            elif choice == "3":
                # Detection + Grad-CAM
                controller.generate_gradcam(image_path, detected_objects)
                
            elif choice == "4":
                # Detection + Visualization
                controller.create_visualization(image_path, detected_objects)
                
            elif choice == "5":
                # Full analysis
                detected_objects = controller.calculate_measurements(
                    detected_objects, scale, solar_incidence_angle
                )
                controller.generate_gradcam(image_path, detected_objects)
                controller.create_visualization(image_path, detected_objects)
                
            elif choice == "6":
                # Custom analysis
                print("\n=== Custom Analysis Options ===")
                calc_measurements = input("Calculate measurements? (y/n): ").strip().lower() == 'y'
                gen_gradcam = input("Generate Grad-CAM? (y/n): ").strip().lower() == 'y'
                create_viz = input("Create visualization? (y/n): ").strip().lower() == 'y'
                
                if calc_measurements:
                    detected_objects = controller.calculate_measurements(
                        detected_objects, scale, solar_incidence_angle
                    )
                if gen_gradcam:
                    controller.generate_gradcam(image_path, detected_objects)
                if create_viz:
                    controller.create_visualization(image_path, detected_objects)
            
            # Calculate density analysis and print summary
            density_analysis = controller.calculate_density_analysis(detected_objects, image_path)
            controller.print_summary(detected_objects, density_analysis)
            
            print("\n✅ Analysis complete!")
            
        else:
            print("❌ Invalid choice. Please enter a number between 0 and 6.")


if __name__ == "__main__":
    main() 