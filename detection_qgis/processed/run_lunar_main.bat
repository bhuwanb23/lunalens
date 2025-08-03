@echo off
echo ========================================
echo    LUNAR TERRAIN ANALYSIS MAIN SYSTEM
echo ========================================
echo.

REM Set QGIS Python path
set QGIS_PYTHON="C:\Program Files\QGIS 3.44.1\bin\python-qgis.bat"

REM Navigate to the script directory
cd /d "%~dp0"

echo Current directory: %CD%
echo QGIS Python: %QGIS_PYTHON%
echo.

echo Starting comprehensive lunar terrain analysis...
echo.

REM Run the lunar main controller script
%QGIS_PYTHON% lunar_main.py

echo.
echo ========================================
echo    ANALYSIS COMPLETED
echo ========================================
echo.

echo Check the 'lunar_analysis_output' directory for summary report
echo Individual analysis outputs:
echo - tif_processor: DEM processing results
echo - elevation_statistics: Elevation statistics analysis
echo - slope: Slope analysis results
echo - lunar_aspect_calculator: aspect_outputs directory
echo - hillshade: hillshade_outputs directory
echo - counter: counter_outputs directory
echo - curvature_statistics: Curvature analysis results
echo - crater_edges: crater_walls directory
echo - scraps_headwalls: headwalls_scraps directory
echo - debris_paths: debris_path_output directory
echo - terrain_ruggedness: Terrian_Reggedness_output directory
echo.

pause 