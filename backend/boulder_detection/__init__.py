"""
Boulder and Crater Detection Package

A comprehensive package for detecting and analyzing boulders and craters in images
using YOLO and Vision Transformer models with Grad-CAM visualization.

Modules:
    - models: Model loading and setup
    - transforms: Data preprocessing and transformations
    - measurements: Physical measurements and calculations
    - gradcam: Grad-CAM visualization
    - detector: Main detection logic and inference pipeline
    - main: User-friendly interface
"""

import os
import sys

# Add current directory to path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from detector import BoulderDetector
from gradcam import GradCAMVisualizer
from main import BoulderDetectionController, main
from measurements import ObjectMeasurements, PhysicalCalculator
from ml_models import ModelLoader, YoloCAMWrapper
from transforms import DataTransforms

__version__ = "1.0.0"
__author__ = "Boulder Detection Team"

__all__ = [
    'ModelLoader',
    'YoloCAMWrapper',
    'DataTransforms',
    'PhysicalCalculator',
    'ObjectMeasurements',
    'GradCAMVisualizer',
    'BoulderDetector',
    'BoulderDetectionController',
    'main'
]
