import sys
import os
import json
from datetime import datetime

# QGIS setup
QGIS_PREFIX_PATH = os.environ.get('QGIS_PREFIX_PATH', r'C:\Program Files\QGIS 3.40.9')
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# Add QGIS Python path
QGIS_QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python")
if QGIS_QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_QGIS_PYTHON_PATH)

from qgis.core import QgsApplication, QgsRasterLayer, QgsProject

# Initialize QGIS only if not already initialized
qgs = None
try:
    QgsApplication.instance()
    print("✅ QGIS already initialized")
except:
    qgs = QgsApplication([], False)
    qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
    qgs.initQgis()
    print("✅ QGIS initialized")

# --- JSON results folder setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_RESULTS_DIR = os.path.join(SCRIPT_DIR, 'json_results')
os.makedirs(JSON_RESULTS_DIR, exist_ok=True)

def save_json_result(data, filename):
    """
    Save analysis results as JSON with metadata
    """
    try:
        json_filepath = os.path.join(JSON_RESULTS_DIR, filename)
        def np_encoder(obj):
            if isinstance(obj, np.generic):
                return obj.item()
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return str(obj)
        with open(json_filepath, 'w') as f:
            json.dump(data, f, indent=2, default=np_encoder)
        print(f"✅ JSON results saved to: {json_filepath}")
        return json_filepath
    except Exception as e:
        print(f"❌ Error saving JSON results: {e}")
        return None

class ElevationStats:
    def __init__(self):
        self.project = QgsProject.instance()
        self.layers = {}
        self.json_results = {}

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

        # --- Save JSON for elevation statistics ---
        elev_json = {
            'analysis_type': 'elevation_statistics',
            'timestamp': str(datetime.now()),
            'layer_name': layer_name,
            'input_file': layer.source(),
            'min_elevation': float(min_elev),
            'max_elevation': float(max_elev),
            'mean_elevation': float(mean_elev),
            'elevation_range': float(elev_range),
            'std_elevation': float(std_elev)
        }
        save_json_result(elev_json, 'elevation_statistics_results.json')
        self.json_results['elevation_statistics'] = elev_json

        return {
            'min': min_elev,
            'max': max_elev,
            'mean': mean_elev,
            'range': elev_range,
            'std': std_elev
        }

    def cleanup(self):
        if qgs is not None:
            qgs.exitQgis()
            print("✅ QGIS cleanup completed")
        else:
            print("✅ QGIS cleanup completed (no cleanup needed)")

def main():
    # Example: tif_path = r"D:\moon extract\ch2_tmc_ndn_20200208T0057596133_d_dtm_m65.tif"
    tif_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not os.path.exists(tif_path):
        print(f"❌ DEM file not found: {tif_path}")
        print("Please check the path and try again.")
        return
    stats = ElevationStats()
    stats.load_tif(tif_path, "Moon_DEM")
    stats.elevation_statistics("Moon_DEM")
    stats.cleanup()

if __name__ == "__main__":
    main()