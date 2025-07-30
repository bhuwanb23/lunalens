# Moon Slope Analysis Toolkit

This toolkit provides scripts for calculating and visualizing terrain slope from lunar (moon) TIF raster data using QGIS and Python. It is designed for scientific analysis, landing site assessment, and general geospatial research on lunar DEMs (Digital Elevation Models).

---

## Contents
- `slope.py` — Calculate slope from a moon TIF file using QGIS or numpy
- `visualize_slope.py` — Visualize the calculated slope and compare with elevation

---

## Requirements
- **QGIS 3.x** (Tested with QGIS 3.44.1)
- **Python** (Use the QGIS Python interpreter: `python-qgis.bat`)
- **Python packages:**
  - `numpy`
  - `matplotlib`

---

## 1. Slope Calculation (`slope.py`)

### **What it does:**
- Loads a lunar TIF DEM file
- Calculates the slope using one of three methods:
  1. QGIS Processing (GDAL Slope)
  2. Manual numpy gradient calculation
  3. Simple statistical estimation (fallback)
- Saves the slope data as a `.npy` file and outputs statistics

### **How to use:**
1. **Edit the paths** at the top of `slope.py` to point to your TIF file and desired output location.
2. **Run the script using the QGIS Python interpreter:**
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\slope.py"
   ```
3. **Outputs:**
   - Slope data as `.npy` file (e.g., `moon_slope.npy`)
   - Slope statistics as `.txt` file
   - (If QGIS processing is available) Slope raster as `.tif`

---

## 2. Slope Visualization (`visualize_slope.py`)

### **What it does:**
- Loads the original TIF DEM and the calculated slope data (`.npy`)
- Visualizes:
  - The original elevation
  - The slope map (color-coded)
  - Landing suitability categories (gentle, moderate, steep, very steep)
  - Slope statistics and landing analysis
- Saves the visualization as a `.png` image and displays it

### **How to use:**
1. **Edit the paths** at the top of `visualize_slope.py` to match your data locations.
2. **Run the script using the QGIS Python interpreter:**
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\visualize_slope.py"
   ```
3. **Outputs:**
   - Visualization image as `.png` (e.g., `moon_slope_visualization.png`)
   - Slope data and statistics (from previous step)

---

## **Workflow Example**
1. Calculate slope:
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\slope.py"
   ```
2. Visualize results:
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\visualize_slope.py"
   ```

---

## **Notes**
- Always use the QGIS Python interpreter to ensure all QGIS modules are available.
- The scripts are robust: if QGIS processing is not available, they fall back to numpy-based or statistical methods.
- For large TIF files, the scripts automatically use manageable sample sizes for visualization.
- You can further customize the scripts for other planetary bodies or DEMs by adjusting parameters.

---

## **Contact & Support**
For questions, improvements, or bug reports, please open an issue or contact the maintainer.