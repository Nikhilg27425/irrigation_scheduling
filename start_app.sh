#!/bin/bash

# Smart Irrigation Scheduling System - Startup Script

echo "🌱 Starting Smart Irrigation Scheduling System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "Installing dependencies..."
    pip install Flask pandas numpy scikit-learn matplotlib seaborn joblib
fi

# Check if model exists
if [ ! -f "irrigation_model.pkl" ]; then
    echo "Training machine learning model..."
    python model.py
fi

# Start the Flask application
echo "🚀 Starting web application..."
echo "The app will automatically find an available port (starting from 5000)"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
