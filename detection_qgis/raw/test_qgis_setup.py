"""
Test script to verify QGIS setup
"""

import sys
import os

def test_qgis_import():
    """Test if QGIS can be imported"""
    print("🔧 Testing QGIS Setup...")
    
    # Set QGIS environment variables
    QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
    
    os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "apps", "Qt5", "plugins")
    os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "bin")
    os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "apps", "Python39")
    os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "apps", "Python39", "Scripts")
    os.environ["GDAL_DATA"] = os.path.join(QGIS_PREFIX_PATH, "share", "gdal")
    os.environ["PROJ_LIB"] = os.path.join(QGIS_PREFIX_PATH, "share", "proj")
    
    # Add QGIS Python paths
    qgis_python_path = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python")
    qgis_python39_path = os.path.join(QGIS_PREFIX_PATH, "apps", "Python39", "Lib", "site-packages")
    
    if qgis_python_path not in sys.path:
        sys.path.insert(0, qgis_python_path)
    if qgis_python39_path not in sys.path:
        sys.path.insert(0, qgis_python39_path)
    
    print(f"✅ Environment variables set")
    print(f"   - QGIS Prefix: {QGIS_PREFIX_PATH}")
    print(f"   - Python Path: {qgis_python_path}")
    print(f"   - Site Packages: {qgis_python39_path}")
    
    try:
        print("🔄 Testing QGIS import...")
        from qgis.core import QgsApplication
        print("✅ QgsApplication imported successfully")
        
        print("🔄 Testing QGIS initialization...")
        qgs = QgsApplication([], False)
        qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
        qgs.initQgis()
        print("✅ QGIS initialized successfully")
        
        print("🔄 Testing QGIS modules...")
        from qgis.core import QgsRasterLayer, QgsProject
        from qgis.analysis import QgsNativeAlgorithms
        print("✅ QGIS modules imported successfully")
        
        print("🔄 Testing processing module...")
        try:
            import processing
            print("✅ Processing module available")
        except ImportError:
            print("⚠️ Processing module not available")
        
        print("🔄 Testing cleanup...")
        qgs.exitQgis()
        print("✅ QGIS cleanup successful")
        
        print("\n🎉 QGIS setup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ QGIS setup test failed: {e}")
        print(f"   - Error type: {type(e).__name__}")
        print(f"   - Error details: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_qgis_import()
    if success:
        print("\n✅ QGIS is properly configured!")
        print("   You can now run the main processor.")
    else:
        print("\n❌ QGIS setup failed!")
        print("   Please check your QGIS installation.")
    
    input("\nPress Enter to exit...") 