@echo off
echo ================================================
echo PYTHON WEBP CONVERTER TEST
echo ================================================
echo.
echo This uses Python + Pillow to fix orientation
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

echo Running conversion test...
echo.

python test_python_convert.py

echo.
pause
