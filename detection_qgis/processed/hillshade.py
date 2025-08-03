#!/usr/bin/env python3
"""
🌙 Lunar Hillshade Processor for Real-Time Landslide Detection
==============================================================

This script processes lunar DEM data to create hillshade visualizations
and analyze landslide potential using numpy and matplotlib processing in real-time.

Hillshade Parameters for Lunar Analysis:
- Azimuth: 315° (NW) - sun direction (default)
- Altitude: 45° - sun elevation angle (default)
- Z Factor: 1.0 - for meter-based DEMs like LOLA
- Scale: 1.0 - horizontal/vertical ratio

Real-time processing capabilities:
- Load DEM from TIF files (using PIL for basic image reading)
- Generate hillshade with lunar-specific parameters
- Analyze landslide potential indicators
- Export results for further analysis

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

class LunarHillshadeProcessor:
    """
    🌙 Lunar Hillshade Processor for Real-Time Landslide Detection
    """
    
    def __init__(self):
        """Initialize the processor"""
        if not PIL_AVAILABLE:
            raise Exception("PIL (Pillow) is required but not available. Install with: pip install pillow")
            
        self.layers = {}
        self.analysis_results = {}
        print("✅ LunarHillshadeProcessor initialized successfully")
    
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
            
            # Convert to numpy array
            data = np.array(image)
            
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
            print(f"   - Min value: {stats['min']:.2f}")
            print(f"   - Max value: {stats['max']:.2f}")
            print(f"   - Mean value: {stats['mean']:.2f}")
            print(f"   - Std dev: {stats['std']:.2f}")
            
            return layer_info
                
        except Exception as e:
            print(f"❌ Error loading raster: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return None
    
    def calculate_hillshade(self, input_layer_name, output_path, 
                           azimuth=315, altitude=45, z_factor=1.0, scale=1.0):
        """
        Calculate hillshade from a raster layer with lunar-specific parameters
        
        Args:
            input_layer_name (str): Name of the input layer
            output_path (str): Path for the output hillshade file
            azimuth (float): Sun direction (degrees from north clockwise) - default 315° (NW)
            altitude (float): Sun elevation angle above the horizon - default 45°
            z_factor (float): Elevation exaggeration - default 1.0 (for meter-based DEMs)
            scale (float): Ratio of horizontal to vertical units - default 1.0
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if input_layer_name not in self.layers:
                print(f"❌ Layer '{input_layer_name}' not found")
                return False
                
            layer_info = self.layers[input_layer_name]
            data = layer_info['data']
            
            print(f"🌙 Calculating lunar hillshade from: {input_layer_name}")
            print(f"   - Azimuth: {azimuth}° (sun direction)")
            print(f"   - Altitude: {altitude}° (sun elevation)")
            print(f"   - Z Factor: {z_factor} (elevation exaggeration)")
            print(f"   - Scale: {scale} (horizontal/vertical ratio)")
            
            # Convert azimuth and altitude to radians
            azimuth_rad = np.radians(azimuth)
            altitude_rad = np.radians(altitude)
            
            # Calculate sun position
            sun_x = np.sin(azimuth_rad) * np.cos(altitude_rad)
            sun_y = np.cos(azimuth_rad) * np.cos(altitude_rad)
            sun_z = np.sin(altitude_rad)
            
            # Get image dimensions
            height, width = data.shape
            
            # Calculate gradients using finite differences
            dx = np.zeros_like(data, dtype=np.float64)
            dy = np.zeros_like(data, dtype=np.float64)
            
            # Central differences for interior pixels
            dx[:, 1:-1] = (data[:, 2:] - data[:, :-2]) / (2 * scale)
            dy[1:-1, :] = (data[2:, :] - data[:-2, :]) / (2 * scale)
            
            # Forward/backward differences for edges
            dx[:, 0] = (data[:, 1] - data[:, 0]) / scale
            dx[:, -1] = (data[:, -1] - data[:, -2]) / scale
            dy[0, :] = (data[1, :] - data[0, :]) / scale
            dy[-1, :] = (data[-1, :] - data[-2, :]) / scale
            
            # Apply Z factor
            dx *= z_factor
            dy *= z_factor
            
            # Calculate hillshade
            hillshade = (sun_x * dx + sun_y * dy + sun_z) / np.sqrt(dx**2 + dy**2 + 1)
            
            # Normalize to 0-255 range
            hillshade = np.clip(hillshade * 255, 0, 255).astype(np.uint8)
            
            # Save hillshade as image
            hillshade_image = Image.fromarray(hillshade, mode='L')
            hillshade_image.save(output_path)
            
            print(f"✅ Lunar hillshade calculation completed!")
            print(f"   - Output saved to: {output_path}")
            
            # Store hillshade information
            hillshade_info = {
                'data': hillshade,
                'width': width,
                'height': height,
                'path': output_path,
                'stats': {
                    'min': np.min(hillshade),
                    'max': np.max(hillshade),
                    'mean': np.mean(hillshade),
                    'std': np.std(hillshade)
                }
            }
            
            self.layers["Lunar_Hillshade"] = hillshade_info
            
            print(f"   - Min hillshade value: {hillshade_info['stats']['min']:.2f}")
            print(f"   - Max hillshade value: {hillshade_info['stats']['max']:.2f}")
            print(f"   - Mean hillshade value: {hillshade_info['stats']['mean']:.2f}")
            print(f"   - Std dev hillshade value: {hillshade_info['stats']['std']:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error calculating hillshade: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def analyze_lunar_landslide_potential(self, hillshade_layer_name="Lunar_Hillshade"):
        """
        Analyze hillshade data for lunar landslide potential in real-time
        
        Args:
            hillshade_layer_name (str): Name of the hillshade layer to analyze
            
        Returns:
            dict or None: Analysis results or None if failed
        """
        if hillshade_layer_name not in self.layers:
            print(f"❌ Hillshade layer '{hillshade_layer_name}' not found")
            return None
            
        try:
            layer_info = self.layers[hillshade_layer_name]
            stats = layer_info['stats']
            
            print(f"\n🌑 Real-Time Lunar Landslide Analysis:")
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"1. Hillshade Layer: {hillshade_layer_name}")
            print(f"2. Min Hillshade Value: {stats['min']:.2f}")
            print(f"3. Max Hillshade Value: {stats['max']:.2f}")
            print(f"4. Mean Hillshade Value: {stats['mean']:.2f}")
            print(f"5. Standard Deviation: {stats['std']:.2f}")
            
            # Analyze hillshade patterns for landslide indicators
            print(f"\n🔍 Landslide Potential Indicators:")
            
            # High contrast areas (potential steep slopes)
            contrast_threshold = stats['mean'] + stats['std']
            print(f"   - High contrast threshold: {contrast_threshold:.2f}")
            
            # Shadow areas (potential overhangs or steep cliffs)
            shadow_threshold = stats['mean'] - stats['std']
            print(f"   - Shadow threshold: {shadow_threshold:.2f}")
            
            # Bright areas (potential exposed slopes)
            bright_threshold = stats['mean'] + 0.5 * stats['std']
            print(f"   - Bright area threshold: {bright_threshold:.2f}")
            
            # Risk assessment
            print(f"\n⚠️  Real-Time Risk Assessment:")
            risk_level = "LOW"
            risk_factors = []
            
            if stats['std'] > 50:
                risk_level = "HIGH"
                risk_factors.append("High terrain variability")
                print("   - HIGH VARIABILITY: Potential for steep terrain and landslides")
            elif stats['std'] > 30:
                risk_level = "MODERATE"
                risk_factors.append("Moderate terrain variability")
                print("   - MODERATE VARIABILITY: Some steep areas present")
            else:
                risk_factors.append("Low terrain variability")
                print("   - LOW VARIABILITY: Generally gentle terrain")
                
            if stats['max'] > 250:
                risk_factors.append("Bright exposed areas")
                print("   - BRIGHT AREAS: Exposed slopes or cliffs detected")
            if stats['min'] < 50:
                risk_factors.append("Deep shadow areas")
                print("   - DARK SHADOWS: Deep shadows or overhangs present")
            
            # Store analysis results
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'min': stats['min'],
                'max': stats['max'],
                'mean': stats['mean'],
                'std': stats['std'],
                'contrast_threshold': contrast_threshold,
                'shadow_threshold': shadow_threshold,
                'bright_threshold': bright_threshold,
                'risk_level': risk_level,
                'risk_factors': risk_factors
            }
            
            self.analysis_results[hillshade_layer_name] = analysis_result
            
            print(f"\n📊 Analysis Summary:")
            print(f"   - Risk Level: {risk_level}")
            print(f"   - Risk Factors: {', '.join(risk_factors)}")
            print(f"   - Analysis stored for further processing")
            
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error analyzing lunar landslide potential: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return None
    
    def export_analysis_report(self, output_file="lunar_landslide_analysis_report.txt"):
        """
        Export analysis results to a text file
        
        Args:
            output_file (str): Path for the output report file
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Lunar Landslide Analysis Report\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for layer_name, analysis in self.analysis_results.items():
                    f.write(f"Layer: {layer_name}\n")
                    f.write(f"Timestamp: {analysis['timestamp']}\n")
                    f.write(f"Risk Level: {analysis['risk_level']}\n")
                    f.write(f"Risk Factors: {', '.join(analysis['risk_factors'])}\n")
                    f.write(f"Statistics:\n")
                    f.write(f"  - Min: {analysis['min']:.2f}\n")
                    f.write(f"  - Max: {analysis['max']:.2f}\n")
                    f.write(f"  - Mean: {analysis['mean']:.2f}\n")
                    f.write(f"  - Std Dev: {analysis['std']:.2f}\n")
                    f.write(f"Thresholds:\n")
                    f.write(f"  - Contrast: {analysis['contrast_threshold']:.2f}\n")
                    f.write(f"  - Shadow: {analysis['shadow_threshold']:.2f}\n")
                    f.write(f"  - Bright: {analysis['bright_threshold']:.2f}\n")
                    f.write("\n" + "-" * 30 + "\n\n")
                
            print(f"✅ Analysis report exported to: {output_file}")
                
            print(f"✅ Analysis report exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exporting analysis report: {e}")
    
    def visualize_hillshade(self, hillshade_layer_name="Lunar_Hillshade", output_file="hillshade_visualization.png"):
        """
        Create a visualization of the hillshade
        
        Args:
            hillshade_layer_name (str): Name of the hillshade layer to visualize
            output_file (str): Path for the output visualization file
        """
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib not available. Cannot create visualization.")
            return False
            
        if hillshade_layer_name not in self.layers:
            print(f"❌ Hillshade layer '{hillshade_layer_name}' not found")
            return False
            
        try:
            layer_info = self.layers[hillshade_layer_name]
            hillshade_data = layer_info['data']
            
            plt.figure(figsize=(12, 8))
            plt.imshow(hillshade_data, cmap='gray', aspect='equal')
            plt.colorbar(label='Hillshade Value')
            plt.title('🌙 Lunar Hillshade Visualization\n(Landslide Detection Analysis)')
            plt.xlabel('Pixel X')
            plt.ylabel('Pixel Y')
            
            # Add analysis information
            stats = layer_info['stats']
            risk_level = self.analysis_results.get(hillshade_layer_name, {}).get('risk_level', 'UNKNOWN')
            
            info_text = f"Risk Level: {risk_level}\n"
            info_text += f"Mean: {stats['mean']:.1f}\n"
            info_text += f"Std Dev: {stats['std']:.1f}"
            
            plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"✅ Hillshade visualization saved to: {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error creating visualization: {e}")
            return False
    
    def process_dem_realtime(self, tif_path, output_dir="hillshade_outputs"):
        """
        Process DEM in real-time for landslide detection
        
        Args:
            tif_path (str): Path to the input DEM TIF file
            output_dir (str): Directory for output files
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
                print("❌ Failed to load DEM. Cannot proceed with analysis.")
                return False
            
            # Generate hillshade with lunar parameters
            print(f"\n🌙 Generating lunar hillshade...")
            hillshade_output = os.path.join(output_dir, "lunar_hillshade.png")
            success = self.calculate_hillshade(layer_name, hillshade_output, 
                                             azimuth=315, altitude=45, z_factor=1.0, scale=1.0)
            
            if success:
                # Analyze landslide potential
                print(f"\n🔍 Analyzing landslide potential...")
                analysis_result = self.analyze_lunar_landslide_potential("Lunar_Hillshade")
                
                if analysis_result:
                    # Export analysis report
                    report_file = os.path.join(output_dir, "lunar_landslide_analysis_report.txt")
                    self.export_analysis_report(report_file)
                    
                    # Create visualization
                    if MATPLOTLIB_AVAILABLE:
                        viz_file = os.path.join(output_dir, "hillshade_visualization.png")
                        self.visualize_hillshade("Lunar_Hillshade", viz_file)
                    
                    print(f"\n✅ Real-time processing completed successfully!")
                    print(f"   - Hillshade saved to: {hillshade_output}")
                    print(f"   - Analysis report saved to: {report_file}")
                    if MATPLOTLIB_AVAILABLE:
                        print(f"   - Visualization saved to: {viz_file}")
                    return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error in real-time processing: {e}")
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
    Main function to demonstrate real-time lunar hillshade processing
    """
    processor = None
    try:
        print("🌙 Starting Real-Time Lunar Hillshade Processor...")
        
        # Initialize processor
        processor = LunarHillshadeProcessor()
        
        # Example TIF file path (replace with your actual path)
        tif_path = r"E:\moon extract\data\derived\20250207\PIA12927.tif"
        
        # Check if file exists
        if not os.path.exists(tif_path):
            print(f"⚠️  Example file not found: {tif_path}")
            print("   Please update the tif_path variable with your actual file path")
            return
        
        # Process DEM in real-time
        print("\n🔄 Processing DEM in real-time...")
        success = processor.process_dem_realtime(tif_path, "hillshade_outputs")
        
        if success:
            print("\n✅ Real-time lunar hillshade processing completed successfully!")
        else:
            print("\n❌ Real-time processing failed!")
        
    except Exception as e:
        print(f"❌ Error in main function: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
    
    finally:
        print("\n📝 Usage Instructions:")
        print("1. Update the tif_path variable with your actual TIF file path")
        print("2. Run the script for real-time hillshade processing")
        print("3. Check the 'hillshade_outputs' directory for results")
        print("4. Hillshade parameters can be adjusted in the calculate_hillshade method")
        print("5. Install required packages: pip install pillow matplotlib numpy")

if __name__ == "__main__":
    main() 