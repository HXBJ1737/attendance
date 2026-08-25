@echo off
cd /d "%~dp0"

echo ========================================
echo   Building AttendanceScraper.exe...
echo ========================================

pyinstaller --onefile --windowed --name "AttendanceScraper" --add-data "config.json;." main.py

echo.
echo ========================================
echo   Building OvertimeCalc.exe...
echo ========================================

pyinstaller --onefile --windowed --name "OvertimeCalc" calc.py

echo.
echo ========================================
echo   Done! Check dist\ folder
echo ========================================
pause
