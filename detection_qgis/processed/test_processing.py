import sys
import os

# QGIS setup
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")

# Add QGIS Python path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# Add QGIS Python path
QGIS_QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python")
if QGIS_QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_QGIS_PYTHON_PATH)

# Add processing module path
PROCESSING_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python", "plugins")
if PROCESSING_PATH not in sys.path:
    sys.path.insert(0, PROCESSING_PATH)

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

# Try to import processing
print("\n🔍 Testing Processing Module Import...")
print("=" * 50)

try:
    import processing
    print("✅ Processing module imported successfully")
    PROCESSING_AVAILABLE = True
except ImportError as e:
    print(f"❌ First import attempt failed: {e}")
    try:
        # Try alternative import path
        sys.path.append(os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python", "plugins", "processing"))
        import processing
        print("✅ Processing module imported (alternative path)")
        PROCESSING_AVAILABLE = True
    except ImportError as e:
        print(f"❌ Second import attempt failed: {e}")
        try:
            # Try another alternative path
            processing_path = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python", "plugins")
            if processing_path not in sys.path:
                sys.path.insert(0, processing_path)
            import processing
            print("✅ Processing module imported (third path)")
            PROCESSING_AVAILABLE = True
        except ImportError as e:
            print(f"❌ Third import attempt failed: {e}")
            PROCESSING_AVAILABLE = False

# Test processing algorithms
if PROCESSING_AVAILABLE:
    print("\n🔍 Testing Processing Algorithms...")
    print("=" * 50)
    
    # Register native algorithms
    from qgis.analysis import QgsNativeAlgorithms
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    
    # Register GDAL algorithms
    try:
        from processing.core.Processing import Processing
        Processing.initialize()
        print("✅ GDAL algorithms registered")
    except Exception as e:
        print(f"⚠️  GDAL algorithms registration failed: {e}")
    
    # List available algorithms
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

print("\n📋 Summary:")
print("=" * 50)
print(f"Processing Available: {PROCESSING_AVAILABLE}")
print(f"QGIS Prefix Path: {QGIS_PREFIX_PATH}")
print(f"Python Path: {QGIS_PYTHON_PATH}")
print(f"Processing Path: {PROCESSING_PATH}")
print(f"All Python Paths: {sys.path}") 