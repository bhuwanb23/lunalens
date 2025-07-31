@echo off
echo 🌙 Lunar Analysis Main Processor
echo ================================================
echo.

REM Set QGIS paths
set QGIS_PREFIX_PATH=C:\Program Files\QGIS 3.40.9
set QGIS_PYTHON_PATH=%QGIS_PREFIX_PATH%\apps\Python39

REM Add QGIS Python to PATH
set PATH=%QGIS_PYTHON_PATH%;%QGIS_PYTHON_PATH%\Scripts;%PATH%

REM Set environment variables
set PYTHONPATH=%QGIS_PREFIX_PATH%\apps\qgis\python;%PYTHONPATH%
set QT_QPA_PLATFORM_PLUGIN_PATH=%QGIS_PREFIX_PATH%\apps\Qt5\plugins
set GDAL_DATA=%QGIS_PREFIX_PATH%\share\gdal
set PROJ_LIB=%QGIS_PREFIX_PATH%\share\proj

echo ✅ QGIS Environment Setup:
echo    - QGIS Path: %QGIS_PREFIX_PATH%
echo    - Python Path: %QGIS_PYTHON_PATH%
echo    - Python Executable: %QGIS_PYTHON_PATH%\python.exe
echo.

REM Check if interactive mode is requested
if "%1"=="--interactive" (
    echo 🎮 Running in Interactive Mode...
    "%QGIS_PYTHON_PATH%\python.exe" main_processor.py --interactive
) else (
    echo 🚀 Running in Batch Mode...
    "%QGIS_PYTHON_PATH%\python.exe" main_processor.py
)

echo.
echo ✅ Processing completed!
pause 