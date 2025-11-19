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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
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
    is_admin = db.Column(db.Boolean, default=False)
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
def calculate_water_requirement(crop_type, temperature, crop_days, soil_moisture):
    """
    Calculate water requirement using Hargreaves ETo method
    """
    # Crop coefficients (Kc) for different crops and growth stages
    crop_kc = {
        'Wheat': {'initial': 0.3, 'mid': 1.15, 'late': 0.4},
        'Rice': {'initial': 1.05, 'mid': 1.2, 'late': 0.9},
        'Cotton': {'initial': 0.35, 'mid': 1.15, 'late': 0.7},
        'Sugarcane': {'initial': 0.4, 'mid': 1.25, 'late': 0.75},
        'Maize': {'initial': 0.3, 'mid': 1.2, 'late': 0.6},
        'Soybean': {'initial': 0.4, 'mid': 1.15, 'late': 0.5},
        'default': {'initial': 0.35, 'mid': 1.0, 'late': 0.6}
    }
    
    # Get Kc for crop (use default if not found)
    kc_values = crop_kc.get(crop_type, crop_kc['default'])
    
    # Determine growth stage based on crop days
    if crop_days < 30:
        Kc = kc_values['initial']
        stage = 'Initial'
    elif crop_days < 90:
        Kc = kc_values['mid']
        stage = 'Mid-Season'
    else:
        Kc = kc_values['late']
        stage = 'Late Season'
    
    # Hargreaves ETo calculation
    # ETo = 0.0023 * (Tmean + 17.8) * ΔT^0.5 * Ra
    # Simplified: Using default values for ΔT and Ra
    Tmean = temperature
    delta_T = 10  # Default temperature range (°C)
    Ra = 25  # Approximate extraterrestrial radiation (MJ/m²/day) - varies by location and season
    
    ETo = 0.0023 * (Tmean + 17.8) * (delta_T ** 0.5) * Ra
    
    # Calculate crop evapotranspiration
    ETc = Kc * ETo
    
    # Available Water (AW) - typical values for different soil types
    # Assuming medium soil: 150 mm/m depth
    AW = 150  # mm
    
    # Management Allowed Depletion (MAD) - typically 0.5 for most crops
    MAD = 0.5
    
    # Current depletion based on soil moisture
    # Assuming soil moisture is on scale 0-1000, where 1000 is field capacity
    current_depletion = (1000 - soil_moisture) / 1000 * AW
    
    # Check if irrigation is needed
    threshold = MAD * AW
    
    # Calculate irrigation amount needed
    # f = fraction of AW to refill (typically 0.8-1.0)
    f = 0.9
    irrigation_needed = max(0, f * AW - (AW - current_depletion))
    
    # Convert to liters per square meter (1 mm = 1 L/m²)
    irrigation_liters_per_m2 = irrigation_needed
    
    return {
        'ETo': round(ETo, 2),  # mm/day
        'Kc': round(Kc, 2),
        'ETc': round(ETc, 2),  # mm/day
        'growth_stage': stage,
        'current_depletion': round(current_depletion, 2),  # mm
        'threshold': round(threshold, 2),  # mm
        'irrigation_amount': round(irrigation_needed, 2),  # mm
        'irrigation_liters_per_m2': round(irrigation_liters_per_m2, 2),  # L/m²
        'irrigation_liters_per_acre': round(irrigation_liters_per_m2 * 4046.86, 2),  # L/acre
        'available_water': AW,
        'MAD': MAD
    }

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
        
        # If irrigation is needed, calculate water requirement
        if prediction == 1:
            water_calc = calculate_water_requirement(crop_type, temperature, crop_days, soil_moisture)
            result['water_requirement'] = water_calc
        
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

@app.route('/admin')
@login_required
def admin():
    """Admin dashboard"""
    if not current_user.is_admin:
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    predictions = Prediction.query.order_by(Prediction.created_at.desc()).limit(50).all()
    
    stats = {
        'total_users': User.query.count(),
        'total_predictions': Prediction.query.count(),
        'predictions_today': Prediction.query.filter(
            Prediction.created_at >= datetime.utcnow().date()
        ).count(),
        'irrigation_needed': Prediction.query.filter_by(prediction=1).count(),
        'no_irrigation': Prediction.query.filter_by(prediction=0).count()
    }
    
    return render_template('admin.html', users=users, predictions=predictions, stats=stats)

@app.route('/api/admin/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if user:
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot delete yourself'}), 400
        
        # Delete user's predictions first
        Prediction.query.filter_by(user_id=user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/api/admin/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin(user_id):
    """Toggle admin status (admin only)"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if user:
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot modify your own admin status'}), 400
        
        user.is_admin = not user.is_admin
        db.session.commit()
        return jsonify({'success': True, 'is_admin': user.is_admin})
    return jsonify({'success': False, 'message': 'User not found'}), 404

# Initialize database and load model on startup
with app.app_context():
    db.create_all()
    try:
        # Create demo user if not exists
        if not User.query.filter_by(username='farmer').first():
            demo_user = User(
                username='farmer',
                email='farmer@example.com',
                farm_name='Green Valley Farm',
                location='Punjab, India',
                farm_size=25.5,
                is_admin=False
            )
            demo_user.set_password('farmer123')
            db.session.add(demo_user)
            db.session.commit()
            print("Demo user created")
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                farm_name='Admin Farm',
                location='System',
                farm_size=0,
                is_admin=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created")
    except Exception as e:
        print(f"Error creating users: {e}")

load_model()

if __name__ == '__main__':
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
