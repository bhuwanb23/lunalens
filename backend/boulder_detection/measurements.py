"""
Measurements module for boulder and crater detection.
Handles physical measurements and calculations for detected objects.
"""

import math
import numpy as np
import cv2
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ObjectMeasurements:
    """Data class to store object measurements."""
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    width_px: int
    height_px: int
    width_real: float
    height_real: float
    area_real: float
    diameter_real: float
    volume_real: float
    circularity: float
    elongation: float
    degradation_state: str
    estimated_depth: Optional[float] = None


class PhysicalCalculator:
    """Class to handle physical measurements and calculations."""
    
    def __init__(self, scale: float = 1.0):
        """
        Initialize the physical calculator.
        
        Args:
            scale: Scale factor (meters per pixel)
        """
        self.scale = scale
    
    def calculate_basic_measurements(self, bbox: Tuple[int, int, int, int]) -> Tuple[int, int, float, float, float, float]:
        """
        Calculate basic measurements from bounding box.
        
        Args:
            bbox: Bounding box (x1, y1, x2, y2)
            
        Returns:
            Tuple of (width_px, height_px, width_real, height_real, area_real, diameter_real)
        """
        x1, y1, x2, y2 = bbox
        width_px = x2 - x1
        height_px = y2 - y1
        width_real = width_px * self.scale
        height_real = height_px * self.scale
        area_real = width_real * height_real
        diameter_real = (width_real + height_real) / 2
        
        return width_px, height_px, width_real, height_real, area_real, diameter_real
    
    def calculate_shape_metrics(self, width_px: int, height_px: int) -> Tuple[float, float]:
        """
        Calculate shape metrics (circularity and elongation).
        
        Args:
            width_px: Width in pixels
            height_px: Height in pixels
            
        Returns:
            Tuple of (circularity, elongation)
        """
        if max(width_px, height_px) > 0:
            circularity = min(width_px, height_px) / max(width_px, height_px)
            elongation = 1 - circularity
        else:
            circularity = 0
            elongation = 1
        
        return circularity, elongation
    
    def calculate_volume(self, diameter_real: float, object_type: str) -> float:
        """
        Calculate volume based on object type and diameter.
        
        Args:
            diameter_real: Diameter in real units
            object_type: Type of object ('crater' or 'boulder')
            
        Returns:
            Volume in cubic units
        """
        radius = diameter_real / 2
        
        if object_type == 'crater':
            # Assuming hemisphere shape for craters
            volume = (2/3) * math.pi * (radius ** 3)
        elif object_type == 'boulder':
            # Assuming spherical shape for boulders
            volume = (4/3) * math.pi * (radius ** 3)
        else:
            volume = 0
        
        return volume
    
    def determine_degradation_state(self, confidence: float) -> str:
        """
        Determine degradation state based on confidence.
        
        Args:
            confidence: Detection confidence score
            
        Returns:
            Degradation state string
        """
        if confidence >= 0.8:
            return "Fresh"
        elif confidence >= 0.6:
            return "Moderately degraded"
        else:
            return "Highly degraded"
    
    def estimate_shadow_depth(self, image_gray: np.ndarray, bbox: Tuple[int, int, int, int], 
                            solar_incidence_angle: float) -> Optional[float]:
        """
        Estimate object depth/height from shadow length.
        Works for both boulders and craters using shadow analysis.
        
        Args:
            image_gray: Grayscale image
            bbox: Bounding box (x1, y1, x2, y2)
            solar_incidence_angle: Solar incidence angle in degrees
            
        Returns:
            Estimated depth in meters, or None if calculation fails
        """
        if not (0 < solar_incidence_angle < 90):
            return None
        
        x1, y1, x2, y2 = bbox
        cropped_gray_crater = image_gray[y1:y2, x1:x2]
        
        # Simple shadow detection
        dark_pixels = cropped_gray_crater < np.mean(cropped_gray_crater) * 0.5
        
        if np.sum(dark_pixels) > 0:
            # Find coordinates of dark pixels
            dark_y, dark_x = np.where(dark_pixels)
            
            # Estimate shadow length
            shadow_length_px = max(np.max(dark_x) - np.min(dark_x), 
                                 np.max(dark_y) - np.min(dark_y))
            shadow_length_real = shadow_length_px * self.scale
            
            # Calculate depth
            angle_radians = math.radians(solar_incidence_angle)
            estimated_depth = shadow_length_real / math.tan(angle_radians)
            
            return estimated_depth
        
        return None
    
    def calculate_density(self, count: int, total_area_real: float) -> float:
        """
        Calculate density (objects per unit area).
        
        Args:
            count: Number of objects
            total_area_real: Total area in real units
            
        Returns:
            Density (objects per unit area)
        """
        return count / total_area_real if total_area_real > 0 else 0
    
    def get_complete_measurements(self, class_name: str, confidence: float, 
                                bbox: Tuple[int, int, int, int], 
                                image_gray: Optional[np.ndarray] = None,
                                solar_incidence_angle: Optional[float] = None) -> ObjectMeasurements:
        """
        Get complete measurements for an object.
        
        Args:
            class_name: Class name of the object
            confidence: Detection confidence
            bbox: Bounding box
            image_gray: Grayscale image for depth estimation
            solar_incidence_angle: Solar incidence angle for depth estimation
            
        Returns:
            ObjectMeasurements object
        """
        # Basic measurements
        width_px, height_px, width_real, height_real, area_real, diameter_real = \
            self.calculate_basic_measurements(bbox)
        
        # Shape metrics
        circularity, elongation = self.calculate_shape_metrics(width_px, height_px)
        
        # Volume
        volume_real = self.calculate_volume(diameter_real, class_name)
        
        # Degradation state
        degradation_state = self.determine_degradation_state(confidence)
        
        # Depth estimation via shadow analysis (for boulders and craters)
        estimated_depth = None
        if class_name in ('boulder', 'crater') and image_gray is not None and solar_incidence_angle is not None:
            estimated_depth = self.estimate_shadow_depth(image_gray, bbox, solar_incidence_angle)
        
        return ObjectMeasurements(
            class_name=class_name,
            confidence=confidence,
            bbox=bbox,
            width_px=width_px,
            height_px=height_px,
            width_real=width_real,
            height_real=height_real,
            area_real=area_real,
            diameter_real=diameter_real,
            volume_real=volume_real,
            circularity=circularity,
            elongation=elongation,
            degradation_state=degradation_state,
            estimated_depth=estimated_depth
        ) 