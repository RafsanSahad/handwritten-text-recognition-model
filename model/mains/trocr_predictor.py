"""
TrOCR (Transformer-based OCR) Predictor for Handwriting Recognition
Uses Microsoft's TrOCR model for superior handwriting recognition accuracy.
"""

# Install the transformers library
# You can do this by running the following command:
# pip install transformers

import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import cv2
import numpy as np
from PIL import Image
import os

from typing import Optional, Union

class TrOCR_Predictor:
    def __init__(self, model_name: str = "microsoft/trocr-base-handwritten", gpu: bool = False):
        """
        Initialize TrOCR model for handwriting recognition.
        
        Args:
            model_name: TrOCR model variant
                - "microsoft/trocr-base-handwritten" (recommended for handwriting)
                - "microsoft/trocr-base-printed" (for printed text)
                - "microsoft/trocr-large-handwritten" (larger, more accurate)
            gpu: Whether to use GPU acceleration
        """
        self.model_name = model_name
        self.device = torch.device("cuda" if gpu and torch.cuda.is_available() else "cpu")
        self.processor: Optional[TrOCRProcessor] = None
        self.model: Optional[VisionEncoderDecoderModel] = None
        self._load_model()

    def _load_model(self):
        """Load TrOCR model and processor."""
        try:
            print(f"Loading TrOCR model: {self.model_name}")
            print(f"Device: {self.device}")
            print("NOTE: First time will download ~1.5GB model (requires internet)")
            print("After first run, works 100% offline!")
            
            # Load processor and model
            self.processor = TrOCRProcessor.from_pretrained(self.model_name)
            self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
            if isinstance(self.model, VisionEncoderDecoderModel):
                self.model = self.model.to(self.device)
            
            print("✅ TrOCR model loaded successfully!")
            print(f"✅ Model size: ~1.5GB")
            print(f"✅ Optimized for: Handwriting recognition")
            
        except Exception as e:
            print(f"❌ ERROR: Failed to load TrOCR model: {e}")
            print("Falling back to mock mode...")
            self.processor = None
            self.model = None

    def predict(self, image_path: str) -> str:
        """
        Predict text from handwritten image using TrOCR.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Recognized text string
        """
        if not self.model or not self.processor:
            return "Mock prediction: TrOCR not loaded"
        
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            # Process image for TrOCR
            inputs = self.processor(image)
            pixel_values = torch.tensor(inputs['pixel_values']).to(self.device)
            
            # Generate text
            with torch.no_grad():
                generated_ids = self.model.generate(pixel_values)
                generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            return generated_text.strip()
            
        except Exception as e:
            print(f"❌ ERROR during TrOCR prediction: {e}")
            return f"Error during recognition: {e}"

    def predict_batch(self, image_paths: list) -> list:
        """
        Predict text from multiple images.
        
        Args:
            image_paths: List of image paths
            
        Returns:
            List of recognized text strings
        """
        results = []
        for image_path in image_paths:
            result = self.predict(image_path)
            results.append(result)
        return results

def create_trocr_predictor(model_variant="handwritten", gpu=False):
    """
    Factory function to create a TrOCR predictor.
    
    Args:
        model_variant: "handwritten", "printed", or "large"
        gpu: Whether to use GPU acceleration
        
    Returns:
        TrOCR_Predictor instance
    """
    model_map = {
        "handwritten": "microsoft/trocr-base-handwritten",
        "printed": "microsoft/trocr-base-printed", 
        "large": "microsoft/trocr-large-handwritten"
    }
    
    model_name = model_map.get(model_variant, "microsoft/trocr-base-handwritten")
    return TrOCR_Predictor(model_name=model_name, gpu=gpu)

# For backward compatibility
def create_predictor():
    """Create TrOCR predictor with default settings."""
    return create_trocr_predictor(model_variant="handwritten", gpu=False)
