# Deploy to Streamlit Cloud - Quick Guide

## Prerequisites
1. Your code is already pushed to GitHub: https://github.com/jaswanth-tiruvee/Freshness-Predictor.git
2. You have a Streamlit Cloud account (free): https://streamlit.io/cloud
3. Your FastAPI backend is deployed (or use demo mode)

## Step-by-Step Deployment

### Step 1: Sign in to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Authorize Streamlit Cloud to access your repositories

### Step 2: Create New App
1. Click **"New app"** button
2. Select your GitHub account
3. Choose repository: **`jaswanth-tiruvee/Freshness-Predictor`**
4. Select branch: **`main`**
5. **Main file path**: `streamlit_app.py` (or `frontend/streamlit_app.py` if using subdirectory)

### Step 3: Configure Environment Variables
1. Click **"Advanced settings"** (gear icon)
2. Click **"Secrets"** tab
3. Add environment variable:
   ```
   API_URL = https://your-backend-url.onrender.com
   ```
   Or if backend is not deployed yet, use:
   ```
   API_URL = http://localhost:8001
   ```
   (Note: This will only work if backend is on same network)

### Step 4: Deploy
1. Click **"Deploy"** button
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://your-app-name.streamlit.app`

## Important Notes

### Backend Deployment Required
For the app to work fully, you need to deploy the FastAPI backend first:

**Option 1: Render (Free)**
- Deploy backend to Render: https://render.com
- Get your backend URL (e.g., `https://freshness-api.onrender.com`)
- Set `API_URL` in Streamlit Cloud to this URL

**Option 2: Railway (Free)**
- Deploy backend to Railway: https://railway.app
- Get your backend URL
- Set `API_URL` in Streamlit Cloud

**Option 3: Demo Mode**
- The backend can run in demo mode without a model
- But it still needs to be deployed somewhere accessible

### Testing Locally First
Before deploying, test locally:
```bash
cd frontend
pip install -r requirements.txt
export API_URL=http://localhost:8001
streamlit run streamlit_app.py
```

## Troubleshooting

**App won't connect to backend:**
- Check that `API_URL` environment variable is set correctly
- Verify backend is running and accessible
- Check CORS settings on backend (should allow all origins for demo)

**Import errors:**
- Make sure `requirements.txt` includes all dependencies
- Check that file paths are correct

**Timeout errors:**
- Backend might be spinning up (cold start on free tier)
- Increase timeout in `streamlit_app.py` if needed

## Your Deployment URLs

After deployment, you'll have:
- **Frontend**: `https://your-app-name.streamlit.app`
- **Backend**: `https://your-backend-url.onrender.com` (or Railway URL)

Make sure to update the `API_URL` in Streamlit Cloud secrets to match your backend URL!

