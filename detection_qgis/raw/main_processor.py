"""
🌙 Lunar Analysis Main Processor
Comprehensive tool for lunar terrain analysis including:
- TIF file processing and loading
- Boulder detection using multiple methods
- Slope analysis (moon-specific)
- Curvature analysis
- Elevation statistics
- Visualization capabilities

Author: Lunar Analysis System
Version: 1.0
"""

import sys
import os
import numpy as np
from typing import Optional, Dict, List, Tuple
import json

# =============================================================================
# 🔧 CONFIGURATION SECTION - EDIT THESE PATHS
# =============================================================================

class Config:
    """Configuration class for all paths and settings"""
    
    # QGIS Installation Path (change this to your QGIS installation)
    QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.40.9"
    
    # Input/Output Paths (change these to your actual paths)
    INPUT_TIF_PATH = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    OUTPUT_FOLDER = r"E:\moon extract\data\derived\20250207\analysis_output"
    
    # Boulder Detection Settings
    BOULDER_DETECTION_MIN_AREA = 100
    BOULDER_DETECTION_MAX_AREA = 10000
    BOULDER_DETECTION_MIN_DISTANCE = 20
    
    # Slope Analysis Settings
    SLOPE_SCALE_FACTOR = 1.0
    SLOPE_AS_PERCENT = False
    
    # Processing Settings
    ENABLE_PROCESSING_MODULE = True
    SAMPLE_SIZE_LIMIT = 1000  # For large files
    
    # Output File Names
    SLOPE_OUTPUT = "slope_analysis.tif"
    ASPECT_OUTPUT = "aspect_analysis.tif"
    BOULDER_OUTPUT = "boulder_detection.json"
    CURVATURE_OUTPUT = "curvature_analysis.json"
    STATISTICS_OUTPUT = "elevation_statistics.json"

# =============================================================================
# QGIS SETUP
# =============================================================================

def setup_qgis():
    """Initialize QGIS environment"""
    try:
        # Set environment variables for QGIS 3.40.9
        os.environ["QGIS_PREFIX_PATH"] = Config.QGIS_PREFIX_PATH
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(Config.QGIS_PREFIX_PATH, "apps", "Qt5", "plugins")
        os.environ["PATH"] += ";" + os.path.join(Config.QGIS_PREFIX_PATH, "apps", "qgis", "bin")
        os.environ["PATH"] += ";" + os.path.join(Config.QGIS_PREFIX_PATH, "apps", "Python39")
        os.environ["PATH"] += ";" + os.path.join(Config.QGIS_PREFIX_PATH, "apps", "Python39", "Scripts")
        
        # Set additional QGIS environment variables
        os.environ["GDAL_DATA"] = os.path.join(Config.QGIS_PREFIX_PATH, "share", "gdal")
        os.environ["PROJ_LIB"] = os.path.join(Config.QGIS_PREFIX_PATH, "share", "proj")
        
        # Add QGIS Python paths
        qgis_python_path = os.path.join(Config.QGIS_PREFIX_PATH, "apps", "qgis", "python")
        qgis_python39_path = os.path.join(Config.QGIS_PREFIX_PATH, "apps", "Python39", "Lib", "site-packages")
        
        if qgis_python_path not in sys.path:
            sys.path.insert(0, qgis_python_path)
        if qgis_python39_path not in sys.path:
            sys.path.insert(0, qgis_python39_path)
        
        print(f"🔧 QGIS Environment Setup:")
        print(f"   - QGIS Prefix: {Config.QGIS_PREFIX_PATH}")
        print(f"   - Python Path: {qgis_python_path}")
        print(f"   - Site Packages: {qgis_python39_path}")
        
        # Initialize QGIS Application
        from qgis.core import QgsApplication
        qgs = QgsApplication([], False)
        qgs.setPrefixPath(Config.QGIS_PREFIX_PATH, True)
        qgs.initQgis()
        
        # Import QGIS modules
        from qgis.core import QgsRasterLayer, QgsProject
        from qgis.analysis import QgsNativeAlgorithms
        
        # Register algorithms
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
        
        # Try to import processing
        try:
            import processing
            Config.ENABLE_PROCESSING_MODULE = True
            print("✅ QGIS setup completed successfully!")
            print("✅ Processing module available")
        except ImportError:
            Config.ENABLE_PROCESSING_MODULE = False
            print("✅ QGIS setup completed successfully!")
            print("⚠️ Processing module not available - some functions will be limited")
        
        return qgs
        
    except Exception as e:
        print(f"❌ QGIS setup failed: {e}")
        print(f"   - Error details: {str(e)}")
        print(f"   - Please ensure QGIS 3.40.9 is installed at: {Config.QGIS_PREFIX_PATH}")
        return None

# =============================================================================
# MAIN PROCESSOR CLASS
# =============================================================================

class LunarAnalysisProcessor:
    """Main processor class that handles all lunar analysis tasks"""
    
    def __init__(self):
        """Initialize the processor"""
        self.qgs = setup_qgis()
        if self.qgs is None:
            raise Exception("Failed to initialize QGIS")
        
        self.project = None
        self.layers = {}
        self.results = {}
        
        # Import required modules
        from qgis.core import QgsProject
        self.project = QgsProject.instance()
        
        print("🌙 Lunar Analysis Processor initialized successfully!")
    
    def validate_paths(self) -> bool:
        """Validate that all required paths exist"""
        print("🔍 Validating paths...")
        
        # Check QGIS installation
        if not os.path.exists(Config.QGIS_PREFIX_PATH):
            print(f"❌ QGIS installation not found at: {Config.QGIS_PREFIX_PATH}")
            return False
        
        # Check input file
        if not os.path.exists(Config.INPUT_TIF_PATH):
            print(f"❌ Input TIF file not found at: {Config.INPUT_TIF_PATH}")
            return False
        
        # Create output folder if it doesn't exist
        if not os.path.exists(Config.OUTPUT_FOLDER):
            os.makedirs(Config.OUTPUT_FOLDER)
            print(f"📁 Created output folder: {Config.OUTPUT_FOLDER}")
        
        print("✅ All paths validated successfully!")
        return True
    
    def load_tif_file(self, layer_name: str = "Lunar_DEM") -> bool:
        """Load TIF file into QGIS"""
        try:
            from qgis.core import QgsRasterLayer
            
            print(f"📁 Loading TIF file: {Config.INPUT_TIF_PATH}")
            
            # Create raster layer
            raster_layer = QgsRasterLayer(Config.INPUT_TIF_PATH, layer_name)
            
            if not raster_layer.isValid():
                print(f"❌ Failed to load raster: {Config.INPUT_TIF_PATH}")
                return False
            
            # Add to project
            self.project.addMapLayer(raster_layer)
            self.layers[layer_name] = raster_layer
            
            print(f"✅ Successfully loaded raster:")
            print(f"   - Width: {raster_layer.width()} pixels")
            print(f"   - Height: {raster_layer.height()} pixels")
            print(f"   - Extent: {raster_layer.extent()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading TIF file: {e}")
            return False
    
    def calculate_slope(self) -> bool:
        """Calculate slope from the loaded raster"""
        try:
            if not Config.ENABLE_PROCESSING_MODULE:
                print("❌ Processing module not available. Cannot calculate slope.")
                return False
            
            import processing
            
            # Get the first loaded layer
            if not self.layers:
                print("❌ No layers loaded. Please load a TIF file first.")
                return False
            
            layer_name = list(self.layers.keys())[0]
            input_layer = self.layers[layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(Config.OUTPUT_FOLDER, Config.SLOPE_OUTPUT)
            
            print(f"🌙 Calculating slope...")
            print(f"   - Input: {layer_name}")
            print(f"   - Scale factor: {Config.SLOPE_SCALE_FACTOR}")
            print(f"   - Output as percentage: {Config.SLOPE_AS_PERCENT}")
            
            # Run slope calculation
            result = processing.run("gdal:slope", {
                'INPUT': input_path,
                'SCALE': Config.SLOPE_SCALE_FACTOR,
                'AS_PERCENT': Config.SLOPE_AS_PERCENT,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Slope calculation completed!")
            print(f"   - Output saved to: {output_path}")
            
            # Load the slope layer
            slope_layer = QgsRasterLayer(output_path, "Slope")
            if slope_layer.isValid():
                self.project.addMapLayer(slope_layer)
                self.layers["Slope"] = slope_layer
                self.results['slope_path'] = output_path
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating slope: {e}")
            return False
    
    def calculate_aspect(self) -> bool:
        """Calculate aspect from the loaded raster"""
        try:
            if not Config.ENABLE_PROCESSING_MODULE:
                print("❌ Processing module not available. Cannot calculate aspect.")
                return False
            
            import processing
            
            # Get the first loaded layer
            if not self.layers:
                print("❌ No layers loaded. Please load a TIF file first.")
                return False
            
            layer_name = list(self.layers.keys())[0]
            input_layer = self.layers[layer_name]
            input_path = input_layer.source()
            output_path = os.path.join(Config.OUTPUT_FOLDER, Config.ASPECT_OUTPUT)
            
            print(f"🌙 Calculating aspect...")
            
            # Run aspect calculation
            result = processing.run("gdal:aspect", {
                'INPUT': input_path,
                'COMPUTE_EDGES': True,
                'ZEVENBERGEN': False,
                'TRIG_ANGLE': False,
                'ZERO_FLAT': False,
                'OUTPUT': output_path
            })
            
            print(f"✅ Aspect calculation completed!")
            print(f"   - Output saved to: {output_path}")
            
            # Load the aspect layer
            aspect_layer = QgsRasterLayer(output_path, "Aspect")
            if aspect_layer.isValid():
                self.project.addMapLayer(aspect_layer)
                self.layers["Aspect"] = aspect_layer
                self.results['aspect_path'] = output_path
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating aspect: {e}")
            return False
    
    def detect_boulders(self) -> bool:
        """Detect boulders using multiple methods"""
        try:
            print("🪨 Detecting boulders...")
            
            # Import boulder detection modules
            import cv2
            from scipy import ndimage
            from skimage import feature, morphology, measure, filters
            from skimage.segmentation import watershed
            from skimage.feature import peak_local_maxima
            import rasterio
            
            # Load the TIF file as numpy array
            with rasterio.open(Config.INPUT_TIF_PATH) as src:
                image = src.read(1)
                height, width = image.shape
                
                print(f"   - Image shape: {image.shape}")
                print(f"   - Data type: {image.dtype}")
                print(f"   - Min value: {np.min(image)}")
                print(f"   - Max value: {np.max(image)}")
            
            # Preprocess image
            normalized = ((image - np.min(image)) / 
                         (np.max(image) - np.min(image)) * 255).astype(np.uint8)
            blurred = cv2.GaussianBlur(normalized, (5, 5), 0)
            
            # Method 1: Edge-based detection
            print("   - Method 1: Edge-based detection")
            edges = cv2.Canny(blurred, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            edge_boulders = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if Config.BOULDER_DETECTION_MIN_AREA <= area <= Config.BOULDER_DETECTION_MAX_AREA:
                    x, y, w, h = cv2.boundingRect(contour)
                    edge_boulders.append({
                        'method': 'edge',
                        'bbox': [x, y, x+w, y+h],
                        'area': area,
                        'confidence': min(area / Config.BOULDER_DETECTION_MAX_AREA, 1.0)
                    })
            
            # Method 2: Watershed detection
            print("   - Method 2: Watershed detection")
            distance = ndimage.distance_transform_edt(blurred)
            local_max_coords = peak_local_maxima(distance, 
                                               min_distance=Config.BOULDER_DETECTION_MIN_DISTANCE,
                                               labels=blurred)
            local_max = np.zeros_like(blurred, dtype=bool)
            local_max[tuple(local_max_coords.T)] = True
            markers = measure.label(local_max)
            watershed_result = watershed(-distance, markers, mask=blurred)
            
            watershed_boulders = []
            for region in measure.regionprops(watershed_result):
                if Config.BOULDER_DETECTION_MIN_AREA <= region.area <= Config.BOULDER_DETECTION_MAX_AREA:
                    watershed_boulders.append({
                        'method': 'watershed',
                        'bbox': region.bbox,
                        'area': region.area,
                        'confidence': min(region.area / Config.BOULDER_DETECTION_MAX_AREA, 1.0)
                    })
            
            # Combine detections
            all_boulders = edge_boulders + watershed_boulders
            
            # Remove duplicates
            final_boulders = self._remove_duplicate_boulders(all_boulders)
            
            print(f"✅ Boulder detection completed!")
            print(f"   - Edge-based detections: {len(edge_boulders)}")
            print(f"   - Watershed detections: {len(watershed_boulders)}")
            print(f"   - Final unique detections: {len(final_boulders)}")
            
            # Save results
            output_path = os.path.join(Config.OUTPUT_FOLDER, Config.BOULDER_OUTPUT)
            with open(output_path, 'w') as f:
                json.dump(final_boulders, f, indent=2)
            
            self.results['boulder_detection'] = final_boulders
            self.results['boulder_path'] = output_path
            
            return True
            
        except Exception as e:
            print(f"❌ Error detecting boulders: {e}")
            return False
    
    def _remove_duplicate_boulders(self, boulders: List[Dict], distance_threshold: int = 20) -> List[Dict]:
        """Remove duplicate boulder detections"""
        if not boulders:
            return []
        
        # Calculate centroids
        for boulder in boulders:
            bbox = boulder['bbox']
            boulder['centroid'] = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
        
        # Remove duplicates based on distance
        unique_boulders = []
        for boulder in boulders:
            is_duplicate = False
            for unique_boulder in unique_boulders:
                dist = np.sqrt((boulder['centroid'][0] - unique_boulder['centroid'][0])**2 + 
                             (boulder['centroid'][1] - unique_boulder['centroid'][1])**2)
                if dist < distance_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_boulders.append(boulder)
        
        return unique_boulders
    
    def calculate_curvature(self) -> bool:
        """Calculate curvature statistics"""
        try:
            print("🌙 Calculating curvature statistics...")
            
            # Get the first loaded layer
            if not self.layers:
                print("❌ No layers loaded. Please load a TIF file first.")
                return False
            
            layer_name = list(self.layers.keys())[0]
            layer = self.layers[layer_name]
            provider = layer.dataProvider()
            
            # Read a sample of the data
            width = layer.width()
            height = layer.height()
            sample_width = min(width, Config.SAMPLE_SIZE_LIMIT)
            sample_height = min(height, Config.SAMPLE_SIZE_LIMIT)
            
            block = provider.block(1, layer.extent(), sample_width, sample_height)
            data = np.array(block.data()).reshape((sample_height, sample_width))
            
            # Calculate curvatures
            cellsize = 1.0  # Assuming 1 meter resolution
            curvatures = self._compute_curvatures(data, cellsize)
            
            # Calculate statistics
            curvature_stats = {}
            for name, curvature in curvatures.items():
                curvature_stats[name] = {
                    'mean': float(np.mean(curvature)),
                    'std': float(np.std(curvature)),
                    'min': float(np.min(curvature)),
                    'max': float(np.max(curvature))
                }
            
            print(f"✅ Curvature analysis completed!")
            for name, stats in curvature_stats.items():
                print(f"   - {name.capitalize()} curvature:")
                print(f"     * Mean: {stats['mean']:.6f}")
                print(f"     * Std: {stats['std']:.6f}")
                print(f"     * Range: {stats['min']:.6f} to {stats['max']:.6f}")
            
            # Save results
            output_path = os.path.join(Config.OUTPUT_FOLDER, Config.CURVATURE_OUTPUT)
            with open(output_path, 'w') as f:
                json.dump(curvature_stats, f, indent=2)
            
            self.results['curvature_analysis'] = curvature_stats
            self.results['curvature_path'] = output_path
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating curvature: {e}")
            return False
    
    def _compute_curvatures(self, elevation: np.ndarray, cellsize: float = 1.0) -> Dict[str, np.ndarray]:
        """Compute various curvature measures"""
        # First and second derivatives
        dzdx = np.gradient(elevation, axis=1) / cellsize
        dzdy = np.gradient(elevation, axis=0) / cellsize
        d2zdx2 = np.gradient(dzdx, axis=1) / cellsize
        d2zdy2 = np.gradient(dzdy, axis=0) / cellsize
        d2zdxdy = np.gradient(dzdx, axis=0) / cellsize
        
        # Slope and aspect
        p = dzdx
        q = dzdy
        r = d2zdx2
        s = d2zdxdy
        t = d2zdy2
        grad2 = p**2 + q**2
        grad = np.sqrt(grad2)
        denom = (1 + grad2)
        denom_sqrt = np.sqrt(denom)
        
        # Profile curvature (in the direction of steepest slope)
        profile_curv = -(r * p**2 + 2 * s * p * q + t * q**2) / (grad2 * denom_sqrt + 1e-10)
        # Plan curvature (perpendicular to slope direction)
        plan_curv = (r * q**2 - 2 * s * p * q + t * p**2) / (grad2 * denom_sqrt + 1e-10)
        # General curvature (Gaussian curvature)
        gaussian_curv = (r * t - s**2) / (denom**2 + 1e-10)
        # Mean curvature (average of principal curvatures)
        mean_curv = 0.5 * (r + t) / (denom_sqrt**3 + 1e-10)
        
        return {
            'profile': profile_curv,
            'plan': plan_curv,
            'gaussian': gaussian_curv,
            'mean': mean_curv
        }
    
    def calculate_elevation_statistics(self) -> bool:
        """Calculate elevation statistics"""
        try:
            print("🌙 Calculating elevation statistics...")
            
            # Get the first loaded layer
            if not self.layers:
                print("❌ No layers loaded. Please load a TIF file first.")
                return False
            
            layer_name = list(self.layers.keys())[0]
            layer = self.layers[layer_name]
            provider = layer.dataProvider()
            
            # Get statistics
            stats = provider.bandStatistics(1)
            min_elev = stats.minimumValue
            max_elev = stats.maximumValue
            mean_elev = stats.mean
            std_elev = stats.stdDev
            elev_range = max_elev - min_elev
            
            elevation_stats = {
                'min': float(min_elev),
                'max': float(max_elev),
                'mean': float(mean_elev),
                'range': float(elev_range),
                'std': float(std_elev)
            }
            
            print(f"✅ Elevation statistics completed!")
            print(f"🌑 Elevation Statistics (Lunar DEM):")
            print(f"   - Minimum Elevation: {min_elev:.2f}")
            print(f"   - Maximum Elevation: {max_elev:.2f}")
            print(f"   - Mean Elevation: {mean_elev:.2f}")
            print(f"   - Elevation Range: {elev_range:.2f}")
            print(f"   - Standard Deviation: {std_elev:.2f}")
            
            # Save results
            output_path = os.path.join(Config.OUTPUT_FOLDER, Config.STATISTICS_OUTPUT)
            with open(output_path, 'w') as f:
                json.dump(elevation_stats, f, indent=2)
            
            self.results['elevation_statistics'] = elevation_stats
            self.results['statistics_path'] = output_path
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating elevation statistics: {e}")
            return False
    
    def list_layers(self):
        """List all loaded layers"""
        print("\n📋 Loaded Layers:")
        for name, layer in self.layers.items():
            print(f"   - {name}: {layer.source()}")
    
    def print_results_summary(self):
        """Print summary of all results"""
        print("\n📊 Analysis Results Summary:")
        print("=" * 50)
        
        if 'slope_path' in self.results:
            print(f"✅ Slope analysis: {self.results['slope_path']}")
        
        if 'aspect_path' in self.results:
            print(f"✅ Aspect analysis: {self.results['aspect_path']}")
        
        if 'boulder_detection' in self.results:
            boulder_count = len(self.results['boulder_detection'])
            print(f"✅ Boulder detection: {boulder_count} boulders found")
            print(f"   - Results saved to: {self.results['boulder_path']}")
        
        if 'curvature_analysis' in self.results:
            print(f"✅ Curvature analysis: {len(self.results['curvature_analysis'])} curvature types calculated")
            print(f"   - Results saved to: {self.results['curvature_path']}")
        
        if 'elevation_statistics' in self.results:
            print(f"✅ Elevation statistics: Basic statistics calculated")
            print(f"   - Results saved to: {self.results['statistics_path']}")
        
        print(f"\n📁 All output files saved to: {Config.OUTPUT_FOLDER}")
    
    def cleanup(self):
        """Cleanup QGIS resources"""
        if self.qgs:
            self.qgs.exitQgis()
        print("✅ QGIS cleanup completed")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function"""
    print("🌙 Lunar Analysis Main Processor")
    print("=" * 50)
    
    try:
        # Initialize processor
        processor = LunarAnalysisProcessor()
        
        # Validate paths
        if not processor.validate_paths():
            print("❌ Path validation failed. Please check your configuration.")
            return
        
        # Load TIF file
        if not processor.load_tif_file():
            print("❌ Failed to load TIF file.")
            return
        
        # Run analyses
        print("\n🚀 Starting lunar analysis...")
        
        # 1. Elevation statistics
        processor.calculate_elevation_statistics()
        
        # 2. Slope analysis
        processor.calculate_slope()
        
        # 3. Aspect analysis
        processor.calculate_aspect()
        
        # 4. Boulder detection
        processor.detect_boulders()
        
        # 5. Curvature analysis
        processor.calculate_curvature()
        
        # Print summary
        processor.list_layers()
        processor.print_results_summary()
        
        print("\n✅ All analyses completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
    
    finally:
        # Cleanup
        if 'processor' in locals():
            processor.cleanup()

def show_menu():
    """Show interactive menu"""
    print("\n🌙 Lunar Analysis Menu")
    print("=" * 30)
    print("1. Load TIF file")
    print("2. Calculate elevation statistics")
    print("3. Calculate slope")
    print("4. Calculate aspect")
    print("5. Detect boulders")
    print("6. Calculate curvature")
    print("7. Run all analyses")
    print("8. List loaded layers")
    print("9. Show results summary")
    print("0. Exit")
    print("=" * 30)
    
    return input("Enter your choice (0-9): ").strip()

def interactive_mode():
    """Run in interactive mode"""
    print("🌙 Lunar Analysis Main Processor - Interactive Mode")
    print("=" * 60)
    
    try:
        processor = LunarAnalysisProcessor()
        
        if not processor.validate_paths():
            print("❌ Path validation failed. Please check your configuration.")
            return
        
        while True:
            choice = show_menu()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            
            elif choice == "1":
                processor.load_tif_file()
            
            elif choice == "2":
                processor.calculate_elevation_statistics()
            
            elif choice == "3":
                processor.calculate_slope()
            
            elif choice == "4":
                processor.calculate_aspect()
            
            elif choice == "5":
                processor.detect_boulders()
            
            elif choice == "6":
                processor.calculate_curvature()
            
            elif choice == "7":
                print("🚀 Running all analyses...")
                processor.calculate_elevation_statistics()
                processor.calculate_slope()
                processor.calculate_aspect()
                processor.detect_boulders()
                processor.calculate_curvature()
                processor.print_results_summary()
            
            elif choice == "8":
                processor.list_layers()
            
            elif choice == "9":
                processor.print_results_summary()
            
            else:
                print("❌ Invalid choice. Please enter a number between 0 and 9.")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        if 'processor' in locals():
            processor.cleanup()

if __name__ == "__main__":
    print("🚀 Starting Lunar Analysis Main Processor...")
    print("⚠️  IMPORTANT: Edit the Config class in this file to set your paths!")
    print()
    
    # Check if interactive mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main() 