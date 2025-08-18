@echo off
echo ========================================
echo    LUNAR IMAGE PROCESSOR
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if input file exists
if not exist "E:\Image L3_ch2_tmc_ndn_20240524T1710018579_d_oth_d18.tif" (
    echo ❌ Error: Input image not found!
    echo Please ensure "Image L3_ch2_tmc_ndn_20240524T1710018579_d_oth_d18.tif" is in the E:\ drive
    pause
    exit /b 1
)

echo 🚀 Starting lunar image processing...
echo 📁 Input: E:\Image L3_ch2_tmc_ndn_20240524T1710018579_d_oth_d18.tif
echo 🔍 Processing: 4x zoom + 4x enhancement = 16x total scaling
echo 📁 Output: enhanced_lunar_tiles
echo.

REM Install required packages
echo 📦 Installing required packages...
pip install numpy pillow opencv-python scikit-image

echo.
echo 🚀 Running image processor...
python process_lunar_images.py "E:\Image L3_ch2_tmc_ndn_20240524T1710018579_d_oth_d18.tif" "enhanced_lunar_tiles" --zoom 4 --enhance 4

if errorlevel 1 (
    echo.
    echo ❌ Processing failed! Check the error messages above.
) else (
    echo.
    echo ✅ Processing completed successfully!
    echo 📁 Check the 'enhanced_lunar_tiles' folder for results
)

echo.
pause
