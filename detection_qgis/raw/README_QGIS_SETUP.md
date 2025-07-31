# 🌙 QGIS Lunar Analysis Setup Guide

This guide explains how to properly set up and run the QGIS-based lunar analysis tools.

## 🔧 QGIS Installation Requirements

### Required QGIS Version
- **QGIS 3.40.9** (Long Term Release)
- Installation path: `C:\Program Files\QGIS 3.40.9`

### QGIS Components Needed
- QGIS Desktop application
- Python 3.9 (included with QGIS)
- Processing framework
- GDAL/OGR libraries

## 🚀 Running the Lunar Analysis Tools

### Method 1: Using QGIS Batch File (Recommended)

1. **Navigate to the raw folder**:
   ```cmd
   cd detection_qgis\raw
   ```

2. **Run the main processor**:
   ```cmd
   run_with_qgis_batch.bat
   ```

3. **For interactive mode**:
   ```cmd
   run_with_qgis_batch.bat --interactive
   ```

### Method 2: Using Direct Python Environment

1. **Test QGIS setup first**:
   ```cmd
   python test_qgis_setup.py
   ```

2. **If test passes, run the main processor**:
   ```cmd
   python main_processor.py
   ```

3. **For interactive mode**:
   ```cmd
   python main_processor.py --interactive
   ```

## 📁 File Structure

```
detection_qgis/raw/
├── main_processor.py              # Main analysis processor
├── test_qgis_setup.py            # QGIS setup test
├── run_main_processor.bat        # Batch file (Method 1)
├── run_with_qgis_batch.bat       # QGIS batch method (Method 2)
├── qgis_setup.py                 # QGIS setup module
├── tif_processor.py              # TIF file processing
├── slope.py                      # Slope analysis
├── boulder_detector.py           # Boulder detection
├── curvature_statistics.py       # Curvature analysis
├── elevation_statistics.py       # Elevation statistics
├── README_QGIS_SETUP.md         # This file
└── README_MAIN_PROCESSOR.md     # Main processor documentation
```

## ⚙️ Configuration

### 1. Update Paths in main_processor.py

Edit the `Config` class in `main_processor.py`:

```python
class Config:
    # QGIS Installation Path
    QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
    
    # Input/Output Paths (change these to your actual paths)
    INPUT_TIF_PATH = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    OUTPUT_FOLDER = r"E:\moon extract\data\derived\20250207\analysis_output"
```

### 2. Verify QGIS Installation

Check that these paths exist:
- `C:\Program Files\QGIS 3.40.9\apps\qgis\bin`
- `C:\Program Files\QGIS 3.40.9\apps\Python39`
- `C:\Program Files\QGIS 3.40.9\bin\python-qgis-ltr.bat`

## 🔍 Troubleshooting

### Issue: "No module named 'qgis'"

**Solution**: Use the QGIS batch file method:
```cmd
run_with_qgis_batch.bat
```

### Issue: "QGIS setup failed"

**Solutions**:
1. **Verify QGIS installation**:
   ```cmd
   python test_qgis_setup.py
   ```

2. **Check QGIS version**:
   - Ensure QGIS 3.40.9 is installed
   - Update path in `main_processor.py` if different version

3. **Use QGIS batch file**:
   ```cmd
   run_with_qgis_batch.bat
   ```

### Issue: "Processing module not available"

**Solutions**:
1. **Install QGIS with processing framework**
2. **Use alternative methods** (the processor will automatically fall back)

### Issue: "Input TIF file not found"

**Solution**: Update the `INPUT_TIF_PATH` in `main_processor.py`:
```python
INPUT_TIF_PATH = r"path\to\your\actual\file.tif"
```

## 📊 Available Analysis Methods

### 1. TIF File Processing
- Load lunar DEM files
- Validate file format and metadata
- Display raster information

### 2. Boulder Detection
- **Edge-based detection**: Uses Canny edge detection
- **Watershed detection**: Uses distance transform and watershed
- **Combination**: Merges both methods and removes duplicates

### 3. Slope Analysis
- GDAL-based slope calculation
- Moon-specific parameters
- Output in degrees or percentage

### 4. Aspect Analysis
- Terrain aspect calculation
- Direction of steepest slope
- Useful for solar illumination analysis

### 5. Curvature Analysis
- **Profile curvature**: Along steepest slope direction
- **Plan curvature**: Perpendicular to slope direction
- **Gaussian curvature**: Product of principal curvatures
- **Mean curvature**: Average of principal curvatures

### 6. Elevation Statistics
- Basic statistical measures
- Min, max, mean, standard deviation
- Elevation range analysis

## 🎮 Interactive Mode Features

When running in interactive mode (`--interactive`):

1. **Load TIF file**: Load your lunar DEM
2. **Calculate elevation statistics**: Get basic stats
3. **Calculate slope**: Generate slope raster
4. **Calculate aspect**: Generate aspect raster
5. **Detect boulders**: Run boulder detection
6. **Calculate curvature**: Compute curvature statistics
7. **Run all analyses**: Execute all analyses
8. **List loaded layers**: Show QGIS layers
9. **Show results summary**: Display analysis results

## 📁 Output Files

### Raster Files (TIF)
- `slope_analysis.tif`: Slope raster
- `aspect_analysis.tif`: Aspect raster

### JSON Results
- `boulder_detection.json`: Boulder coordinates and confidence
- `curvature_analysis.json`: Curvature statistics
- `elevation_statistics.json`: Basic elevation stats

### Text Files
- `slope_analysis_slope_stats.txt`: Slope statistics
- Processing logs and error reports

## 🚀 Quick Start Commands

### Test Setup
```cmd
python test_qgis_setup.py
```

### Run All Analyses
```cmd
run_with_qgis_batch.bat
```

### Interactive Mode
```cmd
run_with_qgis_batch.bat --interactive
```

### Individual Scripts
```cmd
# TIF Processing
python tif_processor.py

# Slope Analysis
python slope.py

# Boulder Detection
python boulder_detector.py

# Curvature Analysis
python curvature_statistics.py

# Elevation Statistics
python elevation_statistics.py
```

## 📝 Requirements

### System Requirements
- Windows 10/11
- QGIS 3.40.9 installed
- Python 3.9 (included with QGIS)
- Sufficient RAM for large raster files
- Write permissions for output folder

### Python Dependencies (included with QGIS)
- `numpy`: Numerical computations
- `opencv-python`: Image processing
- `scikit-image`: Image analysis
- `scipy`: Scientific computing
- `rasterio`: Geospatial raster I/O
- `qgis`: QGIS Python bindings

## 🔧 Advanced Configuration

### Custom QGIS Path
If QGIS is installed in a different location:

1. **Update main_processor.py**:
   ```python
   QGIS_PREFIX_PATH = r"your\qgis\path"
   ```

2. **Update batch files**:
   ```batch
   set QGIS_PREFIX_PATH=your\qgis\path
   ```

### Custom Analysis Parameters
Edit the `Config` class in `main_processor.py`:

```python
# Boulder Detection Settings
BOULDER_DETECTION_MIN_AREA = 100
BOULDER_DETECTION_MAX_AREA = 10000
BOULDER_DETECTION_MIN_DISTANCE = 20

# Slope Analysis Settings
SLOPE_SCALE_FACTOR = 1.0
SLOPE_AS_PERCENT = False

# Processing Settings
SAMPLE_SIZE_LIMIT = 1000  # For large files
```

## 📞 Support

### Common Issues
1. **QGIS not found**: Check installation path
2. **Processing module missing**: Install QGIS with processing framework
3. **Memory errors**: Reduce `SAMPLE_SIZE_LIMIT` for large files
4. **Permission errors**: Check write permissions for output folder

### Getting Help
1. Run `test_qgis_setup.py` to diagnose issues
2. Check error messages for specific problems
3. Verify all paths are correct
4. Ensure QGIS 3.40.9 is properly installed

---

**🌙 Happy Lunar Analysis!** 🚀 