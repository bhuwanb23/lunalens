@echo off
echo 🌙 Lunar Analysis Main Processor (QGIS Batch Method)
echo ======================================================
echo.

REM Set QGIS batch file path
set QGIS_BATCH_PATH="C:\Program Files\QGIS 3.40.9\bin\python-qgis-ltr.bat"

echo ✅ Using QGIS Batch File: %QGIS_BATCH_PATH%
echo.

REM Check if interactive mode is requested
if "%1"=="--interactive" (
    echo 🎮 Running in Interactive Mode...
    %QGIS_BATCH_PATH% main_processor.py --interactive
) else (
    echo 🚀 Running in Batch Mode...
    %QGIS_BATCH_PATH% main_processor.py
)

echo.
echo ✅ Processing completed!
pause 