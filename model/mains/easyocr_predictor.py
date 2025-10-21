"""
EasyOCR-based Handwriting Recognition Predictor
Real AI recognition using EasyOCR instead of TensorFlow
Works with Python 3.13!
"""

import os
import easyocr
import numpy as np


class EasyOCRPredictor:
    """
    Predictor class using EasyOCR for handwriting recognition.
    Works offline after first model download (~500MB).
    """
    
    def __init__(self):
        """Initialize the EasyOCR predictor."""
        self.reader = None
        print("EasyOCR Predictor initialized")
    
    def setup(self):
        """
        Load the EasyOCR model.
        On first run, will download models (~500MB) - requires internet.
        Subsequent runs work completely offline!
        """
        try:
            print("Loading EasyOCR model...")
            print("NOTE: First time will download ~500MB model (requires internet)")
            print("After first run, works 100% offline!")
            
            # Initialize EasyOCR reader for English
            # gpu=False for CPU-only processing (works everywhere)
            # You can add more languages: ['en', 'ch_sim', 'fr', etc.]
            self.reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            
            print("SUCCESS: EasyOCR model loaded successfully!")
            print("The app now has REAL handwriting recognition!")
            
        except Exception as e:
            print(f"ERROR: Failed to load EasyOCR: {e}")
            print("Falling back to mock mode")
            self.reader = None
    
    def predict(self, image_path: str, return_debug: bool = False):
        """
        Predict handwritten text from an image using EasyOCR.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Recognized text string
        """
        if self.reader is None:
            # Fallback to mock if reader didn't load
            return "Mock prediction: EasyOCR not loaded"

        # Verify file exists and is readable
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        import cv2

        # Bind reader to local variable to satisfy static checks
        reader = self.reader
        assert reader is not None

        # Helper: run reader with detail=1 to get confidences
        def run_read(path, **kwargs):
            try:
                return reader.readtext(path, detail=1, **kwargs)
            except Exception as e:
                print(f"EasyOCR readtext error for {path} with {kwargs}: {e}")
                return []

        # Helper: extract text and confidence from various item shapes
        def extract_text_conf(item):
            # Expected: [bbox, text, confidence] or (bbox, text, confidence)
            if isinstance(item, (list, tuple)):
                seq = list(item)
                if len(seq) >= 3:
                    text = seq[1]
                    conf = seq[2]
                    return (text, conf)
                elif len(seq) == 2:
                    # Some callers may return [bbox, text]
                    return (seq[1], 0.0)
                else:
                    return (None, 0.0)
            elif isinstance(item, dict):
                # try common keys
                text = item.get('text') or item.get('Text') or item.get('label')
                conf = item.get('confidence') or item.get('conf') or item.get('score') or 0.0
                return (text, conf)
            else:
                return (None, 0.0)

        # Strategy list: tuples of (description, path_to_check, kwargs)
        strategies = []

        # Strategy A: original image, moderate mag_ratio
        strategies.append(("original_mag1.5", image_path, {"paragraph": False, "mag_ratio": 1.5}))

        # Strategy B: original image, higher mag_ratio (good for small text)
        strategies.append(("original_mag2.0", image_path, {"paragraph": False, "mag_ratio": 2.0}))

        # Preprocess: adaptive thresholding and try again
        preprocessed_path = None
        try:
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Denoise and equalize
                blur = cv2.GaussianBlur(gray, (3, 3), 0)
                eq = cv2.equalizeHist(blur)
                binary = cv2.adaptiveThreshold(eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, 15, 3)
                preprocessed_path = image_path + '.proc.png'
                cv2.imwrite(preprocessed_path, binary)
                strategies.append(("preprocessed_mag1.5", preprocessed_path, {"paragraph": False, "mag_ratio": 1.5}))
                strategies.append(("preprocessed_mag2.0", preprocessed_path, {"paragraph": False, "mag_ratio": 2.0}))
        except Exception as e:
            print(f"Preprocessing error: {e}")
            preprocessed_path = None

        # Try each strategy and pick the best by average confidence
        best_text = None
        best_conf = -1.0
        debug_info = []

        for desc, path, kwargs in strategies:
            results = run_read(path, **kwargs)
            # results: list of [bbox, text, confidence]
            texts = []
            confs = []
            for item in results:
                text, conf = extract_text_conf(item)
                if not text:
                    continue
                try:
                    confv = float(conf)
                except Exception:
                    confv = 0.0
                texts.append(str(text).strip())
                confs.append(confv)

            avg_conf = sum(confs) / len(confs) if confs else 0.0
            joined = ' '.join(texts).strip()
            debug_info.append({"strategy": desc, "text": joined, "avg_conf": avg_conf, "items": len(texts)})

            # prefer non-empty text and higher avg_conf
            if joined and avg_conf > best_conf:
                best_conf = avg_conf
                best_text = joined

        # Clean up preprocessed file if created
        try:
            if preprocessed_path and os.path.exists(preprocessed_path):
                os.remove(preprocessed_path)
        except Exception:
            pass

        # Print debug info for traces
        print(f"EasyOCR strategies debug: {debug_info}")

        if best_text:
            if return_debug:
                return best_text, debug_info
            return best_text
        else:
            if return_debug:
                return "(No text detected in image)", debug_info
            return "(No text detected in image)"
    
    def predict_batch(self, image_paths: list) -> list:
        """
        Predict text from multiple images.
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of recognized text strings
        """
        return [self.predict(path) for path in image_paths]


def create_predictor():
    """
    Factory function to create and setup an EasyOCR predictor.
    
    Returns:
        Initialized EasyOCRPredictor instance
    """
    predictor = EasyOCRPredictor()
    predictor.setup()
    return predictor

