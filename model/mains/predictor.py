"""
Handwriting Recognition Predictor Module
Handles model loading and prediction for handwritten text recognition.
Based on the arshjot/Handwritten-Text-Recognition repository.
"""

import os
import json
import numpy as np
import cv2
from typing import Optional, List

# Try to import TensorFlow, but gracefully handle if not available
try:
    import tensorflow as tf
    # Enable TensorFlow 1.x compatibility mode
    tf.compat.v1.disable_eager_execution()
    tf.compat.v1.disable_v2_behavior()
    TF_AVAILABLE = True
except ImportError:
    print("WARNING: TensorFlow not available. Running in mock mode.")
    TF_AVAILABLE = False
    tf = None


class HandwritingPredictor:
    """
    Predictor class for handwriting recognition.
    Loads a pretrained TensorFlow model and performs inference on images.
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the predictor with configuration.
        
        Args:
            config_path: Path to the configuration JSON file
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        # Image dimensions from config
        self.img_height = self.config.get('image_height', 32)
        self.img_width = self.config.get('image_width', 128)
        self.num_channels = self.config.get('num_channels', 1)
        
        # Character list for decoding
        self.char_list = self.config.get('char_list', '')
        self.num_classes = len(self.char_list) + 1  # +1 for blank
        
        # Model placeholders
        self.session = None
        self.input_tensor = None
        self.output_tensor = None
        self.seq_len_tensor = None
        
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config
    
    def setup(self):
        """
        Load the TensorFlow model and prepare for inference.
        This should be called once during application startup.
        """
        # Check if TensorFlow is available
        if not TF_AVAILABLE:
            print("WARNING: TensorFlow not installed. Using mock predictor.")
            self._use_mock_model()
            return
        
        model_path = self.config.get('model_path', 'model/models/best_model')
        
        # Check if model exists
        if not os.path.exists(model_path + '.meta') and not os.path.exists(model_path):
            print(f"WARNING: Model not found at {model_path}")
            print("Using mock predictor for demonstration.")
            self._use_mock_model()
            return
        
        try:
            # Reset default graph
            tf.compat.v1.reset_default_graph()
            
            # Create TensorFlow session
            self.session = tf.compat.v1.Session()
            
            # Load the saved model
            saver = tf.compat.v1.train.import_meta_graph(model_path + '.meta')
            saver.restore(self.session, model_path)
            
            # Get input and output tensors
            graph = tf.compat.v1.get_default_graph()
            self.input_tensor = graph.get_tensor_by_name('input:0')
            self.seq_len_tensor = graph.get_tensor_by_name('seq_len:0')
            self.output_tensor = graph.get_tensor_by_name('output:0')
            
            print(f"SUCCESS: Model loaded successfully from {model_path}")
            
        except Exception as e:
            print(f"ERROR: Error loading model: {e}")
            print("Using mock predictor for demonstration.")
            self._use_mock_model()
    
    def _use_mock_model(self):
        """Use a mock model when the actual model is not available."""
        self.session = None
        print("MOCK MODE: Mock model activated - will return sample predictions")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess an image for prediction.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Preprocessed image as numpy array
        """
        # Read image in grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Resize to target dimensions
        img = cv2.resize(img, (self.img_width, self.img_height))
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add channel dimension if needed
        if self.num_channels == 1:
            img = np.expand_dims(img, axis=-1)
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def decode_prediction(self, output: np.ndarray) -> str:
        """
        Decode CTC output to text.
        
        Args:
            output: Model output (logits or sparse tensor)
            
        Returns:
            Decoded text string
        """
        # Handle sparse tensor output
        if isinstance(output, tuple) and len(output) == 3:
            # Sparse tensor format: (indices, values, shape)
            indices, values, shape = output
            decoded_indices = values
        else:
            # Dense output - use argmax
            decoded_indices = np.argmax(output, axis=-1)
        
        # Convert indices to characters
        text = ""
        prev_char = -1
        
        for idx in decoded_indices:
            if idx >= 0 and idx < len(self.char_list):
                if idx != prev_char:  # Skip repeats (CTC decoding)
                    text += self.char_list[idx]
                prev_char = idx
        
        return text.strip()
    
    def predict(self, image_path: str) -> str:
        """
        Predict handwritten text from an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Recognized text string
        """
        # Preprocess the image
        img = self.preprocess_image(image_path)
        
        # If using mock model, return sample text
        if self.session is None:
            sample_texts = [
                "Sample handwritten text",
                "Hello World!",
                "This is a demo prediction",
                "Handwriting recognition",
                "Upload your handwritten image"
            ]
            # Use image path hash to get consistent "prediction"
            idx = hash(image_path) % len(sample_texts)
            return sample_texts[idx]
        
        try:
            # Create sequence length (full width for each image)
            seq_len = np.array([self.img_width // 4] * img.shape[0])
            
            # Run inference
            feed_dict = {
                self.input_tensor: img,
                self.seq_len_tensor: seq_len
            }
            
            output = self.session.run(self.output_tensor, feed_dict=feed_dict)
            
            # Decode the output
            text = self.decode_prediction(output)
            
            return text
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return f"Error during prediction: {str(e)}"
    
    def predict_batch(self, image_paths: List[str]) -> List[str]:
        """
        Predict text from multiple images.
        
        Args:
            image_paths: List of image file paths
            
        Returns:
            List of recognized text strings
        """
        return [self.predict(path) for path in image_paths]
    
    def __del__(self):
        """Clean up TensorFlow session."""
        if self.session is not None:
            self.session.close()


def create_predictor(config_path: str = 'model/configs/config.json') -> HandwritingPredictor:
    """
    Factory function to create and setup a predictor instance.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Initialized HandwritingPredictor instance
    """
    predictor = HandwritingPredictor(config_path)
    predictor.setup()
    return predictor

