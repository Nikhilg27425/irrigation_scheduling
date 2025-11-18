# 🚀 Quick Start Guide

## Get Started in 3 Steps!

### Step 1: Run Setup Script
```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```

### Step 2: Open Browser
Navigate to: `http://localhost:5000`

### Step 3: Login
```
Username: farmer
Password: farmer123
```

That's it! You're ready to explore! 🎉

---

## What You'll See

### 1️⃣ Login Page
- Beautiful split-screen design
- Green gradient background
- Easy login form

### 2️⃣ Dashboard (After Login)
- **4 Stat Cards**: Temperature, Humidity, Farm Size, Predictions
- **Weather Overview**: Current conditions + 5-day forecast
- **Recent Predictions**: Your last 5 AI predictions
- **Quick Actions**: Navigate to other pages

### 3️⃣ Weather Page
- **Current Weather**: Large display with all metrics
- **5-Day Forecast**: Detailed day-by-day breakdown
- **Weather Alerts**: Important notifications
- **Recommendations**: When to irrigate based on weather

### 4️⃣ Irrigation Model Page
- **Input Form**: Enter crop and environmental data
  - Crop Type (dropdown)
  - Crop Days (1-200)
  - Soil Moisture (0-1000)
  - Temperature (°C)
  - Humidity (%)
- **AI Prediction**: Get instant recommendation
- **Results**: Color-coded with confidence score

### 5️⃣ API Management Page
- **Weather API**: Connection status
- **Soil Sensors**: IoT integration
- **Statistics**: Usage metrics

### 6️⃣ Profile Page
- **User Info**: Your account details
- **Farm Details**: Edit farm name, location, size
- **Save Changes**: Update your information

---

## Try These Actions

### Make Your First Prediction
1. Click **"Irrigation Model"** in navigation
2. Select a crop type (e.g., "Wheat")
3. Enter values:
   - Crop Days: 30
   - Soil Moisture: 400
   - Temperature: 28
   - Humidity: 65
4. Click **"Predict Irrigation Need"**
5. See your AI-powered recommendation!

### Check the Weather
1. Click **"Weather"** in navigation
2. View current conditions
3. Scroll down for 5-day forecast
4. Read irrigation recommendations

### Update Your Profile
1. Click your username in top-right
2. Select **"Profile"**
3. Edit farm information
4. Click **"Save Changes"**

---

## Navigation Guide

### Top Navigation Bar
```
🌱 Smart Irrigation | Dashboard | Weather | Irrigation Model | API Management | [Your Name ▼]
                                                                                    ├─ Profile
                                                                                    └─ Logout
```

### Quick Tips
- **Dashboard**: Your home base - see everything at a glance
- **Weather**: Check before making irrigation decisions
- **Irrigation Model**: Use AI to optimize water usage
- **API Management**: Configure external data sources
- **Profile**: Keep your farm info up to date

---

## Understanding Results

### Irrigation Prediction Results

#### 🔴 Irrigation Needed
- **Red card** with water drop icon
- Means: Your crops need water now
- Action: Schedule irrigation soon

#### 🔵 No Irrigation Needed
- **Blue card** with ban icon
- Means: Soil moisture is sufficient
- Action: Wait and monitor

### Confidence Scores
- **Green bar (>80%)**: High confidence - trust this result
- **Yellow bar (60-80%)**: Medium confidence - consider other factors
- **Red bar (<60%)**: Low confidence - verify with manual check

---

## Common Tasks

### Task 1: Daily Weather Check
```
1. Login
2. Dashboard → View weather widget
3. Or click "Weather" for details
```

### Task 2: Make Irrigation Decision
```
1. Go to "Irrigation Model"
2. Fill in current conditions
3. Get AI recommendation
4. Check weather forecast
5. Make informed decision
```

### Task 3: Review History
```
1. Dashboard → "Recent Predictions" section
2. See your last 5 predictions
3. Track patterns over time
```

### Task 4: Update Farm Info
```
1. Profile → Edit fields
2. Save changes
3. Info updates across all pages
```

---

## Troubleshooting

### Can't Login?
- Check username: `farmer`
- Check password: `farmer123`
- Make sure you ran `create_demo_user.py`

### Model Not Loading?
- Ensure `irrigation_model.pkl` exists
- Run model training script if needed
- Check console for error messages

### Page Not Loading?
- Verify Flask server is running
- Check port 5000 is not in use
- Look for errors in terminal

### Database Error?
- Delete `farmers.db` file
- Run `create_demo_user.py` again
- Restart application

---

## Next Steps

### For Farmers
1. ✅ Create your own account (Register)
2. ✅ Enter your real farm details
3. ✅ Start making predictions
4. ✅ Track your irrigation history
5. ✅ Optimize water usage

### For Developers
1. ✅ Explore the code in `app.py`
2. ✅ Customize templates in `templates/`
3. ✅ Add new features
4. ✅ Integrate real weather APIs
5. ✅ Connect IoT sensors

---

## Support

### Need Help?
- Read `FEATURES.md` for detailed feature info
- Check `PROJECT_STRUCTURE.md` for code organization
- Review `README_NEW_UI.md` for technical details

### Want to Contribute?
- Add new crop types
- Improve ML model
- Add data visualizations
- Create mobile app
- Translate to other languages

---

## Demo Credentials

**Username:** farmer  
**Password:** farmer123

**Farm Details:**
- Farm Name: Green Valley Farm
- Location: Punjab, India
- Farm Size: 25.5 acres

---

Enjoy your Smart Irrigation System! 🌾💧
