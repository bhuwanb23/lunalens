# 🌙 Lunar Analysis Main Processor

A comprehensive tool for lunar terrain analysis that combines all the functionality from the raw folder into a single, easy-to-use interface.

## 📋 Features

### 🔧 Core Capabilities
- **TIF File Processing**: Load and process lunar DEM (Digital Elevation Model) files
- **Boulder Detection**: Multiple detection methods (edge-based, watershed, morphological)
- **Slope Analysis**: Moon-specific slope calculations with configurable parameters
- **Aspect Analysis**: Calculate terrain aspect (direction of steepest slope)
- **Curvature Analysis**: Profile, plan, Gaussian, and mean curvature calculations
- **Elevation Statistics**: Basic elevation statistics (min, max, mean, std dev)
- **Interactive Mode**: User-friendly menu-driven interface

### 🎯 Analysis Methods
1. **Edge-based Boulder Detection**: Uses Canny edge detection and contour analysis
2. **Watershed Boulder Detection**: Uses distance transform and watershed segmentation
3. **Slope Calculation**: GDAL-based slope analysis with moon-specific parameters
4. **Aspect Calculation**: Terrain aspect analysis
5. **Curvature Analysis**: Multiple curvature types for terrain characterization

## 🚀 Quick Start

### 1. Configuration
Edit the `Config` class in `main_processor.py`:

```python
class Config:
    # QGIS Installation Path (change this to your QGIS installation)
    QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
    
    # Input/Output Paths (change these to your actual paths)
    INPUT_TIF_PATH = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    OUTPUT_FOLDER = r"E:\moon extract\data\derived\20250207\analysis_output"
```

### 2. Run the Processor

#### Option A: Run All Analyses at Once
```bash
python main_processor.py
```

#### Option B: Interactive Mode
```bash
python main_processor.py --interactive
```

## 📁 File Structure

```
detection_qgis/raw/
├── main_processor.py          # Main processor (this file)
├── tif_processor.py          # TIF file processing
├── boulder_detector.py       # Boulder detection algorithms
├── slope.py                  # Slope analysis
├── curvature_statistics.py   # Curvature calculations
├── elevation_statistics.py   # Elevation statistics
├── visualize_slope.py        # Slope visualization
├── example_usage.py          # Example usage
└── README_MAIN_PROCESSOR.md # This file
```

## ⚙️ Configuration Options

### QGIS Path
Set your QGIS installation path:
```python
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1"
```

### Input/Output Paths
Set your input TIF file and output folder:
```python
INPUT_TIF_PATH = r"path\to\your\lunar_dem.tif"
OUTPUT_FOLDER = r"path\to\your\output\folder"
```

### Boulder Detection Settings
```python
BOULDER_DETECTION_MIN_AREA = 100      # Minimum boulder area (pixels)
BOULDER_DETECTION_MAX_AREA = 10000    # Maximum boulder area (pixels)
BOULDER_DETECTION_MIN_DISTANCE = 20   # Minimum distance between boulders
```

### Slope Analysis Settings
```python
SLOPE_SCALE_FACTOR = 1.0    # Scale factor for slope calculation
SLOPE_AS_PERCENT = False     # Output as percentage (False = degrees)
```

## 📊 Output Files

The processor generates the following output files:

### TIF Files (Raster Analysis)
- `slope_analysis.tif`: Slope raster (degrees or percentage)
- `aspect_analysis.tif`: Aspect raster (degrees)

### JSON Files (Analysis Results)
- `boulder_detection.json`: Boulder detection results with coordinates and confidence
- `curvature_analysis.json`: Curvature statistics (profile, plan, Gaussian, mean)
- `elevation_statistics.json`: Basic elevation statistics

### Example Output Structure
```json
{
  "boulder_detection": [
    {
      "method": "edge",
      "bbox": [x1, y1, x2, y2],
      "area": 1500,
      "confidence": 0.75
    }
  ],
  "curvature_analysis": {
    "profile": {
      "mean": 0.001234,
      "std": 0.005678,
      "min": -0.012345,
      "max": 0.023456
    }
  },
  "elevation_statistics": {
    "min": 1234.56,
    "max": 5678.90,
    "mean": 3456.78,
    "range": 4444.34,
    "std": 1234.56
  }
}
```

## 🎮 Interactive Mode

When running in interactive mode (`--interactive`), you can:

1. **Load TIF file**: Load your lunar DEM file
2. **Calculate elevation statistics**: Get basic elevation stats
3. **Calculate slope**: Generate slope raster
4. **Calculate aspect**: Generate aspect raster
5. **Detect boulders**: Run boulder detection algorithms
6. **Calculate curvature**: Compute curvature statistics
7. **Run all analyses**: Execute all analyses in sequence
8. **List loaded layers**: Show currently loaded QGIS layers
9. **Show results summary**: Display analysis results summary

## 🔧 Troubleshooting

### QGIS Installation Issues
1. **Wrong QGIS path**: Update `QGIS_PREFIX_PATH` in the Config class
2. **Processing module not available**: Some functions will be limited
3. **QGIS not found**: Install QGIS or update the path

### File Path Issues
1. **Input TIF not found**: Check `INPUT_TIF_PATH` in Config
2. **Output folder not created**: The processor will create it automatically
3. **Permission errors**: Ensure write permissions for output folder

### Analysis Issues
1. **Large files**: The processor uses sampling for large files (configurable via `SAMPLE_SIZE_LIMIT`)
2. **Memory issues**: Reduce `SAMPLE_SIZE_LIMIT` for very large files
3. **Processing module errors**: Some analyses require the QGIS processing module

## 📈 Analysis Methods Explained

### Boulder Detection
- **Edge-based**: Uses Canny edge detection to find boulder boundaries
- **Watershed**: Uses distance transform and watershed segmentation
- **Combination**: Combines both methods and removes duplicates

### Slope Analysis
- Uses GDAL slope algorithm
- Configurable scale factor for moon-specific parameters
- Output in degrees or percentage

### Curvature Analysis
- **Profile curvature**: Curvature in the direction of steepest slope
- **Plan curvature**: Curvature perpendicular to slope direction
- **Gaussian curvature**: Product of principal curvatures
- **Mean curvature**: Average of principal curvatures

### Elevation Statistics
- Basic statistical measures (min, max, mean, std dev)
- Useful for terrain characterization
- Helps identify craters, ridges, and other features

## 🚀 Advanced Usage

### Custom Analysis Pipeline
```python
# Initialize processor
processor = LunarAnalysisProcessor()

# Load TIF file
processor.load_tif_file()

# Run specific analyses
processor.calculate_elevation_statistics()
processor.calculate_slope()
processor.detect_boulders()

# Get results
processor.print_results_summary()
```

### Batch Processing
You can modify the main function to process multiple files:

```python
def batch_process(input_files):
    for tif_file in input_files:
        Config.INPUT_TIF_PATH = tif_file
        Config.OUTPUT_FOLDER = f"output_{os.path.basename(tif_file)}"
        
        processor = LunarAnalysisProcessor()
        processor.validate_paths()
        processor.load_tif_file()
        processor.calculate_elevation_statistics()
        processor.calculate_slope()
        processor.detect_boulders()
        processor.cleanup()
```

## 📝 Requirements

### Python Dependencies
- `numpy`: Numerical computations
- `opencv-python`: Image processing (boulder detection)
- `scikit-image`: Image analysis
- `scipy`: Scientific computing
- `rasterio`: Geospatial raster I/O
- `qgis`: QGIS Python bindings

### System Requirements
- QGIS 3.x installed
- Python 3.7+
- Sufficient RAM for large raster files
- Write permissions for output folder

## 🤝 Contributing

To add new analysis methods:

1. Add the method to the `LunarAnalysisProcessor` class
2. Update the interactive menu if needed
3. Add configuration options to the `Config` class
4. Update this README with the new functionality

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all paths are correctly set
3. Ensure QGIS is properly installed
4. Check file permissions for output folder

---

**🌙 Happy Lunar Analysis!** 🚀 