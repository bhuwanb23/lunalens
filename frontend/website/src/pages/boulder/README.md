# Boulder Detection Page

## Overview
The Boulder Detection page provides a comprehensive AI-powered interface for detecting and analyzing lunar boulders and craters. Based on the backend boulder detection system, this page offers multiple analysis types with advanced features.

## Features

### Image Upload System
- Drag-and-drop image upload interface
- Support for various image formats (JPG, PNG, TIFF)
- Real-time image preview
- Upload validation and error handling

### Analysis Types

#### 1. Basic Detection
- **Description**: Standard YOLO-based boulder and crater detection
- **Features**: Object detection, size measurement, density analysis
- **Processing Time**: 1-2 seconds
- **Accuracy**: 85-90%
- **Requirements**: YOLO Model, Image Input

#### 2. Advanced Analysis
- **Description**: Dual-model detection using YOLO and Vision Transformer
- **Features**: ViT fallback, high accuracy, confidence validation
- **Processing Time**: 2-3 seconds
- **Accuracy**: 92-95%
- **Requirements**: YOLO Model, ViT Model, Image Input

#### 3. Depth Estimation
- **Description**: Crater depth estimation using shadow analysis
- **Features**: Shadow analysis, depth calculation, solar angle
- **Processing Time**: 3-4 seconds
- **Accuracy**: 88-92%
- **Requirements**: YOLO Model, Solar Angle, Image Input

#### 4. Grad-CAM Visualization
- **Description**: Model interpretability with attention maps
- **Features**: Attention maps, model interpretability, visualization
- **Processing Time**: 4-5 seconds
- **Accuracy**: 90-94%
- **Requirements**: YOLO Model, ViT Model, Grad-CAM

### Results Display
- **Objects Detected**: Boulders and craters count
- **Analysis Metrics**: Density, average size, confidence
- **Processing Info**: Time, status, completion
- **Export Options**: Download results and visualizations

## Components

### Main Boulder Component (`boulder.jsx`)
- Handles state management for analysis selection
- Manages image upload and preview
- Provides analysis results display
- Navigation functionality

### Styling (`boulder.css`)
- Custom animations and effects
- Orange/red theme consistent with boulder detection
- Responsive design rules
- Accessibility features

### Constants (`constants/index.js`)
- Analysis types configuration
- Detection features and capabilities
- Model information and parameters
- Navigation items

## Usage

1. **Upload Image**: Drag and drop or click to upload a lunar surface image
2. **Select Analysis**: Choose from four analysis types based on requirements
3. **Start Analysis**: Initiate the detection process
4. **View Results**: Examine detailed analysis results and metrics
5. **Export**: Download results and visualizations

## Navigation

- **Dashboard**: Returns to main dashboard
- **Analytics**: Navigate to analytics page
- **Boulder Detection**: Current page (active)
- **Settings**: Future feature

## Technical Details

### State Management
- `selectedAnalysis`: Tracks which analysis type is selected
- `showConfirmation`: Controls confirmation section visibility
- `uploadedImage`: Stores uploaded image data
- `analysisResults`: Contains analysis results and metrics

### Routing
- Protected route requiring authentication
- Redirects to login if not authenticated
- Integrates with main app routing

### Styling
- Tailwind CSS for layout and basic styling
- Custom CSS for animations and effects
- Orange/red color scheme for boulder theme
- Responsive design with mobile breakpoints

## Backend Integration

### Models Used
- **YOLO Model** (`best.pt`): 6.0MB, 85-90% accuracy
- **Vision Transformer** (`vit_model.pth`): 327MB, 92-95% accuracy

### Detection Capabilities
- **Physical Measurements**: Size, diameter, area, volume, circularity, elongation
- **Depth Estimation**: Crater depth using shadow analysis
- **Density Analysis**: Objects per unit area
- **Degradation Assessment**: Crater freshness based on confidence

### Parameters
- **Scale**: Meters per pixel (default: 1.0)
- **Confidence Threshold**: ViT fallback threshold (default: 0.6)
- **Solar Incidence Angle**: For depth estimation (default: 45°)

## Future Enhancements

- Real-time analysis progress indicators
- Batch processing for multiple images
- Advanced filtering and sorting options
- Historical analysis data storage
- Integration with lunar mapping systems
- 3D visualization capabilities
- Export to various formats (CSV, JSON, PDF)
- API integration for external data sources 