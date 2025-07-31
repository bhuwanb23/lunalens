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
from models import YoloCAMWrapper


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
        # Setup ViT Grad-CAM
        try:
            vit_target_layer = self.vit_model.blocks[-1].norm1
            self.vit_cam = GradCAM(model=self.vit_model, target_layers=[vit_target_layer])
        except Exception as e:
            print(f"Warning: Could not setup ViT Grad-CAM: {e}")
            self.vit_cam = None
        
        # Setup YOLO Grad-CAM
        try:
            target_layer = self.yolo_model.model.model[-2]  # Use the last C2f layer
            self.yolo_cam = None  # Will be created on-demand
        except Exception as e:
            print(f"Warning: Could not setup YOLO Grad-CAM: {e}")
            self.yolo_cam = None
    
    def get_yolo_gradcam(self, image_tensor: torch.Tensor) -> Optional[np.ndarray]:
        """
        Get Grad-CAM for YOLO model.
        
        Args:
            image_tensor: Input image tensor
            
        Returns:
            Grad-CAM visualization or None if failed
        """
        try:
            if self.yolo_cam is None:
                target_layer = self.yolo_model.model.model[-2]
                wrapped_model = YoloCAMWrapper(self.yolo_model.model)
                self.yolo_cam = GradCAM(model=wrapped_model, target_layers=[target_layer])
            
            grayscale_cam = self.yolo_cam(input_tensor=image_tensor.clone().detach().requires_grad_(True))[0, :]
            return grayscale_cam
        except Exception as e:
            print(f"❌ YOLO Grad-CAM failed: {e}")
            return None
    
    def get_vit_gradcam(self, image: Image.Image, class_id: int, 
                       normalization_params: dict) -> Optional[np.ndarray]:
        """
        Get Grad-CAM for ViT model.
        
        Args:
            image: Input image
            class_id: Target class ID
            normalization_params: Normalization parameters
            
        Returns:
            Grad-CAM visualization or None if failed
        """
        try:
            if self.vit_cam is None:
                return None
            
            # Preprocess image
            input_img_np = np.array(image.resize((224, 224))).astype(np.float32) / 255
            input_tensor = preprocess_image(
                np.copy(input_img_np),
                mean=normalization_params['mean'],
                std=normalization_params['std']
            )
            
            # Generate Grad-CAM
            grayscale_cam = self.vit_cam(
                input_tensor=input_tensor,
                targets=[ClassifierOutputTarget(class_id)]
            )[0]
            
            return grayscale_cam
        except Exception as e:
            print(f"❌ ViT Grad-CAM failed: {e}")
            return None
    
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