import sys
import os

# ✅ 1. QGIS installation path
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1\apps\qgis"

# ✅ 2. Set required environment variables
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")

# ✅ 3. Add QGIS Python path to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "python")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# ✅ 4. Initialize QGIS Application
from qgis.core import QgsApplication
qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs.initQgis()

# ✅ 5. Import QGIS modules
from qgis.core import QgsRasterLayer, QgsProject

print("✅ QGIS setup completed successfully!")

def load_and_analyze_tif(tif_path):
    """
    Load a TIF file and display its information
    """
    try:
        # Create raster layer
        raster_layer = QgsRasterLayer(tif_path, "Raster")
        
        if not raster_layer.isValid():
            print(f"❌ Failed to load raster: {tif_path}")
            return None
        else:
            print(f"✅ Successfully loaded raster: {tif_path}")
            print(f"   - Width: {raster_layer.width()} pixels")
            print(f"   - Height: {raster_layer.height()} pixels")
            print(f"   - Extent: {raster_layer.extent()}")
            
            # Get raster statistics
            provider = raster_layer.dataProvider()
            if provider:
                stats = provider.bandStatistics(1)
                print(f"   - Min value: {stats.minimumValue}")
                print(f"   - Max value: {stats.maximumValue}")
                print(f"   - Mean value: {stats.mean}")
                print(f"   - Standard deviation: {stats.stdDev}")
            
            # Add to project
            project = QgsProject.instance()
            project.addMapLayer(raster_layer)
            
            return raster_layer
            
    except Exception as e:
        print(f"❌ Error loading raster: {e}")
        return None

def main():
    # 🔧 CONFIGURE YOUR TIF FILE PATH HERE
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    
    print(f"🔄 Loading TIF file: {tif_path}")
    
    # Check if file exists
    if not os.path.exists(tif_path):
        print(f"❌ File not found: {tif_path}")
        return
    
    # Load and analyze the TIF file
    raster_layer = load_and_analyze_tif(tif_path)
    
    if raster_layer:
        print("\n✅ TIF file loaded successfully!")
        print("📝 Next steps:")
        print("   - Use QGIS Desktop application for slope/aspect calculations")
        print("   - Or install processing module for automated calculations")
    else:
        print("\n❌ Failed to load TIF file")
    
    # Cleanup
    qgs.exitQgis()
    print("✅ QGIS cleanup completed")

if __name__ == "__main__":
    main() 