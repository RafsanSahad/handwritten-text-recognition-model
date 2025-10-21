# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues with TensorFlow 1.15.5, you can:
- Use Python 3.7 or 3.8 (recommended)
- Or modify `requirements.txt` to use TensorFlow 2.x

## Step 2: Run the App

```bash
python app.py
```

The app will start in **mock mode** (no model required for testing).

## Step 3: Open Browser

Navigate to: **http://localhost:5000**

## Step 4: Upload Image

1. Click "Browse Files" or drag & drop an image
2. Click "Recognize Handwriting"
3. See the result!

---

## 🎯 Full Setup (with Real Model)

For actual handwriting recognition (not mock mode):

### Option 1: Automated Setup

```bash
python setup.py
```

Follow the prompts to download the model.

### Option 2: Manual Setup

1. Clone the model repository:
   ```bash
   git clone https://github.com/arshjot/Handwritten-Text-Recognition.git temp_repo
   ```

2. Copy model files:
   ```bash
   # On Windows PowerShell:
   Copy-Item -Path "temp_repo\experiments\CRNN_h128\*" -Destination "model\models\" -Recurse
   
   # On Linux/Mac:
   cp -r temp_repo/experiments/CRNN_h128/* model/models/
   ```

3. Clean up:
   ```bash
   # Windows:
   Remove-Item -Path "temp_repo" -Recurse -Force
   
   # Linux/Mac:
   rm -rf temp_repo
   ```

4. Run the app:
   ```bash
   python app.py
   ```

---

## 📱 Test It Out

### Mock Mode Testing
The app works immediately in mock mode:
- Upload any image
- Get sample predictions
- Test all UI features
- No model files required!

### Real Model Testing
With the actual model:
- Upload handwritten text images
- Get real AI predictions
- Support for cursive and print handwriting

---

## 🔧 Common Issues

### "No module named 'tensorflow'"
```bash
pip install tensorflow==1.15.5
# or for newer systems:
pip install tensorflow==2.13.0
```

### "Model not found" Warning
This is normal! The app runs in mock mode when model files aren't found.

### Port Already in Use
Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=8080)  # Use 8080 instead of 5000
```

---

## 🎨 UI Features

- ✅ Drag & Drop upload
- ✅ Image preview with details
- ✅ Live recognition
- ✅ Copy to clipboard
- ✅ Download as text file
- ✅ Responsive design
- ✅ Beautiful animations
- ✅ Error handling

---

## 📖 Next Steps

1. Read the full [README.md](README.md) for details
2. Customize colors in `static/css/style.css`
3. Adjust model settings in `model/configs/config.json`
4. Deploy to production with Gunicorn

---

## 🆘 Need Help?

- Check the console output for errors
- Read error messages in the UI
- Check `README.md` troubleshooting section
- Open an issue on GitHub

---

**Enjoy your handwriting recognition app! 🎉**

