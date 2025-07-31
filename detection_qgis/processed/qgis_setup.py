import sys
import os

class QGISSetup:
    def __init__(self, qgis_prefix_path=None):
        """
        Initialize QGIS setup
        
        Args:
            qgis_prefix_path (str): Path to QGIS installation. 
                                   Default: "C:\\Program Files\\QGIS 3.40.9"
        """
        # Try different common QGIS installation paths
        if qgis_prefix_path is None:
            possible_paths = [
                r"C:\Program Files\QGIS 3.40.9",
                r"C:\Program Files\QGIS 3.34.0", 
                r"C:\Program Files\QGIS 3.32.0",
                r"C:\Program Files\QGIS 3.30.0",
                r"C:\Program Files\QGIS 3.28.0",
                r"C:\Program Files\QGIS 3.26.0",
                r"C:\OSGeo4W64\apps\qgis",
                r"C:\OSGeo4W\apps\qgis",
                r"C:\Program Files (x86)\QGIS 3.40.9",
                r"C:\Program Files (x86)\QGIS 3.34.0",
                r"C:\Program Files (x86)\QGIS 3.32.0",
                r"C:\Program Files (x86)\QGIS 3.30.0"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    qgis_prefix_path = path
                    break
            else:
                print("❌ QGIS installation not found in common locations.")
                print("Please specify the correct QGIS installation path.")
                print("Common locations to check:")
                for path in possible_paths:
                    print(f"  - {path}")
                raise FileNotFoundError("QGIS installation not found")
        
        self.qgis_prefix_path = qgis_prefix_path
        self.qgs_app = None
        self._setup_environment()
        self._initialize_qgis()
    
    def _setup_environment(self):
        """Set up environment variables for QGIS"""
        # Set QGIS prefix path
        os.environ["QGIS_PREFIX_PATH"] = self.qgis_prefix_path
        
        # For QGIS 3.40.9, the structure is different
        # Check if this is QGIS 3.40.9 structure
        qgis_ltr_path = os.path.join(self.qgis_prefix_path, "apps", "qgis-ltr")
        python312_path = os.path.join(self.qgis_prefix_path, "apps", "Python312")
        
        if os.path.exists(qgis_ltr_path):
            # QGIS 3.40.9 structure
            print(f"📁 Using QGIS 3.40.9 structure: {self.qgis_prefix_path}")
            
            # Set Qt platform plugin path
            qt_plugins_path = os.path.join(self.qgis_prefix_path, "apps", "Qt5", "plugins")
            if os.path.exists(qt_plugins_path):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path
                os.environ["QT_PLUGIN_PATH"] = qt_plugins_path
            else:
                # Try alternative Qt path
                alt_qt_plugins = os.path.join(self.qgis_prefix_path, "apps", "qt5", "plugins")
                if os.path.exists(alt_qt_plugins):
                    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = alt_qt_plugins
                    os.environ["QT_PLUGIN_PATH"] = alt_qt_plugins
            
            # Add QGIS paths to PATH
            qgis_bin = os.path.join(self.qgis_prefix_path, "bin")
            qgis_python = os.path.join(self.qgis_prefix_path, "apps", "Python312")
            qgis_lib = os.path.join(self.qgis_prefix_path, "lib")
            qgis_apps = os.path.join(self.qgis_prefix_path, "apps")
            
            # Update PATH with all necessary paths
            current_path = os.environ.get("PATH", "")
            new_paths = [
                qgis_bin,
                qgis_python,
                qgis_lib,
                qgis_apps,
                os.path.join(self.qgis_prefix_path, "apps", "Qt5", "bin"),
                os.path.join(self.qgis_prefix_path, "apps", "gdal", "bin"),
                os.path.join(self.qgis_prefix_path, "apps", "grass", "grass84", "bin"),
                os.path.join(self.qgis_prefix_path, "apps", "grass", "grass84", "lib"),
                os.path.join(self.qgis_prefix_path, "apps", "grass", "grass84", "etc", "python"),
                os.path.join(self.qgis_prefix_path, "apps", "Python312", "DLLs"),
            ]
            
            # Add paths that exist
            for path in new_paths:
                if os.path.exists(path) and path not in current_path:
                    current_path = path + ";" + current_path
            
            os.environ["PATH"] = current_path
            
            # Add QGIS Python path to sys.path
            qgis_python_path = os.path.join(qgis_ltr_path, "python")
            if os.path.exists(qgis_python_path) and qgis_python_path not in sys.path:
                sys.path.insert(0, qgis_python_path)
            
            # Add Python312 site-packages to sys.path
            site_packages = os.path.join(python312_path, "Lib", "site-packages")
            if os.path.exists(site_packages) and site_packages not in sys.path:
                sys.path.insert(0, site_packages)
                
        else:
            # Legacy QGIS structure
            print(f"📁 Using legacy QGIS structure: {self.qgis_prefix_path}")
            
            # Set Qt platform plugin path
            qt_plugins_path = os.path.join(self.qgis_prefix_path, "qt5", "plugins")
            if os.path.exists(qt_plugins_path):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugins_path
            else:
                # Try alternative Qt plugins path
                alt_qt_plugins = os.path.join(self.qgis_prefix_path, "qt", "plugins")
                if os.path.exists(alt_qt_plugins):
                    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = alt_qt_plugins
            
            # Add QGIS bin and lib to PATH
            qgis_bin = os.path.join(self.qgis_prefix_path, "bin")
            qgis_lib = os.path.join(self.qgis_prefix_path, "lib")
            
            if os.path.exists(qgis_bin):
                os.environ["PATH"] += ";" + qgis_bin
            if os.path.exists(qgis_lib):
                os.environ["PATH"] += ";" + qgis_lib
            
            # Add QGIS Python path to sys.path
            qgis_python_path = os.path.join(self.qgis_prefix_path, "python")
            if os.path.exists(qgis_python_path) and qgis_python_path not in sys.path:
                sys.path.insert(0, qgis_python_path)
            
            # Also try the site-packages path
            site_packages = os.path.join(qgis_python_path, "Lib", "site-packages")
            if os.path.exists(site_packages) and site_packages not in sys.path:
                sys.path.insert(0, site_packages)
    
    def _initialize_qgis(self):
        """Initialize QGIS application"""
        try:
            # Try to import QGIS modules
            from qgis.core import QgsApplication
            from qgis.analysis import QgsNativeAlgorithms
            
            # Initialize QGIS application
            self.qgs_app = QgsApplication([], False)
            self.qgs_app.setPrefixPath(self.qgis_prefix_path, True)
            self.qgs_app.initQgis()
            
            # Register native algorithms
            QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
            
            print("✅ QGIS setup completed successfully!")
            print(f"QGIS Prefix Path: {self.qgis_prefix_path}")
            
        except ImportError as e:
            print(f"❌ Failed to import QGIS modules: {e}")
            print(f"QGIS Prefix Path: {self.qgis_prefix_path}")
            print("\n💡 This is a common issue with QGIS 3.40.9.")
            print("The QGIS Python environment has some DLL loading issues.")
            print("\n🔧 Solutions:")
            print("1. Use QGIS Python Console directly in QGIS application")
            print("2. Use QGIS Processing algorithms through QGIS GUI")
            print("3. Consider using an older QGIS version (3.34.x)")
            print("4. Use the QGIS Python interpreter for simple scripts")
            raise
        except Exception as e:
            print(f"❌ Failed to initialize QGIS: {e}")
            raise
    
    def get_qgs_app(self):
        """Get the QGIS application instance"""
        return self.qgs_app
    
    def cleanup(self):
        """Clean up QGIS application"""
        if self.qgs_app:
            self.qgs_app.exitQgis()
            print("✅ QGIS cleanup completed")

# Global instance for easy access
_qgis_setup = None

def initialize_qgis(qgis_prefix_path=None):
    """
    Initialize QGIS setup globally
    
    Args:
        qgis_prefix_path (str): Path to QGIS installation
    """
    global _qgis_setup
    if _qgis_setup is None:
        _qgis_setup = QGISSetup(qgis_prefix_path)
    return _qgis_setup

def get_qgis_app():
    """Get the QGIS application instance"""
    global _qgis_setup
    if _qgis_setup is None:
        raise RuntimeError("QGIS not initialized. Call initialize_qgis() first.")
    return _qgis_setup.get_qgs_app()

def cleanup_qgis():
    """Clean up QGIS application"""
    global _qgis_setup
    if _qgis_setup:
        _qgis_setup.cleanup()
        _qgis_setup = None

def test_qgis_setup():
    """
    Test function to verify QGIS setup is working
    Run this function to test if QGIS is properly configured
    """
    try:
        print("🧪 Testing QGIS setup...")
        
        # Initialize QGIS
        qgis_setup = initialize_qgis()
        qgs_app = get_qgis_app()
        
        print("✅ QGIS setup test passed!")
        print("🎉 QGIS is ready to use!")
        
        # Cleanup
        cleanup_qgis()
        return True
        
    except Exception as e:
        print(f"❌ QGIS setup test failed: {e}")
        return False

def get_qgis_info():
    """
    Get information about QGIS installation
    This function works even if QGIS modules can't be imported
    """
    print("🔍 QGIS Installation Information:")
    print(f"QGIS Prefix Path: {os.environ.get('QGIS_PREFIX_PATH', 'Not set')}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.path[:3]}...")  # Show first 3 paths
    
    # Check if QGIS Python paths exist
    qgis_prefix = os.environ.get('QGIS_PREFIX_PATH', r"C:\Program Files\QGIS 3.40.9")
    qgis_ltr_path = os.path.join(qgis_prefix, "apps", "qgis-ltr", "python")
    python312_path = os.path.join(qgis_prefix, "apps", "Python312")
    
    print(f"QGIS-LTR Python exists: {os.path.exists(qgis_ltr_path)}")
    print(f"Python312 exists: {os.path.exists(python312_path)}")

if __name__ == "__main__":
    # When run directly, show QGIS info and test setup
    get_qgis_info()
    print("\n" + "="*50)
    test_qgis_setup() 