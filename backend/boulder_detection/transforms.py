"""
Transforms module for boulder and crater detection.
Handles data preprocessing and transformations for YOLO and ViT models.
"""


import numpy as np
import torch
from PIL import Image
from torchvision import transforms


class DataTransforms:
    """Class to handle data transformations for different models."""

    def __init__(self):
        """Initialize the data transforms."""
        self.setup_transforms()

    def setup_transforms(self):
        """Setup the transformation pipelines."""
        # ViT transforms
        self.vit_transforms = {
            'train': transforms.Compose([
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ]),
        }

        # YOLO transforms (minimal preprocessing)
        self.yolo_transforms = transforms.Compose([
            transforms.Resize((640, 640)),
            transforms.ToTensor()
        ])

        # Class names for ViT
        self.class_names_vit = ['boulder']

    def get_vit_transform(self, mode: str = 'val') -> transforms.Compose:
        """
        Get ViT transformation pipeline.

        Args:
            mode: 'train' or 'val'

        Returns:
            Transformation pipeline
        """
        return self.vit_transforms[mode]

    def get_yolo_transform(self) -> transforms.Compose:
        """
        Get YOLO transformation pipeline.

        Returns:
            Transformation pipeline
        """
        return self.yolo_transforms

    def get_class_names(self) -> list:
        """
        Get class names for ViT model.

        Returns:
            List of class names
        """
        return self.class_names_vit

    def preprocess_image_for_vit(self, image: Image.Image, mode: str = 'val') -> torch.Tensor:
        """
        Preprocess image for ViT model.

        Args:
            image: PIL Image
            mode: 'train' or 'val'

        Returns:
            Preprocessed tensor
        """
        transform = self.get_vit_transform(mode)
        return transform(image).unsqueeze(0)

    def preprocess_image_for_yolo(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess image for YOLO model.

        Args:
            image: PIL Image

        Returns:
            Preprocessed tensor
        """
        transform = self.get_yolo_transform()
        return transform(image).unsqueeze(0)

    def normalize_image_for_gradcam(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize image for Grad-CAM visualization.

        Args:
            image: Input image as numpy array

        Returns:
            Normalized image
        """
        return image.astype(np.float32) / 255.0

    def get_normalization_params(self) -> dict[str, list]:
        """
        Get normalization parameters for different models.

        Returns:
            Dictionary with mean and std values
        """
        return {
            'vit': {
                'mean': [0.485, 0.456, 0.406],
                'std': [0.229, 0.224, 0.225]
            }
        }
