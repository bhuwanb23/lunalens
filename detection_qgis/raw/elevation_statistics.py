import sys
import os

# QGIS setup
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1\apps\qgis"
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "python")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

from qgis.core import QgsApplication, QgsRasterLayer, QgsProject

qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs.initQgis()

class ElevationStats:
    def __init__(self):
        self.project = QgsProject.instance()
        self.layers = {}

    def load_tif(self, tif_path, layer_name="Raster"):
        raster_layer = QgsRasterLayer(tif_path, layer_name)
        if not raster_layer.isValid():
            print(f"❌ Failed to load raster: {tif_path}")
            return None
        self.project.addMapLayer(raster_layer)
        self.layers[layer_name] = raster_layer
        print(f"✅ Loaded raster: {tif_path}")
        return raster_layer

    def elevation_statistics(self, layer_name="Raster"):
        if layer_name not in self.layers:
            print(f"❌ Layer '{layer_name}' not found.")
            return None
        layer = self.layers[layer_name]
        provider = layer.dataProvider()
        stats = provider.bandStatistics(1)
        min_elev = stats.minimumValue
        max_elev = stats.maximumValue
        mean_elev = stats.mean
        std_elev = stats.stdDev
        elev_range = max_elev - min_elev
        print("\n🌑 Elevation Statistics (Lunar DEM):")
        print("1. Elevation (Z value): The vertical height above the lunar reference datum. Base data used for all terrain analysis.")
        print(f"2. Minimum Elevation: {min_elev:.2f} (Lowest value; detects craters, basins)")
        print(f"3. Maximum Elevation: {max_elev:.2f} (Highest value; detects ridges, peaks)")
        print(f"4. Mean Elevation: {mean_elev:.2f} (Average; used for regional profiling)")
        print(f"5. Elevation Range: {elev_range:.2f} (Max - Min; measures terrain variability)")
        print(f"6. Standard Deviation: {std_elev:.2f} (How varied the terrain is; ruggedness)")
        return {
            'min': min_elev,
            'max': max_elev,
            'mean': mean_elev,
            'range': elev_range,
            'std': std_elev
        }

    def cleanup(self):
        qgs.exitQgis()
        print("✅ QGIS cleanup completed")

def main():
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    stats = ElevationStats()
    stats.load_tif(tif_path, "Moon_DEM")
    stats.elevation_statistics("Moon_DEM")
    stats.cleanup()

if __name__ == "__main__":
    main()