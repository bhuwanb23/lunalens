import sys
import os

# ✅ 1. QGIS installation path (corrected)
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"

# ✅ 2. Set required environment variables
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "apps", "Qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "apps")

# ✅ 3. Add QGIS Python path to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# Add QGIS Python libraries
QGIS_PYTHON_LIB = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312", "Lib", "site-packages")
if QGIS_PYTHON_LIB not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_LIB)

# ✅ 4. Initialize QGIS Application BEFORE importing QGIS modules
from qgis.core import QgsApplication
qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs.initQgis()

# ✅ 5. Now import other QGIS modules
from qgis.core import (
    QgsRasterLayer,
    QgsProject,
    QgsProcessingFeedback
)
# import processing  # Uncomment when needed for processing algorithms

# ✅ 6. Register native QGIS algorithms (e.g., slope, buffer)
from qgis.analysis import QgsNativeAlgorithms
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

print("✅ QGIS setup completed successfully!")
print(f"QGIS Prefix Path: {QGIS_PREFIX_PATH}")
print(f"Python Path: {sys.executable}")
print(f"QGIS Python Path: {QGIS_PYTHON_PATH}")

# ✅ 7. Load a raster layer (example: DTM)
# Uncomment and modify the path below to use your actual DTM file
# dtm_path = "C:/your_path/dtm.tif"
# raster = QgsRasterLayer(dtm_path, "DTM")

# if not raster.isValid():
#     print("Failed to load raster.")
# else:
#     print("Raster loaded successfully.")

# ✅ 8. Use a processing algorithm: generate slope from DTM
# Uncomment and modify the paths below to use your actual files
# slope_output = "C:/your_path/slope_output.tif"
# feedback = QgsProcessingFeedback()

# processing.run("gdal:slope", {
#     'INPUT': dtm_path,
#     'SCALE': 1,
#     'AS_PERCENT': False,
#     'COMPUTE_EDGES': True,
#     'ZEVENBERGEN': False,
#     'OUTPUT': slope_output
# }, feedback=feedback)

# print("Slope raster saved to:", slope_output)

# ✅ 9. Cleanup QGIS
qgs.exitQgis()
