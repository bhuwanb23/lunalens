# Boulder and Crater Detection System

A comprehensive Python package for detecting and analyzing boulders and craters in images using YOLO and Vision Transformer models with Grad-CAM visualization.

## Features

- **Dual Model Detection**: Uses YOLO for initial detection and ViT for validation of low-confidence detections
- **Physical Measurements**: Calculates size, diameter, area, volume, circularity, and elongation
- **Depth Estimation**: Estimates crater depth using shadow analysis and solar incidence angle
- **Grad-CAM Visualization**: Provides attention maps for model interpretability
- **Density Analysis**: Calculates object density per unit area
- **Degradation Assessment**: Qualitative assessment of crater freshness based on confidence

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have the trained models:
   - YOLO model: `best.pt`
   - ViT model: `vit_model.pth`

## Project Structure

```
boulder_detection/
├── __init__.py              # Package initialization
├── models.py                # Model loading and setup
├── transforms.py            # Data preprocessing and transformations
├── measurements.py          # Physical measurements and calculations
├── gradcam.py              # Grad-CAM visualization
├── detector.py             # Main detection logic and inference pipeline
├── main.py                 # User-friendly interface
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Usage

### Quick Start

Run the main script for an interactive experience:

```bash
python -m boulder_detection.main
```

### Programmatic Usage

```python
from boulder_detection import BoulderDetector

# Initialize detector
detector = BoulderDetector(
    yolo_model_path="path/to/best.pt",
    vit_model_path="path/to/vit_model.pth",
    scale=1.0  # meters per pixel
)

# Detect objects with ViT fallback
detected_objects = detector.detect_with_vit_fallback(
    image_path="path/to/image.jpg",
    confidence_threshold=0.6
)

# Calculate density analysis
density_analysis = detector.calculate_density_analysis(detected_objects, "path/to/image.jpg")

# Print summary
detector.print_detection_summary(detected_objects, density_analysis)

# Create visualization
visualization = detector.create_visualization("path/to/image.jpg", detected_objects)
```

### Advanced Usage

#### Depth Estimation

```python
# Detect with depth estimation
detected_objects = detector.detect_with_depth_estimation(
    image_path="path/to/image.jpg",
    solar_incidence_angle=45.0  # degrees
)
```

#### Grad-CAM Visualization

```python
from boulder_detection import GradCAMVisualizer

# Initialize visualizer
visualizer = GradCAMVisualizer(vit_model, yolo_model, device)

# Visualize ViT Grad-CAM
vit_cam = visualizer.visualize_vit_gradcam(
    image=image,
    class_id=0,
    normalization_params={'mean': [0.485, 0.456, 0.406], 'std': [0.229, 0.224, 0.225]}
)

# Visualize YOLO Grad-CAM
yolo_cam = visualizer.visualize_yolo_gradcam(image)
```

## Modules

### models.py
- `ModelLoader`: Handles loading and setup of YOLO and ViT models
- `YoloCAMWrapper`: Wrapper to make YOLO compatible with Grad-CAM

### transforms.py
- `DataTransforms`: Handles data preprocessing and transformations for both models

### measurements.py
- `PhysicalCalculator`: Calculates physical measurements and properties
- `ObjectMeasurements`: Data class to store object measurements

### gradcam.py
- `GradCAMVisualizer`: Handles Grad-CAM visualization for both models

### detector.py
- `BoulderDetector`: Main detector class with complete inference pipeline

### main.py
- Interactive command-line interface for the detection system

## Input Parameters

### Scale
- **Purpose**: Converts pixel measurements to real-world units
- **Format**: meters per pixel
- **Example**: `1.0` means 1 pixel = 1 meter

### Solar Incidence Angle
- **Purpose**: Used for crater depth estimation from shadows
- **Format**: degrees (0-90)
- **Example**: `45.0` degrees

### Confidence Threshold
- **Purpose**: Determines when to use ViT fallback
- **Format**: float (0-1)
- **Example**: `0.6` means use ViT for detections with confidence < 0.6

## Output

### Physical Measurements
- **Size/Diameter**: Measured using the provided scale
- **Area**: Calculated from bounding box dimensions
- **Volume**: Estimated based on object type (hemisphere for craters, sphere for boulders)
- **Circularity**: Ratio of minimum to maximum dimension
- **Elongation**: 1 - circularity
- **Depth**: Estimated from shadow length (craters only)

### Degradation State
- **Fresh**: Confidence ≥ 0.8
- **Moderately degraded**: 0.6 ≤ Confidence < 0.8
- **Highly degraded**: Confidence < 0.6

### Density Analysis
- **Crater density**: Craters per square meter
- **Boulder density**: Boulders per square meter

## Model Requirements

### YOLO Model
- **Format**: `.pt` file (PyTorch)
- **Classes**: Should detect 'crater' and 'boulder'
- **Input size**: 640x640 pixels

### ViT Model
- **Format**: `.pth` file (PyTorch state dict)
- **Architecture**: `vit_base_patch16_224`
- **Classes**: 2 classes (crater, rille)
- **Input size**: 224x224 pixels

## Troubleshooting

### Common Issues

1. **Model not found**: Ensure model paths are correct and files exist
2. **CUDA out of memory**: Reduce batch size or use CPU
3. **Grad-CAM errors**: Install `grad-cam` package: `pip install grad-cam`
4. **Import errors**: Ensure all dependencies are installed

### Performance Tips

1. **GPU acceleration**: Use CUDA-enabled PyTorch for faster inference
2. **Batch processing**: Process multiple images in batches
3. **Memory management**: Close unused models and clear GPU cache

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YOLOv8 by Ultralytics
- Vision Transformer by Google Research
- Grad-CAM by Ramprasaath R. Selvaraju et al. 