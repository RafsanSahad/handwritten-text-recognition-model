# 🖋️ Handwriting Recognition Web App

A beautiful, fully offline Flask web application for handwriting recognition using a pretrained CRNN (Convolutional Recurrent Neural Network) model from the [arshjot/Handwritten-Text-Recognition](https://github.com/arshjot/Handwritten-Text-Recognition) repository. Now a more improved version with ui.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-1.15.5-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🎨 **Beautiful UI** - Modern, colorful, and responsive interface with gradient backgrounds
- 📱 **Mobile Friendly** - Works perfectly on all devices
- 🔒 **100% Offline** - No internet required after setup, complete privacy
- ⚡ **Fast Recognition** - Powered by CRNN deep learning model
- 🖼️ **Drag & Drop** - Easy image upload with live preview
- 💾 **Caching** - Intelligent caching to avoid re-processing same images
- 📋 **Copy & Download** - Easy text extraction with clipboard and file download
- 🎯 **Error Handling** - Graceful error handling and user feedback

## 📂 Project Structure

```
handwriting_app/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── model/                          # Model directory
│   ├── configs/
│   │   └── config.json            # Model configuration
│   ├── models/                    # Pretrained model weights (to be added)
│   ├── mains/
│   │   ├── __init__.py
│   │   └── predictor.py           # Prediction logic
│   ├── data_loader/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
│
├── templates/
│   └── index.html                 # Main web interface
│
└── static/
    ├── css/
    │   └── style.css              # Custom styling
    ├── js/
    │   └── script.js              # Interactive JavaScript
    └── uploads/                   # Temporary upload folder
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/RafsanSahad/handwritten-text-recognition-model.git
   cd handwriting_app
   ```

2. **Install Python Cuda dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** If you encounter issues with TensorFlow 1.15.5, you may need to use a compatible Python version (3.7 or 3.8) or adjust the TensorFlow version.

3. **Download the pretrained model:**

   To use the actual model from [arshjot/Handwritten-Text-Recognition](https://github.com/arshjot/Handwritten-Text-Recognition):

   ```bash
   # Clone the original repository
   git clone https://github.com/arshjot/Handwritten-Text-Recognition.git temp_repo
   
   # Copy the model files
   cp -r temp_repo/experiments/CRNN_h128/* model/models/
   
   # Clean up
   rm -rf temp_repo
   ```

   Or download the model weights manually and place them in `model/models/`:
   - Download from the repository's releases or Google Drive link
   - Extract and place checkpoint files in `model/models/`

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to [http://localhost:5000](http://localhost:5000)

## 🎯 Usage

1. **Upload Image:**
   - Click "Browse Files" or drag & drop an image
   - Supported formats: JPG, PNG, JPEG, BMP
   - Maximum size: 16MB

2. **Preview:**
   - View the uploaded image
   - Check file details (name, size, dimensions)

3. **Recognize:**
   - Click "Recognize Handwriting" button
   - Wait for the AI to process (usually < 2 seconds)

4. **Results:**
   - View recognized text in the text area
   - Copy to clipboard with one click
   - Download as text file
   - Upload another image to continue

## 🧪 Testing Without Model

The app includes a **mock predictor** that works even without the actual model files. This is perfect for:
- Testing the UI and functionality
- Development and debugging
- Demonstrating the app before downloading large model files

When model files are not found, the app will:
- Show a warning in the console
- Use sample predictions for demonstration
- Allow you to test all UI features

## 🎨 Customization

### Change Colors

Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    /* Add your custom colors */
}
```

### Adjust Model Settings

Edit `model/configs/config.json`:

```json
{
  "image_height": 32,
  "image_width": 128,
  "model_path": "model/models/best_model"
}
```

### Change Upload Limits

Edit `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Change to your desired size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}  # Add more formats
```

## 🔧 Advanced Configuration

### Production Deployment

For production use with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Desktop Application (PyInstaller)

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "templates:templates" --add-data "static:static" --add-data "model:model" app.py
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t handwriting-app .
docker run -p 5000:5000 handwriting-app
```

## 📊 Model Information

This app uses the CRNN (Convolutional Recurrent Neural Network) architecture:

- **Input:** Grayscale images (32×128 pixels)
- **Architecture:** CNN + Bidirectional LSTM + CTC Loss
- **Output:** Character sequences (text)
- **Training:** Trained on handwritten text datasets

**Model Citation:**
```
@misc{arshjot2020,
  author = {Arshjot Singh},
  title = {Handwritten Text Recognition},
  year = {2020},
  publisher = {GitHub},
  url = {https://github.com/arshjot/Handwritten-Text-Recognition}
}
```

## 🐛 Troubleshooting

### TensorFlow Installation Issues

If you have problems installing TensorFlow 1.15.5:

```bash
# Try TensorFlow 2.x instead (requires code modifications)
pip install tensorflow==2.13.0
```

### Import Errors

```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Model Not Loading

- Check that model files exist in `model/models/`
- Verify the `model_path` in `config.json`
- Check console output for error messages
- App will fall back to mock predictor if model fails

### Permission Errors

On Windows, run as administrator or adjust folder permissions:

```bash
icacls static\uploads /grant Users:(OI)(CI)F
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [arshjot/Handwritten-Text-Recognition](https://github.com/arshjot/Handwritten-Text-Recognition) - For the pretrained CRNN model
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap 5](https://getbootstrap.com/) - UI components
- [TensorFlow](https://www.tensorflow.org/) - Deep learning framework

## 📧 Contact
rafsansahad07@gmail.com

For questions, issues, or suggestions, please open an issue on GitHub.

---




