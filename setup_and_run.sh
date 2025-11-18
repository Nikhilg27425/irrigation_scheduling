#!/bin/bash

echo "🌱 Smart Irrigation System Setup"
echo "================================"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create demo user
echo "Creating demo user..."
python create_demo_user.py

# Run the application
echo ""
echo "✓ Setup complete!"
echo ""
echo "Starting application..."
echo "Login with: username=farmer, password=farmer123"
echo ""
python app.py
