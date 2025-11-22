"""
Unit Tests for Module 2 - Backend API (app.py)
Tests Flask routes, authentication, and API endpoints
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User, Prediction, IrrigationSchedule
import json

class TestBackendAPI(unittest.TestCase):
    """Test cases for Backend API"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        cls.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            # Create test user
            test_user = User(
                username='testuser',
                email='test@example.com',
                farm_name='Test Farm',
                location='Test Location',
                farm_size=10.0,
                preferred_language='en'
            )
            test_user.set_password('testpass')
            db.session.add(test_user)
            db.session.commit()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def login(self):
        """Helper method to login"""
        return self.client.post('/login', 
            data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
            content_type='application/json'
        )
    
    def test_home_redirect(self):
        """Test 2.1: Home page should redirect to login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302, "Should redirect")
    
    def test_login_page_loads(self):
        """Test 2.2: Login page should load"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200, "Login page should load")
    
    def test_register_page_loads(self):
        """Test 2.3: Register page should load"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200, "Register page should load")
    
    def test_successful_login(self):
        """Test 2.4: Test successful login"""
        response = self.login()
        data = json.loads(response.data)
        self.assertTrue(data['success'], "Login should succeed")
    
    def test_failed_login(self):
        """Test 2.5: Test failed login with wrong password"""
        response = self.client.post('/login',
            data=json.dumps({'username': 'testuser', 'password': 'wrongpass'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertFalse(data['success'], "Login should fail")
    
    def test_registration(self):
        """Test 2.6: Test user registration"""
        response = self.client.post('/register',
            data=json.dumps({
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'newpass',
                'language': 'en',
                'farm_name': 'New Farm',
                'location': 'New Location',
                'farm_size': 5.0
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertTrue(data['success'], "Registration should succeed")
    
    def test_duplicate_username(self):
        """Test 2.7: Test registration with duplicate username"""
        response = self.client.post('/register',
            data=json.dumps({
                'username': 'testuser',
                'email': 'another@example.com',
                'password': 'pass',
                'language': 'en',
                'farm_name': 'Farm',
                'location': 'Location',
                'farm_size': 5.0
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertFalse(data['success'], "Should fail with duplicate username")
    
    def test_dashboard_requires_login(self):
        """Test 2.8: Dashboard should require authentication"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302, "Should redirect to login")
    
    def test_crop_types_endpoint(self):
        """Test 2.9: Test crop types API endpoint"""
        self.login()
        response = self.client.get('/api/crop_types')
        self.assertEqual(response.status_code, 200, "Should return crop types")
        data = json.loads(response.data)
        self.assertIn('crop_types', data, "Should have crop_types key")
    
    def test_profile_update(self):
        """Test 2.10: Test profile update"""
        self.login()
        response = self.client.post('/api/profile/update',
            data=json.dumps({
                'farm_name': 'Updated Farm',
                'location': 'Updated Location',
                'farm_size': 15.0
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertTrue(data['success'], "Profile update should succeed")

if __name__ == '__main__':
    unittest.main()
