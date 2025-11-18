from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
from model import IrrigationPredictor
import os
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Global predictor instance
predictor = None

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    farm_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    farm_size = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crop_type = db.Column(db.String(50))
    crop_days = db.Column(db.Float)
    soil_moisture = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    prediction = db.Column(db.Integer)
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def load_model():
    """Load the trained model"""
    global predictor
    try:
        if os.path.exists('irrigation_model.pkl'):
            predictor = IrrigationPredictor()
            predictor.load_model('irrigation_model.pkl')
            print("Model loaded successfully!")
        else:
            print("Model file not found. Please train the model first.")
            return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False
    return True

# Weather API helper
def get_weather_data(location="New Delhi"):
    """Get weather data from OpenWeatherMap API"""
    try:
        # Using OpenWeatherMap API (you'll need to sign up for a free API key)
        api_key = os.environ.get('OPENWEATHER_API_KEY', 'demo')
        
        # Mock data for demo purposes
        mock_weather = {
            'current': {
                'temp': 28.5,
                'humidity': 65,
                'description': 'Partly cloudy',
                'wind_speed': 12,
                'pressure': 1013,
                'icon': '02d'
            },
            'forecast': [
                {'day': 'Today', 'temp_max': 32, 'temp_min': 24, 'humidity': 65, 'description': 'Partly cloudy'},
                {'day': 'Tomorrow', 'temp_max': 33, 'temp_min': 25, 'humidity': 60, 'description': 'Sunny'},
                {'day': 'Day 3', 'temp_max': 31, 'temp_min': 23, 'humidity': 70, 'description': 'Cloudy'},
                {'day': 'Day 4', 'temp_max': 29, 'temp_min': 22, 'humidity': 75, 'description': 'Light rain'},
                {'day': 'Day 5', 'temp_max': 30, 'temp_min': 24, 'humidity': 68, 'description': 'Partly cloudy'},
            ]
        }
        return mock_weather
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if user exists
        if User.query.filter_by(username=data.get('username')).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            farm_name=data.get('farm_name'),
            location=data.get('location'),
            farm_size=float(data.get('farm_size', 0))
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    weather = get_weather_data(current_user.location or "New Delhi")
    recent_predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', weather=weather, predictions=recent_predictions)

@app.route('/weather')
@login_required
def weather():
    weather_data = get_weather_data(current_user.location or "New Delhi")
    return render_template('weather.html', weather=weather_data)

@app.route('/irrigation')
@login_required
def irrigation():
    return render_template('irrigation.html')

@app.route('/api-management')
@login_required
def api_management():
    return render_template('api_management.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# API Endpoints
@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    """API endpoint for making predictions"""
    try:
        if predictor is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        crop_type = data.get('crop_type')
        crop_days = float(data.get('crop_days'))
        soil_moisture = float(data.get('soil_moisture'))
        temperature = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        
        if not all([crop_type, crop_days is not None, soil_moisture is not None, 
                   temperature is not None, humidity is not None]):
            return jsonify({'error': 'All fields are required'}), 400
        
        prediction, probability = predictor.predict(
            crop_type, crop_days, soil_moisture, temperature, humidity
        )
        
        # Save prediction to database
        pred_record = Prediction(
            user_id=current_user.id,
            crop_type=crop_type,
            crop_days=crop_days,
            soil_moisture=soil_moisture,
            temperature=temperature,
            humidity=humidity,
            prediction=int(prediction),
            confidence=float(max(probability))
        )
        db.session.add(pred_record)
        db.session.commit()
        
        result = {
            'prediction': int(prediction),
            'prediction_text': 'Irrigation Needed' if prediction == 1 else 'No Irrigation Needed',
            'confidence': float(max(probability)),
            'probabilities': {
                'no_irrigation': float(probability[0]),
                'irrigation_needed': float(probability[1])
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/crop_types')
@login_required
def get_crop_types():
    """Get available crop types"""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    crop_types = predictor.label_encoder.classes_.tolist()
    return jsonify({'crop_types': crop_types})

@app.route('/api/weather')
@login_required
def api_weather():
    """Get weather data"""
    location = request.args.get('location', current_user.location or 'New Delhi')
    weather_data = get_weather_data(location)
    return jsonify(weather_data)

@app.route('/api/predictions/history')
@login_required
def prediction_history():
    """Get user's prediction history"""
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).limit(20).all()
    
    result = [{
        'id': p.id,
        'crop_type': p.crop_type,
        'prediction': p.prediction,
        'confidence': p.confidence,
        'created_at': p.created_at.strftime('%Y-%m-%d %H:%M')
    } for p in predictions]
    
    return jsonify(result)

@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        if 'farm_name' in data:
            current_user.farm_name = data['farm_name']
        if 'location' in data:
            current_user.location = data['location']
        if 'farm_size' in data:
            current_user.farm_size = float(data['farm_size'])
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    if load_model():
        print("Starting Flask app...")
        import socket
        def find_free_port(start_port=5000):
            for port in range(start_port, start_port + 10):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('localhost', port))
                        return port
                except OSError:
                    continue
            return 5001
        
        port = find_free_port()
        print(f"Server starting on port {port}")
        print(f"Open your browser and go to: http://localhost:{port}")
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        print("Failed to load model. Exiting...")
