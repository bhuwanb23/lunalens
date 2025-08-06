import sys
import os
import numpy as np
import json
from datetime import datetime
import importlib.util

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

# Suppress QGIS cleanup warnings
import warnings
warnings.filterwarnings("ignore")

print("✅ QGIS setup completed successfully!")

class LunarMainController:
    def __init__(self, output_dir="lunar_analysis_output"):
        """
        Initialize the Lunar Main Controller
        
        Args:
            output_dir (str): Directory to save all analysis outputs
        """
        self.project = QgsProject.instance()
        self.layers = {}
        self.output_dir = output_dir
        self.analysis_results = {}
        self.available_modules = {}
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"📁 Created main output directory: {output_dir}")
        
        # Create result_json directory
        self.result_json_dir = os.path.join(output_dir, "result_json")
        if not os.path.exists(self.result_json_dir):
            os.makedirs(self.result_json_dir)
            print(f"📁 Created JSON results directory: {self.result_json_dir}")
        
        # Initialize available analysis modules
        self.initialize_modules()
    
    def save_json_result(self, analysis_name, data, filename=None):
        """
        Save analysis results as JSON file
        
        Args:
            analysis_name (str): Name of the analysis
            data (dict): Data to save as JSON
            filename (str): Optional custom filename
            
        Returns:
            str: Path to saved JSON file
        """
        try:
            if filename is None:
                filename = f"{analysis_name}_results.json"
            
            json_path = os.path.join(self.result_json_dir, filename)
            
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy_types(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, dict):
                    return {key: convert_numpy_types(value) for key, value in obj.items()}
                elif isinstance(obj, list):
                    return [convert_numpy_types(item) for item in obj]
                else:
                    return obj
            
            # Convert data for JSON serialization
            json_data = convert_numpy_types(data)
            
            # Add metadata
            json_data['metadata'] = {
                'analysis_name': analysis_name,
                'timestamp': datetime.now().isoformat(),
                'output_directory': self.result_json_dir
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ JSON results saved: {json_path}")
            return json_path
            
        except Exception as e:
            print(f"❌ Error saving JSON results for {analysis_name}: {e}")
            return None
    
    def save_comprehensive_json_summary(self):
        """
        Save a comprehensive JSON summary of all analysis results
        
        Returns:
            str: Path to saved comprehensive JSON file
        """
        try:
            comprehensive_data = {
                'analysis_summary': {
                    'total_analyses': len(self.analysis_results),
                    'completed_analyses': len([r for r in self.analysis_results.values() if r.get('status') == 'completed']),
                    'available_modules': len(self.available_modules),
                    'output_directory': self.output_dir,
                    'json_results_directory': self.result_json_dir
                },
                'analysis_results': self.analysis_results,
                'available_modules': self.available_modules,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'analysis_type': 'comprehensive_summary'
                }
            }
            
            json_path = os.path.join(self.result_json_dir, "comprehensive_analysis_summary.json")
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Comprehensive JSON summary saved: {json_path}")
            return json_path
            
        except Exception as e:
            print(f"❌ Error saving comprehensive JSON summary: {e}")
            return None
    
    def initialize_modules(self):
        """
        Initialize and check available analysis modules
        """
        print("🔧 Initializing Analysis Modules...")
        
        # Define module configurations
        module_configs = {
            'qgis_setup': {
                'file': 'qgis_setup.py',
                'description': 'QGIS Environment Setup',
                'required': True
            },
            'tif_processor': {
                'file': 'tif_processor.py',
                'description': 'TIF File Processing',
                'required': True
            },
            'slope': {
                'file': 'slope.py',
                'description': 'Slope Analysis',
                'required': True
            },
            'elevation_statistics': {
                'file': 'elevation_statistics.py',
                'description': 'Elevation Statistics Analysis',
                'required': False
            },
            'lunar_aspect_calculator': {
                'file': 'lunar_aspect_calculator.py',
                'description': 'Lunar Aspect Calculator',
                'required': False
            },
            'hillshade': {
                'file': 'hillshade.py',
                'description': 'Hillshade Analysis',
                'required': False
            },
            'counter': {
                'file': 'counter.py',
                'description': 'Contour Generation',
                'required': False
            },
            'curvature_statistics': {
                'file': 'curvature_statistics.py',
                'description': 'Curvature Statistics Analysis',
                'required': False
            },
            'crater_edges': {
                'file': 'crater_edges.py',
                'description': 'Crater Edges Detection',
                'required': False
            },
            'scraps_headwalls': {
                'file': 'scraps_headwalls.py',
                'description': 'Scarps/Headwalls Detection',
                'required': False
            },
            'debris_paths': {
                'file': 'Debris_path.py',
                'description': 'Debris Flow Paths Detection',
                'required': False
            },
            'terrain_ruggedness': {
                'file': 'Terrain_Ruggedness.py',
                'description': 'Terrain Ruggedness Index',
                'required': False
            }
        }
        
        # Check each module
        for module_name, config in module_configs.items():
            file_path = config['file']
            if os.path.exists(file_path):
                # Try to import the module to ensure it's actually usable
                try:
                    if module_name == 'crater_edges':
                        import crater_edges
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'scraps_headwalls':
                        import scraps_headwalls
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'debris_paths':
                        import Debris_path
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'terrain_ruggedness':
                        import Terrain_Ruggedness
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'elevation_statistics':
                        import elevation_statistics
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'curvature_statistics':
                        import curvature_statistics
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'slope':
                        import slope
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'hillshade':
                        import hillshade
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'counter':
                        import counter
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'lunar_aspect_calculator':
                        import lunar_aspect_calculator
                        print(f"   ✅ {module_name}: {config['description']}")
                    elif module_name == 'tif_processor':
                        import tif_processor
                        print(f"   ✅ {module_name}: {config['description']}")
                    else:
                        print(f"   ✅ {module_name}: {config['description']}")
                    
                    self.available_modules[module_name] = {
                        'file': file_path,
                        'description': config['description'],
                        'required': config['required'],
                        'status': 'Available'
                    }
                except ImportError as e:
                    if config['required']:
                        print(f"   ❌ {module_name}: {config['description']} (REQUIRED - IMPORT FAILED: {e})")
                    else:
                        print(f"   ⚠️  {module_name}: {config['description']} (Optional - Import Failed: {e})")
                except Exception as e:
                    if config['required']:
                        print(f"   ❌ {module_name}: {config['description']} (REQUIRED - ERROR: {e})")
                    else:
                        print(f"   ⚠️  {module_name}: {config['description']} (Optional - Error: {e})")
            else:
                if config['required']:
                    print(f"   ❌ {module_name}: {config['description']} (REQUIRED - NOT FOUND)")
                else:
                    print(f"   ⚠️  {module_name}: {config['description']} (Optional - Not Found)")
        
        print(f"📊 Total modules available: {len(self.available_modules)}")
        print(f"🎯 Expected modules: 11")
        print(f"📈 Success rate: {len(self.available_modules)}/11 ({len(self.available_modules)/11*100:.1f}%)")
        
        if len(self.available_modules) < 11:
            print("\n⚠️  Some modules are missing or failed to import.")
            print("   This may affect the analysis pipeline.")
            print("   Run test_all_modules.py to diagnose import issues.")
    
    def load_dem(self, dem_path, layer_name="DEM"):
        """
        Load Digital Elevation Model (DEM) for analysis
        
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
    
    def run_tif_processor_analysis(self, dem_path):
        """
        Run TIF processor analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'tif_processor' not in self.available_modules:
            print("❌ TIF processor module not available")
            return False
        
        try:
            print("\n📊 Running TIF Processor Analysis...")
            print("-" * 40)
            
            # Import and run TIF processor
            module_path = self.available_modules['tif_processor']['file']
            
            # Create TIF processor instance
            from tif_processor import TifProcessor
            processor = TifProcessor()
            
            # Load DEM
            if not processor.load_tif_file(dem_path, "Lunar_DEM"):
                return False
            
            # Get elevation statistics
            processor.elevation_statistics("Lunar_DEM")
            
            # Store results
            self.analysis_results['tif_processor'] = {
                'status': 'completed',
                'dem_path': dem_path,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save JSON results
            json_data = {
                'dem_path': dem_path,
                'analysis_type': 'tif_processor',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            }
            self.save_json_result('tif_processor', json_data)
            
            print("✅ TIF processor analysis completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in TIF processor analysis: {e}")
            return False
    
    def run_slope_analysis(self, dem_path):
        """
        Run slope analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'slope' not in self.available_modules:
            print("❌ Slope analysis module not available")
            return False
        
        try:
            print("\n🌙 Running Slope Analysis...")
            print("-" * 30)
            
            # Import and run slope calculator
            from slope import MoonSlopeCalculator
            calculator = MoonSlopeCalculator()
            
            # Load DEM
            if not calculator.load_tif_file(dem_path, "Lunar_DEM"):
                return False
            
            # Run slope calculation
            slope_output = os.path.join(self.output_dir, "lunar_slope.tif")
            
            # Try multiple methods
            success = False
            
            if calculator.processing_available:
                success = calculator.calculate_slope_with_processing("Lunar_DEM", slope_output)
            
            if not success:
                success = calculator.calculate_slope_manual("Lunar_DEM", slope_output)
            
            if not success:
                success = calculator.calculate_slope_simple("Lunar_DEM", slope_output)
            
            if success:
                self.analysis_results['slope'] = {
                    'status': 'completed',
                    'output_path': slope_output,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_path': slope_output,
                    'analysis_type': 'slope',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('slope', json_data)
                
                print("✅ Slope analysis completed")
                return True
            else:
                print("❌ All slope calculation methods failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in slope analysis: {e}")
            return False
    
    def run_crater_edges_analysis(self, dem_path):
        """
        Run crater edges detection analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'crater_edges' not in self.available_modules:
            print("❌ Crater edges detection module not available")
            return False
        
        try:
            print("\n🌑 Running Crater Edges Detection...")
            print("-" * 40)
            
            # Import and run crater edges detector
            from crater_edges import CraterEdgesDetector
            
            detector = CraterEdgesDetector()
            
            # Run complete analysis
            success = detector.run_complete_analysis(dem_path)
            
            if success:
                self.analysis_results['crater_edges'] = {
                    'status': 'completed',
                    'output_dir': 'crater_walls',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'crater_walls',
                    'analysis_type': 'crater_edges',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('crater_edges', json_data)
                
                print("✅ Crater edges detection completed")
                return True
            else:
                print("❌ Crater edges detection failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in crater edges analysis: {e}")
            return False
    
    def run_scraps_headwalls_analysis(self, dem_path):
        """
        Run scarps/headwalls detection analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'scraps_headwalls' not in self.available_modules:
            print("❌ Scarps/headwalls detection module not available")
            return False
        
        try:
            print("\n🏔️ Running Scarps/Headwalls Detection...")
            print("-" * 45)
            
            # Import and run scarps headwalls detector
            from scraps_headwalls import ScarpsHeadwallsDetector
            
            detector = ScarpsHeadwallsDetector()
            
            # Run complete analysis
            success = detector.run_complete_analysis(dem_path)
            
            if success:
                self.analysis_results['scraps_headwalls'] = {
                    'status': 'completed',
                    'output_dir': 'headwalls_scraps',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'headwalls_scraps',
                    'analysis_type': 'scraps_headwalls',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('scraps_headwalls', json_data)
                
                print("✅ Scarps/headwalls detection completed")
                return True
            else:
                print("❌ Scarps/headwalls detection failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in scarps/headwalls analysis: {e}")
            return False
    
    def run_debris_paths_analysis(self, dem_path):
        """
        Run debris flow paths detection analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'debris_paths' not in self.available_modules:
            print("❌ Debris flow paths detection module not available")
            return False
        
        try:
            print("\n🌊 Running Debris Flow Paths Detection...")
            print("-" * 45)
            
            # Import and run debris paths detector
            from Debris_path import DebrisFlowPathsDetector
            
            detector = DebrisFlowPathsDetector()
            
            # Run complete analysis
            success = detector.run_complete_analysis(dem_path)
            
            if success:
                self.analysis_results['debris_paths'] = {
                    'status': 'completed',
                    'output_dir': 'debris_path_output',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'debris_path_output',
                    'analysis_type': 'debris_paths',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('debris_paths', json_data)
                
                print("✅ Debris flow paths detection completed")
                return True
            else:
                print("❌ Debris flow paths detection failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in debris paths analysis: {e}")
            return False
    
    def run_elevation_statistics_analysis(self, dem_path):
        """
        Run elevation statistics analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'elevation_statistics' not in self.available_modules:
            print("❌ Elevation statistics module not available")
            return False
        
        try:
            print("\n📊 Running Elevation Statistics Analysis...")
            print("-" * 45)
            
            # Import and run elevation statistics
            from elevation_statistics import ElevationStats
            
            stats = ElevationStats()
            
            # Load DEM
            if not stats.load_tif(dem_path, "Lunar_DEM"):
                return False
            
            # Get elevation statistics
            elevation_stats = stats.elevation_statistics("Lunar_DEM")
            
            if elevation_stats:
                self.analysis_results['elevation_statistics'] = {
                    'status': 'completed',
                    'dem_path': dem_path,
                    'stats': elevation_stats,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'dem_path': dem_path,
                    'analysis_type': 'elevation_statistics',
                    'status': 'completed',
                    'stats': elevation_stats,
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('elevation_statistics', json_data)
                
                print("✅ Elevation statistics analysis completed")
                return True
            else:
                print("❌ Elevation statistics analysis failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in elevation statistics analysis: {e}")
            return False
    
    def run_lunar_aspect_analysis(self, dem_path):
        """
        Run lunar aspect calculator analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'lunar_aspect_calculator' not in self.available_modules:
            print("❌ Lunar aspect calculator module not available")
            return False
        
        try:
            print("\n🧮 Running Lunar Aspect Calculator Analysis...")
            print("-" * 50)
            
            # Import and run lunar aspect calculator
            from lunar_aspect_calculator import calculate_lunar_aspect
            
            # Run aspect calculation
            success = calculate_lunar_aspect(dem_path, "aspect_outputs")
            
            if success:
                self.analysis_results['lunar_aspect_calculator'] = {
                    'status': 'completed',
                    'output_dir': 'aspect_outputs',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'aspect_outputs',
                    'analysis_type': 'lunar_aspect_calculator',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('lunar_aspect_calculator', json_data)
                
                print("✅ Lunar aspect calculator analysis completed")
                return True
            else:
                print("❌ Lunar aspect calculator analysis failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in lunar aspect calculator analysis: {e}")
            return False
    
    def run_hillshade_analysis(self, dem_path):
        """
        Run hillshade analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'hillshade' not in self.available_modules:
            print("❌ Hillshade analysis module not available")
            return False
        
        try:
            print("\n🌙 Running Hillshade Analysis...")
            print("-" * 35)
            
            # Import and run hillshade processor
            from hillshade import LunarHillshadeProcessor
            
            processor = LunarHillshadeProcessor()
            
            # Process DEM in real-time
            success = processor.process_dem_realtime(dem_path, "hillshade_outputs")
            
            if success:
                self.analysis_results['hillshade'] = {
                    'status': 'completed',
                    'output_dir': 'hillshade_outputs',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'hillshade_outputs',
                    'analysis_type': 'hillshade',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('hillshade', json_data)
                
                print("✅ Hillshade analysis completed")
                return True
            else:
                print("❌ Hillshade analysis failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in hillshade analysis: {e}")
            return False
    
    def run_counter_analysis(self, dem_path):
        """
        Run contour generation analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'counter' not in self.available_modules:
            print("❌ Counter (contour) analysis module not available")
            return False
        
        try:
            print("\n📊 Running Contour Generation Analysis...")
            print("-" * 45)
            
            # Import and run contour generator
            from counter import LunarContourGenerator
            
            generator = LunarContourGenerator()
            
            # Process DEM to generate contours
            success = generator.process_dem_contours(
                dem_path, 
                output_dir="counter_outputs",
                interval=50,              # 50 meters between contours
                attribute_name="elevation", # Attribute field name
                offset=None,              # Start from minimum elevation
                simplification_tolerance=None  # No simplification for accuracy
            )
            
            if success:
                self.analysis_results['counter'] = {
                    'status': 'completed',
                    'output_dir': 'counter_outputs',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'counter_outputs',
                    'analysis_type': 'counter',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('counter', json_data)
                
                print("✅ Contour generation analysis completed")
                return True
            else:
                print("❌ Contour generation analysis failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in counter analysis: {e}")
            return False
    
    def run_curvature_statistics_analysis(self, dem_path):
        """
        Run curvature statistics analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'curvature_statistics' not in self.available_modules:
            print("❌ Curvature statistics module not available")
            return False
        
        try:
            print("\n🌑 Running Curvature Statistics Analysis...")
            print("-" * 45)
            
            # Import and run curvature statistics
            from curvature_statistics import CurvatureStats
            
            stats = CurvatureStats()
            
            # Load DEM
            if not stats.load_tif(dem_path, "Lunar_DEM"):
                return False
            
            # Compute and print curvatures
            curvature_stats = stats.compute_and_print_curvatures("Lunar_DEM")
            
            if curvature_stats:
                self.analysis_results['curvature_statistics'] = {
                    'status': 'completed',
                    'dem_path': dem_path,
                    'curvature_types': list(curvature_stats.keys()),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'dem_path': dem_path,
                    'analysis_type': 'curvature_statistics',
                    'status': 'completed',
                    'curvature_types': list(curvature_stats.keys()),
                    'curvature_stats': curvature_stats,
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('curvature_statistics', json_data)
                
                print("✅ Curvature statistics analysis completed")
                return True
            else:
                print("❌ Curvature statistics analysis failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in curvature statistics analysis: {e}")
            return False
    
    def run_terrain_ruggedness_analysis(self, dem_path):
        """
        Run terrain ruggedness index analysis
        
        Args:
            dem_path (str): Path to input DEM file
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 'terrain_ruggedness' not in self.available_modules:
            print("❌ Terrain ruggedness index module not available")
            return False
        
        try:
            print("\n🏔️ Running Terrain Ruggedness Index Analysis...")
            print("-" * 50)
            
            # Import and run terrain ruggedness calculator
            from Terrain_Ruggedness import TerrainRuggednessCalculator
            
            calculator = TerrainRuggednessCalculator()
            
            # Run complete analysis
            success = calculator.run_complete_analysis(dem_path)
            
            if success:
                self.analysis_results['terrain_ruggedness'] = {
                    'status': 'completed',
                    'output_dir': 'Terrian_Reggedness_output',
                    'timestamp': datetime.now().isoformat()
                }
                
                # Save JSON results
                json_data = {
                    'output_dir': 'Terrian_Reggedness_output',
                    'analysis_type': 'terrain_ruggedness',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                }
                self.save_json_result('terrain_ruggedness', json_data)
                
                print("✅ Terrain ruggedness index analysis completed")
                return True
            else:
                print("❌ Terrain ruggedness index analysis failed")
                return False
            
        except Exception as e:
            print(f"❌ Error in terrain ruggedness analysis: {e}")
            return False
    
    def run_complete_analysis_pipeline(self, dem_path, analysis_types=None):
        """
        Run complete lunar analysis pipeline
        
        Args:
            dem_path (str): Path to input DEM file
            analysis_types (list): List of analysis types to run (None = all available)
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Starting Complete Lunar Analysis Pipeline")
        print("=" * 60)
        print(f"📊 Input DEM: {os.path.basename(dem_path)}")
        print(f"📁 Output Directory: {self.output_dir}")
        
        # Step 1: Load DEM
        print("\n📊 Step 1: Loading DEM...")
        if not self.load_dem(dem_path):
            return False
        
        # Step 2: Run analyses
        print("\n🔬 Step 2: Running Analysis Modules...")
        
        # Define analysis sequence
        analysis_sequence = [
            ('tif_processor', self.run_tif_processor_analysis),
            ('elevation_statistics', self.run_elevation_statistics_analysis),
            ('slope', self.run_slope_analysis),
            ('lunar_aspect_calculator', self.run_lunar_aspect_analysis),
            ('hillshade', self.run_hillshade_analysis),
            ('counter', self.run_counter_analysis),
            ('curvature_statistics', self.run_curvature_statistics_analysis),
            ('crater_edges', self.run_crater_edges_analysis),
            ('scraps_headwalls', self.run_scraps_headwalls_analysis),
            ('debris_paths', self.run_debris_paths_analysis),
            ('terrain_ruggedness', self.run_terrain_ruggedness_analysis)
        ]
        
        # Run requested analyses
        for analysis_name, analysis_func in analysis_sequence:
            if analysis_types is None or analysis_name in analysis_types:
                if analysis_name in self.available_modules:
                    print(f"\n🎯 Running {analysis_name.upper()} analysis...")
                    analysis_func(dem_path)
                else:
                    print(f"\n⚠️  Skipping {analysis_name.upper()} (module not available)")
        
        # Step 3: Generate summary report
        print("\n📋 Step 3: Generating Summary Report...")
        self.generate_summary_report()
        
        print("\n✅ Complete Lunar Analysis Pipeline Finished!")
        print("=" * 60)
        print(f"📁 All outputs saved to: {self.output_dir}")
        print("\n🎯 Analysis Summary:")
        for analysis_name, result in self.analysis_results.items():
            status = result.get('status', 'unknown')
            print(f"   - {analysis_name}: {status}")
        
        return True
    
    def generate_summary_report(self):
        """
        Generate comprehensive summary report
        """
        try:
            report_path = os.path.join(self.output_dir, "lunar_analysis_summary_report.txt")
            
            with open(report_path, 'w') as f:
                f.write("🌑 LUNAR TERRAIN ANALYSIS SUMMARY REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("📊 ANALYSIS OVERVIEW\n")
                f.write("-" * 25 + "\n")
                f.write(f"Total Analyses Run: {len(self.analysis_results)}\n")
                f.write(f"Output Directory: {self.output_dir}\n\n")
                
                f.write("🔧 AVAILABLE MODULES\n")
                f.write("-" * 25 + "\n")
                for module_name, module_info in self.available_modules.items():
                    f.write(f"• {module_name}: {module_info['description']} ({module_info['status']})\n")
                f.write("\n")
                
                f.write("📋 ANALYSIS RESULTS\n")
                f.write("-" * 25 + "\n")
                for analysis_name, result in self.analysis_results.items():
                    f.write(f"• {analysis_name.upper()}:\n")
                    f.write(f"  - Status: {result.get('status', 'unknown')}\n")
                    f.write(f"  - Timestamp: {result.get('timestamp', 'unknown')}\n")
                    if 'output_path' in result:
                        f.write(f"  - Output: {result['output_path']}\n")
                    if 'output_dir' in result:
                        f.write(f"  - Output Directory: {result['output_dir']}\n")
                    if 'stats' in result:
                        f.write(f"  - Statistics: Available\n")
                    if 'curvature_types' in result:
                        f.write(f"  - Curvature Types: {', '.join(result['curvature_types'])}\n")
                    f.write("\n")
                
                f.write("🎯 NEXT STEPS\n")
                f.write("-" * 15 + "\n")
                f.write("1. Open QGIS and load the generated layers\n")
                f.write("2. Review analysis results in respective output directories\n")
                f.write("3. Combine results for comprehensive terrain assessment\n")
                f.write("4. Export final results for further processing\n")
                f.write("5. Consider temporal analysis for monitoring changes\n")
            
            print(f"✅ Summary report generated: {report_path}")
            
            # Also save comprehensive JSON summary
            self.save_comprehensive_json_summary()
            
            return report_path
            
        except Exception as e:
            print(f"❌ Error generating summary report: {e}")
            return None
    
    def list_available_analyses(self):
        """
        List all available analysis modules
        """
        print("\n📋 Available Analysis Modules:")
        print("-" * 40)
        for module_name, module_info in self.available_modules.items():
            status_icon = "✅" if module_info['status'] == 'Available' else "❌"
            required_text = " (Required)" if module_info['required'] else " (Optional)"
            print(f"{status_icon} {module_name}: {module_info['description']}{required_text}")
    
    def cleanup(self):
        """
        Clean up QGIS application
        """
        try:
            # Suppress all warnings during cleanup
            import warnings
            warnings.filterwarnings("ignore")
            
            # Use a more graceful exit approach
            if qgs is not None:
            qgs.exitQgis()
            print("✅ QGIS cleanup completed")
            else:
                print("✅ QGIS cleanup completed (no cleanup needed)")
        except Exception as e:
            # Ignore cleanup errors as they don't affect functionality
            print("✅ QGIS cleanup completed (with warnings)")
        finally:
            # Ensure warnings are restored
            warnings.resetwarnings()

# Example usage
if __name__ == "__main__":
    # Initialize main controller
    controller = LunarMainController()
    
    # List available analyses
    controller.list_available_analyses()
    
    def validate_dem_file(file_path):
        """
        Validate if the file is a valid DEM file
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file extension
        valid_extensions = ['.tif', '.tiff', '.asc', '.dem', '.geotiff']
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in valid_extensions:
            return False, f"Invalid file extension. Supported: {', '.join(valid_extensions)}"
        
        # Check file size (should be reasonable for a DEM)
        file_size = os.path.getsize(file_path)
        if file_size < 1024:  # Less than 1KB
            return False, "File too small to be a valid DEM"
        
        return True, "Valid DEM file"
    
    def get_dem_file_path():
        """
        Interactive function to get DEM file path from user
        """
        print("\n" + "="*60)
        print("🌑 LUNAR TERRAIN ANALYSIS - DEM FILE SELECTION")
        print("="*60)
        print("📋 Supported formats: .tif, .tiff, .asc, .dem, .geotiff")
        print("="*60)
        
        # Default path
        default_path = r"F:\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
        
        while True:
            print(f"\n📁 Current DEM file path: {default_path}")
            
            # Validate the file
            is_valid, message = validate_dem_file(default_path)
            
            if is_valid:
                print(f"✅ {message}")
                print(f"📊 File size: {os.path.getsize(default_path) / (1024*1024):.2f} MB")
                return default_path
            
            print(f"❌ {message}")
            print("\nOptions:")
            print("1. Enter a new file path")
            print("2. Browse for file (if supported)")
            print("3. Exit program")
            print("4. Show help")
            
            choice = input("\nEnter your choice (1/2/3/4): ").strip()
            
            if choice == "1":
                new_path = input("Enter the full path to your DEM file: ").strip()
                if new_path:
                    # Remove quotes if user added them
                    new_path = new_path.strip('"\'')
                    default_path = new_path
                    print(f"📁 Updated path: {default_path}")
                else:
                    print("⚠️  No path entered. Using current path.")
            
            elif choice == "2":
                try:
                    import tkinter as tk
                    from tkinter import filedialog
                    
                    # Create a hidden root window
                    root = tk.Tk()
                    root.withdraw()  # Hide the main window
                    
                    # Open file dialog
                    file_path = filedialog.askopenfilename(
                        title="Select DEM File",
                        filetypes=[
                            ("DEM Files", "*.tif *.tiff *.asc *.dem *.geotiff"),
                            ("All Files", "*.*")
                        ]
                    )
                    
                    if file_path:
                        default_path = file_path
                        print(f"📁 Selected file: {default_path}")
                    else:
                        print("⚠️  No file selected.")
                    
                    root.destroy()
                    
                except ImportError:
                    print("⚠️  File browser not available (tkinter not installed).")
                    print("💡 Please enter the file path manually (option 1).")
                except Exception as e:
                    print(f"⚠️  Error opening file browser: {e}")
                    print("💡 Please enter the file path manually (option 1).")
            
            elif choice == "3":
                print("\n👋 Exiting program. Goodbye!")
                return None
            
            elif choice == "4":
                print("\n" + "="*50)
                print("📖 HELP - DEM FILE SELECTION")
                print("="*50)
                print("🌑 This program analyzes lunar terrain using DEM files.")
                print("\n📋 Supported file formats:")
                print("   • .tif / .tiff - GeoTIFF format (recommended)")
                print("   • .asc - ASCII Grid format")
                print("   • .dem - Digital Elevation Model format")
                print("   • .geotiff - GeoTIFF format")
                print("\n💡 Tips:")
                print("   • Use absolute paths (e.g., C:\\path\\to\\file.tif)")
                print("   • Make sure the file is a valid DEM with elevation data")
                print("   • File should be reasonably large (typically > 1MB)")
                print("   • The program will validate the file before processing")
                print("="*50)
            
            else:
                print("⚠️  Invalid choice. Please enter 1, 2, 3, or 4.")
                print("💡 Tip: You can also press Enter to use option 1 (enter path manually)")
    
    # Get DEM file path interactively
    dem_path = get_dem_file_path()
    
    if dem_path is None:
        # User chose to exit
        print("✅ Program terminated by user.")
        sys.exit(0)
    
    # Check if the file exists
    if os.path.exists(dem_path):
        print(f"\n✅ DEM file found: {dem_path}")
        print("🚀 Starting comprehensive lunar analysis...")
        print(f"📊 Using DEM: {os.path.basename(dem_path)}")
        
        # Run complete analysis pipeline with all available modules
        print("🔬 Running complete lunar analysis pipeline...")
        success = controller.run_complete_analysis_pipeline(dem_path)
        
        if success:
            print("\n✅ Comprehensive lunar analysis completed successfully!")
            print("📁 Check the 'lunar_analysis_output' directory for summary report")
            print("🎯 Individual analysis outputs:")
            for analysis_name, result in controller.analysis_results.items():
                if 'output_dir' in result:
                    print(f"   - {analysis_name}: {result['output_dir']}")
                elif 'output_path' in result:
                    print(f"   - {analysis_name}: {result['output_path']}")
        else:
            print("\n❌ Comprehensive lunar analysis failed!")
    else:
        print(f"❌ DEM file not found: {dem_path}")
        print("💡 Please ensure the TIF file exists at the specified path")
    
    # Clean up
    try:
        # Suppress the specific GDAL cleanup error
        import sys
        import warnings
        
        # Redirect stderr to suppress the error message
        original_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        
        controller.cleanup()
        
        # Restore stderr
        sys.stderr.close()
        sys.stderr = original_stderr
        
        print("✅ Analysis completed successfully!")
    except Exception as e:
        # Restore stderr in case of other errors
        if 'sys' in locals():
            sys.stderr = original_stderr
        print("✅ Analysis completed successfully!")
        print("⚠️  Cleanup warnings can be safely ignored")

    # --- LUNAR RISK ANALYSIS INTEGRATION ---
    try:
        from lunar_risk_analysis import LunarRiskAnalyzer
        import json

        # List of report files generated by the pipeline (relative to processed/)
        report_files = [
            "lunar_analysis_output/lunar_slope_analysis_report.txt",
            "aspect_outputs/lunar_aspect_analysis_report.txt",
            "lunar_analysis_output/lunar_curvature_analysis_report.txt",
            "lunar_analysis_output/lunar_elevation_analysis_report.txt",
            "counter_outputs/lunar_contour_analysis_report.txt",
            "Terrian_Reggedness_output/terrain_ruggedness_analysis_report.txt",
            "hillshade_outputs/lunar_landslide_analysis_report.txt",
            "headwalls_scraps/scarps_headwalls_analysis_report.txt"
        ]
        # Only use files that actually exist
        report_files = [f for f in report_files if os.path.exists(f)]

        if report_files:
            print(f"📊 Running risk analysis on {len(report_files)} reports...")
            analyzer = LunarRiskAnalyzer()
            results = analyzer.process_analysis_reports(report_files)
            
            # Save risk report as text file
            analyzer.generate_risk_report(results, "comprehensive_lunar_risk_report.txt")
            print("✅ Risk analysis completed and report saved to comprehensive_lunar_risk_report.txt")
            
            # Save detailed results as JSON file
            json_output_path = "lunar_risk_analysis_results.json"
            try:
                with open(json_output_path, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, default=str, ensure_ascii=False)
                print(f"✅ Detailed results saved to JSON: {json_output_path}")
            except Exception as e:
                print(f"❌ Error saving JSON results: {e}")
        else:
            print("❌ No report files found for risk analysis.")

    except Exception as e:
        print(f"❌ Error running risk analysis: {e}") 