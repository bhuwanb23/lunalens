import sys
import os
import numpy as np
from datetime import datetime

# ✅ 1. QGIS installation path (update if needed)
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"

# Add processing module path
PROCESSING_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python", "plugins")

# ✅ 2. Set required environment variables
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")

# ✅ 3. Add QGIS Python path to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "Python312")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# Add QGIS Python path
QGIS_QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python")
if QGIS_QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_QGIS_PYTHON_PATH)

# Add processing module path
if PROCESSING_PATH not in sys.path:
    sys.path.insert(0, PROCESSING_PATH)

# ✅ 4. Initialize QGIS Application (only if not already initialized)
from qgis.core import QgsApplication
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
            sys.path.append(os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python", "plugins", "processing"))
            import processing
            PROCESSING_AVAILABLE = True
            print("✅ Processing module available (alternative path)")
        except ImportError:
            try:
                # Try another alternative path
                processing_path = os.path.join(QGIS_PREFIX_PATH, "apps", "qgis-ltr", "python", "plugins")
                if processing_path not in sys.path:
                    sys.path.insert(0, processing_path)
                import processing
                PROCESSING_AVAILABLE = True
                print("✅ Processing module available (third path)")
            except ImportError:
                PROCESSING_AVAILABLE = False
                print("⚠️  Processing module not available - some functions will be limited")
                print("   This may affect slope, curvature, hillshade, and flow calculations")
                print("   Available paths checked:")
                print(f"   - {os.path.join(QGIS_PREFIX_PATH, 'apps', 'qgis-ltr', 'python', 'plugins')}")
                print(f"   - {os.path.join(QGIS_PREFIX_PATH, 'apps', 'qgis-ltr', 'python', 'plugins', 'processing')}")

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

class DebrisFlowPathsDetector:
    def __init__(self, output_dir="debris_path_output"):
        """
        Initialize the Debris Flow Paths Detector
        
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
        Load Digital Elevation Model (DEM) for debris flow analysis
        
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
        Calculate slope map for debris flow initiation zones
        
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
        Calculate hillshade for visual enhancement of debris flow paths
        
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
    
    def detect_debris_flow_paths(self, slope_threshold=20.0):
        """
        Detect debris flow paths based on slope threshold
        
        Args:
            slope_threshold (float): Minimum slope angle for debris flow initiation (degrees)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot detect debris flow paths.")
            return False
            
        try:
            if 'slope' not in self.layers:
                print("❌ Slope layer required for debris flow path detection")
                return False
            
            print(f"🔄 Detecting debris flow paths...")
            print(f"   - Slope threshold: {slope_threshold}°")
            
            # Create debris flow paths raster using raster calculator
            slope_path = self.layers['slope'].source()
            output_path = os.path.join(self.output_dir, "debris_flow_paths.tif")
            
            # Raster calculator expression for debris flow detection
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
            
            print(f"✅ Debris flow paths detection completed!")
            
            # Load the result
            debris_layer = QgsRasterLayer(output_path, "Debris_Flow_Paths")
            if debris_layer.isValid():
                self.project.addMapLayer(debris_layer)
                self.layers["Debris_Flow_Paths"] = debris_layer
                
                # Get statistics
                provider = debris_layer.dataProvider()
                stats = provider.bandStatistics(1)
                print(f"   - Detected debris flow pixels: {stats.sum}")
                print(f"   - Debris flow density: {(stats.sum / (debris_layer.width() * debris_layer.height()) * 100):.2f}%")
                
                self.detection_results['debris_flow_paths'] = {
                    'path': output_path,
                    'thresholds': {
                        'slope': slope_threshold
                    },
                    'stats': {
                        'debris_pixels': stats.sum,
                        'density_percent': (stats.sum / (debris_layer.width() * debris_layer.height()) * 100)
                    }
                }
            
            return True
            
        except Exception as e:
            print(f"❌ Error detecting debris flow paths: {e}")
            return False
    
    def generate_debris_shapefile(self, output_name="debris_flow_paths"):
        """
        Convert debris flow paths raster to vector shapefile for manual editing
        
        Args:
            output_name (str): Name for output shapefile
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not PROCESSING_AVAILABLE:
            print("❌ Processing module not available. Cannot generate shapefile.")
            return False
            
        try:
            if "Debris_Flow_Paths" not in self.layers:
                print("❌ Debris flow paths layer not found")
                return False
            
            print(f"🔄 Converting debris flow paths to vector...")
            
            input_path = self.layers["Debris_Flow_Paths"].source()
            output_path = os.path.join(self.output_dir, f"{output_name}.shp")
            
            # Convert raster to vector
            result = processing.run("gdal:polygonize", {
                'INPUT': input_path,
                'BAND': 1,
                'FIELD': 'DN',
                'EIGHT_CONNECTEDNESS': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Debris flow paths shapefile generated!")
            print(f"   - Output: {output_path}")
            
            # Load the result
            debris_layer = QgsVectorLayer(output_path, output_name, "ogr")
            if debris_layer.isValid():
                self.project.addMapLayer(debris_layer)
                self.layers[output_name] = debris_layer
                
                # Get feature count
                feature_count = debris_layer.featureCount()
                print(f"   - Number of debris flow features: {feature_count}")
                
                self.detection_results['debris_vector'] = {
                    'path': output_path,
                    'feature_count': feature_count
                }
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating debris flow paths shapefile: {e}")
            return False
    
    def run_complete_analysis(self, dem_path, slope_threshold=20.0):
        """
        Run complete debris flow paths analysis pipeline
        
        Args:
            dem_path (str): Path to input DEM file
            slope_threshold (float): Slope threshold for debris flow detection
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Starting Complete Debris Flow Paths Analysis Pipeline")
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
        
        # Step 3: Detect debris flow paths
        print("\n🎯 Step 3: Detecting Debris Flow Paths")
        print("-" * 40)
        
        if not self.detect_debris_flow_paths(slope_threshold):
            return False
        
        # Step 4: Generate vector output
        print("\n📐 Step 4: Generating Vector Output")
        print("-" * 35)
        
        if not self.generate_debris_shapefile():
            return False
        
        print("\n✅ Complete Analysis Pipeline Finished!")
        print("=" * 60)
        print(f"📁 All outputs saved to: {self.output_dir}")
        print("\n🎯 Next Steps:")
        print("1. Open QGIS and load the generated layers")
        print("2. Use debris_flow_paths.shp for manual editing")
        print("3. Adjust thresholds if needed and re-run analysis")
        print("4. Consider temporal analysis for debris flow monitoring")
        print("5. Overlay with optical imagery for visual confirmation")
        
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
    detector = DebrisFlowPathsDetector()
    
    # Available DEM files - try them in order of preference
    dem_files = [
        r"aspect_outputs\lunar_slope.tif",      # Best for debris flow detection
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
        print("🚀 Starting debris flow paths analysis...")
        print(f"📊 Using DEM: {os.path.basename(dem_path)}")
        
        # Run the complete analysis with optimized parameters
        success = detector.run_complete_analysis(
            dem_path=dem_path,
            slope_threshold=18.0      # Optimized for lunar terrain
        )
        
        if success:
            print("\n✅ Analysis completed successfully!")
            print("📁 Check the 'debris_path_output' directory for outputs")
            print("🎯 Generated files:")
            print("   - slope.tif (Slope analysis)")
            print("   - hillshade.tif (Visual enhancement)")
            print("   - debris_flow_paths.tif (Detected paths)")
            print("   - debris_flow_paths.shp (Vector polygons)")
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