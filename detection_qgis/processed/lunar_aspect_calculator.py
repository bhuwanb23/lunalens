#!/usr/bin/env python3
"""
Lunar Aspect Calculator for Real-Time Landslide Detection
========================================================

This script calculates aspect in real-time using the tif_processor.py integration.
It provides comprehensive aspect analysis for lunar landslide detection.
"""

import os
import sys
from datetime import datetime

# Import the TifProcessor from tif_processor.py
try:
    from tif_processor import TifProcessor
    print("✅ Successfully imported TifProcessor")
except ImportError as e:
    print(f"❌ Error importing TifProcessor: {e}")
    print("   Make sure tif_processor.py is in the same directory")
    sys.exit(1)

def calculate_aspect_with_gdal(input_path, output_path):
    """
    Calculate aspect using GDAL directly
    """
    try:
        from osgeo import gdal
        
        print(f"   - Using GDAL to calculate aspect...")
        
        # Calculate aspect using GDAL DEMProcessing with correct parameters
        result = gdal.DEMProcessing(output_path, input_path, 'aspect', 
                                   format='GTiff', 
                                   computeEdges=True,
                                   alg='Horn')
        
        if result:
            print(f"   ✅ Aspect calculation completed using GDAL")
            return True
        else:
            print(f"   ❌ Aspect calculation failed")
            return False
            
    except ImportError:
        print(f"   ❌ GDAL not available")
        return False
    except Exception as e:
        print(f"   ❌ Error in GDAL aspect calculation: {e}")
        return False

def calculate_slope_with_gdal(input_path, output_path):
    """
    Calculate slope using GDAL directly
    """
    try:
        from osgeo import gdal
        
        print(f"   - Using GDAL to calculate slope...")
        
        # Calculate slope using GDAL DEMProcessing with correct parameters
        # Note: Removed problematic parameters that were causing errors
        result = gdal.DEMProcessing(output_path, input_path, 'slope', 
                                   format='GTiff', 
                                   computeEdges=True,
                                   alg='Horn',
                                   scale=1.0)
        
        if result:
            print(f"   ✅ Slope calculation completed using GDAL")
            return True
        else:
            print(f"   ❌ Slope calculation failed")
            return False
        
    except ImportError:
        print(f"   ❌ GDAL not available")
        return False
    except Exception as e:
        print(f"   ❌ Error in GDAL slope calculation: {e}")
        return False

def calculate_lunar_aspect(dem_path, output_dir="aspect_outputs"):
    """
    Calculate aspect for lunar landslide detection in real-time
    """
    print(f"\n🌙 LUNAR ASPECT CALCULATION FOR LANDSLIDE DETECTION")
    print("=" * 70)
    
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✅ Created output directory: {output_dir}")
        
        # Initialize TifProcessor
        print("🔄 Initializing QGIS TifProcessor...")
        processor = TifProcessor()
        
        # Load the DEM file
        print(f"📁 Loading DEM file: {dem_path}")
        dem_layer = processor.load_tif_file(dem_path, "Lunar_DEM")
        
        if dem_layer is None:
            print("❌ Failed to load DEM file")
            processor.cleanup()
            return False
        
        # Get elevation statistics first
        print("\n📊 ELEVATION STATISTICS:")
        elevation_stats = processor.elevation_statistics("Lunar_DEM")
        
        if elevation_stats:
            print(f"   • Elevation Range: {elevation_stats['range']:.2f} meters")
            print(f"   • Mean Elevation: {elevation_stats['mean']:.2f} meters")
            print(f"   • Standard Deviation: {elevation_stats['std']:.2f} meters")
        
        # Calculate aspect using GDAL
        aspect_output = os.path.join(output_dir, "lunar_aspect.tif")
        print(f"\n🧮 CALCULATING ASPECT:")
        print("   - Input: Lunar DEM")
        print("   - Output: lunar_aspect.tif")
        print("   - Method: GDAL Aspect Algorithm")
        
        aspect_success = calculate_aspect_with_gdal(dem_path, aspect_output)
        
        if aspect_success:
            print("✅ Aspect calculation completed successfully!")
            
            # Calculate slope for comprehensive analysis
            slope_output = os.path.join(output_dir, "lunar_slope.tif")
            print(f"\n📈 CALCULATING SLOPE:")
            print("   - Input: Lunar DEM")
            print("   - Output: lunar_slope.tif")
            print("   - Method: GDAL Slope Algorithm")
            
            slope_success = calculate_slope_with_gdal(dem_path, slope_output)
            
            if slope_success:
                print("✅ Slope calculation completed successfully!")
                
                # Generate comprehensive analysis report
                generate_aspect_analysis_report(dem_path, aspect_output, slope_output, 
                                             elevation_stats, output_dir)
                
                # List all generated layers
                processor.list_layers()
                
                print(f"\n🎯 ASPECT ANALYSIS COMPLETE!")
                print(f"   - DEM loaded: {dem_path}")
                print(f"   - Aspect calculated: {aspect_output}")
                print(f"   - Slope calculated: {slope_output}")
                print(f"   - All outputs saved in: {output_dir}")
                
                return True
            else:
                print("❌ Slope calculation failed")
                return False
        else:
            print("❌ Aspect calculation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error in aspect calculation: {e}")
        return False
    finally:
        # Clean up QGIS
        if 'processor' in locals():
            processor.cleanup()

def generate_aspect_analysis_report(dem_path, aspect_path, slope_path, elevation_stats, output_dir):
    """
    Generate comprehensive aspect analysis report
    """
    report_path = os.path.join(output_dir, "lunar_aspect_analysis_report.txt")
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("LUNAR ASPECT ANALYSIS REPORT\n")
            f.write("=" * 40 + "\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("INPUT PARAMETERS:\n")
            f.write("-" * 20 + "\n")
            f.write("✅ Required Parameters:\n")
            f.write(f"• Elevation (DEM): {dem_path}\n")
            f.write("• Raster cell size: From DEM metadata\n")
            f.write("• Aspect values: Calculated ✓\n")
            f.write("• Slope values: Calculated ✓\n\n")
            
            f.write("OUTPUT FILES:\n")
            f.write("-" * 15 + "\n")
            f.write(f"• Aspect raster: {aspect_path}\n")
            f.write(f"• Slope raster: {slope_path}\n")
            f.write(f"• Analysis report: {report_path}\n\n")
            
            if elevation_stats:
                f.write("ELEVATION STATISTICS:\n")
                f.write("-" * 25 + "\n")
                f.write(f"• Minimum Elevation: {elevation_stats['min']:.2f} m\n")
                f.write(f"• Maximum Elevation: {elevation_stats['max']:.2f} m\n")
                f.write(f"• Mean Elevation: {elevation_stats['mean']:.2f} m\n")
                f.write(f"• Elevation Range: {elevation_stats['range']:.2f} m\n")
                f.write(f"• Standard Deviation: {elevation_stats['std']:.2f} m\n\n")
            
            f.write("LANDSLIDE DETECTION PARAMETERS:\n")
            f.write("-" * 35 + "\n")
            f.write("Required Parameters:\n")
            f.write("• Elevation (DEM) - ✓ Available and processed\n")
            f.write("• Raster cell size - ✓ From DEM metadata\n")
            f.write("• Aspect values - ✓ Calculated and saved\n")
            f.write("• Slope values - ✓ Calculated and saved\n\n")
            
            f.write("Optional Parameters:\n")
            f.write("• Crater mask - Can be added for specific analysis\n")
            f.write("• Solar illumination - Based on calculated aspect\n")
            f.write("• Regolith properties - Local characteristics\n")
            f.write("• Elevation changes - ✓ Analyzed from DEM\n\n")
            
            f.write("ASPECT ANALYSIS RESULTS:\n")
            f.write("-" * 25 + "\n")
            f.write("• Aspect values: 0-360 degrees (0° = North, 90° = East, etc.)\n")
            f.write("• Flat areas: -1 (no aspect)\n")
            f.write("• South-facing aspects (135-225°): Higher landslide risk\n")
            f.write("• North-facing aspects (315-45°): Lower landslide risk\n\n")
            
            f.write("SLOPE ANALYSIS RESULTS:\n")
            f.write("-" * 25 + "\n")
            f.write("• Slope values: 0-90 degrees\n")
            f.write("• Gentle slopes (0-5°): Low landslide risk\n")
            f.write("• Moderate slopes (5-15°): Moderate risk\n")
            f.write("• Steep slopes (>15°): High landslide risk\n")
            f.write("• Very steep slopes (>30°): Very high risk\n\n")
            
            f.write("LUNAR-SPECIFIC CONSIDERATIONS:\n")
            f.write("-" * 35 + "\n")
            f.write("• Moon's lower gravity (1.62 m/s²) affects slope stability\n")
            f.write("• No atmosphere means direct solar radiation impact\n")
            f.write("• Thermal cycling affects surface cohesion\n")
            f.write("• Micro-meteorite impacts can trigger landslides\n")
            f.write("• South-facing slopes receive more solar heating\n\n")
            
            f.write("NEXT STEPS FOR LANDSLIDE ANALYSIS:\n")
            f.write("-" * 40 + "\n")
            f.write("1. Load aspect and slope rasters in QGIS Desktop\n")
            f.write("2. Use Raster Calculator to combine aspect and slope\n")
            f.write("3. Create risk zones based on thresholds:\n")
            f.write("   - High risk: Slope >30° AND Aspect 135-225°\n")
            f.write("   - Medium risk: Slope 15-30° OR Aspect 90-135°/225-270°\n")
            f.write("   - Low risk: Slope <15° AND Aspect 315-45°\n")
            f.write("4. Add crater masks to exclude crater interiors\n")
            f.write("5. Consider solar illumination patterns\n")
            f.write("6. Export final landslide risk map\n")
        
        print(f"✅ Comprehensive analysis report saved to: {report_path}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")

def show_aspect_parameters():
    """
    Show the aspect calculation parameters
    """
    print("\n🧮 ASPECT CALCULATION PARAMETERS")
    print("=" * 50)
    
    parameters = {
        "Required Parameters": {
            "Elevation (DEM)": "From LOLA, SLDEM, or other lunar DEMs - Basis for slope & aspect calculation",
            "Raster cell size": "Comes from DEM metadata - Used in gradient calculation",
            "Aspect values": "Calculated from DEM - Direction of maximum slope (0-360°)",
            "Slope values": "Calculated from DEM - Steepness of terrain (0-90°)"
        },
        "Optional Parameters": {
            "Crater mask": "To exclude crater interiors from analysis",
            "Solar illumination": "Based on aspect and time of day",
            "Regolith properties": "Local soil/rock characteristics",
            "Elevation changes": "Rapid elevation variations"
        },
        "Aspect Directions": {
            "North (0°)": "Lowest landslide risk",
            "East (90°)": "Moderate risk",
            "South (180°)": "Highest landslide risk (solar heating)",
            "West (270°)": "Moderate risk",
            "Flat areas (-1)": "No aspect (flat terrain)"
        }
    }
    
    for category, params in parameters.items():
        print(f"\n{category}:")
        for param, description in params.items():
            print(f"  • {param}: {description}")

def main():
    """
    Main function for lunar aspect calculation
    """
    print("🌙 LUNAR ASPECT CALCULATOR FOR LANDSLIDE DETECTION")
    print("=" * 70)
    
    # Show aspect calculation parameters
    show_aspect_parameters()
    
    # DEM file path - UPDATE THIS WITH YOUR ACTUAL PATH
    dem_path = r"D:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    
    # Check if file exists
    if not os.path.exists(dem_path):
        print(f"\n❌ DEM file not found: {dem_path}")
        print("   Please update the dem_path variable with your actual file path")
        return
    
    # Perform aspect calculation
    print(f"\n🚀 STARTING REAL-TIME ASPECT CALCULATION...")
    success = calculate_lunar_aspect(dem_path)
    
    if success:
        print("\n🎉 ASPECT CALCULATION COMPLETED SUCCESSFULLY!")
        print("\n📝 NEXT STEPS:")
        print("1. Check the 'aspect_outputs' folder for results")
        print("2. Open aspect and slope rasters in QGIS Desktop")
        print("3. Use Raster Calculator for landslide risk analysis")
        print("4. Review the comprehensive analysis report")
        print("5. Consider adding crater masks for specific areas")
    else:
        print("\n❌ Aspect calculation failed")
        print("   Check the error messages above for troubleshooting")
    
    print("\n🌙 Lunar aspect analysis complete!")

if __name__ == "__main__":
    main() 