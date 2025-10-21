/**
 * Handwriting Recognition - Interactive JavaScript
 * Handles file upload, drag & drop, preview, and API communication
 */

// ============================================
// Global Variables
// ============================================
let selectedFile = null;

// DOM Elements
const fileInput = document.getElementById('file-input');
const uploadArea = document.getElementById('upload-area');
const browseBtn = document.getElementById('browse-btn');
const uploadForm = document.getElementById('upload-form');
const uploadSection = document.getElementById('upload-section');
const previewSection = document.getElementById('preview-section');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');
const imagePreview = document.getElementById('image-preview');
const removeImageBtn = document.getElementById('remove-image');
const recognizeBtn = document.getElementById('recognize-btn');
const recognizedText = document.getElementById('recognized-text');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');
const uploadAnotherBtn = document.getElementById('upload-another');
const cacheBadge = document.getElementById('cache-badge');

// File info elements
const fileNameSpan = document.getElementById('file-name');
const fileSizeSpan = document.getElementById('file-size');
const fileDimensionsSpan = document.getElementById('file-dimensions');

// ============================================
// Utility Functions
// ============================================

/**
 * Format file size in human-readable format
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toastElement = document.getElementById('notification-toast');
    const toastBody = document.getElementById('toast-message');
    
    toastBody.textContent = message;
    
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
}

/**
 * Show specific section and hide others
 */
function showSection(section) {
    uploadSection.classList.add('d-none');
    loadingSection.classList.add('d-none');
    resultSection.classList.add('d-none');
    
    section.classList.remove('d-none');
}

/**
 * Reset the form to initial state
 */
function resetForm() {
    selectedFile = null;
    fileInput.value = '';
    previewSection.classList.add('d-none');
    uploadArea.style.display = 'block';
    showSection(uploadSection);
}

// ============================================
// File Upload Handling
// ============================================

/**
 * Handle file selection
 */
function handleFileSelect(file) {
    if (!file) return;
    
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showToast('Please select a valid image file (PNG, JPG, JPEG, BMP)', 'error');
        return;
    }
    
    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showToast('File size must be less than 16MB', 'error');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    displayPreview(file);
}

/**
 * Display image preview and file info
 */
function displayPreview(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        
        // Get image dimensions
        const img = new Image();
        img.onload = function() {
            fileDimensionsSpan.textContent = `${this.width} × ${this.height} px`;
        };
        img.src = e.target.result;
    };
    
    reader.readAsDataURL(file);
    
    // Update file info
    fileNameSpan.textContent = file.name;
    fileSizeSpan.textContent = formatFileSize(file.size);
    
    // Show preview section
    uploadArea.style.display = 'none';
    previewSection.classList.remove('d-none');
}

// ============================================
// Event Listeners
// ============================================

/**
 * Prevent default drag behaviors
 */
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults (e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Highlight drop zone when dragging over it
 */
['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    uploadArea.classList.add('drag-over');
}

function unhighlight(e) {
    uploadArea.classList.remove('drag-over');
}

/**
 * Handle dropped files
 */
uploadArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
}

/**
 * Browse button click
 */
browseBtn.addEventListener('click', (e) => {
    e.preventDefault();
    fileInput.click();
});

/**
 * File input change
 */
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
});

/**
 * Upload area click
 */
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

/**
 * Drag and drop events
 */
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

/**
 * Remove image button
 */
removeImageBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    resetForm();
});

/**
 * Upload another button
 */
uploadAnotherBtn.addEventListener('click', () => {
    resetForm();
});

/**
 * Form submission - Recognition
 */
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
        showToast('Please select an image first', 'error');
        return;
    }
    
    // Show loading section
    showSection(loadingSection);
    
    // Prepare form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        // Send request to server
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show result
            recognizedText.value = data.recognized_text;
            
            // Show cache badge if result was from cache
            if (data.cache_hit) {
                cacheBadge.classList.remove('d-none');
            } else {
                cacheBadge.classList.add('d-none');
            }
            
            showSection(resultSection);
            showToast('Recognition completed successfully!', 'success');
        } else {
            // Show error
            showToast(data.error || 'Error processing image', 'error');
            showSection(uploadSection);
        }
        
    } catch (error) {
        console.error('Error:', error);
        showToast('Network error. Please try again.', 'error');
        showSection(uploadSection);
    }
});

/**
 * Copy to clipboard button
 */
copyBtn.addEventListener('click', () => {
    recognizedText.select();
    document.execCommand('copy');
    
    // Visual feedback
    const originalText = copyBtn.innerHTML;
    copyBtn.innerHTML = '<i class="bi bi-check-lg me-2"></i>Copied!';
    copyBtn.classList.add('btn-success');
    copyBtn.classList.remove('btn-primary');
    
    setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.classList.remove('btn-success');
        copyBtn.classList.add('btn-primary');
    }, 2000);
    
    showToast('Text copied to clipboard!', 'success');
});

/**
 * Download as text file button
 */
downloadBtn.addEventListener('click', () => {
    const text = recognizedText.value;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'recognized_text.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showToast('Text file downloaded!', 'success');
});

// ============================================
// Keyboard Shortcuts
// ============================================
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + V to paste image (if supported)
    if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        navigator.clipboard.read().then(items => {
            for (let item of items) {
                for (let type of item.types) {
                    if (type.startsWith('image/')) {
                        item.getType(type).then(blob => {
                            handleFileSelect(blob);
                        });
                    }
                }
            }
        }).catch(err => {
            console.log('Paste not supported or no image in clipboard');
        });
    }
    
    // Escape to reset
    if (e.key === 'Escape' && !resultSection.classList.contains('d-none')) {
        resetForm();
    }
});

// ============================================
// Page Load Animations
// ============================================
window.addEventListener('load', () => {
    console.log('🎨 Handwriting Recognition App Loaded');
    console.log('✨ UI ready for image upload');
    
    // Check if app is online
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            console.log('✅ Server Status:', data);
        })
        .catch(error => {
            console.warn('⚠️ Server connection issue:', error);
        });
});

// ============================================
// Service Worker (for offline support)
// ============================================
if ('serviceWorker' in navigator) {
    // Optional: Register service worker for better offline support
    // navigator.serviceWorker.register('/sw.js');
}

// ============================================
// Prevent accidental navigation
// ============================================
window.addEventListener('beforeunload', (e) => {
    if (selectedFile && !resultSection.classList.contains('d-none')) {
        e.preventDefault();
        e.returnValue = '';
    }
});

