import sys
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ✅ 1. QGIS installation path
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"

# ✅ 2. Set required environment variables
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")

# ✅ 3. Add QGIS Python path to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "python")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# ✅ 4. Initialize QGIS Application (only if not already initialized)
from qgis.core import QgsApplication
qgs = None
try:
    # Check if QGIS is already initialized
    QgsApplication.instance()
    print("✅ QGIS already initialized")
except:
    qgs = QgsApplication([], False)
    qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
    qgs.initQgis()
    print("✅ QGIS initialized")

# ✅ 5. Import QGIS modules
from qgis.core import (
    QgsRasterLayer,
    QgsProject,
    QgsProcessingFeedback
)

# Try to import processing, but handle if it's not available
try:
    import processing
    PROCESSING_AVAILABLE = True
    print("✅ Processing module available")
except ImportError:
    PROCESSING_AVAILABLE = False
    print("⚠️  Processing module not available - some functions will be limited")

# ✅ 6. Register native QGIS algorithms
from qgis.analysis import QgsNativeAlgorithms
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

print("✅ QGIS setup completed successfully!")

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

class TifProcessor:
    def __init__(self):
        self.project = QgsProject.instance()
        self.layers = {}
        self.json_results = {}
        
    def load_tif_file(self, tif_path, layer_name="Raster"):
        """
        Load a TIF file into QGIS
        """
        try:
            # Create raster layer
            raster_layer = QgsRasterLayer(tif_path, layer_name)
            
            if not raster_layer.isValid():
                print(f"❌ Failed to load raster: {tif_path}")
                return None
            else:
                print(f"✅ Successfully loaded raster: {tif_path}")
                print(f"   - Width: {raster_layer.width()} pixels")
                print(f"   - Height: {raster_layer.height()} pixels")
                print(f"   - Extent: {raster_layer.extent()}")
                
                # Add to project
                self.project.addMapLayer(raster_layer)
                self.layers[layer_name] = raster_layer
                
                # --- Save JSON for file loading ---
                load_json = {
                    'analysis_type': 'tif_loading',
                    'timestamp': str(datetime.now()),
                    'input_file': tif_path,
                    'layer_name': layer_name,
                    'width': raster_layer.width(),
                    'height': raster_layer.height(),
                    'extent': str(raster_layer.extent())
                }
                save_json_result(load_json, 'tif_loading_results.json')
                self.json_results['tif_loading'] = load_json
                
                return raster_layer
                
        except Exception as e:
            print(f"❌ Error loading raster: {e}")
            return None
    
    def calculate_slope(self, input_layer_name, output_path, scale=1.0, as_percent=False):
        """
        Calculate slope from a raster layer
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate slope.")
            print("   Try using QGIS Desktop application for slope calculation.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            
            print(f"🔄 Calculating slope from: {input_layer_name}")
            print(f"   - Scale factor: {scale}")
            print(f"   - Output as percentage: {as_percent}")
            
            # Run slope calculation
            result = processing.run("gdal:slope", {
                'INPUT': input_path,
                'SCALE': scale,
                'AS_PERCENT': as_percent,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Slope calculation completed!")
            print(f"   - Output saved to: {output_path}")
            
            # Load the result
            slope_layer = QgsRasterLayer(output_path, "Slope")
            if slope_layer.isValid():
                self.project.addMapLayer(slope_layer)
                self.layers["Slope"] = slope_layer
                print(f"   - Slope layer added to project")
                
                # Get slope statistics
                provider = slope_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min slope: {stats.minimumValue:.2f}")
                print(f"   - Max slope: {stats.maximumValue:.2f}")
                print(f"   - Mean slope: {stats.mean:.2f}")
                print(f"   - Std dev slope: {stats.stdDev:.2f}")
                
                # --- Save JSON for slope calculation ---
                slope_json = {
                    'analysis_type': 'slope_calculation',
                    'timestamp': str(datetime.now()),
                    'input_layer': input_layer_name,
                    'output_file': output_path,
                    'scale': scale,
                    'as_percent': as_percent,
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                save_json_result(slope_json, 'slope_calculation_results.json')
                self.json_results['slope_calculation'] = slope_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating slope: {e}")
            return False
    
    def calculate_moon_slope(self, input_layer_name, output_path):
        """
        Calculate slope specifically for moon parameters
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate slope.")
            print("   Try using QGIS Desktop application for slope calculation.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            
            print(f"🌙 Calculating moon slope from: {input_layer_name}")
            print("   - Using moon-specific parameters:")
            print("     * Scale: 1.0 (assuming meter resolution)")
            print("     * Output: Degrees (not percentage)")
            print("     * Moon gravity: 1.62 m/s² (vs Earth's 9.81 m/s²)")
            
            # Run slope calculation with moon parameters
            result = processing.run("gdal:slope", {
                'INPUT': input_path,
                'SCALE': 1.0,  # Assuming meter resolution
                'AS_PERCENT': False,  # Output in degrees
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Moon slope calculation completed!")
            print(f"   - Output saved to: {output_path}")
            
            # Load the result
            slope_layer = QgsRasterLayer(output_path, "Moon_Slope")
            if slope_layer.isValid():
                self.project.addMapLayer(slope_layer)
                self.layers["Moon_Slope"] = slope_layer
                print(f"   - Moon slope layer added to project")
                
                # Get slope statistics
                provider = slope_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min slope: {stats.minimumValue:.2f}°")
                print(f"   - Max slope: {stats.maximumValue:.2f}°")
                print(f"   - Mean slope: {stats.mean:.2f}°")
                print(f"   - Std dev slope: {stats.stdDev:.2f}°")
                
                # --- Save JSON for moon slope calculation ---
                moon_slope_json = {
                    'analysis_type': 'moon_slope_calculation',
                    'timestamp': str(datetime.now()),
                    'input_layer': input_layer_name,
                    'output_file': output_path,
                    'moon_parameters': {
                        'scale': 1.0,
                        'as_percent': False,
                        'moon_gravity': 1.62
                    },
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                save_json_result(moon_slope_json, 'moon_slope_calculation_results.json')
                self.json_results['moon_slope_calculation'] = moon_slope_json
                
                # Moon-specific slope analysis
                print("   - Moon slope analysis:")
                gentle_slopes = stats.mean < 5.0
                moderate_slopes = 5.0 <= stats.mean < 15.0
                steep_slopes = stats.mean >= 15.0
                
                if gentle_slopes:
                    print("     * Terrain: Mostly gentle slopes (good for landing)")
                elif moderate_slopes:
                    print("     * Terrain: Moderate slopes (moderate landing difficulty)")
                else:
                    print("     * Terrain: Steep slopes (challenging for landing)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating moon slope: {e}")
            return False
    
    def calculate_aspect(self, input_layer_name, output_path):
        """
        Calculate aspect from a raster layer
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate aspect.")
            print("   Try using QGIS Desktop application for aspect calculation.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            
            print(f"🔄 Calculating aspect from: {input_layer_name}")
            
            # Run aspect calculation
            result = processing.run("gdal:aspect", {
                'INPUT': input_path,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Aspect calculation completed!")
            print(f"   - Output saved to: {output_path}")
            
            # Load the result
            aspect_layer = QgsRasterLayer(output_path, "Aspect")
            if aspect_layer.isValid():
                self.project.addMapLayer(aspect_layer)
                self.layers["Aspect"] = aspect_layer
                print(f"   - Aspect layer added to project")
                
                # --- Save JSON for aspect calculation ---
                aspect_json = {
                    'analysis_type': 'aspect_calculation',
                    'timestamp': str(datetime.now()),
                    'input_layer': input_layer_name,
                    'output_file': output_path
                }
                save_json_result(aspect_json, 'aspect_calculation_results.json')
                self.json_results['aspect_calculation'] = aspect_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating aspect: {e}")
            return False
    
    def list_layers(self):
        """
        List all loaded layers
        """
        print("\n📋 Loaded Layers:")
        for name, layer in self.layers.items():
            print(f"   - {name}: {layer.source()}")
    
    def cleanup(self):
        """
        Clean up QGIS application
        """
        if qgs is not None:
            qgs.exitQgis()
            print("✅ QGIS cleanup completed")
        else:
            print("✅ QGIS cleanup completed (no cleanup needed)")

    def elevation_statistics(self, layer_name="Raster"):
        """
        Compute and print elevation statistics for the given raster layer.
        """
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
        print("\n🌑 Elevation Statistics:")
        print(f"1. Elevation (Z value): Raster band 1 (DEM values)")
        print(f"2. Minimum Elevation: {min_elev:.2f}")
        print(f"3. Maximum Elevation: {max_elev:.2f}")
        print(f"4. Mean Elevation: {mean_elev:.2f}")
        print(f"5. Elevation Range: {elev_range:.2f}")
        print(f"6. Standard Deviation of Elevation: {std_elev:.2f}")
        
        # --- Save JSON for elevation statistics ---
        elev_stats_json = {
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
        save_json_result(elev_stats_json, 'elevation_statistics_results.json')
        self.json_results['elevation_statistics'] = elev_stats_json
        
        return {
            'min': min_elev,
            'max': max_elev,
            'mean': mean_elev,
            'range': elev_range,
            'std': std_elev
        }

def prompt_for_tif_path():
    while True:
        tif_path = input("Enter the full path to your TIF file (or type 'exit' to quit): ").strip()
        if tif_path.lower() == 'exit':
            return None
        if os.path.exists(tif_path) and tif_path.lower().endswith(('.tif', '.tiff')):
            return tif_path
        print(f"❌ File not found or not a TIF: {tif_path}")

# Example usage
if __name__ == "__main__":
    processor = TifProcessor()
    # Add your main DEM path as the first default
    tif_files = [
        r"D:\moon extract\ch2_tmc_ndn_20200208T0057596133_d_dtm_m65.tif",
        r"aspect_outputs\lunar_slope.tif",
        r"aspect_outputs\lunar_aspect.tif",
        r"terrain_outputs\terrain_output.tif"
    ]
    tif_path = None
    for file_path in tif_files:
        if os.path.exists(file_path):
            tif_path = file_path
            print(f"✅ TIF file found: {tif_path}")
            break
    # If not found, prompt user
    if not tif_path:
        print("❌ No default TIF files found!")
        tif_path = prompt_for_tif_path()
        if not tif_path:
            print("Exiting: No TIF file provided.")
            processor.cleanup()
            sys.exit(1)
    print("🚀 Starting TIF processing...")
    print(f"📊 Using TIF: {os.path.basename(tif_path)}")
    # Load and process the TIF file
    if processor.load_tif_file(tif_path, "Moon_DEM"):
        processor.elevation_statistics("Moon_DEM")
        print("\n✅ TIF processing completed successfully!")
        print("📁 Analysis results:")
        print("   - DEM loaded and validated")
        print("   - Elevation statistics calculated")
        print("   - Ready for further processing")
    else:
        print("\n❌ Failed to load TIF file!")
    processor.cleanup() 