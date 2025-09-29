# 🚀 Deployment Guide

## Local Development

### Quick Start
```bash
git clone https://github.com/Nikhilg27425/irrigation_scheduling.git
cd irrigation_scheduling
./start_app.sh
```

### Manual Setup
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install Flask pandas numpy scikit-learn matplotlib seaborn joblib
python model.py
python app.py
```

## Cloud Deployment Options

### 1. Heroku Deployment

1. **Install Heroku CLI** and login
2. **Create Procfile**:
   ```
   web: python app.py
   ```
3. **Create runtime.txt**:
   ```
   python-3.9.18
   ```
4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   heroku create your-app-name
   git push heroku main
   ```

### 2. Railway Deployment

1. **Connect GitHub repository** to Railway
2. **Set environment variables**:
   - `PORT`: Railway will set this automatically
3. **Deploy**: Railway will auto-deploy on git push

### 3. Render Deployment

1. **Create new Web Service** on Render
2. **Connect GitHub repository**
3. **Build Command**: `pip install -r requirements.txt && python model.py`
4. **Start Command**: `python app.py`
5. **Environment**: Python 3

### 4. Google Cloud Platform

1. **Create App Engine app**:
   ```yaml
   # app.yaml
   runtime: python39
   
   handlers:
   - url: /.*
     script: auto
   ```
2. **Deploy**:
   ```bash
   gcloud app deploy
   ```

### 5. AWS Elastic Beanstalk

1. **Install EB CLI**
2. **Initialize**:
   ```bash
   eb init
   eb create production
   ```
3. **Deploy**:
   ```bash
   eb deploy
   ```

## Docker Deployment

### Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python model.py

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build and Run
```bash
docker build -t irrigation-scheduler .
docker run -p 5000:5000 irrigation-scheduler
```

## Environment Variables

For production deployment, consider setting these environment variables:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
```

## Performance Optimization

### For Production:
1. **Use WSGI Server** (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Enable Caching**:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

3. **Database Integration** (Optional):
   - Store prediction history in database
   - User management system
   - Analytics and reporting

## Monitoring and Logging

### Add Logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Health Check Endpoint:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'model_loaded': predictor is not None}
```

## Security Considerations

1. **Input Validation**: Already implemented
2. **Rate Limiting**: Add Flask-Limiter
3. **HTTPS**: Use SSL certificates
4. **Environment Variables**: Don't commit secrets
5. **CORS**: Configure if needed for frontend

## Scaling Considerations

- **Load Balancing**: Multiple app instances
- **Caching**: Redis for model caching
- **Database**: PostgreSQL for data persistence
- **CDN**: Static file delivery
- **Monitoring**: Application performance monitoring

## Backup and Recovery

1. **Model Backup**: Version control for trained models
2. **Data Backup**: Regular dataset backups
3. **Configuration Backup**: Environment variables
4. **Disaster Recovery**: Multi-region deployment

## Cost Optimization

- **Serverless**: Use AWS Lambda or Google Cloud Functions
- **Auto-scaling**: Scale based on demand
- **Caching**: Reduce computation costs
- **Resource Monitoring**: Track usage and costs

## Troubleshooting

### Common Issues:
1. **Port Conflicts**: Use dynamic port detection (already implemented)
2. **Model Loading**: Ensure model file exists
3. **Memory Issues**: Optimize for cloud memory limits
4. **Dependencies**: Use exact version pinning

### Debug Mode:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Support

For deployment issues:
- Check application logs
- Verify environment variables
- Test locally first
- Check cloud provider documentation

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - see LICENSE file for details.
