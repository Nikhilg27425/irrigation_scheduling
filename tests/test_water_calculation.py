"""
Unit Tests for Water Requirement Calculation
Tests the Hargreaves ETo method implementation
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import calculate_water_requirement

class TestWaterCalculation(unittest.TestCase):
    """Test cases for Water Calculation"""
    
    def test_water_calculation_wheat(self):
        """Test 4.1: Water calculation for Wheat"""
        result = calculate_water_requirement('Wheat', 28, 30, 350)
        
        self.assertIn('ETo', result, "Should have ETo")
        self.assertIn('Kc', result, "Should have Kc")
        self.assertIn('ETc', result, "Should have ETc")
        self.assertIn('irrigation_amount', result, "Should have irrigation amount")
        
        self.assertGreater(result['ETo'], 0, "ETo should be positive")
        self.assertGreater(result['irrigation_amount'], 0, "Irrigation amount should be positive")
    
    def test_growth_stages(self):
        """Test 4.2: Different growth stages have different Kc"""
        initial = calculate_water_requirement('Wheat', 28, 15, 400)  # Initial stage
        mid = calculate_water_requirement('Wheat', 28, 60, 400)     # Mid stage
        late = calculate_water_requirement('Wheat', 28, 120, 400)   # Late stage
        
        self.assertNotEqual(initial['Kc'], mid['Kc'], "Initial and mid Kc should differ")
        self.assertNotEqual(mid['Kc'], late['Kc'], "Mid and late Kc should differ")
    
    def test_temperature_effect(self):
        """Test 4.3: Higher temperature increases ETo"""
        low_temp = calculate_water_requirement('Wheat', 20, 30, 400)
        high_temp = calculate_water_requirement('Wheat', 35, 30, 400)
        
        self.assertGreater(high_temp['ETo'], low_temp['ETo'], "Higher temp should increase ETo")
    
    def test_soil_moisture_effect(self):
        """Test 4.4: Lower soil moisture increases irrigation need"""
        low_moisture = calculate_water_requirement('Wheat', 28, 30, 200)
        high_moisture = calculate_water_requirement('Wheat', 28, 30, 700)
        
        self.assertGreater(low_moisture['irrigation_amount'], high_moisture['irrigation_amount'],
                          "Lower moisture should need more irrigation")
    
    def test_rice_high_water_need(self):
        """Test 4.5: Rice should have higher Kc than Wheat"""
        wheat = calculate_water_requirement('Wheat', 28, 60, 400)
        rice = calculate_water_requirement('Rice', 28, 60, 400)
        
        self.assertGreater(rice['Kc'], wheat['Kc'], "Rice should have higher Kc")
    
    def test_liters_conversion(self):
        """Test 4.6: Verify liters per m² equals mm"""
        result = calculate_water_requirement('Wheat', 28, 30, 400)
        
        self.assertEqual(result['irrigation_amount'], result['irrigation_liters_per_m2'],
                        "mm should equal L/m²")
    
    def test_acre_conversion(self):
        """Test 4.7: Verify acre conversion"""
        result = calculate_water_requirement('Wheat', 28, 30, 400)
        
        expected_liters_per_acre = result['irrigation_liters_per_m2'] * 4046.86
        self.assertAlmostEqual(result['irrigation_liters_per_acre'], expected_liters_per_acre, places=1,
                              msg="Acre conversion should be correct")
    
    def test_all_crops(self):
        """Test 4.8: Test calculation for all crop types"""
        crops = ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Maize', 'Soybean']
        
        for crop in crops:
            result = calculate_water_requirement(crop, 28, 30, 400)
            self.assertGreater(result['irrigation_amount'], 0, f"{crop} should have positive irrigation amount")

if __name__ == '__main__':
    unittest.main()
