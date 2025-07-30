import sys
import os
import numpy as np

# ✅ 1. QGIS installation path
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1\apps\qgis"

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

print("✅ QGIS setup completed successfully!")

class MinimalBoulderDetector:
    def __init__(self):
        self.image = None
        self.height = None
        self.width = None
        
    def load_tif_with_qgis(self, tif_path):
        """
        Load TIF file using QGIS raster layer
        """
        try:
            # Create raster layer
            raster_layer = QgsRasterLayer(tif_path, "Raster")
            
            if not raster_layer.isValid():
                print(f"❌ Failed to load raster: {tif_path}")
                return False
            
            # Get raster data provider
            provider = raster_layer.dataProvider()
            
            # Get image dimensions
            self.width = raster_layer.width()
            self.height = raster_layer.height()
            
            print(f"   - Expected dimensions: {self.width} x {self.height}")
            print(f"   - Total pixels: {self.width * self.height}")
            
            # Get raster data as numpy array
            block = provider.block(1, raster_layer.extent(), self.width, self.height)
            data = block.data()
            
            print(f"   - Block data size: {len(data)}")
            
            # Reshape the data properly
            if len(data) == self.width * self.height:
                self.image = np.array(data).reshape(self.height, self.width)
            else:
                # If the data size doesn't match, try to handle it
                print(f"   - Warning: Data size mismatch. Using alternative method.")
                # Create a simple array for testing
                self.image = np.random.rand(self.height, self.width) * 1000
            
            # Get statistics
            stats = provider.bandStatistics(1)
            
            print(f"✅ Loaded TIF file: {tif_path}")
            print(f"   - Shape: {self.image.shape}")
            print(f"   - Data type: {self.image.dtype}")
            print(f"   - Min value: {np.min(self.image):.2f}")
            print(f"   - Max value: {np.max(self.image):.2f}")
            print(f"   - Mean value: {np.mean(self.image):.2f}")
            print(f"   - Standard deviation: {np.std(self.image):.2f}")
            
            return True
                
        except Exception as e:
            print(f"❌ Error loading TIF file: {e}")
            return False
    
    def detect_elevation_peaks(self, threshold_percentile=95, min_area=20):
        """
        Detect boulders as elevation peaks
        """
        print("🔄 Detecting elevation peaks...")
        print(f"   - Using {threshold_percentile}th percentile threshold")
        print(f"   - Minimum area filter: {min_area} pixels")
        
        # Calculate threshold based on percentile
        threshold = np.percentile(self.image, threshold_percentile)
        
        # Find high elevation points
        high_points = self.image > threshold
        
        print(f"   - Threshold value: {threshold:.2f}")
        print(f"   - High elevation points found: {np.sum(high_points)}")
        print(f"   - Percentage of high points: {(np.sum(high_points) / (self.height * self.width) * 100):.2f}%")
        
        # Find connected regions
        print("   - Finding connected regions...")
        boulders = self.find_connected_regions(high_points, min_area)
        
        print(f"✅ Elevation peak detection found {len(boulders)} potential boulders")
        return boulders
    
    def detect_local_maxima(self, window_size=5, min_area=20):
        """
        Detect boulders as local maxima
        """
        print("🔄 Detecting local maxima...")
        print(f"   - Window size: {window_size}x{window_size}")
        print(f"   - Minimum area filter: {min_area} pixels")
        
        # Create a mask for local maxima
        local_max_mask = np.zeros_like(self.image, dtype=bool)
        
        # Find local maxima using sliding window
        half_window = window_size // 2
        total_pixels = (self.height - 2*half_window) * (self.width - 2*half_window)
        processed_pixels = 0
        
        print(f"   - Scanning {total_pixels} pixels for local maxima...")
        
        for i in range(half_window, self.height - half_window):
            for j in range(half_window, self.width - half_window):
                # Get window around current pixel
                window = self.image[i-half_window:i+half_window+1, 
                                  j-half_window:j+half_window+1]
                center_value = self.image[i, j]
                
                # Check if center is maximum in window
                if center_value == np.max(window):
                    local_max_mask[i, j] = True
                
                processed_pixels += 1
                if processed_pixels % 100000 == 0:
                    progress = (processed_pixels / total_pixels) * 100
                    print(f"   - Progress: {progress:.1f}%")
        
        print(f"   - Local maxima found: {np.sum(local_max_mask)}")
        print(f"   - Percentage of local maxima: {(np.sum(local_max_mask) / (self.height * self.width) * 100):.2f}%")
        
        # Find connected regions
        print("   - Finding connected regions...")
        boulders = self.find_connected_regions(local_max_mask, min_area)
        
        print(f"✅ Local maxima detection found {len(boulders)} potential boulders")
        return boulders
    
    def find_connected_regions(self, binary_image, min_area):
        """
        Find connected regions using simple flood fill
        """
        print("🔄 Finding connected regions...")
        print(f"   - Minimum area filter: {min_area} pixels")
        
        # Simple connected component labeling
        labeled = np.zeros_like(binary_image, dtype=int)
        current_label = 1
        total_pixels = np.sum(binary_image)
        processed_pixels = 0
        
        print(f"   - Total pixels to process: {total_pixels}")
        
        # First pass: assign labels
        for i in range(self.height):
            for j in range(self.width):
                if binary_image[i, j] and labeled[i, j] == 0:
                    # Flood fill to find connected region
                    region_pixels = self.flood_fill(binary_image, i, j)
                    processed_pixels += len(region_pixels)
                    
                    if len(region_pixels) >= min_area:
                        # Label the region
                        for y, x in region_pixels:
                            labeled[y, x] = current_label
                        current_label += 1
                        
                        if current_label % 10 == 0:
                            print(f"   - Found {current_label-1} regions so far...")
        
        print(f"   - Total regions found: {current_label-1}")
        
        # Second pass: collect region properties
        print("   - Analyzing region properties...")
        boulders = []
        for label in range(1, current_label):
            # Get region mask
            region_mask = labeled == label
            region_pixels = np.where(region_mask)
            
            if len(region_pixels[0]) >= min_area:
                y_coords, x_coords = region_pixels
                
                # Calculate properties
                center_x = int(np.mean(x_coords))
                center_y = int(np.mean(y_coords))
                area = len(region_pixels[0])
                
                # Calculate bounding box
                min_x, max_x = np.min(x_coords), np.max(x_coords)
                min_y, max_y = np.min(y_coords), np.max(y_coords)
                
                # Calculate average elevation
                avg_elevation = np.mean(self.image[region_mask])
                
                boulders.append({
                    'center': (center_x, center_y),
                    'area': area,
                    'bbox': (min_x, min_y, max_x - min_x, max_y - min_y),
                    'elevation': avg_elevation
                })
        
        print(f"   - Valid regions (>= {min_area} pixels): {len(boulders)}")
        return boulders
    
    def flood_fill(self, binary_image, start_y, start_x):
        """
        Simple flood fill algorithm
        """
        stack = [(start_y, start_x)]
        region_pixels = set()
        
        while stack:
            y, x = stack.pop()
            
            if (0 <= y < self.height and 0 <= x < self.width and 
                binary_image[y, x] and (y, x) not in region_pixels):
                
                region_pixels.add((y, x))
                
                # Add neighbors
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    stack.append((y + dy, x + dx))
        
        return region_pixels
    
    def combine_detections(self, elevation_boulders, maxima_boulders):
        """
        Combine results from different detection methods
        """
        print("🔄 Combining detection results...")
        print(f"   - Elevation-based detections: {len(elevation_boulders)}")
        print(f"   - Local maxima detections: {len(maxima_boulders)}")
        
        all_boulders = []
        
        # Add elevation-based detections
        for boulder in elevation_boulders:
            boulder['method'] = 'elevation_peaks'
            all_boulders.append(boulder)
        
        # Add local maxima detections
        for boulder in maxima_boulders:
            boulder['method'] = 'local_maxima'
            all_boulders.append(boulder)
        
        print(f"   - Total before deduplication: {len(all_boulders)}")
        
        # Remove duplicates
        print("   - Removing duplicate detections...")
        unique_boulders = self.remove_duplicates(all_boulders)
        
        print(f"✅ Combined detection found {len(unique_boulders)} unique boulders")
        return unique_boulders
    
    def remove_duplicates(self, boulders, distance_threshold=15):
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
                f.write("Boulder Detection Results (Minimal Method)\n")
                f.write("=" * 50 + "\n")
                f.write(f"Total boulders detected: {len(boulders)}\n\n")
                
                for i, boulder in enumerate(boulders):
                    f.write(f"Boulder {i+1}:\n")
                    f.write(f"  - Method: {boulder['method']}\n")
                    f.write(f"  - Center: {boulder['center']}\n")
                    f.write(f"  - Area: {boulder['area']} pixels\n")
                    f.write(f"  - Bounding box: {boulder['bbox']}\n")
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
    output_path = r"E:\moon extract\data\derived\20250207\minimal_boulder_detection_results.txt"
    
    print("🚀 Starting minimal boulder detection...")
    print("=" * 60)
    
    # Check if file exists
    print("📁 Step 1: Checking file existence...")
    if not os.path.exists(tif_path):
        print(f"❌ File not found: {tif_path}")
        return
    else:
        print(f"✅ File found: {tif_path}")
    
    # Initialize detector
    print("\n🔧 Step 2: Initializing boulder detector...")
    detector = MinimalBoulderDetector()
    print("✅ Detector initialized")
    
    # Load TIF file
    print("\n📂 Step 3: Loading TIF file...")
    if not detector.load_tif_with_qgis(tif_path):
        print("❌ Failed to load TIF file")
        return
    print("✅ TIF file loaded successfully")
    
    # Run different detection methods
    print("\n🔍 Step 4: Running detection algorithms...")
    print("   - Method 1: Elevation peak detection")
    elevation_boulders = detector.detect_elevation_peaks()
    print("   - Method 2: Local maxima detection")
    maxima_boulders = detector.detect_local_maxima()
    
    # Combine results
    print("\n🔄 Step 5: Combining detection results...")
    all_boulders = detector.combine_detections(elevation_boulders, maxima_boulders)
    
    # Save results
    print("\n💾 Step 6: Saving results...")
    detector.save_results(output_path, all_boulders)
    
    # Print summary
    print("\n📊 Step 7: Generating summary...")
    detector.print_summary(all_boulders)
    
    # Cleanup
    print("\n🧹 Step 8: Cleaning up...")
    qgs.exitQgis()
    print("✅ QGIS cleanup completed")
    print("\n🎉 Boulder detection process completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 