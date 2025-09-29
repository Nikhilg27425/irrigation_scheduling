import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

class IrrigationPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def load_data(self, file_path):
        """Load and preprocess the dataset"""
        self.data = pd.read_csv(file_path)
        print(f"Dataset loaded: {self.data.shape}")
        print(f"Columns: {self.data.columns.tolist()}")
        print(f"Target distribution:\n{self.data['Irrigation'].value_counts()}")
        return self.data
    
    def preprocess_data(self):
        """Preprocess the data for training"""
        # Encode categorical variables
        self.data['CropType_encoded'] = self.label_encoder.fit_transform(self.data['CropType'])
        
        # Feature engineering
        self.data['moisture_temp_ratio'] = self.data['SoilMoisture'] / (self.data['temperature'] + 1)
        self.data['humidity_temp_ratio'] = self.data['Humidity'] / (self.data['temperature'] + 1)
        self.data['moisture_deficit'] = 1000 - self.data['SoilMoisture']  # Assuming 1000 as max moisture
        
        # Select features for training
        feature_columns = ['CropDays', 'SoilMoisture', 'temperature', 'Humidity', 
                          'CropType_encoded', 'moisture_temp_ratio', 'humidity_temp_ratio', 'moisture_deficit']
        
        self.X = self.data[feature_columns]
        self.y = self.data['Irrigation']
        
        print(f"Features selected: {feature_columns}")
        print(f"Feature matrix shape: {self.X.shape}")
        
        return self.X, self.y
    
    def train_model(self):
        """Train the irrigation prediction model"""
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Evaluate model
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.3f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Feature importance
        feature_names = self.X.columns
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(importance_df)
        
        self.is_trained = True
        self.feature_names = feature_names
        
        return accuracy, importance_df
    
    def predict(self, crop_type, crop_days, soil_moisture, temperature, humidity):
        """Make prediction for new data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Encode crop type
        crop_type_encoded = self.label_encoder.transform([crop_type])[0]
        
        # Calculate derived features
        moisture_temp_ratio = soil_moisture / (temperature + 1)
        humidity_temp_ratio = humidity / (temperature + 1)
        moisture_deficit = 1000 - soil_moisture
        
        # Create feature vector
        features = np.array([[
            crop_days, soil_moisture, temperature, humidity, crop_type_encoded,
            moisture_temp_ratio, humidity_temp_ratio, moisture_deficit
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        return prediction, probability
    
    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = True
        print(f"Model loaded from {filepath}")

def main():
    """Main function to train the model"""
    predictor = IrrigationPredictor()
    
    # Load and preprocess data
    data = predictor.load_data('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/datasets - datasets.csv')
    X, y = predictor.preprocess_data()
    
    # Train model
    accuracy, importance = predictor.train_model()
    
    # Save model
    predictor.save_model('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/irrigation_model.pkl')
    
    # Test prediction
    print("\nTesting prediction:")
    test_pred, test_prob = predictor.predict('Wheat', 15, 400, 25, 30)
    print(f"Prediction: {test_pred}")
    print(f"Probability: {test_prob}")
    
    return predictor

if __name__ == "__main__":
    predictor = main()
