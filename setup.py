"""
Setup script for Handwriting Recognition Web App
Helps with initial setup and model download
"""

import os
import sys
import subprocess
import urllib.request
import shutil
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major != 3 or version.minor < 7:
        print("❌ Error: Python 3.7 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def install_requirements():
    """Install required Python packages"""
    print_header("Installing Python Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("\nTry installing manually:")
        print("  pip install -r requirements.txt")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        "static/uploads",
        "model/models",
        "model/experiments"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")
    
    # Create .gitkeep files
    Path("static/uploads/.gitkeep").touch()
    Path("model/models/.gitkeep").touch()
    
    print("\n✅ All directories created")
    return True


def download_model_instructions():
    """Provide instructions for downloading the model"""
    print_header("Model Setup Instructions")
    
    print("To use the full functionality, you need to download the pretrained model.")
    print("\nOption 1: Clone from GitHub")
    print("  git clone https://github.com/arshjot/Handwritten-Text-Recognition.git temp_repo")
    print("  Copy the files from temp_repo/experiments/CRNN_h128/ to model/models/")
    print("  Remove temp_repo directory")
    
    print("\nOption 2: Manual Download")
    print("  1. Visit: https://github.com/arshjot/Handwritten-Text-Recognition")
    print("  2. Download the model weights")
    print("  3. Place them in: model/models/")
    
    print("\nOption 3: Use Mock Mode (for testing)")
    print("  The app includes a mock predictor that works without the model.")
    print("  Just run 'python app.py' and it will use sample predictions.")
    
    print("\n" + "-"*60)
    choice = input("\nWould you like to try cloning the repository now? (y/n): ")
    
    if choice.lower() == 'y':
        try:
            print("\nCloning repository...")
            subprocess.check_call([
                "git", "clone", 
                "https://github.com/arshjot/Handwritten-Text-Recognition.git",
                "temp_repo"
            ])
            
            print("Copying model files...")
            src = Path("temp_repo/experiments/CRNN_h128")
            dst = Path("model/models")
            
            if src.exists():
                for item in src.glob("*"):
                    shutil.copy2(item, dst)
                print("✅ Model files copied successfully")
            else:
                print("⚠️ Model files not found in expected location")
            
            print("Cleaning up...")
            shutil.rmtree("temp_repo")
            print("✅ Setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please download the model manually.")
            return False
    else:
        print("\n⚠️ Skipping model download. App will run in mock mode.")
        return True


def run_tests():
    """Run basic tests to verify setup"""
    print_header("Running Tests")
    
    try:
        print("Testing imports...")
        import flask
        import cv2
        import numpy
        from PIL import Image
        print("✅ All imports successful")
        
        print("\nTesting Flask app...")
        import app
        print("✅ Flask app loads successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


def main():
    """Main setup function"""
    print("\n" + "🎨"*30)
    print("  HANDWRITING RECOGNITION APP - SETUP")
    print("🎨"*30)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Create Directories", create_directories),
        ("Install Dependencies", install_requirements),
        ("Model Setup", download_model_instructions),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the errors and run setup again.")
            return False
    
    print_header("Setup Complete!")
    print("✅ Your handwriting recognition app is ready!")
    print("\nNext steps:")
    print("  1. Run the app: python app.py")
    print("  2. Open browser: http://localhost:5000")
    print("  3. Upload handwritten images and enjoy!")
    print("\n" + "🎉"*30 + "\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

