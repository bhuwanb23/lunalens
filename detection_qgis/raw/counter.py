#!/usr/bin/env python3
"""
🌙 Lunar Contour Generator for Real-Time DEM Processing
=======================================================

This script processes lunar DEM data to generate accurate contour lines
for lunar terrain analysis and mapping.

Required Parameters:
- Input Raster Layer: The DEM file (.tif) containing elevation data
- Interval Between Contours: Vertical distance between contour lines (e.g., 50 meters)
- Attribute Name: Name for elevation value attribute field
- Offset (optional): Base elevation to start generating contours
- Simplification Tolerance (optional): Smoothing for contour lines

Real-time processing capabilities:
- Load DEM from TIF files
- Generate contours with lunar-specific parameters
- Export contour data for analysis
- Create visualization outputs

Author: Lunar Analysis Team
Date: 2024
"""

import sys
import os
import traceback
import time
import numpy as np
from datetime import datetime

try:
    from PIL import Image
    PIL_AVAILABLE = True
    print("✅ PIL (Pillow) is available")
    
    # Increase the decompression bomb limit for large lunar DEM images
    Image.MAX_IMAGE_PIXELS = None  # Disable the limit completely
    print("✅ Decompression bomb limit disabled for large lunar images")
    
except ImportError:
    PIL_AVAILABLE = False
    print("❌ PIL not available. Please install: pip install pillow")

try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as colors
    MATPLOTLIB_AVAILABLE = True
    print("✅ Matplotlib is available")
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib not available. Visualization will be limited.")

class LunarContourGenerator:
    """
    🌙 Lunar Contour Generator for Real-Time DEM Processing
    """
    
    def __init__(self):
        """Initialize the contour generator"""
        if not PIL_AVAILABLE:
            raise Exception("PIL (Pillow) is required but not available. Install with: pip install pillow")
            
        self.layers = {}
        self.contour_results = {}
        print("✅ LunarContourGenerator initialized successfully")
    
    def load_tif_file(self, tif_path, layer_name="Raster", max_size=8192):
        """
        Load a TIF file using PIL (basic image reading)
        
        Args:
            tif_path (str): Path to the TIF file
            layer_name (str): Name for the layer
            max_size (int): Maximum dimension size for resizing large images
            
        Returns:
            dict or None: Layer information or None if failed
        """
        try:
            # Check if file exists
            if not os.path.exists(tif_path):
                print(f"❌ File not found: {tif_path}")
                return None
            
            # Open the image using PIL
            image = Image.open(tif_path)
            
            # Check image size and warn if very large
            width, height = image.size
            total_pixels = width * height
            print(f"   - Image size: {width} x {height} = {total_pixels:,} pixels")
            
            if total_pixels > 100000000:  # 100 million pixels
                print(f"   ⚠️  Large image detected ({total_pixels:,} pixels)")
                print(f"   - This may take some time to process...")
            
            # For very large images, resize for faster processing
            if width > max_size or height > max_size:
                print(f"   ⚠️  Large image detected. Resizing for faster processing...")
                print(f"   - Original size: {width} x {height}")
                
                # Calculate new dimensions while maintaining aspect ratio
                if width > height:
                    new_width = max_size
                    new_height = int(height * max_size / width)
                else:
                    new_height = max_size
                    new_width = int(width * max_size / height)
                
                print(f"   - Resized to: {new_width} x {new_height}")
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                width, height = new_width, new_height
                total_pixels = width * height
            
            # Convert to numpy array
            data = np.array(image)
            
            # Convert to grayscale if it's RGB/RGBA
            if len(data.shape) == 3:
                # Convert to grayscale using luminance formula
                if data.shape[2] == 3:  # RGB
                    data = np.dot(data[..., :3], [0.299, 0.587, 0.114])
                elif data.shape[2] == 4:  # RGBA
                    data = np.dot(data[..., :3], [0.299, 0.587, 0.114])
            
            # Get image information
            width, height = image.size
            mode = image.mode
            
            # Calculate basic statistics
            stats = {
                'min': np.min(data),
                'max': np.max(data),
                'mean': np.mean(data),
                'std': np.std(data)
            }
            
            layer_info = {
                'data': data,
                'width': width,
                'height': height,
                'mode': mode,
                'stats': stats,
                'path': tif_path
            }
            
            self.layers[layer_name] = layer_info
            
            print(f"✅ Successfully loaded raster: {tif_path}")
            print(f"   - Width: {width} pixels")
            print(f"   - Height: {height} pixels")
            print(f"   - Mode: {mode}")
            print(f"   - Min elevation: {stats['min']:.2f}")
            print(f"   - Max elevation: {stats['max']:.2f}")
            print(f"   - Mean elevation: {stats['mean']:.2f}")
            print(f"   - Std dev elevation: {stats['std']:.2f}")
            
            return layer_info
                
        except Exception as e:
            print(f"❌ Error loading raster: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return None
    
    def generate_contours(self, input_layer_name, output_path, 
                         interval=50, attribute_name="elevation", 
                         offset=None, simplification_tolerance=None):
        """
        Generate contours from a raster layer with lunar-specific parameters
        
        Args:
            input_layer_name (str): Name of the input layer
            output_path (str): Path for the output contour file
            interval (float): Vertical distance between contour lines (meters)
            attribute_name (str): Name for elevation value attribute field
            offset (float, optional): Base elevation to start generating contours
            simplification_tolerance (float, optional): Smoothing tolerance for contour lines
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            layer_info = self.layers[input_layer_name]
            data = layer_info['data']
            
            print(f"🌙 Generating lunar contours from: {input_layer_name}")
            print(f"   - Interval between contours: {interval} meters")
            print(f"   - Attribute name: {attribute_name}")
            if offset is not None:
                print(f"   - Offset: {offset} meters")
            if simplification_tolerance is not None:
                print(f"   - Simplification tolerance: {simplification_tolerance}")
            
            # Get elevation range
            min_elev = layer_info['stats']['min']
            max_elev = layer_info['stats']['max']
            
            # Handle NaN values
            if np.isnan(min_elev) or np.isnan(max_elev):
                print(f"   ⚠️  NaN values detected in elevation data")
                print(f"   - Using fallback values: min=0, max=100")
                min_elev = 0.0
                max_elev = 100.0
            
            # Set offset if not provided
            if offset is None:
                offset = min_elev
            
            # Generate contour levels
            contour_levels = np.arange(offset, max_elev + interval, interval)
            print(f"   - Contour levels: {len(contour_levels)} levels from {offset:.1f} to {max_elev:.1f}")
            
            # Generate contours using a simpler approach
            if MATPLOTLIB_AVAILABLE:
                # Create contour array
                contour_array = np.zeros_like(data, dtype=np.uint8)
                contour_data = []
                
                # Generate contours for each level
                for level in contour_levels:
                    # Create mask for this elevation level
                    mask = (data >= level) & (data < level + interval)
                    
                    if np.any(mask):
                        # Find the boundary of the mask
                        from scipy import ndimage
                        
                        # Create a binary mask
                        binary_mask = mask.astype(np.uint8)
                        
                        # Find edges using morphological operations
                        eroded = ndimage.binary_erosion(binary_mask)
                        edges = binary_mask & ~eroded
                        
                        if np.any(edges):
                            # Get contour points
                            y_coords, x_coords = np.where(edges)
                            if len(x_coords) > 2:
                                # Sort points to create a continuous line
                                points = np.column_stack((x_coords, y_coords))
                                
                                # Add to contour data
                                contour_data.append({
                                    'level': level,
                                    'vertices': points,
                                    'attribute': attribute_name,
                                    'elevation': level
                                })
                                
                                # Draw contour on array
                                contour_array[edges] = 255
                
                print(f"   - Generated {len(contour_data)} contour lines")
                
                # Save contour image
                contour_image = Image.fromarray(contour_array, mode='L')
                contour_image.save(output_path)
                
                print(f"✅ Lunar contour generation completed!")
                print(f"   - Output saved to: {output_path}")
                print(f"   - Generated {len(contour_data)} contour lines")
                
                # Store contour information
                contour_info = {
                    'data': contour_array,
                    'width': data.shape[1],
                    'height': data.shape[0],
                    'path': output_path,
                    'contour_levels': contour_levels,
                    'contour_data': contour_data,
                    'stats': {
                        'min': np.min(contour_array),
                        'max': np.max(contour_array),
                        'mean': np.mean(contour_array),
                        'std': np.std(contour_array),
                        'num_contours': len(contour_data)
                    }
                }
                
                self.layers["Lunar_Contours"] = contour_info
                
                print(f"   - Contour levels: {len(contour_levels)}")
                print(f"   - Contour lines: {len(contour_data)}")
                print(f"   - Elevation range: {min_elev:.1f} to {max_elev:.1f} meters")
                
                return True
            else:
                print("❌ Matplotlib not available. Cannot generate contours.")
                return False
                
        except Exception as e:
            print(f"❌ Error generating contours: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def analyze_contour_statistics(self, contour_layer_name="Lunar_Contours"):
        """
        Analyze contour data for lunar terrain characteristics
        
        Args:
            contour_layer_name (str): Name of the contour layer to analyze
            
        Returns:
            dict or None: Analysis results or None if failed
        """
        if contour_layer_name not in self.layers:
            print(f"❌ Contour layer '{contour_layer_name}' not found")
            return None
            
        try:
            layer_info = self.layers[contour_layer_name]
            contour_data = layer_info['contour_data']
            contour_levels = layer_info['contour_levels']
            
            print(f"\n🌑 Lunar Contour Analysis:")
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"1. Contour Layer: {contour_layer_name}")
            print(f"2. Number of Contour Lines: {len(contour_data)}")
            print(f"3. Number of Contour Levels: {len(contour_levels)}")
            print(f"4. Elevation Range: {contour_levels[0]:.1f} to {contour_levels[-1]:.1f} meters")
            
            # Analyze contour patterns
            print(f"\n🔍 Terrain Characteristics:")
            
            # Calculate contour density
            total_contour_length = sum(len(contour['vertices']) for contour in contour_data)
            area = layer_info['width'] * layer_info['height']
            contour_density = total_contour_length / area if area > 0 else 0
            
            print(f"   - Contour density: {contour_density:.4f} pixels per pixel²")
            
            # Analyze elevation distribution
            elevation_ranges = []
            for i in range(len(contour_levels) - 1):
                count = sum(1 for contour in contour_data 
                           if contour_levels[i] <= contour['level'] < contour_levels[i + 1])
                elevation_ranges.append({
                    'range': f"{contour_levels[i]:.0f}-{contour_levels[i + 1]:.0f}m",
                    'count': count
                })
            
            print(f"   - Elevation distribution:")
            for range_info in elevation_ranges:
                if range_info['count'] > 0:
                    print(f"     * {range_info['range']}: {range_info['count']} contours")
            
            # Terrain complexity assessment
            if contour_density > 0.01:
                terrain_complexity = "HIGH"
                print("   - HIGH TERRAIN COMPLEXITY: Steep, varied lunar landscape")
            elif contour_density > 0.005:
                terrain_complexity = "MODERATE"
                print("   - MODERATE TERRAIN COMPLEXITY: Mixed lunar terrain")
            else:
                terrain_complexity = "LOW"
                print("   - LOW TERRAIN COMPLEXITY: Gentle lunar landscape")
            
            # Store analysis results
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'num_contours': len(contour_data),
                'num_levels': len(contour_levels),
                'elevation_range': [contour_levels[0], contour_levels[-1]],
                'contour_density': contour_density,
                'terrain_complexity': terrain_complexity,
                'elevation_distribution': elevation_ranges
            }
            
            self.contour_results[contour_layer_name] = analysis_result
            
            print(f"\n📊 Analysis Summary:")
            print(f"   - Terrain Complexity: {terrain_complexity}")
            print(f"   - Contour Density: {contour_density:.4f}")
            print(f"   - Total Contour Lines: {len(contour_data)}")
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error analyzing contour statistics: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return None
    
    def export_contour_report(self, output_file="lunar_contour_analysis_report.txt"):
        """
        Export contour analysis results to a text file
        
        Args:
            output_file (str): Path for the output report file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Lunar Contour Analysis Report\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for layer_name, analysis in self.contour_results.items():
                    f.write(f"Layer: {layer_name}\n")
                    f.write(f"Timestamp: {analysis['timestamp']}\n")
                    f.write(f"Terrain Complexity: {analysis['terrain_complexity']}\n")
                    f.write(f"Statistics:\n")
                    f.write(f"  - Number of Contours: {analysis['num_contours']}\n")
                    f.write(f"  - Number of Levels: {analysis['num_levels']}\n")
                    f.write(f"  - Contour Density: {analysis['contour_density']:.4f}\n")
                    f.write(f"  - Elevation Range: {analysis['elevation_range'][0]:.1f} to {analysis['elevation_range'][1]:.1f} meters\n")
                    f.write(f"Elevation Distribution:\n")
                    for range_info in analysis['elevation_distribution']:
                        if range_info['count'] > 0:
                            f.write(f"  - {range_info['range']}: {range_info['count']} contours\n")
                    f.write("\n" + "-" * 30 + "\n\n")
                
            print(f"✅ Contour analysis report exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exporting contour report: {e}")
    
    def visualize_contours(self, contour_layer_name="Lunar_Contours", output_file="contour_visualization.png"):
        """
        Create a visualization of the contours
        
        Args:
            contour_layer_name (str): Name of the contour layer to visualize
            output_file (str): Path for the output visualization file
        """
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available. Cannot create visualization.")
            return False
            
        if contour_layer_name not in self.layers:
            print(f"❌ Contour layer '{contour_layer_name}' not found")
            return False
            
        try:
            layer_info = self.layers[contour_layer_name]
            contour_data = layer_info['contour_data']
            contour_levels = layer_info['contour_levels']
            
            plt.figure(figsize=(12, 8))
            
            # Plot contours
            for contour in contour_data:
                vertices = contour['vertices']
                plt.plot(vertices[:, 0], vertices[:, 1], 'k-', linewidth=0.5, alpha=0.7)
            
            plt.title('Lunar Contour Visualization\n(Terrain Analysis)')
            plt.xlabel('Pixel X')
            plt.ylabel('Pixel Y')
            plt.gca().invert_yaxis()  # Invert Y-axis to match image coordinates
            
            # Add analysis information
            terrain_complexity = self.contour_results.get(contour_layer_name, {}).get('terrain_complexity', 'UNKNOWN')
            num_contours = len(contour_data)
            
            info_text = f"Terrain Complexity: {terrain_complexity}\n"
            info_text += f"Number of Contours: {num_contours}\n"
            info_text += f"Elevation Levels: {len(contour_levels)}"
            
            plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Contour visualization saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating contour visualization: {e}")
            return False
    
    def process_dem_contours(self, tif_path, output_dir="counter_outputs", 
                           interval=50, attribute_name="elevation", 
                           offset=None, simplification_tolerance=None):
        """
        Process DEM to generate contours in real-time
        
        Args:
            tif_path (str): Path to the input DEM TIF file
            output_dir (str): Directory for output files
            interval (float): Vertical distance between contour lines
            attribute_name (str): Name for elevation attribute field
            offset (float, optional): Base elevation to start contours
            simplification_tolerance (float, optional): Smoothing tolerance
        """
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                print(f"✅ Created output directory: {output_dir}")
            
            # Load DEM
            print(f"\n📁 Loading DEM: {tif_path}")
            layer_name = "Moon_DEM"
            dem_layer = self.load_tif_file(tif_path, layer_name)
            
            if dem_layer is None:
                print("❌ Failed to load DEM. Cannot proceed with contour generation.")
                return False
            
            # Generate contours with lunar parameters
            print(f"\n🌙 Generating lunar contours...")
            contour_output = os.path.join(output_dir, "counter_output.tif")
            success = self.generate_contours(layer_name, contour_output, 
                                           interval=interval, attribute_name=attribute_name,
                                           offset=offset, simplification_tolerance=simplification_tolerance)
            
            if success:
                # Analyze contour statistics
                print(f"\n🔍 Analyzing contour statistics...")
                analysis_result = self.analyze_contour_statistics("Lunar_Contours")
                
                if analysis_result:
                    # Export analysis report
                    report_file = os.path.join(output_dir, "lunar_contour_analysis_report.txt")
                    self.export_contour_report(report_file)
                    
                    # Create visualization
                    if MATPLOTLIB_AVAILABLE:
                        viz_file = os.path.join(output_dir, "contour_visualization.png")
                        self.visualize_contours("Lunar_Contours", viz_file)
                    
                    print(f"\n✅ Real-time contour processing completed successfully!")
                    print(f"   - Contours saved to: {contour_output}")
                    print(f"   - Analysis report saved to: {report_file}")
                    if MATPLOTLIB_AVAILABLE:
                        print(f"   - Visualization saved to: {viz_file}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error in real-time contour processing: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def list_layers(self):
        """List all loaded layers"""
        print("\n📋 Loaded Layers:")
        for name, layer_info in self.layers.items():
            if 'path' in layer_info:
                print(f"   - {name}: {layer_info['path']}")
            else:
                print(f"   - {name}: {layer_info['width']}x{layer_info['height']} pixels")

def main():
    """
    Main function to demonstrate real-time lunar contour processing
    """
    processor = None
    try:
        print("🌙 Starting Real-Time Lunar Contour Generator...")
        
        # Initialize processor
        processor = LunarContourGenerator()
        
        # Example TIF file path (replace with your actual path)
        # Example: # Example: tif_path = r"D:\data\derived\20090731\ch1_tmc_ndn_20090731T1812342475_d_oth_d18.tif"
    tif_path = sys.argv[1] if len(sys.argv) > 1 else None
    tif_path = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Check if file exists
        if not os.path.exists(tif_path):
            print(f"⚠️  Example file not found: {tif_path}")
            print("   Please update the tif_path variable with your actual file path")
            return
        
        # Process DEM to generate contours in real-time
        print("\n🔄 Processing DEM for contour generation...")
        success = processor.process_dem_contours(
            tif_path, 
            output_dir="counter_outputs",
            interval=50,              # 50 meters between contours
            attribute_name="elevation", # Attribute field name
            offset=None,              # Start from minimum elevation
            simplification_tolerance=None  # No simplification for accuracy
        )
        
        if success:
            print("\n✅ Real-time lunar contour generation completed successfully!")
        else:
            print("\n❌ Real-time contour generation failed!")
        
    except Exception as e:
        print(f"❌ Error in main function: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
    
    finally:
        print("\n📝 Usage Instructions:")
        print("1. Update the tif_path variable with your actual TIF file path")
        print("2. Run the script for real-time contour generation")
        print("3. Check the 'counter_outputs' directory for results")
        print("4. Contour parameters can be adjusted in the process_dem_contours method")
        print("5. Install required packages: pip install pillow matplotlib numpy")

if __name__ == "__main__":
    main() 