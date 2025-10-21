# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the directory where this spec file is located
block_cipher = None
spec_root = Path(__file__).parent.absolute()

# Define data files to include
datas = [
    # Include templates
    (str(spec_root / 'templates'), 'templates'),
    # Include static files
    (str(spec_root / 'static'), 'static'),
    # Include model directory
    (str(spec_root / 'model'), 'model'),
    # Include requirements file
    (str(spec_root / 'requirements.txt'), '.'),
]

# Define hidden imports (modules that PyInstaller might miss)
hiddenimports = [
    'flask',
    'werkzeug',
    'torch',
    'torchvision',
    'transformers',
    'cv2',
    'PIL',
    'numpy',
    'easyocr',
    'model.mains.easyocr_predictor',
    'model.mains.predictor',
    'model.mains.trocr_predictor',
    'model.configs',
    'model.data_loader',
    'model.utils',
]

# Define binaries (if any external executables are needed)
binaries = []

# Analysis configuration
a = Analysis(
    ['app.py'],
    pathex=[str(spec_root)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib.backends._tkagg',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate files
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='HandwritingRecognition',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
