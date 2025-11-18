# 🚀 Deployment Guide - Render

## Quick Deploy to Render

### Step 1: Prepare Your Repository
Your code is already on GitHub at: `https://github.com/Nikhilg27425/irrigation_scheduling`

### Step 2: Deploy on Render

1. **Go to Render**: https://render.com
2. **Sign up/Login** with your GitHub account
3. **Click "New +"** → Select **"Web Service"**
4. **Connect your repository**: `Nikhilg27425/irrigation_scheduling`
5. **Configure the service**:

   ```
   Name: smart-irrigation-system
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

6. **Add Environment Variable**:
   - Key: `SECRET_KEY`
   - Value: (Generate a random string or let Render auto-generate)

7. **Click "Create Web Service"**

### Step 3: Upload Model File

Since the `irrigation_model.pkl` file is in `.gitignore`, you need to upload it:

**Option A: Using Render Disk**
1. Go to your service dashboard
2. Navigate to "Disks" tab
3. Create a persistent disk
4. Upload `irrigation_model.pkl` to the disk

**Option B: Store in Cloud Storage**
1. Upload model to AWS S3, Google Cloud Storage, or similar
2. Modify `app.py` to download model on startup

**Option C: Include in Git (Not Recommended for large files)**
1. Remove `*.pkl` from `.gitignore`
2. Commit and push the model file

### Step 4: Wait for Deployment

Render will:
- Clone your repository
- Install dependencies
- Start the application
- Provide you with a URL like: `https://smart-irrigation-system.onrender.com`

### Step 5: Access Your App

Once deployed, visit your Render URL and login with:
- Username: `farmer`
- Password: `farmer123`

---

## Alternative: Deploy to Other Platforms

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku login
   heroku create smart-irrigation-app
   git push heroku main
   ```

### Railway

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Python and deploys

### PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Upload your code
3. Configure WSGI file
4. Set up virtual environment

---

## Important Notes

### Database
- SQLite works for development but consider PostgreSQL for production
- Render provides free PostgreSQL databases

### Model File
- The `irrigation_model.pkl` file (640KB) needs to be accessible
- Consider using cloud storage for production

### Environment Variables
- Set `SECRET_KEY` in production
- Add `OPENWEATHER_API_KEY` if using real weather API

### Free Tier Limitations
- Render free tier: Service spins down after 15 min of inactivity
- First request after spin-down takes ~30 seconds

---

## Upgrade to PostgreSQL (Recommended for Production)

1. **Create PostgreSQL database on Render**
2. **Update requirements.txt**:
   ```
   psycopg2-binary==2.9.9
   ```
3. **Update app.py**:
   ```python
   DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///farmers.db')
   if DATABASE_URL.startswith('postgres://'):
       DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
   app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
   ```
4. **Add DATABASE_URL environment variable in Render**

---

## Monitoring

After deployment, monitor:
- Application logs in Render dashboard
- Response times
- Error rates
- Database size

---

## Custom Domain (Optional)

1. Purchase a domain (e.g., from Namecheap, GoDaddy)
2. In Render dashboard, go to "Settings" → "Custom Domain"
3. Add your domain and configure DNS records

---

## Troubleshooting

### Build Fails
- Check Python version compatibility
- Verify all dependencies in requirements.txt

### App Crashes
- Check logs in Render dashboard
- Ensure model file is accessible
- Verify database connection

### Slow Performance
- Upgrade to paid tier for better resources
- Optimize database queries
- Add caching

---

Your app is now ready for deployment! 🎉
