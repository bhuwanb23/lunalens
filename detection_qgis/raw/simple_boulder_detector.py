import sys
import os
import numpy as np

# ✅ 1. QGIS installation path
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat" 

# ✅ 2. Set required environment variables
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")

# ✅ 3. Add QGIS Python path to sys.path
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "python")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

# ✅ 4. Initialize QGIS Application
from qgis.core import QgsApplication
qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs.initQgis()

# ✅ 5. Import QGIS modules
from qgis.core import QgsRasterLayer, QgsProject
import rasterio

print("✅ QGIS setup completed successfully!")

class SimpleBoulderDetector:
    def __init__(self):
        self.image = None
        self.height = None
        self.width = None
        
    def load_tif_as_array(self, tif_path):
        """
        Load TIF file as numpy array for processing
        """
        try:
            with rasterio.open(tif_path) as src:
                # Read the first band (assuming single band DEM)
                self.image = src.read(1)
                self.height, self.width = self.image.shape
                
                # Get metadata
                print(f"✅ Loaded TIF file: {tif_path}")
                print(f"   - Shape: {self.image.shape}")
                print(f"   - Data type: {self.image.dtype}")
                print(f"   - Min value: {np.min(self.image)}")
                print(f"   - Max value: {np.max(self.image)}")
                print(f"   - Mean value: {np.mean(self.image):.2f}")
                print(f"   - Standard deviation: {np.std(self.image):.2f}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error loading TIF file: {e}")
            return False
    
    def detect_elevation_anomalies(self, threshold_std=2.0, min_area=50):
        """
        Detect boulders as elevation anomalies (high points)
        """
        print("🔄 Detecting elevation anomalies...")
        
        # Calculate statistics
        mean_elevation = np.mean(self.image)
        std_elevation = np.std(self.image)
        
        # Find high elevation points (potential boulders)
        threshold = mean_elevation + threshold_std * std_elevation
        high_points = self.image > threshold
        
        print(f"   - Mean elevation: {mean_elevation:.2f}")
        print(f"   - Standard deviation: {std_elevation:.2f}")
        print(f"   - Threshold: {threshold:.2f}")
        print(f"   - High points found: {np.sum(high_points)}")
        
        # Find connected regions
        boulders = self.find_connected_regions(high_points, min_area)
        
        print(f"✅ Elevation-based detection found {len(boulders)} potential boulders")
        return boulders
    
    def detect_slope_anomalies(self, slope_threshold=30, min_area=50):
        """
        Detect boulders as areas with high slope
        """
        print("🔄 Detecting slope anomalies...")
        
        # Calculate slope using simple gradient
        grad_x = np.gradient(self.image, axis=1)
        grad_y = np.gradient(self.image, axis=0)
        slope = np.sqrt(grad_x**2 + grad_y**2)
        
        # Find high slope areas
        high_slope = slope > slope_threshold
        
        print(f"   - Max slope: {np.max(slope):.2f}")
        print(f"   - Mean slope: {np.mean(slope):.2f}")
        print(f"   - High slope areas: {np.sum(high_slope)}")
        
        # Find connected regions
        boulders = self.find_connected_regions(high_slope, min_area)
        
        print(f"✅ Slope-based detection found {len(boulders)} potential boulders")
        return boulders
    
    def find_connected_regions(self, binary_image, min_area):
        """
        Find connected regions in binary image
        """
        from scipy import ndimage
        
        # Label connected components
        labeled, num_features = ndimage.label(binary_image)
        
        boulders = []
        for i in range(1, num_features + 1):
            # Get region mask
            region_mask = labeled == i
            area = np.sum(region_mask)
            
            if area >= min_area:
                # Get region properties
                coords = np.where(region_mask)
                y_coords, x_coords = coords
                
                # Calculate center
                center_x = int(np.mean(x_coords))
                center_y = int(np.mean(y_coords))
                
                # Calculate bounding box
                min_x, max_x = np.min(x_coords), np.max(x_coords)
                min_y, max_y = np.min(y_coords), np.max(y_coords)
                
                # Calculate circularity
                perimeter = self.calculate_perimeter(region_mask)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
                boulders.append({
                    'center': (center_x, center_y),
                    'area': area,
                    'bbox': (min_x, min_y, max_x - min_x, max_y - min_y),
                    'circularity': circularity,
                    'elevation': np.mean(self.image[region_mask])
                })
        
        return boulders
    
    def calculate_perimeter(self, region_mask):
        """
        Calculate perimeter of a region
        """
        from scipy import ndimage
        
        # Erode the region
        eroded = ndimage.binary_erosion(region_mask)
        
        # Perimeter is the difference between original and eroded
        perimeter = np.sum(region_mask) - np.sum(eroded)
        
        return perimeter
    
    def combine_detections(self, elevation_boulders, slope_boulders):
        """
        Combine results from different detection methods
        """
        print("🔄 Combining detection results...")
        
        all_boulders = []
        
        # Add elevation-based detections
        for boulder in elevation_boulders:
            boulder['method'] = 'elevation'
            all_boulders.append(boulder)
        
        # Add slope-based detections
        for boulder in slope_boulders:
            boulder['method'] = 'slope'
            all_boulders.append(boulder)
        
        # Remove duplicates
        unique_boulders = self.remove_duplicates(all_boulders)
        
        print(f"✅ Combined detection found {len(unique_boulders)} unique boulders")
        return unique_boulders
    
    def remove_duplicates(self, boulders, distance_threshold=20):
        """
        Remove duplicate boulder detections
        """
        unique_boulders = []
        
        for boulder in boulders:
            is_duplicate = False
            
            for existing in unique_boulders:
                # Calculate distance between centers
                dist = np.sqrt((boulder['center'][0] - existing['center'][0])**2 + 
                             (boulder['center'][1] - existing['center'][1])**2)
                
                if dist < distance_threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_boulders.append(boulder)
        
        return unique_boulders
    
    def save_results(self, output_path, boulders):
        """
        Save detection results to file
        """
        try:
            with open(output_path, 'w') as f:
                f.write("Boulder Detection Results (Simple Method)\n")
                f.write("=" * 50 + "\n")
                f.write(f"Total boulders detected: {len(boulders)}\n\n")
                
                for i, boulder in enumerate(boulders):
                    f.write(f"Boulder {i+1}:\n")
                    f.write(f"  - Method: {boulder['method']}\n")
                    f.write(f"  - Center: {boulder['center']}\n")
                    f.write(f"  - Area: {boulder['area']} pixels\n")
                    f.write(f"  - Bounding box: {boulder['bbox']}\n")
                    f.write(f"  - Circularity: {boulder['circularity']:.3f}\n")
                    f.write(f"  - Average elevation: {boulder['elevation']:.2f}\n")
                    f.write("\n")
            
            print(f"✅ Results saved to: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return False
    
    def print_summary(self, boulders):
        """
        Print summary of detection results
        """
        print("\n" + "="*50)
        print("BOULDER DETECTION SUMMARY")
        print("="*50)
        print(f"Total boulders detected: {len(boulders)}")
        
        if boulders:
            areas = [b['area'] for b in boulders]
            elevations = [b['elevation'] for b in boulders]
            
            print(f"Average area: {np.mean(areas):.1f} pixels")
            print(f"Min area: {np.min(areas):.1f} pixels")
            print(f"Max area: {np.max(areas):.1f} pixels")
            print(f"Average elevation: {np.mean(elevations):.2f}")
            
            # Count by method
            methods = {}
            for boulder in boulders:
                method = boulder['method']
                methods[method] = methods.get(method, 0) + 1
            
            print("\nDetection by method:")
            for method, count in methods.items():
                print(f"  - {method}: {count} boulders")
        
        print("="*50)

def main():
    # 🔧 CONFIGURE YOUR PATHS HERE
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    output_path = r"E:\moon extract\data\derived\20250207\simple_boulder_detection_results.txt"
    
    print("🚀 Starting simple boulder detection...")
    
    # Check if file exists
    if not os.path.exists(tif_path):
        print(f"❌ File not found: {tif_path}")
        return
    
    # Initialize detector
    detector = SimpleBoulderDetector()
    
    # Load TIF file
    if not detector.load_tif_as_array(tif_path):
        return
    
    # Run different detection methods
    elevation_boulders = detector.detect_elevation_anomalies()
    slope_boulders = detector.detect_slope_anomalies()
    
    # Combine results
    all_boulders = detector.combine_detections(elevation_boulders, slope_boulders)
    
    # Save results
    detector.save_results(output_path, all_boulders)
    
    # Print summary
    detector.print_summary(all_boulders)
    
    # Cleanup
    qgs.exitQgis()
    print("✅ QGIS cleanup completed")

if __name__ == "__main__":
    main() 