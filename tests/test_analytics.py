"""
Unit Tests for Module 5 - Analytics/Visualization Module (analytics.py)
Tests data visualization and analytics generation
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analytics import calculate_stats, generate_user_analytics
from app import app, db, User, Prediction
from datetime import datetime

class TestAnalyticsModule(unittest.TestCase):
    """Test cases for Analytics Module"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with app.app_context():
            db.create_all()
            
            # Create test user
            test_user = User(
                username='analyticstest',
                email='analytics@test.com',
                preferred_language='en'
            )
            test_user.set_password('test')
            db.session.add(test_user)
            db.session.commit()
            
            # Create test predictions
            for i in range(10):
                pred = Prediction(
                    user_id=test_user.id,
                    crop_type='Wheat' if i % 2 == 0 else 'Rice',
                    crop_days=30 + i,
                    soil_moisture=400 - i * 10,
                    temperature=28 + i,
                    humidity=65 - i,
                    prediction=i % 2,
                    confidence=0.8 + i * 0.01
                )
                db.session.add(pred)
            db.session.commit()
            
            cls.test_user_id = test_user.id
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_calculate_stats_with_data(self):
        """Test 5.1: Calculate stats with predictions"""
        with app.app_context():
            predictions = Prediction.query.filter_by(user_id=self.test_user_id).all()
            stats = calculate_stats(predictions)
            
            self.assertEqual(stats['total'], 10, "Should have 10 predictions")
            self.assertGreater(stats['avg_confidence'], 0, "Should have average confidence")
            self.assertIn(stats['most_common_crop'], ['Wheat', 'Rice'], "Should identify common crop")
    
    def test_calculate_stats_empty(self):
        """Test 5.2: Calculate stats with no data"""
        stats = calculate_stats([])
        
        self.assertEqual(stats['total'], 0, "Total should be 0")
        self.assertEqual(stats['irrigation_needed'], 0, "Irrigation needed should be 0")
        self.assertEqual(stats['avg_confidence'], 0, "Avg confidence should be 0")
    
    def test_generate_user_analytics(self):
        """Test 5.3: Generate user analytics charts"""
        with app.app_context():
            predictions = Prediction.query.filter_by(user_id=self.test_user_id).all()
            charts = generate_user_analytics(predictions)
            
            self.assertIsNotNone(charts, "Should generate charts")
            self.assertIn('timeline', charts, "Should have timeline chart")
            self.assertIn('crop_rate', charts, "Should have crop rate chart")
            self.assertIn('moisture', charts, "Should have moisture chart")
    
    def test_analytics_with_no_data(self):
        """Test 5.4: Analytics with no predictions"""
        charts = generate_user_analytics([])
        self.assertIsNone(charts, "Should return None for empty data")
    
    def test_chart_html_format(self):
        """Test 5.5: Charts should be in HTML format"""
        with app.app_context():
            predictions = Prediction.query.filter_by(user_id=self.test_user_id).all()
            charts = generate_user_analytics(predictions)
            
            if charts:
                for chart_name, chart_html in charts.items():
                    self.assertIsInstance(chart_html, str, f"{chart_name} should be string")
                    self.assertIn('plotly', chart_html.lower(), f"{chart_name} should contain plotly")
    
    def test_stats_accuracy(self):
        """Test 5.6: Verify stats calculation accuracy"""
        with app.app_context():
            predictions = Prediction.query.filter_by(user_id=self.test_user_id).all()
            stats = calculate_stats(predictions)
            
            # Manual count
            irrigation_count = sum(1 for p in predictions if p.prediction == 1)
            
            self.assertEqual(stats['irrigation_needed'], irrigation_count,
                           "Irrigation count should match")
            self.assertEqual(stats['total'], len(predictions), "Total should match")

if __name__ == '__main__':
    unittest.main()
