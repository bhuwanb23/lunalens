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
        
        # Class name mapping for YOLO results
        self.class_name_mapping = {0: 'boulder'}
    
    def _get_class_name(self, class_id: int) -> str:
        """
        Get the mapped class name for a given class ID.
        
        Args:
            class_id: The class ID from YOLO model
            
        Returns:
            The mapped class name
        """
        return self.class_name_mapping.get(class_id, 'unknown')
    
    def detect_objects(self, image_path: str, confidence_threshold: float = 0.1) -> List[ObjectMeasurements]:
        """
        Detect objects in an image with improved sensitivity.
        
        Args:
            image_path: Path to the image
            confidence_threshold: Lower confidence threshold to detect more objects
            
        Returns:
            List of detected objects with measurements
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        image_np = np.array(original_image)
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        
        # Run YOLO inference with lower confidence threshold
        results = self.yolo_model(image_path, conf=confidence_threshold, iou=0.3)
        
        detected_objects = []
        
        for r in results:
            boxes = r.boxes
            for i, box in enumerate(boxes):
                class_id = int(box.cls)
                class_name = self._get_class_name(class_id)
                confidence = box.conf[0].item()
                bbox = tuple(map(int, box.xyxy[0]))
                
                # Get measurements
                measurements = self.calculator.get_complete_measurements(
                    class_name, confidence, bbox, image_gray
                )
                detected_objects.append(measurements)
        
        return detected_objects
    
    def detect_with_vit_fallback(self, image_path: str, confidence_threshold: float = 0.3) -> List[ObjectMeasurements]:
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
        
        # Run YOLO inference with lower confidence threshold
        results = self.yolo_model(image_path, conf=0.1, iou=0.3)
        
        detected_objects = []
        
        for r in results:
            boxes = r.boxes
            for i, box in enumerate(boxes):
                class_id = int(box.cls)
                class_name = self._get_class_name(class_id)
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
    
    def detect_with_enhanced_sensitivity(self, image_path: str) -> List[ObjectMeasurements]:
        """
        Detect objects with enhanced sensitivity using multiple strategies.
        
        Args:
            image_path: Path to the image
            
        Returns:
            List of detected objects with measurements
        """
        print("🔍 Running enhanced detection with multiple strategies...")
        
        # Strategy 1: Very low confidence threshold
        results_low = self.yolo_model(image_path, conf=0.05, iou=0.2)
        
        # Strategy 2: Medium confidence threshold
        results_medium = self.yolo_model(image_path, conf=0.2, iou=0.3)
        
        # Strategy 3: Higher confidence threshold
        results_high = self.yolo_model(image_path, conf=0.4, iou=0.4)
        
        # Combine all results
        all_boxes = []
        all_confidences = []
        all_class_ids = []
        
        # Collect from all strategies
        for results in [results_low, results_medium, results_high]:
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    all_boxes.append(box.xyxy[0])
                    all_confidences.append(box.conf[0].item())
                    all_class_ids.append(int(box.cls))
        
        # Remove duplicates using non-maximum suppression
        detected_objects = []
        used_indices = set()
        
        for i in range(len(all_boxes)):
            if i in used_indices:
                continue
                
            current_box = all_boxes[i]
            current_confidence = all_confidences[i]
            current_class_id = all_class_ids[i]
            
            # Check for overlapping boxes
            overlapping_indices = []
            for j in range(i + 1, len(all_boxes)):
                if j in used_indices:
                    continue
                    
                other_box = all_boxes[j]
                
                # Calculate IoU
                x1 = max(current_box[0], other_box[0])
                y1 = max(current_box[1], other_box[1])
                x2 = min(current_box[2], other_box[2])
                y2 = min(current_box[3], other_box[3])
                
                if x2 > x1 and y2 > y1:
                    intersection = (x2 - x1) * (y2 - y1)
                    area1 = (current_box[2] - current_box[0]) * (current_box[3] - current_box[1])
                    area2 = (other_box[2] - other_box[0]) * (other_box[3] - other_box[1])
                    union = area1 + area2 - intersection
                    iou = intersection / union if union > 0 else 0
                    
                    if iou > 0.5:  # High overlap threshold
                        overlapping_indices.append(j)
            
            # Keep the box with highest confidence
            best_confidence = current_confidence
            best_index = i
            
            for idx in overlapping_indices:
                if all_confidences[idx] > best_confidence:
                    best_confidence = all_confidences[idx]
                    best_index = idx
            
            # Mark all overlapping boxes as used
            used_indices.add(i)
            for idx in overlapping_indices:
                used_indices.add(idx)
            
            # Use the best box
            best_box = all_boxes[best_index]
            best_class_id = all_class_ids[best_index]
            
            class_name = self._get_class_name(best_class_id)
            bbox = tuple(map(int, best_box))
            
            # Load image for measurements
            original_image = Image.open(image_path).convert('RGB')
            image_np = np.array(original_image)
            image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            
            # Get measurements
            measurements = self.calculator.get_complete_measurements(
                class_name, best_confidence, bbox, image_gray
            )
            detected_objects.append(measurements)
        
        print(f"✅ Enhanced detection found {len(detected_objects)} objects")
        
        # Additional strategy: Look for very small objects that might be missed
        print("🔍 Running additional small object detection...")
        small_objects = self._detect_small_objects(image_path, detected_objects)
        detected_objects.extend(small_objects)
        
        print(f"✅ Total objects after small object detection: {len(detected_objects)}")
        return detected_objects
    
    def _detect_small_objects(self, image_path: str, existing_objects: List[ObjectMeasurements]) -> List[ObjectMeasurements]:
        """
        Detect very small objects that might be missed by standard detection.
        
        Args:
            image_path: Path to the image
            existing_objects: Already detected objects
            
        Returns:
            List of additional small objects
        """
        try:
            # Load image
            original_image = Image.open(image_path).convert('RGB')
            image_np = np.array(original_image)
            image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            
            # Use very low confidence threshold for small objects
            results = self.yolo_model(image_path, conf=0.01, iou=0.1)
            
            small_objects = []
            existing_bboxes = [obj.bbox for obj in existing_objects]
            
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    class_id = int(box.cls)
                    class_name = self._get_class_name(class_id)
                    confidence = box.conf[0].item()
                    bbox = tuple(map(int, box.xyxy[0]))
                    
                    # Check if this is a small object (small area)
                    x1, y1, x2, y2 = bbox
                    area = (x2 - x1) * (y2 - y1)
                    
                    # Only consider small objects (area < 1000 pixels)
                    if area < 1000:
                        # Check if this bbox overlaps significantly with existing detections
                        is_duplicate = False
                        for existing_bbox in existing_bboxes:
                            ex1, ey1, ex2, ey2 = existing_bbox
                            
                            # Calculate IoU
                            ix1 = max(x1, ex1)
                            iy1 = max(y1, ey1)
                            ix2 = min(x2, ex2)
                            iy2 = min(y2, ey2)
                            
                            if ix2 > ix1 and iy2 > iy1:
                                intersection = (ix2 - ix1) * (iy2 - iy1)
                                area1 = (x2 - x1) * (y2 - y1)
                                area2 = (ex2 - ex1) * (ey2 - ey1)
                                union = area1 + area2 - intersection
                                iou = intersection / union if union > 0 else 0
                                
                                if iou > 0.3:  # Lower threshold for small objects
                                    is_duplicate = True
                                    break
                        
                        if not is_duplicate:
                            # Get measurements
                            measurements = self.calculator.get_complete_measurements(
                                class_name, confidence, bbox, image_gray
                            )
                            small_objects.append(measurements)
            
            print(f"✅ Small object detection found {len(small_objects)} additional objects")
            return small_objects
            
        except Exception as e:
            print(f"❌ Small object detection failed: {e}")
            return []
    
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
                class_id = int(box.cls)
                class_name = self._get_class_name(class_id)
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
        Create visualization of detected objects with only bounding boxes.
        
        Args:
            image_path: Path to the image
            detected_objects: List of detected objects
            show_gradcam: Whether to show Grad-CAM visualizations
            
        Returns:
            Visualization image with only bounding boxes
        """
        # Load image
        original_image = Image.open(image_path).convert('RGB')
        image_np = np.array(original_image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Draw only bounding boxes without any text labels
        for obj in detected_objects:
            x1, y1, x2, y2 = obj.bbox
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
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
        boulder_count = sum(1 for obj in detected_objects if obj.class_name == 'boulder')
        
        # Calculate densities
        boulder_density = self.calculator.calculate_density(boulder_count, total_area_real)
        
        return {
            'total_area_real': total_area_real,
            'boulder_count': boulder_count,
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
        print(f"Boulder Count: {density_analysis['boulder_count']}")
        print(f"Boulder Density: {density_analysis['boulder_density']:.6f} boulders per square meter") 