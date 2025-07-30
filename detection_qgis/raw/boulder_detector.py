import sys
import os
import numpy as np
import cv2
from scipy import ndimage
from skimage import feature, morphology, measure, filters
from skimage.segmentation import watershed
from skimage.feature import peak_local_maxima

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
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

print("✅ QGIS setup completed successfully!")

class BoulderDetector:
    def __init__(self):
        self.image = None
        self.height = None
        self.width = None
        self.boulders = []
        
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
                print(f"   - Mean value: {np.mean(self.image)}")
                
                return True
                
        except Exception as e:
            print(f"❌ Error loading TIF file: {e}")
            return False
    
    def preprocess_image(self):
        """
        Preprocess the image for boulder detection
        """
        if self.image is None:
            print("❌ No image loaded")
            return False
            
        print("🔄 Preprocessing image...")
        
        # Normalize image to 0-255 range
        self.normalized = ((self.image - np.min(self.image)) / 
                          (np.max(self.image) - np.min(self.image)) * 255).astype(np.uint8)
        
        # Apply Gaussian blur to reduce noise
        self.blurred = cv2.GaussianBlur(self.normalized, (5, 5), 0)
        
        # Apply morphological operations to enhance features
        kernel = np.ones((3,3), np.uint8)
        self.morph = cv2.morphologyEx(self.blurred, cv2.MORPH_CLOSE, kernel)
        
        print("✅ Image preprocessing completed")
        return True
    
    def detect_boulders_edge_based(self, min_area=100, max_area=10000):
        """
        Detect boulders using edge detection and contour analysis
        """
        print("🔄 Detecting boulders using edge-based method...")
        
        # Edge detection
        edges = cv2.Canny(self.blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        boulders = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate circularity
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                
                # Filter by circularity (boulders are somewhat circular)
                if circularity > 0.3:
                    boulders.append({
                        'contour': contour,
                        'area': area,
                        'bbox': (x, y, w, h),
                        'circularity': circularity,
                        'center': (x + w//2, y + h//2)
                    })
        
        print(f"✅ Edge-based detection found {len(boulders)} potential boulders")
        return boulders
    
    def detect_boulders_watershed(self, min_distance=20, min_area=100):
        """
        Detect boulders using watershed segmentation
        """
        print("🔄 Detecting boulders using watershed method...")
        
        # Calculate distance transform
        distance = ndimage.distance_transform_edt(self.morph)
        
        # Find local maxima
        local_max_coords = peak_local_maxima(distance, min_distance=min_distance)
        local_max = np.zeros_like(distance, dtype=bool)
        local_max[tuple(local_max_coords.T)] = True
        
        # Watershed segmentation
        markers = measure.label(local_max)
        labels = watershed(-distance, markers, mask=self.morph)
        
        # Analyze regions
        boulders = []
        for region in measure.regionprops(labels):
            if region.area > min_area:
                # Get region properties
                bbox = region.bbox
                area = region.area
                eccentricity = region.eccentricity
                
                # Filter by eccentricity (boulders are not too elongated)
                if eccentricity < 0.8:
                    boulders.append({
                        'bbox': (bbox[1], bbox[0], bbox[3] - bbox[1], bbox[2] - bbox[0]),
                        'area': area,
                        'eccentricity': eccentricity,
                        'center': (bbox[1] + (bbox[3] - bbox[1])//2, 
                                 bbox[0] + (bbox[2] - bbox[0])//2)
                    })
        
        print(f"✅ Watershed detection found {len(boulders)} potential boulders")
        return boulders
    
    def detect_boulders_morphological(self, min_size=10, max_size=100):
        """
        Detect boulders using morphological operations
        """
        print("🔄 Detecting boulders using morphological method...")
        
        # Apply morphological operations to isolate potential boulders
        kernel = np.ones((min_size, min_size), np.uint8)
        
        # Opening to remove small noise
        opened = cv2.morphologyEx(self.morph, cv2.MORPH_OPEN, kernel)
        
        # Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opened, connectivity=8)
        
        boulders = []
        for i in range(1, num_labels):  # Skip background (label 0)
            area = stats[i, cv2.CC_STAT_AREA]
            width = stats[i, cv2.CC_STAT_WIDTH]
            height = stats[i, cv2.CC_STAT_HEIGHT]
            
            # Filter by size
            if min_size < area < max_size and width > min_size and height > min_size:
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                
                boulders.append({
                    'bbox': (x, y, width, height),
                    'area': area,
                    'center': (centroids[i][0], centroids[i][1])
                })
        
        print(f"✅ Morphological detection found {len(boulders)} potential boulders")
        return boulders
    
    def combine_detections(self, edge_boulders, watershed_boulders, morph_boulders):
        """
        Combine results from different detection methods
        """
        print("🔄 Combining detection results...")
        
        all_boulders = []
        
        # Add edge-based detections
        for boulder in edge_boulders:
            boulder['method'] = 'edge'
            all_boulders.append(boulder)
        
        # Add watershed detections
        for boulder in watershed_boulders:
            boulder['method'] = 'watershed'
            all_boulders.append(boulder)
        
        # Add morphological detections
        for boulder in morph_boulders:
            boulder['method'] = 'morphological'
            all_boulders.append(boulder)
        
        # Remove duplicates (boulders detected by multiple methods)
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
                f.write("Boulder Detection Results\n")
                f.write("=" * 50 + "\n")
                f.write(f"Total boulders detected: {len(boulders)}\n\n")
                
                for i, boulder in enumerate(boulders):
                    f.write(f"Boulder {i+1}:\n")
                    f.write(f"  - Method: {boulder['method']}\n")
                    f.write(f"  - Center: {boulder['center']}\n")
                    f.write(f"  - Area: {boulder['area']}\n")
                    if 'bbox' in boulder:
                        f.write(f"  - Bounding box: {boulder['bbox']}\n")
                    if 'circularity' in boulder:
                        f.write(f"  - Circularity: {boulder['circularity']:.3f}\n")
                    if 'eccentricity' in boulder:
                        f.write(f"  - Eccentricity: {boulder['eccentricity']:.3f}\n")
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
            print(f"Average area: {np.mean(areas):.1f}")
            print(f"Min area: {np.min(areas):.1f}")
            print(f"Max area: {np.max(areas):.1f}")
            
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
    output_path = r"E:\moon extract\data\derived\20250207\boulder_detection_results.txt"
    
    print("🚀 Starting boulder detection...")
    
    # Check if file exists
    if not os.path.exists(tif_path):
        print(f"❌ File not found: {tif_path}")
        return
    
    # Initialize detector
    detector = BoulderDetector()
    
    # Load TIF file
    if not detector.load_tif_as_array(tif_path):
        return
    
    # Preprocess image
    if not detector.preprocess_image():
        return
    
    # Run different detection methods
    edge_boulders = detector.detect_boulders_edge_based()
    watershed_boulders = detector.detect_boulders_watershed()
    morph_boulders = detector.detect_boulders_morphological()
    
    # Combine results
    all_boulders = detector.combine_detections(edge_boulders, watershed_boulders, morph_boulders)
    
    # Save results
    detector.save_results(output_path, all_boulders)
    
    # Print summary
    detector.print_summary(all_boulders)
    
    # Cleanup
    qgs.exitQgis()
    print("✅ QGIS cleanup completed")

if __name__ == "__main__":
    main() 