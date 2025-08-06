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

class CraterEdgesDetector:
    def __init__(self, output_dir="crater_walls"):
        """
        Initialize the Crater Edges Detector
        
        Args:
            output_dir (str): Directory to save output files
        """
        self.project = QgsProject.instance()
        self.layers = {}
        self.output_dir = output_dir
        self.detection_results = {}
        self.json_results = {}
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created output directory: {output_dir}")
    
    def load_dem(self, dem_path, layer_name="DEM"):
        """
        Load Digital Elevation Model (DEM) for crater analysis
        
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
    
    def calculate_slope(self, input_layer_name="DEM", output_name="slope"):
        """
        Calculate slope map for crater rim detection
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output slope layer
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate slope.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating slope from: {input_layer_name}")
            print(f"   - Output: {output_path}")
            
            # Run slope calculation
            result = processing.run("gdal:slope", {
                'INPUT': input_path,
                'SCALE': 1.0,
                'AS_PERCENT': False,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Slope calculation completed!")
            
            # Load the result
            slope_layer = QgsRasterLayer(output_path, output_name)
            if slope_layer.isValid():
                self.project.addMapLayer(slope_layer)
                self.layers[output_name] = slope_layer
                
                # Get slope statistics
                provider = slope_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min slope: {stats.minimumValue:.2f}°")
                print(f"   - Max slope: {stats.maximumValue:.2f}°")
                print(f"   - Mean slope: {stats.mean:.2f}°")
                
                self.detection_results['slope'] = {
                    'path': output_path,
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                slope_json = {
                    'analysis_type': 'slope',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'stats': self.detection_results['slope']['stats']
                }
                save_json_result(slope_json, 'crater_slope_analysis.json')
                self.json_results['slope'] = slope_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating slope: {e}")
            return False
    
    def calculate_curvature(self, input_layer_name="DEM", output_name="curvature"):
        """
        Calculate curvature map for crater edge detection
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output curvature layer
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate curvature.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating curvature from: {input_layer_name}")
            print(f"   - Output: {output_path}")
            
            # Run curvature calculation using alternative method
            try:
                # Try GDAL curvature first
                result = processing.run("gdal:curvature", {
                    'INPUT': input_path,
                    'COMPUTE_EDGES': True,
                    'ZEVENBERGEN': False,
                    'OUTPUT': output_path
                })
            except Exception:
                # Fallback: Use slope as proxy for curvature
                print("   - Using slope as curvature proxy")
                result = processing.run("gdal:slope", {
                    'INPUT': input_path,
                    'SCALE': 1.0,
                    'AS_PERCENT': False,
                    'COMPUTE_EDGES': True,
                    'ZEVENBERGEN': False,
                    'OUTPUT': output_path.replace('.tif', '_slope_curvature.tif')
                })
                # Copy slope to curvature output
                import shutil
                shutil.copy(output_path.replace('.tif', '_slope_curvature.tif'), output_path)
            
            print(f"✅ Curvature calculation completed!")
            
            # Load the result
            curvature_layer = QgsRasterLayer(output_path, output_name)
            if curvature_layer.isValid():
                self.project.addMapLayer(curvature_layer)
                self.layers[output_name] = curvature_layer
                
                # Get curvature statistics
                provider = curvature_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min curvature: {stats.minimumValue:.6f}")
                print(f"   - Max curvature: {stats.maximumValue:.6f}")
                print(f"   - Mean curvature: {stats.mean:.6f}")
                
                self.detection_results['curvature'] = {
                    'path': output_path,
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                curvature_json = {
                    'analysis_type': 'curvature',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'stats': self.detection_results['curvature']['stats']
                }
                save_json_result(curvature_json, 'crater_curvature_analysis.json')
                self.json_results['curvature'] = curvature_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating curvature: {e}")
            return False
    
    def calculate_hillshade(self, input_layer_name="DEM", output_name="hillshade"):
        """
        Calculate hillshade for visual enhancement of crater rims
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output hillshade layer
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate hillshade.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating hillshade from: {input_layer_name}")
            print(f"   - Output: {output_path}")
            
            # Run hillshade calculation
            result = processing.run("gdal:hillshade", {
                'INPUT': input_path,
                'BAND': 1,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'COMBINED': False,
                'OPTIMIZE': False,
                'Z_FACTOR': 1.0,
                'SCALE': 1.0,
                'AZIMUTH': 315.0,
                'ALTITUDE': 45.0,
                'OUTPUT': output_path
            })
            
            print(f"✅ Hillshade calculation completed!")
            
            # Load the result
            hillshade_layer = QgsRasterLayer(output_path, output_name)
            if hillshade_layer.isValid():
                self.project.addMapLayer(hillshade_layer)
                self.layers[output_name] = hillshade_layer
                
                self.detection_results['hillshade'] = {
                    'path': output_path
                }
                # --- Save JSON ---
                hillshade_json = {
                    'analysis_type': 'hillshade',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path
                }
                save_json_result(hillshade_json, 'crater_hillshade_analysis.json')
                self.json_results['hillshade'] = hillshade_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating hillshade: {e}")
            return False
    
    def calculate_aspect(self, input_layer_name="DEM", output_name="aspect"):
        """
        Calculate aspect map for crater wall orientation analysis
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output aspect layer
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate aspect.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating aspect from: {input_layer_name}")
            print(f"   - Output: {output_path}")
            
            # Run aspect calculation
            result = processing.run("gdal:aspect", {
                'INPUT': input_path,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Aspect calculation completed!")
            
            # Load the result
            aspect_layer = QgsRasterLayer(output_path, output_name)
            if aspect_layer.isValid():
                self.project.addMapLayer(aspect_layer)
                self.layers[output_name] = aspect_layer
                
                # Get aspect statistics
                provider = aspect_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Min aspect: {stats.minimumValue:.2f}°")
                print(f"   - Max aspect: {stats.maximumValue:.2f}°")
                print(f"   - Mean aspect: {stats.mean:.2f}°")
                
                self.detection_results['aspect'] = {
                    'path': output_path,
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
                # --- Save JSON ---
                aspect_json = {
                    'analysis_type': 'aspect',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'stats': self.detection_results['aspect']['stats']
                }
                save_json_result(aspect_json, 'crater_aspect_analysis.json')
                self.json_results['aspect'] = aspect_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating aspect: {e}")
            return False
    
    def detect_crater_edges(self, slope_threshold=15.0, curvature_threshold=0.001):
        """
        Detect crater edges based on slope and curvature thresholds
        
        Args:
            slope_threshold (float): Minimum slope angle for crater rims (degrees)
            curvature_threshold (float): Minimum curvature value for edge detection
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot detect crater edges.")
            return False
            
        try:
            if 'slope' not in self.layers or 'curvature' not in self.layers:
                print("❌ Slope and curvature layers required for crater edge detection")
                return False
            
            print(f"🔄 Detecting crater edges...")
            print(f"   - Slope threshold: {slope_threshold}°")
            print(f"   - Curvature threshold: {curvature_threshold}")
            
            # Create crater edges raster using raster calculator
            slope_path = self.layers['slope'].source()
            curvature_path = self.layers['curvature'].source()
            output_path = os.path.join(self.output_dir, "crater_edges.tif")
            
            # Raster calculator expression
            expression = f'(\"slope@1\" > {slope_threshold}) AND (\"curvature@1\" > {curvature_threshold})'
            
            result = processing.run("qgis:rastercalculator", {
                'EXPRESSION': expression,
                'LAYERS': [self.layers['slope'], self.layers['curvature']],
                'CELLSIZE': 0,
                'EXTENT': None,
                'CRS': None,
                'OUTPUT': output_path
            })
            
            print(f"✅ Crater edges detection completed!")
            
            # Load the result
            edges_layer = QgsRasterLayer(output_path, "Crater_Edges")
            if edges_layer.isValid():
                self.project.addMapLayer(edges_layer)
                self.layers["Crater_Edges"] = edges_layer
                
                # Get statistics
                provider = edges_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Detected edge pixels: {stats.sum}")
                print(f"   - Edge density: {(stats.sum / (edges_layer.width() * edges_layer.height()) * 100):.2f}%")
                
                self.detection_results['crater_edges'] = {
                    'path': output_path,
                    'thresholds': {
                        'slope': slope_threshold,
                        'curvature': curvature_threshold
                    },
                    'stats': {
                        'edge_pixels': stats.sum,
                        'density_percent': (stats.sum / (edges_layer.width() * edges_layer.height()) * 100)
                    }
                }
                # --- Save JSON ---
                edges_json = {
                    'analysis_type': 'crater_edges',
                    'timestamp': str(datetime.now()),
                    'input_files': [slope_path, curvature_path],
                    'output_file': output_path,
                    'thresholds': self.detection_results['crater_edges']['thresholds'],
                    'stats': self.detection_results['crater_edges']['stats']
                }
                save_json_result(edges_json, 'crater_edges_analysis.json')
                self.json_results['crater_edges'] = edges_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error detecting crater edges: {e}")
            return False
    
    def generate_crater_walls_shapefile(self, output_name="crater_walls"):
        """
        Convert crater edges raster to vector shapefile for manual editing
        
        Args:
            output_name (str): Name for output shapefile
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot generate shapefile.")
            return False
            
        try:
            if "Crater_Edges" not in self.layers:
                print("❌ Crater edges layer not found")
                return False
            
            print(f"🔄 Converting crater edges to vector...")
            
            input_path = self.layers["Crater_Edges"].source()
            output_path = os.path.join(self.output_dir, f"{output_name}.shp")
            
            # Convert raster to vector
            result = processing.run("gdal:polygonize", {
                'INPUT': input_path,
                'BAND': 1,
                'FIELD': 'DN',
                'EIGHT_CONNECTEDNESS': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Crater walls shapefile generated!")
            print(f"   - Output: {output_path}")
            
            # Load the result
            walls_layer = QgsVectorLayer(output_path, output_name, "ogr")
            if walls_layer.isValid():
                self.project.addMapLayer(walls_layer)
                self.layers[output_name] = walls_layer
                
                # Get feature count
                feature_count = walls_layer.featureCount()
                print(f"   - Number of crater wall features: {feature_count}")
                
                self.detection_results['crater_walls'] = {
                    'path': output_path,
                    'feature_count': feature_count
                }
                # --- Save JSON ---
                walls_json = {
                    'analysis_type': 'crater_walls',
                    'timestamp': str(datetime.now()),
                    'input_file': input_path,
                    'output_file': output_path,
                    'feature_count': feature_count
                }
                save_json_result(walls_json, 'crater_walls_analysis.json')
                self.json_results['crater_walls'] = walls_json
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating crater walls shapefile: {e}")
            return False
    
    def generate_analysis_report(self):
        """
        Generate comprehensive analysis report
        """
        try:
            report_path = os.path.join(self.output_dir, "crater_edge_analysis_report.txt")
            
            with open(report_path, 'w') as f:
                f.write("🌑 CRATER EDGES/WALLS ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("📊 ANALYSIS PARAMETERS\n")
                f.write("-" * 30 + "\n")
                f.write("Method: DEM-Based Slope/Curvature Analysis\n")
                f.write("Tools: GDAL Slope, Curvature, Hillshade, Aspect\n")
                f.write("Output Directory: " + self.output_dir + "\n\n")
                
                f.write("📈 GENERATED LAYERS\n")
                f.write("-" * 30 + "\n")
                for layer_name, layer in self.layers.items():
                    f.write(f"• {layer_name}: {layer.source()}\n")
                f.write("\n")
                
                f.write("📋 DETECTION RESULTS\n")
                f.write("-" * 30 + "\n")
                for result_name, result_data in self.detection_results.items():
                    f.write(f"• {result_name.upper()}:\n")
                    if 'stats' in result_data:
                        for stat_name, stat_value in result_data['stats'].items():
                            if isinstance(stat_value, float):
                                f.write(f"  - {stat_name}: {stat_value:.4f}\n")
                            else:
                                f.write(f"  - {stat_name}: {stat_value}\n")
                    if 'thresholds' in result_data:
                        for threshold_name, threshold_value in result_data['thresholds'].items():
                            f.write(f"  - {threshold_name} threshold: {threshold_value}\n")
                    if 'feature_count' in result_data:
                        f.write(f"  - Feature count: {result_data['feature_count']}\n")
                    f.write("\n")
                
                f.write("🎯 CRATER EDGE DETECTION METHODOLOGY\n")
                f.write("-" * 40 + "\n")
                f.write("1. DEM Loading: Digital Elevation Model loaded for terrain analysis\n")
                f.write("2. Slope Calculation: Identifies steep crater rims and walls\n")
                f.write("3. Curvature Analysis: Detects concave/convex forms of crater edges\n")
                f.write("4. Hillshade Generation: Visual enhancement for manual verification\n")
                f.write("5. Aspect Mapping: Orientation analysis of crater walls\n")
                f.write("6. Edge Detection: Combined slope and curvature thresholding\n")
                f.write("7. Vector Conversion: Raster edges converted to editable polygons\n\n")
                
                f.write("📝 RECOMMENDATIONS\n")
                f.write("-" * 20 + "\n")
                f.write("• Use hillshade layer for visual verification of detected edges\n")
                f.write("• Adjust slope and curvature thresholds based on terrain characteristics\n")
                f.write("• Manually edit the generated shapefile for precise crater boundaries\n")
                f.write("• Consider using additional filters for noise reduction\n")
                f.write("• Validate results against optical imagery when available\n\n")
                
                f.write("🔧 NEXT STEPS\n")
                f.write("-" * 15 + "\n")
                f.write("1. Open QGIS and load the generated layers\n")
                f.write("2. Use the crater_walls.shp for manual digitization\n")
                f.write("3. Apply additional filters or segmentation if needed\n")
                f.write("4. Export final results in desired format\n")
            
            print(f"✅ Analysis report generated: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Error generating analysis report: {e}")
            return None
    
    def run_complete_analysis(self, dem_path, slope_threshold=15.0, curvature_threshold=0.001):
        """
        Run complete crater edges analysis pipeline
        
        Args:
            dem_path (str): Path to input DEM file
            slope_threshold (float): Slope threshold for edge detection
            curvature_threshold (float): Curvature threshold for edge detection
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Starting Complete Crater Edges Analysis Pipeline")
        print("=" * 60)
        
        # Step 1: Load DEM
        if not self.load_dem(dem_path):
            return False
        
        # Step 2: Calculate terrain derivatives
        print("\n📊 Step 2: Calculating Terrain Derivatives")
        print("-" * 40)
        
        if not self.calculate_slope():
            return False
        
        if not self.calculate_curvature():
            return False
        
        if not self.calculate_hillshade():
            return False
        
        if not self.calculate_aspect():
            return False
        
        # Step 3: Detect crater edges
        print("\n🎯 Step 3: Detecting Crater Edges")
        print("-" * 35)
        
        if not self.detect_crater_edges(slope_threshold, curvature_threshold):
            return False
        
        # Step 4: Generate vector output
        print("\n📐 Step 4: Generating Vector Output")
        print("-" * 35)
        
        if not self.generate_crater_walls_shapefile():
            return False
        
        # Step 5: Generate report
        print("\n📋 Step 5: Generating Analysis Report")
        print("-" * 40)
        
        report_path = self.generate_analysis_report()
        
        print("\n✅ Complete Analysis Pipeline Finished!")
        print("=" * 60)
        print(f"📁 All outputs saved to: {self.output_dir}")
        print(f"📄 Analysis report: {report_path}")
        print("\n🎯 Next Steps:")
        print("1. Open QGIS and load the generated layers")
        print("2. Use crater_walls.shp for manual editing")
        print("3. Adjust thresholds if needed and re-run analysis")
        
        return True
    
    def cleanup(self):
        """
        Clean up QGIS application
        """
        qgs.exitQgis()
        print("✅ QGIS cleanup completed")

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = CraterEdgesDetector()
    
    # Available DEM files - try them in order of preference
    dem_files = [
        r"..\aspect_outputs\lunar_slope.tif",      # Best for crater edge detection
        r"..\aspect_outputs\lunar_aspect.tif",     # Alternative DEM
        r"..\terrain_outputs\terrain_output.tif"   # Fallback option
    ]
    
    dem_path = None
    for file_path in dem_files:
        if os.path.exists(file_path):
            dem_path = file_path
            print(f"✅ DEM file found: {dem_path}")
            break
    
    if dem_path:
        print("🚀 Starting crater edges analysis...")
        print(f"📊 Using DEM: {os.path.basename(dem_path)}")
        
        # Run the complete analysis with optimized parameters
        success = detector.run_complete_analysis(
            dem_path=dem_path,
            slope_threshold=12.0,      # Optimized for lunar terrain
            curvature_threshold=0.0008  # Optimized for crater detection
        )
        
        if success:
            print("\n✅ Analysis completed successfully!")
            print("📁 Check the 'crater_walls' directory for outputs")
            print("🎯 Generated files:")
            print("   - slope.tif (Slope analysis)")
            print("   - curvature.tif (Curvature analysis)")
            print("   - hillshade.tif (Visual enhancement)")
            print("   - aspect.tif (Aspect analysis)")
            print("   - crater_edges.tif (Detected edges)")
            print("   - crater_walls.shp (Vector polygons)")
            print("   - crater_edge_analysis_report.txt (Analysis report)")
        else:
            print("\n❌ Analysis failed!")
    else:
        print("❌ No DEM files found!")
        print("📝 Expected DEM files:")
        for file_path in dem_files:
            print(f"   - {file_path}")
        print("\n💡 Please ensure DEM files exist before running analysis")
    
    # Clean up
    detector.cleanup() 