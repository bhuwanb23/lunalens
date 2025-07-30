# Example usage of TifProcessor
# Replace the file paths below with your actual TIF file paths

from tif_processor import TifProcessor

def main():
    # Initialize the processor
    processor = TifProcessor()
    
    # 🔧 CONFIGURE YOUR PATHS HERE
    # Replace these paths with your actual file paths
    input_tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"  # Your input TIF file
    output_folder = r"E:\moon extract\data\derived\20250207\slope"          # Your output folder
    
    # Create output paths
    slope_output = output_folder + r"\slope.tif"
    aspect_output = output_folder + r"\aspect.tif"
    
    # 📋 STEP 1: Load your TIF file
    print("Step 1: Loading TIF file...")
    raster_layer = processor.load_tif_file(input_tif_path, "DEM")
    
    if raster_layer is None:
        print("❌ Failed to load TIF file. Please check the path.")
        processor.cleanup()
        return
    
    # 📋 STEP 2: Calculate slope
    print("\nStep 2: Calculating slope...")
    success = processor.calculate_slope("DEM", slope_output, scale=1.0, as_percent=False)
    
    if not success:
        print("❌ Failed to calculate slope.")
        processor.cleanup()
        return
    
    # 📋 STEP 3: Calculate aspect
    print("\nStep 3: Calculating aspect...")
    success = processor.calculate_aspect("DEM", aspect_output)
    
    if not success:
        print("❌ Failed to calculate aspect.")
        processor.cleanup()
        return
    
    # 📋 STEP 4: List all processed layers
    print("\nStep 4: Summary of processed layers...")
    processor.list_layers()
    
    # 📋 STEP 5: Cleanup
    print("\nStep 5: Cleaning up...")
    processor.cleanup()
    
    print("\n✅ All processing completed successfully!")
    print(f"📁 Output files:")
    print(f"   - Slope: {slope_output}")
    print(f"   - Aspect: {aspect_output}")

if __name__ == "__main__":
    print("🚀 Starting TIF processing example...")
    print("⚠️  IMPORTANT: Edit this file and update the file paths before running!")
    print("   - input_tif_path: Path to your input TIF file")
    print("   - output_folder: Folder where output files will be saved")
    print()
    
    # Uncomment the line below after updating the file paths
    # main()
    
    print("📝 To use this script:")
    print("1. Edit the file paths in the main() function")
    print("2. Uncomment the main() call at the bottom")
    print("3. Run: & \"C:\\Program Files\\QGIS 3.44.1\\bin\\python-qgis.bat\" example_usage.py") 