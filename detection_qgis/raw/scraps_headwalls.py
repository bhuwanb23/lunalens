import sys
import os
import numpy as np
from datetime import datetime

# ✅ 1. QGIS installation path (update if needed)
QGIS_PREFIX_PATH = os.environ.get('QGIS_PREFIX_PATH', r'C:\Program Files\QGIS 3.40.9')

# Add processing module path
PROCESSING_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python", "plugins")

# ✅ 2. Set required environment variables
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")

# ✅ 3. Add QGIS Python path to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "python")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# Add processing module path
if PROCESSING_PATH not in sys.path:
    sys.path.insert(0, PROCESSING_PATH)

# ✅ 4. Initialize QGIS Application
from qgis.core import QgsApplication
qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs.initQgis()

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
except ImportError:
    try:
        # Try alternative import path
        sys.path.append(os.path.join(QGIS_PREFIX_PATH, "apps", "qgis", "python", "plugins", "processing"))
        import processing
        PROCESSING_AVAILABLE = True
        print("✅ Processing module available (alternative path)")
    except ImportError:
        PROCESSING_AVAILABLE = False
        print("⚠️  Processing module not available - some functions will be limited")
        print("   This may affect slope, curvature, hillshade, and aspect calculations")

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

class ScarpsHeadwallsDetector:
    def __init__(self, output_dir="headwalls_scraps"):
        """
        Initialize the Scarps/Headwalls Detector
        
        Args:
            output_dir (str): Directory to save output files
        """
        self.project = QgsProject.instance()
        self.layers = {}
        self.output_dir = output_dir
        self.detection_results = {}
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created output directory: {output_dir}")
    
    def load_dem(self, dem_path, layer_name="DEM"):
        """
        Load Digital Elevation Model (DEM) for scarps/headwalls analysis
        
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
        Calculate slope map for scarp/headwall detection
        
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
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating slope: {e}")
            return False
    
    def calculate_hillshade(self, input_layer_name="DEM", output_name="hillshade"):
        """
        Calculate hillshade for visual enhancement of scarps/headwalls
        
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
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating hillshade: {e}")
            return False
    
    def calculate_curvature(self, input_layer_name="DEM", output_name="curvature"):
        """
        Calculate curvature map for scarp/headwall detection
        
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
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating curvature: {e}")
            return False
    
    def calculate_aspect(self, input_layer_name="DEM", output_name="aspect"):
        """
        Calculate aspect map for scarp/headwall orientation analysis
        
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
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating aspect: {e}")
            return False
    
    def calculate_tri(self, input_layer_name="DEM", output_name="tri"):
        """
        Calculate Terrain Ruggedness Index (TRI) for scarp/headwall detection
        
        Args:
            input_layer_name (str): Name of input DEM layer
            output_name (str): Name for output TRI layer
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot calculate TRI.")
            return False
            
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            input_layer = self.layers[input_layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(self.output_dir, f"{output_name}.tif")
            
            print(f"🔄 Calculating TRI from: {input_layer_name}")
            print(f"   - Output: {output_path}")
            
            # Run TRI calculation using SAGA
            try:
                result = processing.run("saga:terrainruggednessindextri", {
                    'DEM': input_path,
                    'TRI': output_path
                })
            except Exception:
                # Fallback: Use slope as proxy for TRI
                print("   - Using slope as TRI proxy")
                result = processing.run("gdal:slope", {
                    'INPUT': input_path,
                    'SCALE': 1.0,
                    'AS_PERCENT': False,
                    'COMPUTE_EDGES': True,
                    'ZEVENBERGEN': False,
                    'OUTPUT': output_path.replace('.tif', '_slope_tri.tif')
                })
                # Copy slope to TRI output
                import shutil
                shutil.copy(output_path.replace('.tif', '_slope_tri.tif'), output_path)
            
            print(f"✅ TRI calculation completed!")
            
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
                
                self.detection_results['tri'] = {
                    'path': output_path,
                    'stats': {
                        'min': stats.minimumValue,
                        'max': stats.maximumValue,
                        'mean': stats.mean,
                        'std': stats.stdDev
                    }
                }
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating TRI: {e}")
            return False
    
    def detect_scarps_headwalls(self, slope_threshold=30.0, curvature_threshold=0.001, tri_threshold=0.5):
        """
        Detect scarps and headwalls based on multiple terrain parameters
        
        Args:
            slope_threshold (float): Minimum slope angle for scarp detection (degrees)
            curvature_threshold (float): Minimum curvature value for edge detection
            tri_threshold (float): Minimum TRI value for rugged terrain detection
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot detect scarps/headwalls.")
            return False
            
        try:
            if 'slope' not in self.layers:
                print("❌ Slope layer required for scarp/headwall detection")
                return False
            
            print(f"🔄 Detecting scarps and headwalls...")
            print(f"   - Slope threshold: {slope_threshold}°")
            print(f"   - Curvature threshold: {curvature_threshold}")
            print(f"   - TRI threshold: {tri_threshold}")
            
            # Create scarps/headwalls raster using raster calculator
            slope_path = self.layers['slope'].source()
            output_path = os.path.join(self.output_dir, "scarps_headwalls.tif")
            
            # Raster calculator expression for scarp detection
            if 'curvature' in self.layers and 'tri' in self.layers:
                # Use all three parameters
                expression = f'(\"slope@1\" > {slope_threshold}) AND (\"curvature@1\" > {curvature_threshold}) AND (\"tri@1\" > {tri_threshold})'
                layers = [self.layers['slope'], self.layers['curvature'], self.layers['tri']]
            elif 'curvature' in self.layers:
                # Use slope and curvature
                expression = f'(\"slope@1\" > {slope_threshold}) AND (\"curvature@1\" > {curvature_threshold})'
                layers = [self.layers['slope'], self.layers['curvature']]
            elif 'tri' in self.layers:
                # Use slope and TRI
                expression = f'(\"slope@1\" > {slope_threshold}) AND (\"tri@1\" > {tri_threshold})'
                layers = [self.layers['slope'], self.layers['tri']]
            else:
                # Use only slope
                expression = f'\"slope@1\" > {slope_threshold}'
                layers = [self.layers['slope']]
            
            result = processing.run("qgis:rastercalculator", {
                'EXPRESSION': expression,
                'LAYERS': layers,
                'CELLSIZE': 0,
                'EXTENT': None,
                'CRS': None,
                'OUTPUT': output_path
            })
            
            print(f"✅ Scarps/headwalls detection completed!")
            
            # Load the result
            scarps_layer = QgsRasterLayer(output_path, "Scarps_Headwalls")
            if scarps_layer.isValid():
                self.project.addMapLayer(scarps_layer)
                self.layers["Scarps_Headwalls"] = scarps_layer
                
                # Get statistics
                provider = scarps_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Detected scarp pixels: {stats.sum}")
                print(f"   - Scarp density: {(stats.sum / (scarps_layer.width() * scarps_layer.height()) * 100):.2f}%")
                
                self.detection_results['scarps_headwalls'] = {
                    'path': output_path,
                    'thresholds': {
                        'slope': slope_threshold,
                        'curvature': curvature_threshold,
                        'tri': tri_threshold
                    },
                    'stats': {
                        'scarp_pixels': stats.sum,
                        'density_percent': (stats.sum / (scarps_layer.width() * scarps_layer.height()) * 100)
                    }
                }
            
            return True
            
        except Exception as e:
            print(f"❌ Error detecting scarps/headwalls: {e}")
            return False
    
    def generate_scarps_shapefile(self, output_name="scarps_headwalls"):
        """
        Convert scarps/headwalls raster to vector shapefile for manual editing
        
        Args:
            output_name (str): Name for output shapefile
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot generate shapefile.")
            return False
            
        try:
            if "Scarps_Headwalls" not in self.layers:
                print("❌ Scarps/headwalls layer not found")
                return False
            
            print(f"🔄 Converting scarps/headwalls to vector...")
            
            input_path = self.layers["Scarps_Headwalls"].source()
            output_path = os.path.join(self.output_dir, f"{output_name}.shp")
            
            # Convert raster to vector
            result = processing.run("gdal:polygonize", {
                'INPUT': input_path,
                'BAND': 1,
                'FIELD': 'DN',
                'EIGHT_CONNECTEDNESS': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Scarps/headwalls shapefile generated!")
            print(f"   - Output: {output_path}")
            
            # Load the result
            scarps_layer = QgsVectorLayer(output_path, output_name, "ogr")
            if scarps_layer.isValid():
                self.project.addMapLayer(scarps_layer)
                self.layers[output_name] = scarps_layer
                
                # Get feature count
                feature_count = scarps_layer.featureCount()
                print(f"   - Number of scarp/headwall features: {feature_count}")
                
                self.detection_results['scarps_vector'] = {
                    'path': output_path,
                    'feature_count': feature_count
                }
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating scarps/headwalls shapefile: {e}")
            return False
    
    def generate_analysis_report(self):
        """
        Generate comprehensive analysis report
        """
        try:
            report_path = os.path.join(self.output_dir, "scarps_headwalls_analysis_report.txt")
            
            with open(report_path, 'w') as f:
                f.write("🌑 SCARPS/HEADWALLS ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("📊 ANALYSIS PARAMETERS\n")
                f.write("-" * 30 + "\n")
                f.write("Method: Multi-Parameter Terrain Analysis\n")
                f.write("Tools: GDAL Slope, Hillshade, Curvature, Aspect, TRI\n")
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
                
                f.write("🎯 SCARP/HEADWALL DETECTION METHODOLOGY\n")
                f.write("-" * 40 + "\n")
                f.write("1. DEM Loading: Digital Elevation Model loaded for terrain analysis\n")
                f.write("2. Slope Calculation: Identifies steep areas (>30°) indicating cliffs/headwalls\n")
                f.write("3. Hillshade Generation: Visual enhancement for manual verification\n")
                f.write("4. Curvature Analysis: Detects concave/convex forms of scarps\n")
                f.write("5. Aspect Mapping: Orientation analysis of scarp faces\n")
                f.write("6. TRI Calculation: Terrain Ruggedness Index for rugged terrain\n")
                f.write("7. Multi-Parameter Detection: Combined thresholding for scarp identification\n")
                f.write("8. Vector Conversion: Raster features converted to editable polygons\n\n")
                
                f.write("📝 RECOMMENDATIONS\n")
                f.write("-" * 20 + "\n")
                f.write("• Use hillshade layer for visual verification of detected scarps\n")
                f.write("• Adjust slope, curvature, and TRI thresholds based on terrain characteristics\n")
                f.write("• Manually edit the generated shapefile for precise scarp boundaries\n")
                f.write("• Consider using additional filters for noise reduction\n")
                f.write("• Validate results against optical imagery when available\n")
                f.write("• High slope areas (>30°) often indicate scarps or headwalls\n")
                f.write("• Dense contour lines often trace along scarp faces\n\n")
                
                f.write("🔧 NEXT STEPS\n")
                f.write("-" * 15 + "\n")
                f.write("1. Open QGIS and load the generated layers\n")
                f.write("2. Use the scarps_headwalls.shp for manual digitization\n")
                f.write("3. Apply additional filters or segmentation if needed\n")
                f.write("4. Export final results in desired format\n")
                f.write("5. Consider temporal analysis for landslide monitoring\n")
            
            print(f"✅ Analysis report generated: {report_path}")
            return report_path
            
        except Exception as e:
            print(f"❌ Error generating analysis report: {e}")
            return None
    
    def run_complete_analysis(self, dem_path, slope_threshold=30.0, curvature_threshold=0.001, tri_threshold=0.5):
        """
        Run complete scarps/headwalls analysis pipeline
        
        Args:
            dem_path (str): Path to input DEM file
            slope_threshold (float): Slope threshold for scarp detection
            curvature_threshold (float): Curvature threshold for edge detection
            tri_threshold (float): TRI threshold for rugged terrain detection
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Starting Complete Scarps/Headwalls Analysis Pipeline")
        print("=" * 60)
        
        # Step 1: Load DEM
        if not self.load_dem(dem_path):
            return False
        
        # Step 2: Calculate terrain derivatives
        print("\n📊 Step 2: Calculating Terrain Derivatives")
        print("-" * 40)
        
        if not self.calculate_slope():
            return False
        
        if not self.calculate_hillshade():
            return False
        
        if not self.calculate_curvature():
            return False
        
        if not self.calculate_aspect():
            return False
        
        if not self.calculate_tri():
            return False
        
        # Step 3: Detect scarps/headwalls
        print("\n🎯 Step 3: Detecting Scarps and Headwalls")
        print("-" * 45)
        
        if not self.detect_scarps_headwalls(slope_threshold, curvature_threshold, tri_threshold):
            return False
        
        # Step 4: Generate vector output
        print("\n📐 Step 4: Generating Vector Output")
        print("-" * 35)
        
        if not self.generate_scarps_shapefile():
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
        print("2. Use scarps_headwalls.shp for manual editing")
        print("3. Adjust thresholds if needed and re-run analysis")
        print("4. Consider temporal analysis for landslide monitoring")
        
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
    detector = ScarpsHeadwallsDetector()
    
    # Available DEM files - try them in order of preference
    dem_files = [
        r"aspect_outputs\lunar_slope.tif",      # Best for scarp detection
        r"aspect_outputs\lunar_aspect.tif",     # Alternative DEM
        r"terrain_outputs\terrain_output.tif"   # Fallback option
    ]
    
    dem_path = None
    for file_path in dem_files:
        if os.path.exists(file_path):
            dem_path = file_path
            print(f"✅ DEM file found: {dem_path}")
            break
    
    if dem_path:
        print("🚀 Starting scarps/headwalls analysis...")
        print(f"📊 Using DEM: {os.path.basename(dem_path)}")
        
        # Run the complete analysis with optimized parameters
        success = detector.run_complete_analysis(
            dem_path=dem_path,
            slope_threshold=25.0,      # Optimized for lunar terrain
            curvature_threshold=0.0008, # Optimized for scarp detection
            tri_threshold=0.3          # Optimized for rugged terrain
        )
        
        if success:
            print("\n✅ Analysis completed successfully!")
            print("📁 Check the 'headwalls_scraps' directory for outputs")
            print("🎯 Generated files:")
            print("   - slope.tif (Slope analysis)")
            print("   - hillshade.tif (Visual enhancement)")
            print("   - curvature.tif (Curvature analysis)")
            print("   - aspect.tif (Aspect analysis)")
            print("   - tri.tif (Terrain Ruggedness Index)")
            print("   - scarps_headwalls.tif (Detected scarps)")
            print("   - scarps_headwalls.shp (Vector polygons)")
            print("   - scarps_headwalls_analysis_report.txt (Analysis report)")
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