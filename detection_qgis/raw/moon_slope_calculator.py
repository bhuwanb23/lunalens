# Moon Slope Calculator
# Uses tif_processor.py with moon-specific parameters

from tif_processor import TifProcessor

def main():
    print("🌙 Moon Slope Calculator")
    print("=" * 50)
    
    # Initialize processor
    processor = TifProcessor()
    
    # 🔧 CONFIGURE YOUR PATHS HERE
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    slope_output = r"E:\moon extract\data\derived\20250207\moon_slope.tif"
    
    print("📁 Step 1: Loading moon TIF file...")
    
    # Load the moon TIF file
    raster_layer = processor.load_tif_file(tif_path, "Moon_DEM")
    
    if raster_layer is None:
        print("❌ Failed to load moon TIF file")
        processor.cleanup()
        return
    
    print("✅ Moon TIF file loaded successfully")
    
    print("\n🌙 Step 2: Calculating moon slope...")
    print("Moon-specific parameters:")
    print("   - Scale: 1.0 (assuming meter resolution)")
    print("   - Output: Degrees (not percentage)")
    print("   - Moon gravity: 1.62 m/s² (vs Earth's 9.81 m/s²)")
    print("   - Terrain analysis for landing suitability")
    
    # Calculate moon slope
    success = processor.calculate_moon_slope("Moon_DEM", slope_output)
    
    if not success:
        print("❌ Failed to calculate moon slope")
        processor.cleanup()
        return
    
    print("\n📊 Step 3: Moon slope analysis completed!")
    
    # List all layers
    processor.list_layers()
    
    # Cleanup
    processor.cleanup()
    
    print("\n🎉 Moon slope calculation completed!")
    print(f"📁 Output file: {slope_output}")
    print("\n📋 Moon slope interpretation:")
    print("   - 0-5°: Gentle slopes (excellent for landing)")
    print("   - 5-15°: Moderate slopes (acceptable for landing)")
    print("   - 15-30°: Steep slopes (challenging for landing)")
    print("   - >30°: Very steep slopes (unsuitable for landing)")

if __name__ == "__main__":
    main() 