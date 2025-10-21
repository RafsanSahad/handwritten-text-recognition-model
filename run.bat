@echo off
REM Windows batch file to run the Handwriting Recognition app

echo.
echo ========================================
echo  Handwriting Recognition Web App
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error creating virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\Lib\site-packages\flask\" (
    echo Installing dependencies...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error installing dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
)

REM Run the Flask app
echo.
echo Starting Flask application...
echo.
python app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Error running the application
    pause
)

deactivate

