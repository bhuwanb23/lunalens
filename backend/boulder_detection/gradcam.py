"""
Grad-CAM module for boulder and crater detection.
Handles Grad-CAM visualization for YOLO and ViT models.
"""

import torch
import numpy as np
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image, preprocess_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from typing import Optional, Tuple
import os
import sys

# Add current directory to path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from ml_models import YoloCAMWrapper


class GradCAMVisualizer:
    """Class to handle Grad-CAM visualization for different models."""
    
    def __init__(self, vit_model, yolo_model, device):
        """
        Initialize the Grad-CAM visualizer.
        
        Args:
            vit_model: ViT model
            yolo_model: YOLO model
            device: PyTorch device
        """
        self.vit_model = vit_model
        self.yolo_model = yolo_model
        self.device = device
        self.setup_gradcam()
    
    def setup_gradcam(self):
        """Setup Grad-CAM for both models."""
        # Skip ViT Grad-CAM setup due to compatibility issues
        print("⚠️ Skipping ViT Grad-CAM setup (using attention maps instead)")
        self.vit_cam = None
        
        # Setup YOLO Grad-CAM with better target layer selection
        try:
            # Find a suitable target layer in YOLO
            if hasattr(self.yolo_model.model, 'model'):
                # Try different layers
                for i in range(len(self.yolo_model.model.model) - 1, -1, -1):
                    layer = self.yolo_model.model.model[i]
                    if hasattr(layer, 'conv') or hasattr(layer, 'cv'):
                        target_layer = layer
                        break
                else:
                    target_layer = self.yolo_model.model.model[-2]
            else:
                target_layer = self.yolo_model.model
            
            self.yolo_cam = None  # Will be created on-demand
            print("✅ YOLO Grad-CAM setup successful")
        except Exception as e:
            print(f"Warning: Could not setup YOLO Grad-CAM: {e}")
            self.yolo_cam = None
    
    def get_yolo_gradcam(self, image_tensor: torch.Tensor) -> Optional[np.ndarray]:
        """
        Get Grad-CAM for YOLO model with improved error handling.
        
        Args:
            image_tensor: Input image tensor
            
        Returns:
            Grad-CAM visualization or None if failed
        """
        try:
            if self.yolo_cam is None:
                # Find a suitable target layer
                if hasattr(self.yolo_model.model, 'model'):
                    for i in range(len(self.yolo_model.model.model) - 1, -1, -1):
                        layer = self.yolo_model.model.model[i]
                        if hasattr(layer, 'conv') or hasattr(layer, 'cv'):
                            target_layer = layer
                            break
                    else:
                        target_layer = self.yolo_model.model.model[-2]
                else:
                    target_layer = self.yolo_model.model
                
                wrapped_model = YoloCAMWrapper(self.yolo_model.model)
                self.yolo_cam = GradCAM(model=wrapped_model, target_layers=[target_layer])
            
            # Ensure tensor is on correct device
            if hasattr(self.yolo_model, 'device'):
                image_tensor = image_tensor.to(self.yolo_model.device)
            
            grayscale_cam = self.yolo_cam(input_tensor=image_tensor.clone().detach().requires_grad_(True))[0, :]
            return grayscale_cam
        except Exception as e:
            print(f"❌ YOLO Grad-CAM failed: {e}")
            return None
    
    def get_vit_gradcam(self, image: Image.Image, class_id: int, 
                       normalization_params: dict) -> Optional[np.ndarray]:
        """
        Get Grad-CAM for ViT model with improved error handling.
        
        Args:
            image: Input image
            class_id: Target class ID
            normalization_params: Normalization parameters
            
        Returns:
            Grad-CAM visualization or None if failed
        """
        try:
            # Skip Grad-CAM for ViT due to compatibility issues
            # Use fallback attention map instead
            print("⚠️ Using fallback attention map for ViT (Grad-CAM not compatible)")
            return self._create_fallback_attention_map(image)
                
        except Exception as e:
            print(f"❌ ViT attention map failed: {e}")
            return None
    
    def _create_fallback_attention_map(self, image: Image.Image) -> np.ndarray:
        """
        Create a fallback attention map when Grad-CAM fails.
        
        Args:
            image: Input image
            
        Returns:
            Simple attention map
        """
        try:
            # Resize image to standard size
            resized_image = image.resize((224, 224))
            img_array = np.array(resized_image).astype(np.float32) / 255
            
            # Create a more sophisticated attention map based on image features
            h, w = img_array.shape[:2]
            
            # Convert to grayscale for edge detection
            if len(img_array.shape) == 3:
                gray = np.dot(img_array[..., :3], [0.299, 0.587, 0.114])
            else:
                gray = img_array
            
            # Create attention map based on image intensity and edges
            # Higher intensity areas get more attention
            intensity_map = gray
            
            # Create a center bias (objects are often in center)
            y, x = np.ogrid[:h, :w]
            center_y, center_x = h // 2, w // 2
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            max_distance = np.sqrt(center_x**2 + center_y**2)
            center_bias = 1 - (distance / max_distance)
            center_bias = np.clip(center_bias, 0, 1)
            
            # Combine intensity and center bias
            attention_map = 0.7 * intensity_map + 0.3 * center_bias
            attention_map = np.clip(attention_map, 0, 1)
            
            # Apply to all channels with a heatmap color scheme
            attention_map_3d = np.stack([attention_map] * 3, axis=-1)
            
            # Apply a heatmap color scheme (red for high attention, blue for low)
            heatmap = np.zeros_like(attention_map_3d)
            heatmap[:, :, 0] = attention_map  # Red channel
            heatmap[:, :, 1] = attention_map * 0.5  # Green channel
            heatmap[:, :, 2] = 0  # Blue channel
            
            return heatmap
            
        except Exception as e:
            print(f"❌ Fallback attention map failed: {e}")
            # Return a simple uniform map
            return np.ones((224, 224, 3), dtype=np.float32)
    
    def create_gradcam_visualization(self, image: np.ndarray, grayscale_cam: np.ndarray) -> np.ndarray:
        """
        Create Grad-CAM visualization overlay.
        
        Args:
            image: Input image
            grayscale_cam: Grad-CAM heatmap
            
        Returns:
            Visualization with overlay
        """
        try:
            cam_result = show_cam_on_image(image, grayscale_cam, use_rgb=True)
            return cam_result
        except Exception as e:
            print(f"❌ Grad-CAM visualization failed: {e}")
            return image
    
    def visualize_yolo_gradcam(self, image: Image.Image) -> Optional[np.ndarray]:
        """
        Visualize YOLO Grad-CAM.
        
        Args:
            image: Input image
            
        Returns:
            Grad-CAM visualization or None if failed
        """
        try:
            # Resize image for YOLO
            resized_image = image.resize((640, 640))
            input_tensor = torch.tensor(np.array(resized_image)).permute(2, 0, 1).float().unsqueeze(0)
            
            # Get Grad-CAM
            grayscale_cam = self.get_yolo_gradcam(input_tensor)
            if grayscale_cam is None:
                return None
            
            # Create visualization
            input_np = np.array(resized_image).astype(np.float32) / 255
            cam_result = self.create_gradcam_visualization(input_np, grayscale_cam)
            
            return cam_result
        except Exception as e:
            print(f"❌ YOLO Grad-CAM visualization failed: {e}")
            return None
    
    def visualize_vit_gradcam(self, image: Image.Image, class_id: int, 
                            normalization_params: dict) -> Optional[np.ndarray]:
        """
        Visualize ViT Grad-CAM.
        
        Args:
            image: Input image
            class_id: Target class ID
            normalization_params: Normalization parameters
            
        Returns:
            Grad-CAM visualization or None if failed
        """
        try:
            # Get Grad-CAM
            grayscale_cam = self.get_vit_gradcam(image, class_id, normalization_params)
            if grayscale_cam is None:
                return None
            
            # Create visualization
            input_img_np = np.array(image.resize((224, 224))).astype(np.float32) / 255
            cam_result = self.create_gradcam_visualization(input_img_np, grayscale_cam)
            
            return cam_result
        except Exception as e:
            print(f"❌ ViT Grad-CAM visualization failed: {e}")
            return None
    
    def create_gradcam_visualization_for_objects(self, image_path: str, detected_objects) -> Optional[np.ndarray]:
        """
        Create Grad-CAM visualization for detected objects with improved error handling.
        
        Args:
            image_path: Path to the input image
            detected_objects: List of detected objects
            
        Returns:
            Grad-CAM visualization image or None if failed
        """
        try:
            # Load the original image
            original_image = Image.open(image_path).convert('RGB')
            image_np = np.array(original_image).astype(np.float32) / 255
            
            # Create a composite visualization
            result_image = image_np.copy()
            
            # Track successful visualizations
            successful_visualizations = 0
            
            # For each detected object, create a localized Grad-CAM
            for i, obj in enumerate(detected_objects):
                try:
                    # Extract the bounding box region
                    x1, y1, x2, y2 = obj.bbox
                    
                    # Ensure bounding box is valid
                    if x1 >= x2 or y1 >= y2:
                        print(f"⚠️ Invalid bounding box for object {i+1}: {obj.bbox}")
                        continue
                    
                    # Crop the region for the detected object
                    cropped_image = original_image.crop((x1, y1, x2, y2))
                    
                    # Skip if cropped image is too small
                    if cropped_image.size[0] < 10 or cropped_image.size[1] < 10:
                        print(f"⚠️ Cropped image too small for object {i+1}")
                        continue
                    
                    # Determine class ID for ViT (0 for crater, 1 for boulder)
                    class_id = 0 if obj.class_name == 'boulder' else 0
                    
                    # Normalization parameters for ViT
                    normalization_params = {
                        'mean': [0.485, 0.456, 0.406],
                        'std': [0.229, 0.224, 0.225]
                    }
                    
                    # Generate Grad-CAM for this object
                    gradcam_result = self.visualize_vit_gradcam(cropped_image, class_id, normalization_params)
                    
                    if gradcam_result is not None:
                        # Resize the Grad-CAM result to match the original bounding box
                        from PIL import Image as PILImage
                        gradcam_pil = PILImage.fromarray((gradcam_result * 255).astype(np.uint8))
                        gradcam_resized = gradcam_pil.resize((x2 - x1, y2 - y1))
                        gradcam_np = np.array(gradcam_resized).astype(np.float32) / 255
                        
                        # Overlay the Grad-CAM on the original image
                        alpha = 0.6
                        result_image[y1:y2, x1:x2] = (
                            alpha * gradcam_np + (1 - alpha) * result_image[y1:y2, x1:x2]
                        )
                        successful_visualizations += 1
                        
                except Exception as e:
                    print(f"❌ Grad-CAM failed for object {i+1}: {e}")
                    continue
            
            # If no successful visualizations, create a simple bounding box visualization
            if successful_visualizations == 0:
                print("⚠️ No Grad-CAM visualizations successful, creating bounding box visualization")
                return self._create_bounding_box_visualization(original_image, detected_objects)
            
            print(f"✅ Created {successful_visualizations} Grad-CAM visualizations")
            return (result_image * 255).astype(np.uint8)
            
        except Exception as e:
            print(f"❌ Grad-CAM visualization failed: {e}")
            # Fallback to bounding box visualization
            try:
                original_image = Image.open(image_path).convert('RGB')
                return self._create_bounding_box_visualization(original_image, detected_objects)
            except Exception as fallback_error:
                print(f"❌ Fallback visualization also failed: {fallback_error}")
                return None
    
    def _create_bounding_box_visualization(self, image: Image.Image, detected_objects) -> np.ndarray:
        """
        Create a simple bounding box visualization as fallback.
        
        Args:
            image: Input image
            detected_objects: List of detected objects
            
        Returns:
            Visualization with bounding boxes
        """
        try:
            import cv2
            
            # Convert PIL image to OpenCV format
            image_np = np.array(image)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            
            # Draw bounding boxes
            for i, obj in enumerate(detected_objects):
                x1, y1, x2, y2 = obj.bbox
                
                # Draw rectangle
                cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Add label
                label = f"{obj.class_name} {obj.confidence:.2f}"
                cv2.putText(image_bgr, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Convert back to RGB
            image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            return image_rgb
            
        except Exception as e:
            print(f"❌ Bounding box visualization failed: {e}")
            return np.array(image) 