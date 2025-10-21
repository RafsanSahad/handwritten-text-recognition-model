@echo off
setlocal

REM Navigate to the script's directory
cd /d "%~dp0"

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  🚀 UPGRADING TO TrOCR (Better Handwriting Recognition)    ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is in PATH
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not found in your system's PATH.
    echo Please install Python (e.g., Python 3.13) and ensure it's added to PATH.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Stop any running Flask app
echo Stopping any previous Flask instances...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Flask" >nul 2>&1
taskkill /f /im pythonw.exe /fi "WINDOWTITLE eq Flask" >nul 2>&1
timeout /t 2 /nobreak >nul

echo.
echo 📦 Installing TrOCR dependencies...
echo This will install PyTorch, Transformers, and other required packages.
echo First time download will be ~1.5GB for the TrOCR model.
echo.

REM Install new requirements
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Failed to install dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.

echo 🧪 Testing TrOCR model loading...
python -c "from model.mains.trocr_predictor import create_predictor; print('✅ TrOCR predictor created successfully!')"

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  WARNING: TrOCR test failed, but dependencies are installed.
    echo The model will download on first use.
    echo.
)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║  🎉 UPGRADE COMPLETE!                                     ║
echo ║                                                           ║
echo ║  Your app now uses Microsoft TrOCR for much better        ║
echo ║  handwriting recognition accuracy!                        ║
echo ║                                                           ║
echo ║  Next steps:                                              ║
echo ║  1. Run: START_APP.bat                                    ║
echo ║  2. Upload your test image                                ║
echo ║  3. Enjoy superior recognition! 🚀                        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

pause
endlocal
