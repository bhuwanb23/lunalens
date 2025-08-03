import sys
import os
from datetime import datetime

# QGIS setup
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1"
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

    def generate_elevation_report(self, stats_data, layer_name="Raster", output_dir="elevation_outputs"):
        """Generate elevation analysis report similar to lunar landslide analysis report"""
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Determine risk level based on elevation statistics
            elev_range = stats_data['range']
            std_elev = stats_data['std']
            
            if elev_range > 1000 and std_elev > 200:
                risk_level = "HIGH"
                risk_factors = "High terrain variability, Extreme elevation differences"
            elif elev_range > 500 and std_elev > 100:
                risk_level = "MEDIUM"
                risk_factors = "Moderate terrain variability, Significant elevation differences"
            else:
                risk_level = "LOW"
                risk_factors = "Low terrain variability, Gentle elevation changes"
            
            # Generate report content
            report_content = f"""Lunar Elevation Analysis Report
==================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Layer: {layer_name}
Timestamp: {datetime.now().isoformat()}
Risk Level: {risk_level}
Risk Factors: {risk_factors}
Statistics:
  - Min: {stats_data['min']:.2f}
  - Max: {stats_data['max']:.2f}
  - Mean: {stats_data['mean']:.2f}
  - Std Dev: {stats_data['std']:.2f}
  - Range: {stats_data['range']:.2f}
Thresholds:
  - Low Elevation: {stats_data['min'] + stats_data['range'] * 0.25:.2f}
  - Medium Elevation: {stats_data['min'] + stats_data['range'] * 0.5:.2f}
  - High Elevation: {stats_data['min'] + stats_data['range'] * 0.75:.2f}

Analysis:
- Elevation range indicates terrain complexity
- Standard deviation shows surface roughness
- Mean elevation provides regional context
- Risk assessment based on terrain variability

------------------------------
"""
            
            # Save report
            report_path = os.path.join(output_dir, "lunar_elevation_analysis_report.txt")
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            print(f"✅ Elevation analysis report saved to: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Error generating elevation report: {e}")
            return None

    def cleanup(self):
        qgs.exitQgis()
        print("✅ QGIS cleanup completed")

def main():
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    stats = ElevationStats()
    
    # Load TIF file
    raster_layer = stats.load_tif(tif_path, "Moon_DEM")
    if raster_layer is None:
        print("❌ Failed to load TIF file")
        stats.cleanup()
        return
    
    # Calculate elevation statistics
    elevation_stats = stats.elevation_statistics("Moon_DEM")
    if elevation_stats is None:
        print("❌ Failed to calculate elevation statistics")
        stats.cleanup()
        return
    
    # Generate and save report
    report_path = stats.generate_elevation_report(elevation_stats, "Moon_DEM")
    if report_path:
        print(f"📊 Elevation analysis completed! Report saved to: {report_path}")
    
    stats.cleanup()

if __name__ == "__main__":
    main()