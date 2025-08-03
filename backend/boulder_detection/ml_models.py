"""
ML Models module for boulder and crater detection.
Handles loading and setup of YOLO and ViT models.
"""

import torch
import timm
from ultralytics import YOLO
from typing import Tuple, Optional
import os


class ModelLoader:
    """Class to handle loading and setup of detection models."""
    
    def __init__(self, yolo_model_path: str, vit_model_path: str):
        """
        Initialize the model loader.
        
        Args:
            yolo_model_path: Path to the trained YOLO model
            vit_model_path: Path to the trained ViT model
        """
        self.yolo_model_path = yolo_model_path
        self.vit_model_path = vit_model_path
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        self.yolo_model = None
        self.vit_model = None
        
    def load_yolo_model(self) -> YOLO:
        """
        Load the YOLO model for inference.
        
        Returns:
            Loaded YOLO model
        """
        if not os.path.exists(self.yolo_model_path):
            raise FileNotFoundError(f"YOLO model not found at: {self.yolo_model_path}")
            
        self.yolo_model = YOLO(self.yolo_model_path)
        print("✅ YOLOv8 model loaded successfully in inference mode.")
        return self.yolo_model
    
    def load_vit_model(self, num_classes: int = 2) -> torch.nn.Module:
        """
        Load the ViT model for inference.
        
        Args:
            num_classes: Number of classes for the ViT model
            
        Returns:
            Loaded ViT model
        """
        if not os.path.exists(self.vit_model_path):
            raise FileNotFoundError(f"ViT model not found at: {self.vit_model_path}")
            
        self.vit_model = timm.create_model('vit_base_patch16_224', 
                                         pretrained=False, 
                                         num_classes=num_classes)
        self.vit_model.load_state_dict(torch.load(self.vit_model_path, 
                                                 map_location=self.device))
        self.vit_model.to(self.device)
        self.vit_model.eval()
        print("✅ ViT model loaded successfully in inference mode.")
        return self.vit_model
    
    def load_all_models(self, num_classes: int = 2) -> Tuple[YOLO, torch.nn.Module]:
        """
        Load both YOLO and ViT models.
        
        Args:
            num_classes: Number of classes for the ViT model
            
        Returns:
            Tuple of (yolo_model, vit_model)
        """
        yolo_model = self.load_yolo_model()
        vit_model = self.load_vit_model(num_classes)
        return yolo_model, vit_model
    
    def get_device(self) -> torch.device:
        """Get the current device (CPU/GPU)."""
        return self.device


class YoloCAMWrapper(torch.nn.Module):
    """Wrapper to make YOLO compatible with Grad-CAM."""
    
    def __init__(self, model):
        super(YoloCAMWrapper, self).__init__()
        self.model = model

    def forward(self, x):
        """
        Forward pass for Grad-CAM compatibility.
        
        Args:
            x: Input tensor
            
        Returns:
            Scalar value for Grad-CAM
        """
        preds = self.model(x)
        if isinstance(preds, tuple):
            return preds[0].max()
        return preds.max() 