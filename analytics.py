"""
Analytics module - Generate interactive visualizations using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

def generate_user_analytics(predictions):
    """
    Generate analytics for a specific user's predictions
    """
    if not predictions or len(predictions) == 0:
        return None
    
    # Convert to DataFrame
    data = []
    for p in predictions:
        data.append({
            'date': p.created_at,
            'crop_type': p.crop_type,
            'soil_moisture': p.soil_moisture,
            'temperature': p.temperature,
            'humidity': p.humidity,
            'prediction': p.prediction,
            'confidence': p.confidence
        })
    
    df = pd.DataFrame(data)
    
    charts = {}
    
    # 1. Prediction Timeline
    df['date_only'] = df['date'].dt.date
    timeline = df.groupby(['date_only', 'prediction']).size().reset_index(name='count')
    
    fig_timeline = go.Figure()
    for pred_val in [0, 1]:
        subset = timeline[timeline['prediction'] == pred_val]
        fig_timeline.add_trace(go.Scatter(
            x=subset['date_only'],
            y=subset['count'],
            mode='lines+markers',
            name='Irrigation Needed' if pred_val == 1 else 'No Irrigation',
            line=dict(color='#ff6b6b' if pred_val == 1 else '#74b9ff', width=3),
            marker=dict(size=8)
        ))
    
    fig_timeline.update_layout(
        title='Prediction Timeline',
        xaxis_title='Date',
        yaxis_title='Number of Predictions',
        hovermode='x unified',
        template='plotly_white'
    )
    charts['timeline'] = fig_timeline.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 2. Irrigation Rate by Crop
    crop_irrigation = df.groupby('crop_type')['prediction'].agg(['sum', 'count'])
    crop_irrigation['rate'] = (crop_irrigation['sum'] / crop_irrigation['count'] * 100).round(1)
    
    fig_crop = go.Figure(data=[
        go.Bar(
            x=crop_irrigation.index,
            y=crop_irrigation['rate'],
            marker_color='#00b894',
            text=crop_irrigation['rate'].apply(lambda x: f'{x}%'),
            textposition='outside'
        )
    ])
    fig_crop.update_layout(
        title='Irrigation Rate by Crop Type',
        xaxis_title='Crop Type',
        yaxis_title='Irrigation Rate (%)',
        template='plotly_white'
    )
    charts['crop_rate'] = fig_crop.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 3. Soil Moisture Distribution
    fig_moisture = go.Figure()
    fig_moisture.add_trace(go.Histogram(
        x=df[df['prediction'] == 0]['soil_moisture'],
        name='No Irrigation',
        marker_color='#74b9ff',
        opacity=0.7,
        nbinsx=30
    ))
    fig_moisture.add_trace(go.Histogram(
        x=df[df['prediction'] == 1]['soil_moisture'],
        name='Irrigation Needed',
        marker_color='#ff6b6b',
        opacity=0.7,
        nbinsx=30
    ))
    fig_moisture.update_layout(
        title='Soil Moisture Distribution',
        xaxis_title='Soil Moisture',
        yaxis_title='Frequency',
        barmode='overlay',
        template='plotly_white'
    )
    charts['moisture'] = fig_moisture.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 4. Temperature vs Humidity Scatter
    fig_scatter = px.scatter(
        df,
        x='temperature',
        y='humidity',
        color='prediction',
        color_discrete_map={0: '#74b9ff', 1: '#ff6b6b'},
        labels={'prediction': 'Irrigation', 'temperature': 'Temperature (°C)', 'humidity': 'Humidity (%)'},
        title='Temperature vs Humidity',
        hover_data=['crop_type', 'soil_moisture']
    )
    fig_scatter.update_layout(template='plotly_white')
    charts['scatter'] = fig_scatter.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 5. Confidence Distribution
    fig_confidence = go.Figure(data=[
        go.Box(
            y=df[df['prediction'] == 0]['confidence'],
            name='No Irrigation',
            marker_color='#74b9ff'
        ),
        go.Box(
            y=df[df['prediction'] == 1]['confidence'],
            name='Irrigation Needed',
            marker_color='#ff6b6b'
        )
    ])
    fig_confidence.update_layout(
        title='Prediction Confidence Distribution',
        yaxis_title='Confidence',
        template='plotly_white'
    )
    charts['confidence'] = fig_confidence.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 6. Weekly Summary
    df['week'] = df['date'].dt.to_period('W').astype(str)
    weekly = df.groupby(['week', 'prediction']).size().unstack(fill_value=0)
    
    fig_weekly = go.Figure()
    if 0 in weekly.columns:
        fig_weekly.add_trace(go.Bar(
            x=weekly.index,
            y=weekly[0],
            name='No Irrigation',
            marker_color='#74b9ff'
        ))
    if 1 in weekly.columns:
        fig_weekly.add_trace(go.Bar(
            x=weekly.index,
            y=weekly[1],
            name='Irrigation Needed',
            marker_color='#ff6b6b'
        ))
    
    fig_weekly.update_layout(
        title='Weekly Prediction Summary',
        xaxis_title='Week',
        yaxis_title='Number of Predictions',
        barmode='stack',
        template='plotly_white'
    )
    charts['weekly'] = fig_weekly.to_html(full_html=False, include_plotlyjs='cdn')
    
    return charts

def generate_system_analytics(all_predictions):
    """
    Generate system-wide analytics (for admin)
    """
    if not all_predictions or len(all_predictions) == 0:
        return None
    
    data = []
    for p in all_predictions:
        data.append({
            'date': p.created_at,
            'user': p.user.username,
            'crop_type': p.crop_type,
            'prediction': p.prediction,
            'confidence': p.confidence
        })
    
    df = pd.DataFrame(data)
    
    charts = {}
    
    # 1. System-wide prediction distribution
    pred_counts = df['prediction'].value_counts()
    fig_pie = go.Figure(data=[go.Pie(
        labels=['No Irrigation', 'Irrigation Needed'],
        values=[pred_counts.get(0, 0), pred_counts.get(1, 0)],
        marker_colors=['#74b9ff', '#ff6b6b'],
        hole=0.4
    )])
    fig_pie.update_layout(
        title='Overall Irrigation Distribution',
        template='plotly_white'
    )
    charts['distribution'] = fig_pie.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 2. Top users by predictions
    user_counts = df['user'].value_counts().head(10)
    fig_users = go.Figure(data=[
        go.Bar(
            x=user_counts.values,
            y=user_counts.index,
            orientation='h',
            marker_color='#00b894'
        )
    ])
    fig_users.update_layout(
        title='Top 10 Active Users',
        xaxis_title='Number of Predictions',
        yaxis_title='User',
        template='plotly_white'
    )
    charts['top_users'] = fig_users.to_html(full_html=False, include_plotlyjs='cdn')
    
    # 3. Crop popularity
    crop_counts = df['crop_type'].value_counts()
    fig_crops = go.Figure(data=[go.Pie(
        labels=crop_counts.index,
        values=crop_counts.values,
        hole=0.3
    )])
    fig_crops.update_layout(
        title='Crop Type Distribution',
        template='plotly_white'
    )
    charts['crops'] = fig_crops.to_html(full_html=False, include_plotlyjs='cdn')
    
    return charts

def calculate_stats(predictions):
    """Calculate summary statistics"""
    if not predictions or len(predictions) == 0:
        return {
            'total': 0,
            'irrigation_needed': 0,
            'no_irrigation': 0,
            'avg_confidence': 0,
            'most_common_crop': 'N/A'
        }
    
    total = len(predictions)
    irrigation_needed = sum(1 for p in predictions if p.prediction == 1)
    no_irrigation = total - irrigation_needed
    avg_confidence = sum(p.confidence for p in predictions) / total * 100
    
    crop_counts = {}
    for p in predictions:
        crop_counts[p.crop_type] = crop_counts.get(p.crop_type, 0) + 1
    
    most_common_crop = max(crop_counts.items(), key=lambda x: x[1])[0] if crop_counts else 'N/A'
    
    return {
        'total': total,
        'irrigation_needed': irrigation_needed,
        'no_irrigation': no_irrigation,
        'avg_confidence': round(avg_confidence, 1),
        'most_common_crop': most_common_crop
    }
