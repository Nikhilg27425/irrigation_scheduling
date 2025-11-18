# 📁 Project Structure

## File Organization

```
irrigation_scheduling/
│
├── 📄 app.py                      # Main Flask application with all routes
├── 📄 model.py                    # ML model class and training logic
├── 📄 create_demo_user.py         # Script to create demo user
├── 📄 setup_and_run.sh            # Automated setup script
│
├── 📁 templates/                  # HTML templates
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── dashboard.html             # Main dashboard
│   ├── weather.html               # Weather information page
│   ├── irrigation.html            # AI prediction page
│   ├── api_management.html        # API settings page
│   ├── profile.html               # User profile page
│   ├── navbar.html                # Reusable navigation bar
│   └── index.html                 # Old single-page (kept for reference)
│
├── 📁 static/                     # Static assets
│   ├── css/
│   │   └── style.css              # Custom styles
│   ├── js/
│   │   ├── app.js                 # Old JavaScript (kept for reference)
│   │   └── irrigation.js          # Irrigation page JavaScript
│   └── images/
│       └── .gitkeep
│
├── 📁 Database/
│   └── farmers.db                 # SQLite database (created on first run)
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 README_NEW_UI.md            # Setup and usage guide
├── 📄 FEATURES.md                 # Complete feature documentation
└── 📄 PROJECT_STRUCTURE.md        # This file
```

## Page Flow Diagram

```
┌─────────────┐
│   Login     │ ◄─── First entry point
│   /login    │
└──────┬──────┘
       │
       ├─────► Register (/register) ─── New users
       │
       ▼
┌─────────────────────────────────────────────────┐
│              Dashboard (/dashboard)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Weather  │  │ Humidity │  │Farm Size │      │
│  │  Stats   │  │  Stats   │  │  Stats   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │     Weather Overview & Forecast        │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │      Recent Predictions History        │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
       │
       ├─────► Weather (/weather)
       │       ├── Current conditions
       │       ├── 5-day forecast
       │       └── Irrigation recommendations
       │
       ├─────► Irrigation Model (/irrigation)
       │       ├── Input form
       │       ├── AI prediction
       │       └── Results display
       │
       ├─────► API Management (/api-management)
       │       ├── Weather API status
       │       ├── Sensor connections
       │       └── Usage statistics
       │
       └─────► Profile (/profile)
               ├── User information
               ├── Farm details
               └── Edit settings
```

## Navigation Structure

```
┌────────────────────────────────────────────────────────┐
│  🌱 Smart Irrigation  [Dashboard] [Weather] [Model]   │
│                       [API] [Profile ▼] [Logout]       │
└────────────────────────────────────────────────────────┘
```

## Database Schema

```
┌─────────────────────────────────────┐
│            Users Table               │
├─────────────────────────────────────┤
│ id (PK)          INTEGER             │
│ username         VARCHAR(80) UNIQUE  │
│ email            VARCHAR(120) UNIQUE │
│ password_hash    VARCHAR(200)        │
│ farm_name        VARCHAR(100)        │
│ location         VARCHAR(100)        │
│ farm_size        FLOAT               │
│ created_at       DATETIME            │
└─────────────────────────────────────┘
                  │
                  │ 1:N
                  ▼
┌─────────────────────────────────────┐
│         Predictions Table            │
├─────────────────────────────────────┤
│ id (PK)          INTEGER             │
│ user_id (FK)     INTEGER             │
│ crop_type        VARCHAR(50)         │
│ crop_days        FLOAT               │
│ soil_moisture    FLOAT               │
│ temperature      FLOAT               │
│ humidity         FLOAT               │
│ prediction       INTEGER (0 or 1)    │
│ confidence       FLOAT               │
│ created_at       DATETIME            │
└─────────────────────────────────────┘
```

## API Endpoints Map

```
Authentication Endpoints:
├── POST   /login              → Authenticate user
├── POST   /register           → Create new account
└── GET    /logout             → End session

Page Endpoints:
├── GET    /                   → Redirect to dashboard
├── GET    /dashboard          → Main dashboard
├── GET    /weather            → Weather page
├── GET    /irrigation         → Irrigation model page
├── GET    /api-management     → API settings page
└── GET    /profile            → User profile page

API Endpoints:
├── POST   /api/predict        → Make irrigation prediction
├── GET    /api/crop_types     → Get available crops
├── GET    /api/weather        → Get weather data
├── GET    /api/predictions/history → Get user's predictions
└── POST   /api/profile/update → Update user profile
```

## Component Breakdown

### 1. Authentication Components
- **Login Form**: Username/password input
- **Register Form**: Multi-field registration
- **Session Manager**: Flask-Login integration

### 2. Dashboard Components
- **Stat Cards**: 4 overview cards
- **Weather Widget**: Current conditions
- **Forecast Strip**: 5-day preview
- **Recent Predictions**: Last 5 predictions
- **Quick Actions**: Navigation buttons

### 3. Weather Components
- **Current Weather Card**: Large display
- **Forecast List**: Detailed 5-day
- **Weather Alerts**: Warning system
- **Recommendations**: Irrigation advice

### 4. Irrigation Components
- **Input Form**: 5 parameter fields
- **Prediction Display**: Result card
- **Confidence Bar**: Visual indicator
- **History**: Saved predictions

### 5. API Management Components
- **API Cards**: Service status
- **Connection Tests**: Verify APIs
- **Statistics**: Usage metrics

### 6. Profile Components
- **User Info**: Display card
- **Edit Form**: Update fields
- **Save Button**: Submit changes

## Technology Stack Layers

```
┌─────────────────────────────────────┐
│         Frontend Layer               │
│  Bootstrap 5 + Font Awesome + JS    │
└─────────────────────────────────────┘
                  ▲
                  │
┌─────────────────────────────────────┐
│        Application Layer             │
│  Flask + Flask-Login + Jinja2       │
└─────────────────────────────────────┘
                  ▲
                  │
┌─────────────────────────────────────┐
│         Database Layer               │
│  Flask-SQLAlchemy + SQLite          │
└─────────────────────────────────────┘
                  ▲
                  │
┌─────────────────────────────────────┐
│          ML Model Layer              │
│  Scikit-learn + Joblib              │
└─────────────────────────────────────┘
```

## Key Files Explained

### app.py (Main Application)
- Flask app initialization
- Database models (User, Prediction)
- All route handlers
- Authentication logic
- API endpoints
- Weather data integration

### templates/*.html
- **login.html**: Split-screen login design
- **register.html**: Multi-field registration
- **dashboard.html**: Main overview with stats
- **weather.html**: Detailed weather display
- **irrigation.html**: AI prediction interface
- **api_management.html**: API configuration
- **profile.html**: User settings
- **navbar.html**: Reusable navigation

### static/css/style.css
- Custom styling
- Responsive design rules
- Animation definitions
- Color schemes
- Card styles

### static/js/irrigation.js
- Form handling
- API calls
- Result display
- Error handling

## Setup Flow

```
1. Run setup_and_run.sh
   ↓
2. Create virtual environment
   ↓
3. Install dependencies
   ↓
4. Initialize database
   ↓
5. Create demo user
   ↓
6. Start Flask server
   ↓
7. Open browser → localhost:5000
   ↓
8. Login with demo credentials
   ↓
9. Explore all pages!
```
