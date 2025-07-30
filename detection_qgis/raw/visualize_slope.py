import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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

class SlopeVisualizer:
    def __init__(self):
        self.project = QgsProject.instance()
        self.layers = {}
        
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
                return raster_layer
                
        except Exception as e:
            print(f"❌ Error loading raster: {e}")
            return None
    
    def load_slope_data(self, slope_path):
        """
        Load slope data from numpy file
        """
        try:
            if slope_path.endswith('.npy'):
                slope_data = np.load(slope_path)
                print(f"✅ Loaded slope data: {slope_path}")
                print(f"   - Shape: {slope_data.shape}")
                print(f"   - Min slope: {np.min(slope_data):.2f}°")
                print(f"   - Max slope: {np.max(slope_data):.2f}°")
                print(f"   - Mean slope: {np.mean(slope_data):.2f}°")
                return slope_data
            else:
                print(f"❌ Unsupported slope file format: {slope_path}")
                return None
        except Exception as e:
            print(f"❌ Error loading slope data: {e}")
            return None
    
    def create_slope_visualization(self, elevation_layer, slope_data, output_path):
        """
        Create a visualization showing elevation and slope overlay
        """
        try:
            print("🎨 Creating slope visualization...")
            
            # Get elevation data for visualization
            provider = elevation_layer.dataProvider()
            width = elevation_layer.width()
            height = elevation_layer.height()
            
            # Read a sample of elevation data for visualization
            sample_height, sample_width = slope_data.shape
            block = provider.block(1, elevation_layer.extent(), sample_width, sample_height)
            elevation_sample = np.array(list(block.data())).reshape(sample_height, sample_width)
            
            # Create the visualization
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('🌙 Moon Terrain Analysis - Elevation and Slope', fontsize=16, fontweight='bold')
            
            # 1. Original elevation
            ax1 = axes[0, 0]
            im1 = ax1.imshow(elevation_sample, cmap='terrain', aspect='auto')
            ax1.set_title('Original Moon Elevation', fontweight='bold')
            ax1.set_xlabel('Pixels')
            ax1.set_ylabel('Pixels')
            plt.colorbar(im1, ax=ax1, label='Elevation (meters)')
            
            # 2. Slope visualization
            ax2 = axes[0, 1]
            # Create a moon-appropriate colormap for slope
            colors = ['darkblue', 'blue', 'cyan', 'yellow', 'orange', 'red', 'darkred']
            n_bins = 100
            cmap = LinearSegmentedColormap.from_list('moon_slope', colors, N=n_bins)
            
            im2 = ax2.imshow(slope_data, cmap=cmap, aspect='auto', vmin=0, vmax=30)
            ax2.set_title('Moon Slope Analysis', fontweight='bold')
            ax2.set_xlabel('Pixels')
            ax2.set_ylabel('Pixels')
            plt.colorbar(im2, ax=ax2, label='Slope (degrees)')
            
            # 3. Slope categories
            ax3 = axes[1, 0]
            slope_categories = np.zeros_like(slope_data)
            slope_categories[slope_data < 5] = 1    # Gentle
            slope_categories[(slope_data >= 5) & (slope_data < 15)] = 2  # Moderate
            slope_categories[(slope_data >= 15) & (slope_data < 30)] = 3 # Steep
            slope_categories[slope_data >= 30] = 4  # Very steep
            
            category_colors = ['green', 'yellow', 'orange', 'red']
            category_cmap = LinearSegmentedColormap.from_list('landing_categories', category_colors, N=4)
            
            im3 = ax3.imshow(slope_categories, cmap=category_cmap, aspect='auto', vmin=1, vmax=4)
            ax3.set_title('Landing Suitability Categories', fontweight='bold')
            ax3.set_xlabel('Pixels')
            ax3.set_ylabel('Pixels')
            
            # Add category labels
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='green', label='Gentle (0-5°) - Excellent'),
                Patch(facecolor='yellow', label='Moderate (5-15°) - Acceptable'),
                Patch(facecolor='orange', label='Steep (15-30°) - Challenging'),
                Patch(facecolor='red', label='Very Steep (>30°) - Unsuitable')
            ]
            ax3.legend(handles=legend_elements, loc='upper right', fontsize=8)
            
            # 4. Statistics
            ax4 = axes[1, 1]
            ax4.axis('off')
            
            # Calculate statistics
            gentle_pct = np.sum(slope_data < 5) / slope_data.size * 100
            moderate_pct = np.sum((slope_data >= 5) & (slope_data < 15)) / slope_data.size * 100
            steep_pct = np.sum((slope_data >= 15) & (slope_data < 30)) / slope_data.size * 100
            very_steep_pct = np.sum(slope_data >= 30) / slope_data.size * 100
            
            stats_text = f"""
🌙 Moon Slope Analysis Results
{'='*40}

📊 Slope Statistics:
• Min slope: {np.min(slope_data):.2f}°
• Max slope: {np.max(slope_data):.2f}°
• Mean slope: {np.mean(slope_data):.2f}°
• Std dev: {np.std(slope_data):.2f}°

🎯 Landing Suitability:
• Gentle slopes (0-5°): {gentle_pct:.1f}%
• Moderate slopes (5-15°): {moderate_pct:.1f}%
• Steep slopes (15-30°): {steep_pct:.1f}%
• Very steep (>30°): {very_steep_pct:.1f}%

🌍 Moon-Specific Notes:
• Moon gravity: 1.62 m/s² (vs Earth's 9.81 m/s²)
• Lower gravity means less erosion
• Steeper slopes more common on moon
• Landing criteria adjusted for lunar conditions
"""
            
            ax4.text(0.05, 0.95, stats_text, transform=ax4.transAxes, 
                     fontsize=10, verticalalignment='top', fontfamily='monospace',
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
            
            plt.tight_layout()
            
            # Save the visualization
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✅ Visualization saved to: {output_path}")
            
            # Show the plot
            plt.show()
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            return False
    
    def cleanup(self):
        """
        Clean up QGIS application
        """
        qgs.exitQgis()
        print("✅ QGIS cleanup completed")

def main():
    print("🌙 Moon Slope Visualizer")
    print("=" * 50)
    
    # Initialize visualizer
    visualizer = SlopeVisualizer()
    
    # 🔧 CONFIGURE YOUR PATHS HERE
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    slope_path = r"E:\moon extract\data\derived\20250207\moon_slope.npy"
    visualization_output = r"E:\moon extract\data\derived\20250207\moon_slope_visualization.png"
    
    print("📁 Step 1: Loading moon TIF file...")
    
    # Load the moon TIF file
    raster_layer = visualizer.load_tif_file(tif_path, "Moon_DEM")
    
    if raster_layer is None:
        print("❌ Failed to load moon TIF file")
        visualizer.cleanup()
        return
    
    print("✅ Moon TIF file loaded successfully")
    
    print("\n📊 Step 2: Loading slope data...")
    
    # Load the slope data
    slope_data = visualizer.load_slope_data(slope_path)
    
    if slope_data is None:
        print("❌ Failed to load slope data")
        visualizer.cleanup()
        return
    
    print("✅ Slope data loaded successfully")
    
    print("\n🎨 Step 3: Creating visualization...")
    
    # Create the visualization
    success = visualizer.create_slope_visualization(raster_layer, slope_data, visualization_output)
    
    if not success:
        print("❌ Failed to create visualization")
        visualizer.cleanup()
        return
    
    print("\n🎉 Visualization completed!")
    print(f"📁 Output files:")
    print(f"   - Visualization: {visualization_output}")
    print(f"   - Slope data: {slope_path}")
    
    # Cleanup
    visualizer.cleanup()

if __name__ == "__main__":
    main() 