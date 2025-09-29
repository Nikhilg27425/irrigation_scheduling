import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

class DataVisualizer:
    def __init__(self, data):
        self.data = data
        
    def plot_data_distribution(self):
        """Create visualizations for data distribution and insights"""
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Smart Irrigation Dataset Analysis', fontsize=16, fontweight='bold')
        
        # 1. Crop Type Distribution
        crop_counts = self.data['CropType'].value_counts()
        axes[0, 0].pie(crop_counts.values, labels=crop_counts.index, autopct='%1.1f%%', startangle=90)
        axes[0, 0].set_title('Distribution of Crop Types')
        
        # 2. Irrigation vs No Irrigation
        irrigation_counts = self.data['Irrigation'].value_counts()
        colors = ['#ff6b6b', '#74b9ff']
        labels = ['No Irrigation', 'Irrigation Needed']
        axes[0, 1].bar(labels, irrigation_counts.values, color=colors)
        axes[0, 1].set_title('Irrigation Requirements Distribution')
        axes[0, 1].set_ylabel('Count')
        
        # 3. Soil Moisture Distribution by Irrigation
        irrigation_data = self.data[self.data['Irrigation'] == 1]['SoilMoisture']
        no_irrigation_data = self.data[self.data['Irrigation'] == 0]['SoilMoisture']
        
        axes[0, 2].hist(no_irrigation_data, bins=30, alpha=0.7, label='No Irrigation', color='#74b9ff')
        axes[0, 2].hist(irrigation_data, bins=30, alpha=0.7, label='Irrigation Needed', color='#ff6b6b')
        axes[0, 2].set_title('Soil Moisture Distribution')
        axes[0, 2].set_xlabel('Soil Moisture')
        axes[0, 2].set_ylabel('Frequency')
        axes[0, 2].legend()
        
        # 4. Temperature vs Humidity Scatter Plot
        scatter = axes[1, 0].scatter(self.data['temperature'], self.data['Humidity'], 
                                   c=self.data['Irrigation'], cmap='RdYlBu', alpha=0.6)
        axes[1, 0].set_title('Temperature vs Humidity')
        axes[1, 0].set_xlabel('Temperature (°C)')
        axes[1, 0].set_ylabel('Humidity (%)')
        plt.colorbar(scatter, ax=axes[1, 0], label='Irrigation (0=No, 1=Yes)')
        
        # 5. Crop Days Distribution
        axes[1, 1].hist(self.data['CropDays'], bins=30, color='#00b894', alpha=0.7)
        axes[1, 1].set_title('Crop Days Distribution')
        axes[1, 1].set_xlabel('Days Since Planting')
        axes[1, 1].set_ylabel('Frequency')
        
        # 6. Correlation Heatmap
        numeric_cols = ['CropDays', 'SoilMoisture', 'temperature', 'Humidity', 'Irrigation']
        correlation_matrix = self.data[numeric_cols].corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, ax=axes[1, 2])
        axes[1, 2].set_title('Feature Correlation Matrix')
        
        plt.tight_layout()
        plt.savefig('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/static/images/data_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
    def plot_crop_specific_analysis(self):
        """Analyze irrigation patterns by crop type"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Crop-Specific Irrigation Analysis', fontsize=16, fontweight='bold')
        
        # 1. Irrigation rate by crop type
        crop_irrigation = self.data.groupby('CropType')['Irrigation'].mean().sort_values(ascending=False)
        axes[0, 0].bar(range(len(crop_irrigation)), crop_irrigation.values, color='#e17055')
        axes[0, 0].set_xticks(range(len(crop_irrigation)))
        axes[0, 0].set_xticklabels(crop_irrigation.index, rotation=45)
        axes[0, 0].set_title('Irrigation Rate by Crop Type')
        axes[0, 0].set_ylabel('Irrigation Rate')
        
        # 2. Average soil moisture by crop and irrigation status
        moisture_by_crop_irrigation = self.data.groupby(['CropType', 'Irrigation'])['SoilMoisture'].mean().unstack()
        moisture_by_crop_irrigation.plot(kind='bar', ax=axes[0, 1], color=['#74b9ff', '#ff6b6b'])
        axes[0, 1].set_title('Average Soil Moisture by Crop and Irrigation Status')
        axes[0, 1].set_ylabel('Average Soil Moisture')
        axes[0, 1].legend(['No Irrigation', 'Irrigation Needed'])
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Temperature distribution by irrigation status
        self.data.boxplot(column='temperature', by='Irrigation', ax=axes[1, 0])
        axes[1, 0].set_title('Temperature Distribution by Irrigation Status')
        axes[1, 0].set_xlabel('Irrigation (0=No, 1=Yes)')
        axes[1, 0].set_ylabel('Temperature (°C)')
        
        # 4. Humidity vs Soil Moisture colored by irrigation
        scatter = axes[1, 1].scatter(self.data['Humidity'], self.data['SoilMoisture'], 
                                   c=self.data['Irrigation'], cmap='RdYlBu', alpha=0.6)
        axes[1, 1].set_title('Humidity vs Soil Moisture')
        axes[1, 1].set_xlabel('Humidity (%)')
        axes[1, 1].set_ylabel('Soil Moisture')
        plt.colorbar(scatter, ax=axes[1, 1], label='Irrigation (0=No, 1=Yes)')
        
        plt.tight_layout()
        plt.savefig('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/static/images/crop_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
    def plot_model_performance(self, y_true, y_pred, feature_importance=None):
        """Plot model performance metrics"""
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Model Performance Analysis', fontsize=16, fontweight='bold')
        
        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Irrigation', 'Irrigation'], 
                   yticklabels=['No Irrigation', 'Irrigation'],
                   ax=axes[0])
        axes[0].set_title('Confusion Matrix')
        axes[0].set_xlabel('Predicted')
        axes[0].set_ylabel('Actual')
        
        # Feature Importance
        if feature_importance is not None:
            feature_importance.plot(kind='barh', ax=axes[1], color='#00b894')
            axes[1].set_title('Feature Importance')
            axes[1].set_xlabel('Importance')
        else:
            axes[1].text(0.5, 0.5, 'Feature importance not available', 
                        ha='center', va='center', transform=axes[1].transAxes)
            axes[1].set_title('Feature Importance')
        
        plt.tight_layout()
        plt.savefig('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/static/images/model_performance.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Generate all visualizations"""
    # Load data
    data = pd.read_csv('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/datasets - datasets.csv')
    
    # Create directory for images if it doesn't exist
    import os
    os.makedirs('/Users/nikhilgupta/Desktop/irrigtaion_scheduling/static/images', exist_ok=True)
    
    # Create visualizer and generate plots
    visualizer = DataVisualizer(data)
    
    print("Generating data distribution analysis...")
    visualizer.plot_data_distribution()
    
    print("Generating crop-specific analysis...")
    visualizer.plot_crop_specific_analysis()
    
    print("Visualizations saved to static/images/ directory")

if __name__ == "__main__":
    main()
