@echo off
REM Handwriting Recognition App Launcher
REM This uses the correct Python with Flask installed

echo.
echo ============================================================
echo   Starting Handwriting Recognition App
echo ============================================================
echo.

cd /d "%~dp0"

REM Use 'python' command (not WindowsApps version)
python app.py

pause

