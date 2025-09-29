from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
from model import IrrigationPredictor
import os

app = Flask(__name__)

# Global predictor instance
predictor = None

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

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    try:
        if predictor is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get form data
        data = request.get_json()
        
        crop_type = data.get('crop_type')
        crop_days = float(data.get('crop_days'))
        soil_moisture = float(data.get('soil_moisture'))
        temperature = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        
        # Validate inputs
        if not all([crop_type, crop_days is not None, soil_moisture is not None, 
                   temperature is not None, humidity is not None]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Make prediction
        prediction, probability = predictor.predict(
            crop_type, crop_days, soil_moisture, temperature, humidity
        )
        
        # Format response
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

@app.route('/crop_types')
def get_crop_types():
    """Get available crop types"""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    crop_types = predictor.label_encoder.classes_.tolist()
    return jsonify({'crop_types': crop_types})

@app.route('/model_info')
def model_info():
    """Get model information"""
    if predictor is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'is_trained': predictor.is_trained,
        'feature_names': predictor.feature_names.tolist() if hasattr(predictor, 'feature_names') else []
    })

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        print("Starting Flask app...")
        # Try port 5000 first, fallback to 5001 if busy
        import socket
        def find_free_port(start_port=5000):
            for port in range(start_port, start_port + 10):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('localhost', port))
                        return port
                except OSError:
                    continue
            return 5001  # fallback
        
        port = find_free_port()
        print(f"Server starting on port {port}")
        print(f"Open your browser and go to: http://localhost:{port}")
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        print("Failed to load model. Exiting...")
