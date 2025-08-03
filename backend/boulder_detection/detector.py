"""
Detector module for boulder and crater detection.
Handles the main detection logic and inference pipeline.
"""

import cv2
import numpy as np
from PIL import Image
import torch
from typing import List, Dict, Any, Optional, Tuple
import os
import sys

# Add current directory to path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from ml_models import ModelLoader
from transforms import DataTransforms
from measurements import PhysicalCalculator, ObjectMeasurements
from gradcam import GradCAMVisualizer


class BoulderDetector:
    """Main detector class for boulder and crater detection."""
    
    def __init__(self, yolo_model_path: str, vit_model_path: str, scale: float = 1.0):
        """
        Initialize the detector.
        
        Args:
            yolo_model_path: Path to YOLO model
            vit_model_path: Path to ViT model
            scale: Scale factor (meters per pixel)
        """
        self.model_loader = ModelLoader(yolo_model_path, vit_model_path)
        self.transforms = DataTransforms()
        self.calculator = PhysicalCalculator(scale)
        self.scale = scale
        
        # Load models
        self.yolo_model, self.vit_model = self.model_loader.load_all_models()
        self.device = self.model_loader.get_device()
        
        # Setup Grad-CAM
        self.gradcam_visualizer = GradCAMVisualizer(
            self.vit_model, self.yolo_model, self.device
        )
        
        # Class names
        self.class_names_vit = self.transforms.get_class_names()
    
    def detect_objects(self, image_path: str) -> List[ObjectMeasurements]:
        """
        Detect objects in an image.
        
        Args:
            image_path: Path to the image
            
        Returns:
            List of detected objects with measurements
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        image_np = np.array(original_image)
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Run YOLO inference
        results = self.yolo_model(image_path)
        
        detected_objects = []
        
        for r in results:
            boxes = r.boxes
            for i, box in enumerate(boxes):
                class_name = r.names[int(box.cls)]
                confidence = box.conf[0].item()
                bbox = tuple(map(int, box.xyxy[0]))
                
                # Get measurements
                measurements = self.calculator.get_complete_measurements(
                    class_name, confidence, bbox, image_gray
                )
                detected_objects.append(measurements)
        
        return detected_objects
    
    def detect_with_vit_fallback(self, image_path: str, confidence_threshold: float = 0.6) -> List[ObjectMeasurements]:
        """
        Detect objects with ViT fallback for low confidence detections.
        
        Args:
            image_path: Path to the image
            confidence_threshold: Confidence threshold for ViT fallback
            
        Returns:
            List of detected objects with measurements
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        image_np = np.array(original_image)
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Run YOLO inference
        results = self.yolo_model(image_path)
        
        detected_objects = []
        
        for r in results:
            boxes = r.boxes
            for i, box in enumerate(boxes):
                class_name = r.names[int(box.cls)]
                confidence = box.conf[0].item()
                bbox = tuple(map(int, box.xyxy[0]))
                
                # ViT fallback for low confidence
                if confidence < confidence_threshold:
                    print(f"🔍 Low confidence ({confidence:.2f}). Sending to ViT for validation...")
                    
                    # Crop the detected region
                    x1, y1, x2, y2 = bbox
                    cropped_image = original_image.crop((x1, y1, x2, y2))
                    
                    # ViT inference
                    vit_input = self.transforms.preprocess_image_for_vit(cropped_image).to(self.device)
                    with torch.no_grad():
                        vit_output = self.vit_model(vit_input)
                    
                    # Get ViT prediction
                    probs = torch.nn.functional.softmax(vit_output[0], dim=0)
                    top_prob, top_catid = torch.topk(probs, 1)
                    vit_prediction = self.class_names_vit[top_catid[0]]
                    vit_confidence = top_prob[0].item()
                    
                    print(f"--- ViT Validation: '{vit_prediction}', Confidence: {vit_confidence:.2f} ---")
                    
                    # Use ViT prediction if confidence is higher
                    if vit_confidence > confidence:
                        class_name = vit_prediction
                        confidence = vit_confidence
                
                # Get measurements
                measurements = self.calculator.get_complete_measurements(
                    class_name, confidence, bbox, image_gray
                )
                detected_objects.append(measurements)
        
        return detected_objects
    
    def detect_with_depth_estimation(self, image_path: str, solar_incidence_angle: Optional[float] = None) -> List[ObjectMeasurements]:
        """
        Detect objects with depth estimation for craters.
        
        Args:
            image_path: Path to the image
            solar_incidence_angle: Solar incidence angle for depth estimation
            
        Returns:
            List of detected objects with measurements
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        image_np = np.array(original_image)
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Run YOLO inference
        results = self.yolo_model(image_path)
        
        detected_objects = []
        
        for r in results:
            boxes = r.boxes
            for i, box in enumerate(boxes):
                class_name = r.names[int(box.cls)]
                confidence = box.conf[0].item()
                bbox = tuple(map(int, box.xyxy[0]))
                
                # Get measurements with depth estimation
                measurements = self.calculator.get_complete_measurements(
                    class_name, confidence, bbox, image_gray, solar_incidence_angle
                )
                detected_objects.append(measurements)
        
        return detected_objects
    
    def create_visualization(self, image_path: str, detected_objects: List[ObjectMeasurements], 
                           show_gradcam: bool = False) -> np.ndarray:
        """
        Create visualization of detected objects.
        
        Args:
            image_path: Path to the image
            detected_objects: List of detected objects
            show_gradcam: Whether to show Grad-CAM visualizations
            
        Returns:
            Visualization image
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        image_np = np.array(original_image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Draw bounding boxes and labels
        for i, obj in enumerate(detected_objects):
            x1, y1, x2, y2 = obj.bbox
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Prepare text lines
            text_lines = [
                f"{obj.class_name} #{i+1}",
                f"Conf: {obj.confidence:.2f}",
                f"Dia: {obj.diameter_real:.2f}m, Vol: {obj.volume_real:.2f}m³"
            ]
            
            if obj.circularity > 0:
                text_lines.append(f"Circ: {obj.circularity:.2f}, Elong: {obj.elongation:.2f}")
            
            if obj.degradation_state != "N/A":
                text_lines.append(f"Degradation: {obj.degradation_state}")
            
            if obj.estimated_depth is not None:
                text_lines.append(f"Depth: {obj.estimated_depth:.2f}m")
            
            # Put text on image
            for line_num, text_line in enumerate(text_lines):
                cv2.putText(image_bgr, text_line, 
                           (x1, y1 - 10 - line_num * 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        return image_bgr
    
    def calculate_density_analysis(self, detected_objects: List[ObjectMeasurements], 
                                 image_path: str) -> Dict[str, Any]:
        """
        Calculate density analysis for detected objects.
        
        Args:
            detected_objects: List of detected objects
            image_path: Path to the image
            
        Returns:
            Dictionary with density analysis results
        """
        # Get image dimensions
        image = Image.open(image_path)
        image_width, image_height = image.size
        total_area_px = image_width * image_height
        total_area_real = total_area_px * (self.scale ** 2)
        
        # Count objects by type
        crater_count = sum(1 for obj in detected_objects if obj.class_name == 'crater')
        boulder_count = sum(1 for obj in detected_objects if obj.class_name == 'boulder')
        
        # Calculate densities
        crater_density = self.calculator.calculate_density(crater_count, total_area_real)
        boulder_density = self.calculator.calculate_density(boulder_count, total_area_real)
        
        return {
            'total_area_real': total_area_real,
            'crater_count': crater_count,
            'boulder_count': boulder_count,
            'crater_density': crater_density,
            'boulder_density': boulder_density
        }
    
    def print_detection_summary(self, detected_objects: List[ObjectMeasurements], 
                              density_analysis: Dict[str, Any]):
        """
        Print a summary of detection results.
        
        Args:
            detected_objects: List of detected objects
            density_analysis: Density analysis results
        """
        print("\n--- Detection Summary ---")
        
        for i, obj in enumerate(detected_objects):
            print(f"\n--- Detected {obj.class_name} #{i+1} ---")
            print(f"  - Bounding Box (px): {obj.bbox}")
            print(f"  - Confidence: {obj.confidence:.2f}")
            print(f"  - Width: {obj.width_real:.2f} meters")
            print(f"  - Height: {obj.height_real:.2f} meters")
            print(f"  - Area: {obj.area_real:.2f} square meters")
            print(f"  - Approx. Diameter: {obj.diameter_real:.2f} meters")
            print(f"  - Estimated Volume: {obj.volume_real:.2f} cubic meters")
            print(f"  - Circularity: {obj.circularity:.2f}")
            print(f"  - Elongation: {obj.elongation:.2f}")
            print(f"  - Degradation State: {obj.degradation_state}")
            
            if obj.estimated_depth is not None:
                print(f"  - Estimated Depth: {obj.estimated_depth:.2f} meters")
        
        print("\n--- Density Analysis ---")
        print(f"Total Image Area: {density_analysis['total_area_real']:.2f} square meters")
        print(f"Crater Count: {density_analysis['crater_count']}")
        print(f"Crater Density: {density_analysis['crater_density']:.6f} craters per square meter")
        print(f"Boulder Count: {density_analysis['boulder_count']}")
        print(f"Boulder Density: {density_analysis['boulder_density']:.6f} boulders per square meter") 