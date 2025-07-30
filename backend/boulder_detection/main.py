"""
Main module for boulder and crater detection.
Provides a user-friendly interface to run the detection system.
"""

import os
import sys
from typing import Optional, List
from .detector import BoulderDetector
from .gradcam import GradCAMVisualizer
from .measurements import PhysicalCalculator, ObjectMeasurements


class BoulderDetectionController:
    """Main controller class for boulder detection system."""
    
    def __init__(self):
        """Initialize the controller with models from the boulder_detection folder."""
        # Model paths in the boulder_detection folder
        self.yolo_model_path = "best.pt"
        self.vit_model_path = "vit_model.pth"
        
        # Validate model paths
        if not self._validate_model_paths():
            print("❌ Model files not found. Please ensure best.pt and vit_model.pth are in the boulder_detection folder.")
            sys.exit(1)
        
        print("🚀 Loading models...")
        try:
            self.detector = BoulderDetector(self.yolo_model_path, self.vit_model_path, scale=1.0)
            print("✅ Models loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            sys.exit(1)
    
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
                       confidence_threshold: float = 0.6) -> List[ObjectMeasurements]:
        """Detect boulders in the image."""
        print(f"🔍 Detecting boulders in: {image_path}")
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found at: {image_path}")
            return []
        
        try:
            if use_vit_fallback:
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
        
        calculator = PhysicalCalculator(scale)
        results = []
        
        for i, obj in enumerate(detected_objects):
            print(f"  Processing object {i+1}/{len(detected_objects)}...")
            
            # Basic measurements
            measurements = calculator.calculate_basic_measurements(obj)
            
            # Shape metrics
            shape_metrics = calculator.calculate_shape_metrics(obj)
            
            # Volume
            volume = calculator.calculate_volume(obj)
            
            # Degradation state
            degradation = calculator.calculate_degradation_state(obj)
            
            # Depth estimation (if solar angle provided)
            depth = None
            if solar_incidence_angle is not None:
                depth = calculator.calculate_crater_depth(obj, solar_incidence_angle)
            
            # Update object with all measurements
            obj.size = measurements.size
            obj.diameter = measurements.diameter
            obj.area = measurements.area
            obj.circularity = shape_metrics.circularity
            obj.elongation = shape_metrics.elongation
            obj.volume = volume
            obj.degradation_state = degradation
            obj.depth = depth
            
            results.append(obj)
        
        print("✅ Measurements calculated!")
        return results
    
    def generate_gradcam(self, image_path: str, detected_objects: List[ObjectMeasurements]) -> str:
        """Generate Grad-CAM visualizations for detected objects."""
        print("🎨 Generating Grad-CAM visualizations...")
        
        try:
            # Create Grad-CAM visualizations
            gradcam_image = self.detector.gradcam_visualizer.create_gradcam_visualization(
                image_path, detected_objects
            )
            
            # Save visualization
            output_path = image_path.replace('.', '_gradcam.')
            import cv2
            cv2.imwrite(output_path, gradcam_image)
            print(f"💾 Grad-CAM visualization saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating Grad-CAM: {e}")
            return ""
    
    def create_visualization(self, image_path: str, detected_objects: List[ObjectMeasurements]) -> str:
        """Create detection visualization with bounding boxes and measurements."""
        print("🎨 Creating detection visualization...")
        
        try:
            visualization = self.detector.create_visualization(image_path, detected_objects)
            
            # Save visualization
            output_path = image_path.replace('.', '_detected.')
            import cv2
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
            print(f"  Size: {obj.size:.2f} m")
            print(f"  Diameter: {obj.diameter:.2f} m")
            print(f"  Area: {obj.area:.2f} m²")
            print(f"  Volume: {obj.volume:.2f} m³")
            print(f"  Circularity: {obj.circularity:.3f}")
            print(f"  Elongation: {obj.elongation:.3f}")
            print(f"  Degradation State: {obj.degradation_state}")
            if obj.depth is not None:
                print(f"  Estimated Depth: {obj.depth:.2f} m")


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
    
    # Initialize controller
    controller = BoulderDetectionController()
    
    while True:
        choice = show_menu()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        
        elif choice in ["1", "2", "3", "4", "5", "6"]:
            # Get image path
            image_path = input("\nEnter the path to the image: ").strip()
            if not image_path:
                print("❌ No image path provided.")
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