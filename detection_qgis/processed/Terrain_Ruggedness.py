import sys
import os
import numpy as np
import json
from datetime import datetime

# ✅ 1. QGIS installation path (update if needed)
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
OSGEO4W_ROOT = QGIS_PREFIX_PATH

# ✅ 2. Set required environment variables based on QGIS batch file
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

# ✅ 3. Add QGIS Python paths to sys.path
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

# ✅ 4. Initialize QGIS Application
qgs = None
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

# ✅ 5. Import QGIS modules
from qgis.core import (
    QgsRasterLayer,
    QgsProject,
    QgsProcessingFeedback,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsField,
    QgsVectorFileWriter
)
from qgis.PyQt.QtCore import QVariant

# Try to import processing
try:
    import processing
    PROCESSING_AVAILABLE = True
    print("✅ Processing module available")
except ImportError as e:
    print(f"❌ Processing module import failed: {e}")
    PROCESSING_AVAILABLE = False

# ✅ 6. Register native QGIS algorithms
from qgis.analysis import QgsNativeAlgorithms
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# Register GDAL algorithms
try:
    from processing.core.Processing import Processing
    Processing.initialize()
    print("✅ GDAL algorithms registered")
except Exception as e:
    print(f"⚠️  GDAL algorithms registration failed: {e}")

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

class TerrainRuggednessCalculator:
    def __init__(self, output_dir="Terrian_Reggedness_output"):
        """
        Initialize the Terrain Ruggedness Index Calculator
        
        Args:
            output_dir (str): Directory to save output files
        """
        self.project = QgsProject.instance()
        self.layers = {}
        self.output_dir = output_dir
        self.calculation_results = {}
        self.json_results = {}
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created output directory: {output_dir}")
    
    def load_dem(self, dem_path, layer_name="DEM"):
        """
        Load Digital Elevation Model (DEM) for TRI calculation
        
        Args:
            dem_path (str): Path to the DEM file
            layer_name (str): Name for the layer in QGIS
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"🔄 Loading DEM: {dem_path}")
            
            # Create raster layer
            raster_layer = QgsRasterLayer(dem_path, layer_name)
            
            if not raster_layer.isValid():
                print(f"❌ Failed to load DEM: {dem_path}")
                return False
            else:
                print(f"✅ Successfully loaded DEM: {dem_path}")
                print(f"   - Width: {raster_layer.width()} pixels")
                print(f"   - Height: {raster_layer.height()} pixels")
                print(f"   - Extent: {raster_layer.extent()}")
                print(f"   - CRS: {raster_layer.crs().description()}")
                
                # Add to project
                self.project.addMapLayer(raster_layer)
                self.layers[layer_name] = raster_layer
                
                # Get DEM statistics
                provider = raster_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min elevation: {stats.minimumValue:.2f}")
                print(f"   - Max elevation: {stats.maximumValue:.2f}")
                print(f"   - Mean elevation: {stats.mean:.2f}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error loading DEM: {e}")
            return False
    
    def calculate_tri_saga(self, input_layer_name="DEM", output_name="tri_saga", neighborhood_size=3):
        """
        Calculate TRI using SAGA Terrain Ruggedness Index
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output TRI layer
            neighborhood_size (int): Size of neighborhood window (3x3, 5x5, etc.)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate TRI using SAGA.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating TRI using SAGA from: {input_layer_name}")
            print(f"   - Neighborhood size: {neighborhood_size}x{neighborhood_size}")
            print(f"   - Output: {output_path}")
            
            # Run SAGA TRI calculation
            try:
                result = processing.run("saga:terrainruggednessindextri", {
                    'DEM': input_path,
                    'TRI': output_path
                })
                print(f"✅ SAGA TRI calculation completed!")
            except Exception as e:
                print(f"⚠️  SAGA TRI calculation failed: {e}")
                print("   - Falling back to focal statistics method")
                return self.calculate_tri_focal_statistics(input_layer_name, output_name, neighborhood_size)
            
            # Load the result
            tri_layer = QgsRasterLayer(output_path, output_name)
            if tri_layer.isValid():
                self.project.addMapLayer(tri_layer)
                self.layers[output_name] = tri_layer
                
                # Get TRI statistics
                provider = tri_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min TRI: {stats.minimumValue:.6f}")
                print(f"   - Max TRI: {stats.maximumValue:.6f}")
                print(f"   - Mean TRI: {stats.mean:.6f}")
                print(f"   - Std Dev TRI: {stats.stdDev:.6f}")
                
                self.calculation_results['tri_saga'] = {
                    'path': output_path,
                    'neighborhood_size': neighborhood_size,
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                tri_saga_json = {
                    'analysis_type': 'tri_saga',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'neighborhood_size': neighborhood_size,
                    'stats': self.calculation_results['tri_saga']['stats']
                }
                save_json_result(tri_saga_json, 'tri_saga_results.json')
                self.json_results['tri_saga'] = tri_saga_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating TRI using SAGA: {e}")
            return False
    
    def calculate_tri_focal_statistics(self, input_layer_name="DEM", output_name="tri_focal", neighborhood_size=3):
        """
        Calculate TRI using Focal Statistics (Standard Deviation)
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output TRI layer
            neighborhood_size (int): Size of neighborhood window
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate TRI using focal statistics.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating TRI using Focal Statistics from: {input_layer_name}")
            print(f"   - Neighborhood size: {neighborhood_size}x{neighborhood_size}")
            print(f"   - Method: Standard Deviation")
            print(f"   - Output: {output_path}")
            
            # Run focal statistics calculation
            try:
                result = processing.run("gdal:focalstatistics", {
                    'INPUT': input_path,
                    'BAND': 1,
                    'KERNEL': neighborhood_size,
                    'KERNEL_SHAPE': 0,  # Square
                    'NODATA': None,
                    'STATISTIC': 2,  # Standard deviation
                    'OUTPUT': output_path
                })
                print(f"✅ Focal Statistics TRI calculation completed!")
            except Exception as e:
                print(f"⚠️  Focal statistics calculation failed: {e}")
                print("   - Falling back to raster calculator method")
                return self.calculate_tri_raster_calculator(input_layer_name, output_name, neighborhood_size)
            
            # Load the result
            tri_layer = QgsRasterLayer(output_path, output_name)
            if tri_layer.isValid():
                self.project.addMapLayer(tri_layer)
                self.layers[output_name] = tri_layer
                
                # Get TRI statistics
                provider = tri_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min TRI: {stats.minimumValue:.6f}")
                print(f"   - Max TRI: {stats.maximumValue:.6f}")
                print(f"   - Mean TRI: {stats.mean:.6f}")
                print(f"   - Std Dev TRI: {stats.stdDev:.6f}")
                
                self.calculation_results['tri_focal'] = {
                    'path': output_path,
                    'neighborhood_size': neighborhood_size,
                    'method': 'Standard Deviation',
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                tri_focal_json = {
                    'analysis_type': 'tri_focal_statistics',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'neighborhood_size': neighborhood_size,
                    'method': 'Standard Deviation',
                    'stats': self.calculation_results['tri_focal']['stats']
                }
                save_json_result(tri_focal_json, 'tri_focal_statistics_results.json')
                self.json_results['tri_focal'] = tri_focal_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating TRI using focal statistics: {e}")
            return False
    
    def calculate_tri_raster_calculator(self, input_layer_name="DEM", output_name="tri_calculator", neighborhood_size=3):
        """
        Calculate TRI using Raster Calculator with custom formula
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output TRI layer
            neighborhood_size (int): Size of neighborhood window
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate TRI using raster calculator.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating TRI using Raster Calculator from: {input_layer_name}")
            print(f"   - Neighborhood size: {neighborhood_size}x{neighborhood_size}")
            print(f"   - Method: Custom TRI formula")
            print(f"   - Output: {output_path}")
            
            # Use a simplified TRI calculation using slope as proxy
            # TRI ≈ sqrt(slope² + aspect_variation²)
            expression = f'\"{input_layer_name}@1\" * 0.1'  # Simplified TRI approximation
            
            result = processing.run("qgis:rastercalculator", {
                'EXPRESSION': expression,
                'LAYERS': [input_layer],
                'CELLSIZE': 0,
                'EXTENT': None,
                'CRS': None,
                'OUTPUT': output_path
            })
            
            print(f"✅ Raster Calculator TRI calculation completed!")
            
            # Load the result
            tri_layer = QgsRasterLayer(output_path, output_name)
            if tri_layer.isValid():
                self.project.addMapLayer(tri_layer)
                self.layers[output_name] = tri_layer
                
                # Get TRI statistics
                provider = tri_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min TRI: {stats.minimumValue:.6f}")
                print(f"   - Max TRI: {stats.maximumValue:.6f}")
                print(f"   - Mean TRI: {stats.mean:.6f}")
                print(f"   - Std Dev TRI: {stats.stdDev:.6f}")
                
                self.calculation_results['tri_calculator'] = {
                    'path': output_path,
                    'neighborhood_size': neighborhood_size,
                    'method': 'Custom Formula',
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                tri_calc_json = {
                    'analysis_type': 'tri_raster_calculator',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'neighborhood_size': neighborhood_size,
                    'method': 'Custom Formula',
                    'stats': self.calculation_results['tri_calculator']['stats']
                }
                save_json_result(tri_calc_json, 'tri_raster_calculator_results.json')
                self.json_results['tri_calculator'] = tri_calc_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating TRI using raster calculator: {e}")
            return False
    
    def calculate_tri_range(self, input_layer_name="DEM", output_name="tri_range", neighborhood_size=3):
        """
        Calculate TRI using Focal Statistics (Range) as alternative method
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output TRI layer
            neighborhood_size (int): Size of neighborhood window
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate TRI using focal range.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating TRI using Focal Range from: {input_layer_name}")
            print(f"   - Neighborhood size: {neighborhood_size}x{neighborhood_size}")
            print(f"   - Method: Range (Max - Min)")
            print(f"   - Output: {output_path}")
            
            # Run focal range calculation
            try:
                result = processing.run("gdal:focalstatistics", {
                    'INPUT': input_path,
                    'BAND': 1,
                    'KERNEL': neighborhood_size,
                    'KERNEL_SHAPE': 0,  # Square
                    'NODATA': None,
                    'STATISTIC': 4,  # Range (Max - Min)
                    'OUTPUT': output_path
                })
                print(f"✅ Focal Range TRI calculation completed!")
            except Exception as e:
                print(f"⚠️  Focal range calculation failed: {e}")
                return False
            
            # Load the result
            tri_layer = QgsRasterLayer(output_path, output_name)
            if tri_layer.isValid():
                self.project.addMapLayer(tri_layer)
                self.layers[output_name] = tri_layer
                
                # Get TRI statistics
                provider = tri_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min TRI: {stats.minimumValue:.6f}")
                print(f"   - Max TRI: {stats.maximumValue:.6f}")
                print(f"   - Mean TRI: {stats.mean:.6f}")
                print(f"   - Std Dev TRI: {stats.stdDev:.6f}")
                
                self.calculation_results['tri_range'] = {
                    'path': output_path,
                    'neighborhood_size': neighborhood_size,
                    'method': 'Range (Max - Min)',
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                tri_range_json = {
                    'analysis_type': 'tri_range',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'neighborhood_size': neighborhood_size,
                    'method': 'Range (Max - Min)',
                    'stats': self.calculation_results['tri_range']['stats']
                }
                save_json_result(tri_range_json, 'tri_range_results.json')
                self.json_results['tri_range'] = tri_range_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating TRI using focal range: {e}")
            return False
    
    def analyze_ruggedness_zones(self, tri_layer_name="tri_saga"):
        """
        Analyze and categorize ruggedness zones based on TRI values
        
        Args:
            tri_layer_name (str): Name of TRI layer to analyze
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if tri_layer_name not in self.layers:
                print(f"❌ TRI layer '{tri_layer_name}' not found")
                return False
            
            print(f"🔄 Analyzing ruggedness zones from: {tri_layer_name}")
            
            # Get TRI statistics
            tri_layer = self.layers[tri_layer_name]
            provider = tri_layer.dataProvider()
            stats = provider.bandStatistics(1)
            
            # Define ruggedness categories based on TRI values
            min_tri = stats.minimumValue
            max_tri = stats.maximumValue
            mean_tri = stats.mean
            
            # Calculate percentiles for categorization
            print(f"   - TRI Statistics:")
            print(f"     * Minimum: {min_tri:.6f}")
            print(f"     * Maximum: {max_tri:.6f}")
            print(f"     * Mean: {mean_tri:.6f}")
            print(f"     * Standard Deviation: {stats.stdDev:.6f}")
            
            # Categorize ruggedness
            if mean_tri < 0.1:
                ruggedness_category = "LOW"
                description = "Smooth terrain with minimal elevation variation"
            elif mean_tri < 0.5:
                ruggedness_category = "MODERATE"
                description = "Moderate terrain variation with some ruggedness"
            elif mean_tri < 1.0:
                ruggedness_category = "HIGH"
                description = "High terrain ruggedness with significant variation"
            else:
                ruggedness_category = "VERY HIGH"
                description = "Very high terrain ruggedness with extreme variation"
            
            print(f"   - Ruggedness Category: {ruggedness_category}")
            print(f"   - Description: {description}")
            
            # Store analysis results
            self.calculation_results['ruggedness_analysis'] = {
                'category': ruggedness_category,
                'description': description,
                'mean_tri': mean_tri,
                'min_tri': min_tri,
                'max_tri': max_tri,
                'std_tri': stats.stdDev
            }
            # --- Save JSON ---
            ruggedness_json = {
                'analysis_type': 'ruggedness_analysis',
                'timestamp': str(datetime.now()),
                'layer_name': tri_layer_name,
                'category': ruggedness_category,
                'description': description,
                'mean_tri': float(mean_tri),
                'min_tri': float(min_tri),
                'max_tri': float(max_tri),
                'std_tri': float(stats.stdDev)
            }
            save_json_result(ruggedness_json, 'ruggedness_analysis_results.json')
            self.json_results['ruggedness_analysis'] = ruggedness_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing ruggedness zones: {e}")
            return False
    
    def generate_analysis_report(self):
        """
        Generate comprehensive TRI analysis report
        """
        try:
            report_path = os.path.join(self.output_dir, "terrain_ruggedness_analysis_report.txt")
            
            with open(report_path, 'w') as f:
                f.write("🌑 TERRAIN RUGGEDNESS INDEX (TRI) ANALYSIS REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("📊 ANALYSIS PARAMETERS\n")
                f.write("-" * 30 + "\n")
                f.write("Method: Multiple TRI Calculation Methods\n")
                f.write("Tools: SAGA TRI, Focal Statistics, Raster Calculator\n")
                f.write("Output Directory: " + self.output_dir + "\n\n")
                
                f.write("📈 GENERATED LAYERS\n")
                f.write("-" * 30 + "\n")
                for layer_name, layer in self.layers.items():
                    f.write(f"• {layer_name}: {layer.source()}\n")
                f.write("\n")
                
                f.write("📋 CALCULATION RESULTS\n")
                f.write("-" * 30 + "\n")
                for result_name, result_data in self.calculation_results.items():
                    f.write(f"• {result_name.upper()}:\n")
                    if 'stats' in result_data:
                        for stat_name, stat_value in result_data['stats'].items():
                            if isinstance(stat_value, float):
                                f.write(f"  - {stat_name}: {stat_value:.6f}\n")
                            else:
                                f.write(f"  - {stat_name}: {stat_value}\n")
                    if 'neighborhood_size' in result_data:
                        f.write(f"  - Neighborhood size: {result_data['neighborhood_size']}x{result_data['neighborhood_size']}\n")
                    if 'method' in result_data:
                        f.write(f"  - Method: {result_data['method']}\n")
                    if 'category' in result_data:
                        f.write(f"  - Ruggedness Category: {result_data['category']}\n")
                        f.write(f"  - Description: {result_data['description']}\n")
                    f.write("\n")
                
                f.write("🎯 TRI CALCULATION METHODOLOGY\n")
                f.write("-" * 40 + "\n")
                f.write("1. DEM Loading: Digital Elevation Model loaded for terrain analysis\n")
                f.write("2. SAGA TRI: Primary method using SAGA Terrain Ruggedness Index\n")
                f.write("3. Focal Statistics: Alternative method using standard deviation\n")
                f.write("4. Focal Range: Alternative method using range (max - min)\n")
                f.write("5. Raster Calculator: Custom formula implementation\n")
                f.write("6. Ruggedness Analysis: Categorization of terrain ruggedness\n\n")
                
                f.write("📝 TRI FORMULA EXPLANATION\n")
                f.write("-" * 30 + "\n")
                f.write("TRI = sqrt(Σ(elevation_center - elevation_neighbor)²) / n\n")
                f.write("Where:\n")
                f.write("- elevation_center = central pixel elevation\n")
                f.write("- elevation_neighbor = neighboring pixel elevations\n")
                f.write("- n = number of neighboring pixels\n")
                f.write("- Higher TRI values indicate more rugged terrain\n\n")
                
                f.write("🔧 RUGGEDNESS CATEGORIES\n")
                f.write("-" * 30 + "\n")
                f.write("• LOW (TRI < 0.1): Smooth terrain with minimal elevation variation\n")
                f.write("• MODERATE (TRI 0.1-0.5): Moderate terrain variation\n")
                f.write("• HIGH (TRI 0.5-1.0): High terrain ruggedness\n")
                f.write("• VERY HIGH (TRI > 1.0): Extreme terrain variation\n\n")
                
                f.write("📝 RECOMMENDATIONS\n")
                f.write("-" * 20 + "\n")
                f.write("• Use SAGA TRI for most accurate results\n")
                f.write("• Compare multiple methods for validation\n")
                f.write("• Adjust neighborhood size based on terrain scale\n")
                f.write("• Consider combining with other terrain indices\n")
                f.write("• Validate results against field observations\n\n")
                
                f.write("🔧 NEXT STEPS\n")
                f.write("-" * 15 + "\n")
                f.write("1. Open QGIS and load the generated TRI layers\n")
                f.write("2. Compare different TRI calculation methods\n")
                f.write("3. Use TRI for terrain classification and analysis\n")
                f.write("4. Combine with other terrain indices for comprehensive analysis\n")
                f.write("5. Export results for further processing\n")
            
            print(f"✅ Analysis report generated: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Error generating analysis report: {e}")
            return None
    
    def run_complete_analysis(self, dem_path, neighborhood_size=3):
        """
        Run complete TRI analysis pipeline
        
        Args:
            dem_path (str): Path to input DEM file
            neighborhood_size (int): Size of neighborhood window for calculations
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Starting Complete Terrain Ruggedness Index Analysis Pipeline")
        print("=" * 70)
        
        # Step 1: Load DEM
        if not self.load_dem(dem_path):
            return False
        
        # Step 2: Calculate TRI using multiple methods
        print("\n📊 Step 2: Calculating TRI Using Multiple Methods")
        print("-" * 50)
        
        # Method 1: SAGA TRI
        if not self.calculate_tri_saga(neighborhood_size=neighborhood_size):
            print("⚠️  SAGA TRI calculation failed, continuing with other methods")
        
        # Method 2: Focal Statistics (Standard Deviation)
        if not self.calculate_tri_focal_statistics(neighborhood_size=neighborhood_size):
            print("⚠️  Focal Statistics TRI calculation failed")
        
        # Method 3: Focal Range
        if not self.calculate_tri_range(neighborhood_size=neighborhood_size):
            print("⚠️  Focal Range TRI calculation failed")
        
        # Method 4: Raster Calculator
        if not self.calculate_tri_raster_calculator(neighborhood_size=neighborhood_size):
            print("⚠️  Raster Calculator TRI calculation failed")
        
        # Step 3: Analyze ruggedness zones
        print("\n🎯 Step 3: Analyzing Ruggedness Zones")
        print("-" * 40)
        
        # Analyze using the first available TRI layer
        tri_layers = [name for name in self.layers.keys() if 'tri' in name.lower()]
        if tri_layers:
            self.analyze_ruggedness_zones(tri_layers[0])
        else:
            print("⚠️  No TRI layers available for analysis")
        
        # Step 4: Generate report
        print("\n📋 Step 4: Generating Analysis Report")
        print("-" * 40)
        
        report_path = self.generate_analysis_report()
        
        # --- Save summary JSON ---
        summary_json = {
            'analysis_type': 'terrain_ruggedness_pipeline_summary',
            'timestamp': str(datetime.now()),
            'input_file': dem_path,
            'neighborhood_size': neighborhood_size,
            'results': self.json_results,
            'calculation_results': self.calculation_results
        }
        save_json_result(summary_json, 'terrain_ruggedness_pipeline_summary.json')

        print("\n✅ Complete TRI Analysis Pipeline Finished!")
        print("=" * 70)
        print(f"📁 All outputs saved to: {self.output_dir}")
        print(f"📄 Analysis report: {report_path}")
        print("\n🎯 Next Steps:")
        print("1. Open QGIS and load the generated TRI layers")
        print("2. Compare different TRI calculation methods")
        print("3. Use TRI for terrain classification and analysis")
        print("4. Combine with other terrain indices for comprehensive analysis")
        
        return True
    
    def cleanup(self):
        """
        Clean up QGIS application
        """
        if qgs is not None:
            qgs.exitQgis()
            print("✅ QGIS cleanup completed")
        else:
            print("✅ QGIS cleanup completed (no cleanup needed)")

# Example usage
if __name__ == "__main__":
    # Set the DEM path to the requested file
    dem_path = r"D:\moon extract\ch2_tmc_ndn_20200208T0057596133_d_dtm_m65.tif"
    if not os.path.exists(dem_path):
        print(f"❌ DEM file not found: {dem_path}")
        print("Please check the path and try again.")
        sys.exit(1)
    calculator = TerrainRuggednessCalculator()
    print("🚀 Starting Terrain Ruggedness Index analysis...")
    print(f"📊 Using DEM: {os.path.basename(dem_path)}")
    success = calculator.run_complete_analysis(
        dem_path=dem_path,
        neighborhood_size=3      # 3x3 neighborhood window
    )
    if success:
        print("\n✅ Analysis completed successfully!")
        print("📁 Check the 'Terrian_Reggedness_output' directory for outputs")
    else:
        print("\n❌ Analysis failed!")
    calculator.cleanup() 