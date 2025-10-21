"""
Flask Web Application for Handwriting Recognition
Uses pretrained CRNN model from arshjot/Handwritten-Text-Recognition
Completely offline application with colorful interactive UI
"""

from flask import Flask, render_template, request, jsonify
import os
import hashlib
import time
from werkzeug.utils import secure_filename
from model.mains.easyocr_predictor import create_predictor

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'handwriting-recognition-secret-key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global predictor instance (loaded once at startup)
predictor = None

# Cache for predictions (optional: cache results for same images)
prediction_cache = {}


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename: Name of the uploaded file
        
    Returns:
        True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_file_hash(filepath):
    """
    Calculate MD5 hash of a file for caching purposes.
    
    Args:
        filepath: Path to the file
        
    Returns:
        MD5 hash string
    """
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


@app.route('/')
def index():
    """
    Render the main upload page.
    
    Returns:
        Rendered HTML template
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle image upload and perform handwriting recognition.
    
    Returns:
        JSON response with recognized text or error message
    """
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file part in the request'
        }), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    # Check file type
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': f'Invalid file type. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'
        }), 400
    
    try:
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Check if filename is None
        if not file.filename:
            return jsonify({
                'success': False,
                'error': 'No filename provided'
            }), 400
            
        # Save the uploaded file
        filename = secure_filename(file.filename)
        timestamp = str(int(time.time() * 1000))
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to save uploaded file: {str(e)}'
            }), 500
            
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File upload failed: File not saved'
            }), 500
        
        # Calculate file hash for caching
        file_hash = get_file_hash(filepath)
        
        # Check cache
        if file_hash in prediction_cache:
            recognized_text = prediction_cache[file_hash]
            cache_hit = True
        else:
            # Check if predictor is initialized
            if predictor is None:
                return jsonify({
                    'success': False,
                    'error': 'OCR model not initialized'
                }), 500
                
            # Perform prediction
            recognized_text = predictor.predict(filepath)
            
            # Store in cache
            prediction_cache[file_hash] = recognized_text
            cache_hit = False
        
        # Clean up: delete the uploaded file after processing
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Warning: Could not delete file {filepath}: {e}")
        
        # Return success response
        return jsonify({
            'success': True,
            'recognized_text': recognized_text,
            'cache_hit': cache_hit
        })
        
    except Exception as e:
        # Handle errors gracefully
        print(f"Error during prediction: {e}")
        return jsonify({
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        JSON response with application status
    """
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'cache_size': len(prediction_cache)
    })


@app.route('/clear_cache', methods=['POST'])
def clear_cache():
    """
    Clear the prediction cache.
    
    Returns:
        JSON response confirming cache clear
    """
    global prediction_cache
    cache_size = len(prediction_cache)
    prediction_cache.clear()
    
    return jsonify({
        'success': True,
        'message': f'Cache cleared. Removed {cache_size} entries.'
    })


def initialize_model():
    """
    Initialize the handwriting recognition model.
    Called once at application startup.
    """
    global predictor
    
    try:
        print("Loading handwriting recognition model...")
        predictor = create_predictor()  # EasyOCR doesn't need config path
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Application will continue with limited functionality.")


if __name__ == '__main__':
    # Initialize model before starting the server
    initialize_model()
    
    # Run Flask development server
    print("\n" + "="*60)
    print("Handwriting Recognition Web App - EasyOCR")
    print("="*60)
    print("Open your browser and navigate to: http://localhost:5000")
    print("Upload handwritten images to recognize text")
    print("The app runs completely offline (after first model download)!")
    print("="*60 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False  # Disable reloader to prevent double model loading
    )

