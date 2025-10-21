import unittest
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from handwriting_app.app import app
from handwriting_app.model.mains.easyocr_predictor import create_predictor

class TestHandwritingApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global predictor
        predictor = create_predictor()
        
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    def test_home_page(self):
        """Test if home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_upload_endpoint(self):
        """Test if prediction endpoint works"""
        test_image_path = os.path.join(os.path.dirname(__file__), 'inigo_montoya1.png')
        if not os.path.exists(test_image_path):
            self.skipTest("Test image not found")
            
        with open(test_image_path, 'rb') as img:
            response = self.app.post('/predict',
                                   data={'file': (img, 'test.jpg')},
                                   content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        
    def test_predictor_initialization(self):
        """Test if predictor can be initialized"""
        try:
            predictor = create_predictor()
            self.assertIsNotNone(predictor)
        except Exception as e:
            self.fail(f"Predictor initialization failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()