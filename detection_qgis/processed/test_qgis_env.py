import sys
import os

# Set up QGIS environment variables
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["GDAL_FILENAME_IS_UTF8"] = "YES"
os.environ["VSI_CACHE"] = "TRUE"
os.environ["VSI_CACHE_SIZE"] = "1000000"

# Set up paths
OSGEO4W_ROOT = QGIS_PREFIX_PATH
os.environ["QT_PLUGIN_PATH"] = f"{OSGEO4W_ROOT}\\apps\\qgis-ltr\\qtplugins;{OSGEO4W_ROOT}\\apps\\qt5\\plugins"

# Add to PATH
qgis_bin = os.path.join(OSGEO4W_ROOT, "apps", "qgis-ltr", "bin")
if qgis_bin not in os.environ["PATH"]:
    os.environ["PATH"] = qgis_bin + ";" + os.environ["PATH"]

# Add Python paths
qgis_python = os.path.join(OSGEO4W_ROOT, "apps", "qgis-ltr", "python")
if qgis_python not in sys.path:
    sys.path.insert(0, qgis_python)

# Add processing module path
processing_path = os.path.join(OSGEO4W_ROOT, "apps", "qgis-ltr", "python", "plugins")
if processing_path not in sys.path:
    sys.path.insert(0, processing_path)

print("🔍 Testing QGIS Environment Setup...")
print("=" * 50)
print(f"QGIS_PREFIX_PATH: {os.environ.get('QGIS_PREFIX_PATH')}")
print(f"QT_PLUGIN_PATH: {os.environ.get('QT_PLUGIN_PATH')}")
print(f"Python paths: {sys.path[:5]}")  # Show first 5 paths

# Try to import QGIS
try:
    from qgis.core import QgsApplication
    print("✅ QGIS core imported successfully")
    
    # Initialize QGIS
    try:
        QgsApplication.instance()
        print("✅ QGIS already initialized")
    except:
        qgs = QgsApplication([], False)
        qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
        qgs.initQgis()
        print("✅ QGIS initialized")
    
    # Try to import processing
    try:
        import processing
        print("✅ Processing module imported successfully")
        PROCESSING_AVAILABLE = True
    except ImportError as e:
        print(f"❌ Processing import failed: {e}")
        PROCESSING_AVAILABLE = False
    
    # Test processing algorithms
    if PROCESSING_AVAILABLE:
        print("\n🔍 Testing Processing Algorithms...")
        print("=" * 50)
        
        # Register native algorithms
        from qgis.analysis import QgsNativeAlgorithms
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
        print("✅ Native algorithms registered")
        
        # Register GDAL algorithms
        try:
            from processing.core.Processing import Processing
            Processing.initialize()
            print("✅ GDAL algorithms registered")
        except Exception as e:
            print(f"⚠️  GDAL algorithms registration failed: {e}")
        
        # Test algorithm availability
        try:
            algorithms = processing.algorithmHelp("gdal:slope")
            print("✅ GDAL slope algorithm available")
        except Exception as e:
            print(f"❌ GDAL slope algorithm not available: {e}")
        
        try:
            algorithms = processing.algorithmHelp("native:slope")
            print("✅ Native slope algorithm available")
        except Exception as e:
            print(f"❌ Native slope algorithm not available: {e}")
    
    print("\n✅ QGIS environment setup completed successfully!")
    
except Exception as e:
    print(f"❌ QGIS setup failed: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc() 