#!/usr/bin/env python3
"""
Test script to verify all lunar analysis modules can be imported successfully
"""

import sys
import os

def test_module_imports():
    """Test importing all lunar analysis modules"""
    
    print("🔧 Testing Lunar Analysis Module Imports")
    print("=" * 50)
    
    # List of modules to test
    modules_to_test = [
        ('tif_processor', 'tif_processor.py'),
        ('slope', 'slope.py'),
        ('elevation_statistics', 'elevation_statistics.py'),
        ('lunar_aspect_calculator', 'lunar_aspect_calculator.py'),
        ('hillshade', 'hillshade.py'),
        ('counter', 'counter.py'),
        ('curvature_statistics', 'curvature_statistics.py'),
        ('crater_edges', 'crater_edges.py'),
        ('scraps_headwalls', 'scraps_headwalls.py'),
        ('debris_paths', 'Debris_path.py'),
        ('terrain_ruggedness', 'Terrain_Ruggedness.py')
    ]
    
    successful_imports = []
    failed_imports = []
    
    for module_name, file_name in modules_to_test:
        print(f"\n📦 Testing {module_name}...")
        
        # Check if file exists
        if not os.path.exists(file_name):
            print(f"   ❌ File not found: {file_name}")
            failed_imports.append((module_name, f"File not found: {file_name}"))
            continue
        
        # Try to import the module
        try:
            if module_name == 'crater_edges':
                import crater_edges
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'scraps_headwalls':
                import scraps_headwalls
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'debris_paths':
                import Debris_path
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'terrain_ruggedness':
                import Terrain_Ruggedness
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'elevation_statistics':
                import elevation_statistics
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'curvature_statistics':
                import curvature_statistics
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'slope':
                import slope
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'hillshade':
                import hillshade
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'counter':
                import counter
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'lunar_aspect_calculator':
                import lunar_aspect_calculator
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            elif module_name == 'tif_processor':
                import tif_processor
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
            else:
                print(f"   ✅ {module_name} imported successfully")
                successful_imports.append(module_name)
                
        except ImportError as e:
            print(f"   ❌ Import failed: {e}")
            failed_imports.append((module_name, f"ImportError: {e}"))
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed_imports.append((module_name, f"Error: {e}"))
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 IMPORT TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Successful imports: {len(successful_imports)}")
    print(f"❌ Failed imports: {len(failed_imports)}")
    
    if successful_imports:
        print(f"\n✅ Successfully imported modules:")
        for module in successful_imports:
            print(f"   - {module}")
    
    if failed_imports:
        print(f"\n❌ Failed imports:")
        for module, error in failed_imports:
            print(f"   - {module}: {error}")
    
    print(f"\n🎯 Expected: 11 modules")
    print(f"📈 Success rate: {len(successful_imports)}/11 ({len(successful_imports)/11*100:.1f}%)")
    
    return len(successful_imports) == 11

if __name__ == "__main__":
    success = test_module_imports()
    if success:
        print("\n🎉 All modules imported successfully! Ready for lunar analysis.")
    else:
        print("\n⚠️  Some modules failed to import. Check the errors above.") 