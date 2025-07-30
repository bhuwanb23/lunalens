# Lunar DEM Terrain Analysis Toolkit: Elevation & Curvature

This toolkit provides scripts for computing and analyzing elevation and curvature statistics from lunar (moon) TIF raster data using QGIS and Python. It is designed for scientific analysis, landing site assessment, and general geospatial research on lunar DEMs (Digital Elevation Models).

---

## Contents
- `elevation_statistics.py` — Compute and print elevation statistics from a lunar TIF file
- `curvature_statistics.py` — Compute and print various curvature statistics from a lunar TIF file

---

## Requirements
- **QGIS 3.x** (Tested with QGIS 3.44.1)
- **Python** (Use the QGIS Python interpreter: `python-qgis.bat`)
- **Python packages:**
  - `numpy`

---

## 1. Elevation Statistics (`elevation_statistics.py`)

### **What it does:**
- Loads a lunar TIF DEM file
- Computes and prints:
  1. **Elevation (Z value):** The vertical height above the lunar reference datum
  2. **Minimum Elevation:** Lowest value (craters, basins)
  3. **Maximum Elevation:** Highest value (ridges, peaks)
  4. **Mean Elevation:** Average (regional profiling)
  5. **Elevation Range:** Max - Min (terrain variability)
  6. **Standard Deviation:** How varied the terrain is (ruggedness)

### **How to use:**
1. **Edit the TIF path** at the top of `elevation_statistics.py` to point to your TIF file.
2. **Run the script using the QGIS Python interpreter:**
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\elevation_statistics.py"
   ```
3. **Outputs:**
   - Prints elevation statistics to the terminal

---

## 2. Curvature Statistics (`curvature_statistics.py`)

### **What it does:**
- Loads a lunar TIF DEM file
- Computes and prints the following curvature statistics using numpy:
  1. **Profile Curvature:** In the direction of steepest slope (affects flow acceleration/deceleration)
  2. **Plan Curvature:** Perpendicular to slope (controls flow divergence/convergence)
  3. **General (Gaussian) Curvature:** Overall convexity/concavity
  4. **Tangential Curvature:** Combination of plan/profile (compound terrain)
  5. **Mean Curvature:** Average of principal curvatures (advanced geomorphology)
- Prints the mean and standard deviation for each, with clear explanations

### **How to use:**
1. **Edit the TIF path** at the top of `curvature_statistics.py` to point to your TIF file.
2. **Run the script using the QGIS Python interpreter:**
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\curvature_statistics.py"
   ```
3. **Outputs:**
   - Prints curvature statistics to the terminal

---

## **Workflow Example**
1. Compute elevation statistics:
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\elevation_statistics.py"
   ```
2. Compute curvature statistics:
   ```powershell
   & "C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" "e:\landslide\curvature_statistics.py"
   ```

---

## **Notes**
- Always use the QGIS Python interpreter to ensure all QGIS modules are available.
- The scripts are robust: if the raster block size is unexpected, they will print diagnostics and use a fallback zero-padded array.
- For large TIF files, the scripts automatically use manageable sample sizes for analysis.
- You can further customize the scripts for other planetary bodies or DEMs by adjusting parameters.

---

## **Contact & Support**
For questions, improvements, or bug reports, please open an issue or contact the maintainer.