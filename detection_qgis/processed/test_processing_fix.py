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

# Set QT_PLUGIN_PATH - this is crucial for PyQt5 DLL loading
os.environ["QT_PLUGIN_PATH"] = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\qtplugins;{OSGEO4W_ROOT}\\apps\\qt5\\plugins"

# Set PYTHONPATH to include QGIS Python modules
os.environ["PYTHONPATH"] = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\python;{os.environ.get('PYTHONPATH', '')}"

# Add QGIS bin directory to PATH - this must be at the beginning for DLL loading
qgis_bin_path = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\bin"
current_path = os.environ.get('PATH', '')
if qgis_bin_path not in current_path:
    os.environ["PATH"] = f"{qgis_bin_path};{current_path}"

# Add QGIS Python paths to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312")
QGIS_QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python")
PROCESSING_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python", "plugins")

# Add paths in the correct order
paths_to_add = [
    QGIS_PYTHON_PATH,
    QGIS_QGIS_PYTHON_PATH,
    PROCESSING_PATH
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

print("🔧 Testing Processing Module Import...")
print(f"QGIS_PREFIX_PATH: {QGIS_PREFIX_PATH}")
print(f"QGIS_PYTHON_PATH: {QGIS_PYTHON_PATH}")
print(f"QGIS_QGIS_PYTHON_PATH: {QGIS_QGIS_PYTHON_PATH}")
print(f"PROCESSING_PATH: {PROCESSING_PATH}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"QT_PLUGIN_PATH: {os.environ.get('QT_PLUGIN_PATH', 'Not set')}")
print(f"PATH starts with: {os.environ.get('PATH', 'Not set')[:200]}...")

# Test if we can import PyQt5 first
try:
    import PyQt5
    print("✅ PyQt5 imported successfully!")
except ImportError as e:
    print(f"❌ PyQt5 import failed: {e}")

# Initialize QGIS
try:
    from qgis.core import QgsApplication
    print("✅ QGIS core imported successfully!")
    
    # Check if QGIS is already initialized
    if QgsApplication.instance():
        print("✅ QGIS already initialized")
    else:
        qgs = QgsApplication([], False)
        qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
        qgs.initQgis()
        print("✅ QGIS initialized successfully!")
        
except ImportError as e:
    print(f"❌ QGIS core import failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ QGIS initialization failed: {e}")
    sys.exit(1)

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