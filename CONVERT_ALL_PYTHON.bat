@echo off
echo ================================================
echo PYTHON WEBP CONVERTER - FULL BATCH
echo ================================================
echo.
echo This will convert ALL images in the main directory
echo (NOT including subfolders) with proper orientation
echo No ImageMagick needed!
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python found! Checking for Pillow...
echo.

REM Check if Pillow is installed, install if not
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Pillow not found. Installing...
    pip install Pillow
    echo.
)

python convert_all_images.py

echo.
pause
