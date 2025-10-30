@echo off
REM Update HTML files to use responsive WebP images with JPG fallback
REM This script calls update_html_responsive.py

echo ============================================================
echo HTML Responsive Image Updater
echo ============================================================
echo.
echo This will update your HTML files to use responsive WebP images
echo with JPG fallback for older browsers.
echo.
echo Backups will be created automatically.
echo.
pause

REM Run the Python script
python update_html_responsive.py

echo.
echo ============================================================
pause
