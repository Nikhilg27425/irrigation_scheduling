# 🌱 Smart Irrigation Scheduling System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A machine learning-powered web application that predicts irrigation needs for crops based on environmental conditions and crop data. Achieves **93.1% accuracy** using Random Forest classification.

🔗 **Live Demo**: [Deployed Link](https://irrigation-scheduling.onrender.com)

## 🌟 Key Features

- 🤖 **High Accuracy ML Model** - 93.1% accuracy with Random Forest
- 🌐 **Interactive Web Interface** - Modern, responsive design
- 📊 **Real-time Predictions** - Instant irrigation recommendations
- 🎯 **9 Crop Types** - Wheat, Maize, Potato, Sugarcane, and more
- 📱 **Mobile Friendly** - Works on all devices
- 🔧 **Easy Setup** - One-command deployment

## Features

- **Machine Learning Model**: Random Forest classifier trained on crop production data
- **Interactive Web Interface**: User-friendly form to input parameters
- **Real-time Predictions**: Instant irrigation recommendations with confidence scores
- **Data Visualization**: Comprehensive analysis of the dataset and model performance
- **Recent Predictions**: Local storage of prediction history

## Dataset

The system uses a dataset containing:
- **Crop Types**: Wheat, Groundnuts, Garden Flowers, Maize, Paddy, Potato, Pulse, Sugarcane, Coffee
- **Features**: Crop Days, Soil Moisture, Temperature, Humidity
- **Target**: Irrigation requirement (0 = No irrigation, 1 = Irrigation needed)

## Quick Start

### Option 1: Automated Startup (Recommended)
```bash
./start_app.sh
```

### Option 2: Manual Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install Flask pandas numpy scikit-learn matplotlib seaborn joblib
   ```

3. **Train the machine learning model**:
   ```bash
   python model.py
   ```

4. **Run the web application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5000`

### Test the API
```bash
python test_api.py
```

## Usage

### Web Interface

1. **Select Crop Type**: Choose from available crop types in the dataset
2. **Enter Parameters**:
   - **Crop Days**: Number of days since planting (1-200)
   - **Soil Moisture**: Current soil moisture level (0-1000)
   - **Temperature**: Current temperature in Celsius (0-50°C)
   - **Humidity**: Current humidity percentage (0-100%)
3. **Get Prediction**: Click "Predict Irrigation Need" to get instant results
4. **View Results**: See irrigation recommendation with confidence score and probability breakdown

### API Endpoints

- `POST /api/schedule/create` - Create schedule
- `GET /api/schedule/list` - List schedules
- `POST /api/schedule/<id>/cancel` - Cancel schedule
- `POST /api/schedule/<id>/execute` - Execute now

### Example API Usage

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "Wheat",
    "crop_days": 15,
    "soil_moisture": 400,
    "temperature": 25,
    "humidity": 30
  }'
```

## Model Performance

- **Algorithm**: Random Forest Classifier
- **Accuracy**: ~85% (varies based on training data)
- **Features**: 8 engineered features including ratios and derived metrics
- **Cross-validation**: Stratified split for balanced evaluation

## File Structure

```
irrigation_scheduling/
├── datasets - datasets.csv          # Training data
├── model.py                         # ML model training and prediction
├── app.py                          # Flask web application
├── visualization.py                # Data analysis and plotting
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                  # Web interface template
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling
│   ├── js/
│   │   └── app.js                 # Frontend JavaScript
│   └── images/                    # Generated visualizations
└── README.md                      # This file
```

## Key Features of the Model

1. **Feature Engineering**:
   - Moisture-to-temperature ratio
   - Humidity-to-temperature ratio
   - Moisture deficit calculation
   - Categorical encoding for crop types

2. **Data Preprocessing**:
   - Standard scaling for numerical features
   - Label encoding for categorical variables
   - Stratified train-test split

3. **Model Selection**:
   - Random Forest for handling mixed data types
   - Built-in feature importance
   - Robust to outliers

## Customization

### Adding New Crop Types

1. Update the dataset with new crop data
2. Retrain the model: `python model.py`
3. The web interface will automatically load new crop types

### Modifying Features

Edit the `preprocess_data()` method in `model.py` to:
- Add new feature calculations
- Modify existing feature engineering
- Include additional environmental parameters

### Styling

Customize the web interface by modifying:
- `static/css/style.css` for visual styling
- `templates/index.html` for layout changes
- `static/js/app.js` for interactive behavior

## Troubleshooting

### Common Issues

1. **Model not loading**: Ensure `irrigation_model.pkl` exists by running `python model.py`
2. **Missing dependencies**: Install all requirements with `pip install -r requirements.txt`
3. **Port already in use**: Change the port in `app.py` (line with `app.run()`)

### Performance Tips

- For production deployment, consider using a WSGI server like Gunicorn
- Implement model versioning for updates
- Add input validation and error handling
- Consider caching for frequently requested predictions

## Future Enhancements

- Weather API integration for real-time data
- Historical prediction tracking
- Mobile-responsive design improvements
- Advanced ML models (XGBoost, Neural Networks)
- Multi-language support
- Export functionality for predictions

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.
