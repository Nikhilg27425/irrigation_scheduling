"""
Unit Tests for Module 3 - Scheduler Module (scheduler.py)
Tests irrigation scheduling logic and decision flow
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler import check_rain_forecast, check_soil_moisture_threshold
from scheduler import send_notification, execute_irrigation

class TestSchedulerModule(unittest.TestCase):
    """Test cases for Scheduler Module"""
    
    def test_rain_forecast_check(self):
        """Test 3.1: Rain forecast check returns boolean"""
        rain_expected, probability = check_rain_forecast("Test Location")
        
        self.assertIsInstance(rain_expected, bool, "Should return boolean")
        self.assertIsInstance(probability, (int, float), "Probability should be numeric")
        self.assertGreaterEqual(probability, 0.0, "Probability should be >= 0")
        self.assertLessEqual(probability, 100.0, "Probability should be <= 100")
    
    def test_soil_moisture_threshold_wheat(self):
        """Test 3.2: Soil moisture threshold for Wheat"""
        # Low moisture should need irrigation
        needs_irrigation = check_soil_moisture_threshold(300, 'Wheat')
        self.assertTrue(needs_irrigation, "Low moisture should need irrigation")
        
        # High moisture should not need irrigation
        no_irrigation = check_soil_moisture_threshold(600, 'Wheat')
        self.assertFalse(no_irrigation, "High moisture should not need irrigation")
    
    def test_soil_moisture_threshold_rice(self):
        """Test 3.3: Soil moisture threshold for Rice"""
        # Rice needs more water
        needs_irrigation = check_soil_moisture_threshold(500, 'Rice')
        self.assertTrue(needs_irrigation, "Rice with 500 moisture should need irrigation")
    
    def test_soil_moisture_threshold_default(self):
        """Test 3.4: Default threshold for unknown crop"""
        needs_irrigation = check_soil_moisture_threshold(350, 'UnknownCrop')
        self.assertTrue(needs_irrigation, "Should use default threshold")
    
    def test_notification_function(self):
        """Test 3.5: Notification function doesn't crash"""
        from app import User
        test_user = User(username='test', email='test@test.com')
        
        try:
            send_notification(test_user, "Test message")
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success, "Notification should not crash")
    
    def test_execute_irrigation_function(self):
        """Test 3.6: Execute irrigation function doesn't crash"""
        from app import IrrigationSchedule
        
        test_schedule = IrrigationSchedule(
            water_amount=50.0,
            duration=60
        )
        
        try:
            execute_irrigation(test_schedule)
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success, "Execute irrigation should not crash")
    
    def test_moisture_boundary_conditions(self):
        """Test 3.7: Test boundary conditions for soil moisture"""
        # Test at 0 moisture
        self.assertTrue(check_soil_moisture_threshold(0, 'Wheat'), "0 moisture should need irrigation")
        
        # Test at 1000 moisture
        self.assertFalse(check_soil_moisture_threshold(1000, 'Wheat'), "1000 moisture should not need irrigation")
    
    def test_multiple_crop_types(self):
        """Test 3.8: Test threshold for multiple crop types"""
        crops = ['Wheat', 'Rice', 'Cotton', 'Maize', 'Soybean']
        
        for crop in crops:
            result = check_soil_moisture_threshold(400, crop)
            self.assertIsInstance(result, bool, f"Should return bool for {crop}")

if __name__ == '__main__':
    unittest.main()
