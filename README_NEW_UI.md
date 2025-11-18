# Smart Irrigation System - Multi-Page UI with Login

## 🌟 Features

### 1. **Authentication System**
- User registration and login
- Secure password hashing
- Session management

### 2. **Dashboard**
- Real-time weather overview
- Quick stats (temperature, humidity, farm size, predictions)
- Recent predictions history
- 5-day weather forecast
- Quick action buttons

### 3. **Weather Page**
- Detailed current weather information
- 5-day forecast with detailed metrics
- Weather alerts
- Irrigation recommendations based on weather

### 4. **Irrigation Model Page**
- AI-powered irrigation predictions
- Input parameters for crops
- Real-time prediction results
- Confidence scores

### 5. **API Management Page**
- Weather API integration status
- Soil sensor API configuration
- API usage statistics
- Connection testing

### 6. **Profile Page**
- User account information
- Farm details management
- Update location and farm size

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
./setup_and_run.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create demo user
python create_demo_user.py

# Run the application
python app.py
```

## 🔐 Demo Login Credentials

**Username:** farmer  
**Password:** farmer123

## 📱 Pages Overview

1. **Login** (`/login`) - User authentication
2. **Register** (`/register`) - New user registration
3. **Dashboard** (`/dashboard`) - Main overview page
4. **Weather** (`/weather`) - Detailed weather information
5. **Irrigation Model** (`/irrigation`) - AI prediction tool
6. **API Management** (`/api-management`) - API integrations
7. **Profile** (`/profile`) - User settings

## 🎨 UI Features

- **Responsive Design** - Works on desktop, tablet, and mobile
- **Modern Interface** - Clean, professional design with Bootstrap 5
- **Interactive Elements** - Real-time updates and animations
- **Color-Coded Results** - Easy-to-understand visual feedback
- **Navigation Bar** - Easy access to all pages
- **User Dropdown** - Quick access to profile and logout

## 🔧 Technology Stack

- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy
- **Frontend:** Bootstrap 5, Font Awesome, JavaScript
- **Database:** SQLite
- **ML Model:** Scikit-learn (Random Forest)

## 📊 Database Schema

### Users Table
- id, username, email, password_hash
- farm_name, location, farm_size
- created_at

### Predictions Table
- id, user_id, crop_type, crop_days
- soil_moisture, temperature, humidity
- prediction, confidence, created_at

## 🌐 API Endpoints

- `POST /login` - User login
- `POST /register` - User registration
- `GET /dashboard` - Dashboard page
- `GET /weather` - Weather page
- `GET /irrigation` - Irrigation model page
- `POST /api/predict` - Make irrigation prediction
- `GET /api/crop_types` - Get available crop types
- `GET /api/weather` - Get weather data
- `GET /api/predictions/history` - Get prediction history
- `POST /api/profile/update` - Update user profile

## 🎯 Next Steps

1. Add real weather API integration (OpenWeatherMap)
2. Connect IoT soil sensors
3. Add data visualization charts
4. Implement email notifications
5. Add crop management features
6. Create mobile app version

## 📝 Notes

- The weather data is currently mocked for demo purposes
- To use real weather data, sign up for OpenWeatherMap API and set the `OPENWEATHER_API_KEY` environment variable
- The model file (`irrigation_model.pkl`) must exist in the root directory
