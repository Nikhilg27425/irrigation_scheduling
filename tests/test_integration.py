"""
Integration Tests - Testing complete workflows
Tests end-to-end scenarios across multiple modules
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User, Prediction, IrrigationSchedule
import json
from datetime import datetime, timedelta

class TestIntegration(unittest.TestCase):
    """Integration test cases"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_complete_user_journey(self):
        """INT-1: Complete user journey from registration to prediction"""
        # Step 1: Register
        response = self.client.post('/register',
            data=json.dumps({
                'username': 'journeyuser',
                'email': 'journey@test.com',
                'password': 'testpass',
                'language': 'en',
                'farm_name': 'Journey Farm',
                'location': 'Test City',
                'farm_size': 10.0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Login
        response = self.client.post('/login',
            data=json.dumps({'username': 'journeyuser', 'password': 'testpass'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        # Step 3: Access dashboard
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        
        # Step 4: Make prediction
        response = self.client.post('/api/predict',
            data=json.dumps({
                'crop_type': 'Wheat',
                'crop_days': 30,
                'soil_moisture': 350,
                'temperature': 28,
                'humidity': 65
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)
    
    def test_prediction_to_schedule_workflow(self):
        """INT-2: Prediction to scheduling workflow"""
        # Login
        self.client.post('/register',
            data=json.dumps({
                'username': 'scheduser',
                'email': 'sched@test.com',
                'password': 'test',
                'language': 'en',
                'farm_name': 'Farm',
                'location': 'City',
                'farm_size': 5.0
            }),
            content_type='application/json'
        )
        
        self.client.post('/login',
            data=json.dumps({'username': 'scheduser', 'password': 'test'}),
            content_type='application/json'
        )
        
        # Make prediction
        response = self.client.post('/api/predict',
            data=json.dumps({
                'crop_type': 'Wheat',
                'crop_days': 30,
                'soil_moisture': 300,
                'temperature': 30,
                'humidity': 60
            }),
            content_type='application/json'
        )
        pred_data = json.loads(response.data)
        
        if pred_data.get('prediction') == 1:
            # Create schedule
            tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat()
            response = self.client.post('/api/schedule/create',
                data=json.dumps({
                    'prediction_id': pred_data.get('prediction_id'),
                    'water_amount': 50.0,
                    'duration': 60,
                    'scheduled_time': tomorrow
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            sched_data = json.loads(response.data)
            self.assertTrue(sched_data['success'])
    
    def test_analytics_generation(self):
        """INT-3: Analytics generation after predictions"""
        # Create user and predictions
        self.client.post('/register',
            data=json.dumps({
                'username': 'analyticsuser',
                'email': 'analytics@test.com',
                'password': 'test',
                'language': 'en',
                'farm_name': 'Farm',
                'location': 'City',
                'farm_size': 5.0
            }),
            content_type='application/json'
        )
        
        self.client.post('/login',
            data=json.dumps({'username': 'analyticsuser', 'password': 'test'}),
            content_type='application/json'
        )
        
        # Make multiple predictions
        for i in range(3):
            self.client.post('/api/predict',
                data=json.dumps({
                    'crop_type': 'Wheat',
                    'crop_days': 30 + i,
                    'soil_moisture': 400 - i * 50,
                    'temperature': 28 + i,
                    'humidity': 65 - i
                }),
                content_type='application/json'
            )
        
        # Access analytics
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
