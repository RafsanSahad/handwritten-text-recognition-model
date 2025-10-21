import os
import sys

# Add project root so we can import model package
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from model.mains.easyocr_predictor import create_predictor

u = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
up = os.path.abspath(u)
print('Upload folder:', up)

p = create_predictor()

for fname in os.listdir(up):
    if not fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        continue
    path = os.path.join(up, fname)
    print('\nProcessing:', fname)
    text, debug = p.predict(path, return_debug=True)
    print('Result:', text)
    print('Debug info:')
    for d in debug:
        print(' ', d)
