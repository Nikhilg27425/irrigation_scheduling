#!/usr/bin/env python3
"""
Test script for the Smart Irrigation Scheduling API
"""

import requests
import json
import time

def test_api():
    """Test the irrigation prediction API"""
    
    base_url = "http://localhost:5000"
    
    print("🌱 Testing Smart Irrigation Scheduling API")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/crop_types", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            crop_types = response.json()['crop_types']
            print(f"📊 Available crop types: {', '.join(crop_types)}")
        else:
            print(f"❌ Server error: {response.status_code}")
            return
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Make sure the Flask app is running with: python app.py")
        return
    
    print("\n" + "=" * 50)
    print("🧪 Testing Irrigation Predictions")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Wheat - Low Moisture",
            "data": {
                "crop_type": "Wheat",
                "crop_days": 15,
                "soil_moisture": 200,
                "temperature": 30,
                "humidity": 25
            }
        },
        {
            "name": "Maize - High Moisture",
            "data": {
                "crop_type": "Maize",
                "crop_days": 20,
                "soil_moisture": 700,
                "temperature": 25,
                "humidity": 60
            }
        },
        {
            "name": "Potato - Moderate Conditions",
            "data": {
                "crop_type": "Potato",
                "crop_days": 30,
                "soil_moisture": 400,
                "temperature": 20,
                "humidity": 70
            }
        }
    ]
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                f"{base_url}/predict",
                headers={'Content-Type': 'application/json'},
                json=test_case['data'],
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Prediction: {result['prediction_text']}")
                print(f"📈 Confidence: {result['confidence']:.1%}")
                print(f"📊 Probabilities:")
                print(f"   - No Irrigation: {result['probabilities']['no_irrigation']:.1%}")
                print(f"   - Irrigation Needed: {result['probabilities']['irrigation_needed']:.1%}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary")
    print("=" * 50)
    print("✅ API tests completed!")
    print("🌐 Web interface available at: http://localhost:5000")
    print("📚 Check the README.md for detailed usage instructions")

if __name__ == "__main__":
    test_api()
