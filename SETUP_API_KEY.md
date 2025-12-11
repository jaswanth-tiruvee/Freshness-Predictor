# 🔐 API Key Setup Guide

## Generated API Key
**IMPORTANT:** Use the same key in both Render and Streamlit Cloud!

## Step 1: Set API Key in Render (Backend)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign in if needed

2. **Select Your Service**
   - Click on your backend service (e.g., `freshness-predictor`)

3. **Go to Environment Tab**
   - Click on "Environment" in the left sidebar
   - Or scroll down to "Environment Variables" section

4. **Add API_KEY**
   - Click "Add Environment Variable" or the "+" button
   - **Key:** `API_KEY`
   - **Value:** `YOUR_GENERATED_KEY_HERE` (paste the key from above)
   - Click "Save Changes"

5. **Redeploy**
   - The service will automatically redeploy
   - Wait for deployment to complete (2-3 minutes)

## Step 2: Set API Key in Streamlit Cloud (Frontend)

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/ (or your app's dashboard)
   - Sign in if needed

2. **Select Your App**
   - Click on your Freshness Predictor app

3. **Go to Settings**
   - Click the "⚙️ Settings" button (gear icon)

4. **Go to Secrets Tab**
   - Click on "Secrets" tab

5. **Add API_KEY**
   - In the secrets editor, add:
     ```
     API_KEY = YOUR_GENERATED_KEY_HERE
     ```
   - Make sure it's the SAME key as in Render
   - Click "Save"

6. **Auto-Redeploy**
   - Streamlit will automatically redeploy your app
   - Wait 1-2 minutes

## Step 3: Verify It Works

1. **Check Backend**
   - Visit: `https://your-backend-url.onrender.com/health`
   - Should return: `{"status":"healthy",...}`

2. **Test from Streamlit**
   - Go to your Streamlit app
   - Upload an image and test prediction
   - Should work if API_KEY is set correctly

3. **Test Without Key (Should Fail)**
   - Try accessing `/predict` directly without API key
   - Should return: `{"detail":"Invalid or missing API key"}`

## Troubleshooting

**If predictions fail:**
- Check that API_KEY is set in BOTH Render and Streamlit Cloud
- Make sure the keys match exactly (copy-paste to avoid typos)
- Check backend logs in Render dashboard
- Check Streamlit Cloud logs

**If you want to disable API key:**
- Remove API_KEY from both Render and Streamlit Cloud
- API will work without authentication (less secure)

## Security Notes

- ✅ Keep your API key secret
- ✅ Don't commit API keys to GitHub
- ✅ Use different keys for different environments (dev/prod)
- ✅ Rotate keys periodically

