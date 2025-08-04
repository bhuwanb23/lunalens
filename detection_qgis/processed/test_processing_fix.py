import sys
import os

# QGIS installation path
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
OSGEO4W_ROOT = QGIS_PREFIX_PATH

# Set required environment variables based on QGIS batch file
os.environ["QGIS_PREFIX_PATH"] = f"{OSGEO4W_ROOT.replace('\\', '/')}/apps/qgis-ltr"
os.environ["GDAL_FILENAME_IS_UTF8"] = "YES"
os.environ["VSI_CACHE"] = "TRUE"
os.environ["VSI_CACHE_SIZE"] = "1000000"
os.environ["QT_PLUGIN_PATH"] = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\qtplugins;{OSGEO4W_ROOT}\\apps\\qt5\\plugins"
os.environ["PYTHONPATH"] = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\python;{os.environ.get('PYTHONPATH', '')}"

# Add to PATH
os.environ["PATH"] = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\bin;{os.environ.get('PATH', '')}"

# Add QGIS Python paths
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312")
QGIS_QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python")
PROCESSING_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python", "plugins")

if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)
if QGIS_QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_QGIS_PYTHON_PATH)
if PROCESSING_PATH not in sys.path:
    sys.path.insert(0, PROCESSING_PATH)

print("🔧 Testing Processing Module Import...")
print(f"QGIS_PREFIX_PATH: {QGIS_PREFIX_PATH}")
print(f"QGIS_PYTHON_PATH: {QGIS_PYTHON_PATH}")
print(f"QGIS_QGIS_PYTHON_PATH: {QGIS_QGIS_PYTHON_PATH}")
print(f"PROCESSING_PATH: {PROCESSING_PATH}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"PATH: {os.environ.get('PATH', 'Not set')[:200]}...")

# Initialize QGIS
from qgis.core import QgsApplication
try:
    QgsApplication.instance()
    print("✅ QGIS already initialized")
except:
    qgs = QgsApplication([], False)
    qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
    qgs.initQgis()
    print("✅ QGIS initialized")

# Test processing import
try:
    import processing
    print("✅ Processing module imported successfully!")
    
    # Test if processing algorithms are available
    from qgis.analysis import QgsNativeAlgorithms
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    
    # Try to access a simple algorithm
    algorithms = processing.algorithmHelp("gdal:slope")
    print("✅ Processing algorithms are available!")
    print("✅ Processing module is working correctly!")
    
except ImportError as e:
    print(f"❌ Processing module import failed: {e}")
except Exception as e:
    print(f"❌ Processing module test failed: {e}")

print("✅ Test completed!") 