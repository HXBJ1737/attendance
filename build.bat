@echo off
cd /d "%~dp0"

echo ========================================
echo   Building exe (using system browser)...
echo ========================================

C:\Users\zhangjie\Desktop\attendance\.venv\Scripts\pyinstaller.exe --onefile --windowed --name "AttendanceScraper" --add-data "config.json;." main.py scraper.py

echo.
echo ========================================
echo   Done! Check dist\ folder
echo ========================================
pause
