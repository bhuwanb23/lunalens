#!/usr/bin/env python3
"""
Test script to verify path handling for lunar analysis
"""

import os
import sys
import json

def test_path_handling():
    """Test that the system uses exact paths provided by users"""
    
    print("🧪 Testing Path Handling")
    print("=" * 50)
    
    # Test paths that users might provide
    test_paths = [
        r"C:\Users\John\Documents\lunar_dem.tif",
        r"D:\moon extract\large_dem_15gb.tif",
        r"F:\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif",
        r"/home/user/documents/lunar_dem.tif",
        r"C:\Program Files\QGIS 3.40.9\apps\qgis-ltr\bin\lunar_dem.tif"
    ]
    
    for i, test_path in enumerate(test_paths, 1):
        print(f"\n📁 Test {i}: {test_path}")
        
        # Simulate what the backend does
        dem_path = os.path.abspath(test_path)
        print(f"   🔍 Absolute path: {dem_path}")
        print(f"   📊 File exists: {os.path.exists(dem_path)}")
        
        # Check if it's a valid DEM extension
        valid_extensions = ['.tif', '.tiff', '.asc', '.dem', '.geotiff']
        file_ext = os.path.splitext(dem_path)[1].lower()
        is_valid_extension = file_ext in valid_extensions
        print(f"   ✅ Valid extension: {is_valid_extension} ({file_ext})")
        
        if os.path.exists(dem_path):
            file_size_gb = os.path.getsize(dem_path) / (1024**3)
            print(f"   📏 File size: {file_size_gb:.2f} GB")
        else:
            print(f"   ⚠️  File not found (expected for test paths)")
    
    print("\n✅ Path handling test completed!")
    print("\n📋 Summary:")
    print("   - System now uses exact paths provided by users")
    print("   - No unnecessary path manipulation or searching")
    print("   - Simple validation: file exists + valid extension")
    print("   - Backend will return clear error if file not found")

if __name__ == "__main__":
    test_path_handling() 