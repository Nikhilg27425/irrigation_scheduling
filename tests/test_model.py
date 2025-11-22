"""
Unit Tests for Module 1 - ML Module (model.py)
Tests the IrrigationPredictor class and ML functionality
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import IrrigationPredictor
import numpy as np

class TestMLModule(unittest.TestCase):
    """Test cases for ML Module"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.predictor = IrrigationPredictor()
        # Load the trained model
        if os.path.exists('irrigation_model.pkl'):
            cls.predictor.load_model('irrigation_model.pkl')
    
    def test_model_loaded(self):
        """Test 1.1: Verify model is loaded successfully"""
        self.assertTrue(self.predictor.is_trained, "Model should be trained")
        self.assertIsNotNone(self.predictor.model, "Model should not be None")
    
    def test_label_encoder_exists(self):
        """Test 1.2: Verify label encoder is initialized"""
        self.assertIsNotNone(self.predictor.label_encoder, "Label encoder should exist")
        self.assertTrue(len(self.predictor.label_encoder.classes_) > 0, "Should have crop types")
    
    def test_prediction_wheat(self):
        """Test 1.3: Test prediction for Wheat crop"""
        crop_type = 'Wheat'
        crop_days = 30
        soil_moisture = 350
        temperature = 28
        humidity = 65
        
        prediction, probability = self.predictor.predict(
            crop_type, crop_days, soil_moisture, temperature, humidity
        )
        
        self.assertIn(prediction, [0, 1], "Prediction should be 0 or 1")
        self.assertEqual(len(probability), 2, "Should have 2 probabilities")
        self.assertAlmostEqual(sum(probability), 1.0, places=5, msg="Probabilities should sum to 1")
    
    def test_prediction_rice(self):
        """Test 1.4: Test prediction for Rice crop"""
        prediction, probability = self.predictor.predict('Rice', 45, 500, 30, 70)
        
        self.assertIsInstance(prediction, (int, np.integer), "Prediction should be integer")
        self.assertIsInstance(probability, np.ndarray, "Probability should be numpy array")
    
    def test_low_moisture_triggers_irrigation(self):
        """Test 1.5: Low soil moisture should likely trigger irrigation"""
        prediction, probability = self.predictor.predict('Wheat', 30, 200, 35, 40)
        
        # With very low moisture, irrigation should be needed
        self.assertEqual(prediction, 1, "Low moisture should trigger irrigation")
    
    def test_high_moisture_no_irrigation(self):
        """Test 1.6: High soil moisture should not need irrigation"""
        prediction, probability = self.predictor.predict('Wheat', 30, 800, 25, 70)
        
        # With high moisture, irrigation should not be needed
        self.assertEqual(prediction, 0, "High moisture should not need irrigation")
    
    def test_confidence_range(self):
        """Test 1.7: Confidence should be between 0 and 1"""
        prediction, probability = self.predictor.predict('Cotton', 20, 400, 28, 60)
        
        max_prob = max(probability)
        self.assertGreaterEqual(max_prob, 0.0, "Confidence should be >= 0")
        self.assertLessEqual(max_prob, 1.0, "Confidence should be <= 1")
    
    def test_invalid_crop_type(self):
        """Test 1.8: Test handling of invalid crop type"""
        with self.assertRaises(Exception):
            self.predictor.predict('InvalidCrop', 30, 400, 28, 60)
    
    def test_feature_names_exist(self):
        """Test 1.9: Verify feature names are stored"""
        self.assertIsNotNone(self.predictor.feature_names, "Feature names should exist")
        self.assertGreater(len(self.predictor.feature_names), 0, "Should have features")

if __name__ == '__main__':
    unittest.main()
