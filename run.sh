#!/bin/bash
# Linux/Mac shell script to run the Handwriting Recognition app

echo ""
echo "========================================"
echo "  Handwriting Recognition Web App"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully!"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ ! -d "venv/lib/python*/site-packages/flask" ]; then
    echo "Installing dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error installing dependencies"
        exit 1
    fi
    echo "Dependencies installed successfully!"
fi

# Run the Flask app
echo ""
echo "Starting Flask application..."
echo ""
python app.py

# Deactivate virtual environment
deactivate

