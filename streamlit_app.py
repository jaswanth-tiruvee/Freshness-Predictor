"""
Streamlit Frontend for Freshness Predictor
Entry point for Streamlit Cloud deployment
"""
import streamlit as st
import requests
from PIL import Image
import io
import os

# Configuration
# For Streamlit Cloud, API_URL must be set as an environment variable
# pointing to your deployed backend (e.g., https://your-app.onrender.com)
API_URL = os.getenv("API_URL", "")
API_KEY = os.getenv("API_KEY", "")  # Optional: API key for authentication
PREDICT_ENDPOINT = f"{API_URL}/predict" if API_URL else None

# Page configuration
st.set_page_config(
    page_title="Freshness Predictor",
    page_icon="🍌",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .prediction-value {
        font-size: 4rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🍌 Freshness Predictor</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Upload an image to predict days remaining until spoiled</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar with API status
    with st.sidebar:
        st.header("🔧 Configuration")
        
        if not API_URL:
            st.error("⚠️ API_URL not configured")
            st.markdown("""
            **To use this app, you need to:**
            
            1. Deploy your FastAPI backend to Render or Railway
            2. Set the `API_URL` environment variable in Streamlit Cloud:
               - Go to app settings → Secrets
               - Add: `API_URL = https://your-backend-url.onrender.com`
            3. Redeploy the app
            
            **For local testing:**
            ```bash
            export API_URL=http://localhost:8001
            streamlit run streamlit_app.py
            ```
            """)
        else:
            st.write(f"**API URL:** {API_URL}")
            if API_KEY:
                st.write("🔐 **API Key:** Configured")
            else:
                st.info("💡 Tip: Set API_KEY in secrets for added security")
            
            # Check API health
            try:
                headers = {}
                if API_KEY:
                    headers["X-API-Key"] = API_KEY
                response = requests.get(f"{API_URL}/health", headers=headers, timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    st.success("✅ API is healthy")
                    st.write(f"**Model loaded:** {health_data.get('model_loaded', False)}")
                    if health_data.get('demo_mode'):
                        st.info("⚠️ Running in demo mode")
                else:
                    st.warning("⚠️ API returned unexpected status")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Cannot connect to API")
                st.code(str(e)[:100] + "..." if len(str(e)) > 100 else str(e))
                st.info("Make sure your FastAPI backend is deployed and accessible!")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload an image of a perishable item (e.g., banana)"
    )
    
    if not API_URL:
        st.warning("⚠️ Please configure the API_URL environment variable to use this app.")
        st.info("See the sidebar for instructions on how to set it up.")
        return
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Predict button
        if st.button("🔮 Predict Freshness", type="primary", use_container_width=True):
            with st.spinner("Analyzing image..."):
                try:
                    # Prepare image for API
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='JPEG')
                    img_bytes.seek(0)
                    
                    # Send request to FastAPI
                    files = {"file": ("image.jpg", img_bytes, "image/jpeg")}
                    headers = {}
                    if API_KEY:
                        headers["X-API-Key"] = API_KEY
                    response = requests.post(PREDICT_ENDPOINT, files=files, headers=headers, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        days_remaining = result.get("days_remaining", 0)
                        demo_mode = result.get("demo_mode", False)
                        
                        # Display prediction
                        st.markdown("---")
                        st.markdown(f"""
                            <div class="prediction-box">
                                <h2>Prediction Result</h2>
                                <div class="prediction-value">{days_remaining:.1f}</div>
                                <h3>Days Remaining</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if demo_mode:
                            st.info("ℹ️ This is a demo prediction. Train a model for real predictions.")
                        
                        # Additional info
                        days_int = int(round(days_remaining))
                        if days_int == 0:
                            st.error("⚠️ Item is spoiled or very close to spoiling!")
                        elif days_int <= 1:
                            st.warning("🔴 Item will spoil very soon (within 1 day)")
                        elif days_int <= 2:
                            st.warning("🟡 Item will spoil soon (within 2 days)")
                        elif days_int <= 3:
                            st.info("🟠 Item has moderate freshness (2-3 days remaining)")
                        else:
                            st.success("🟢 Item is fresh! (3+ days remaining)")
                    
                    else:
                        error_msg = response.json().get("detail", "Unknown error")
                        st.error(f"❌ Prediction failed: {error_msg}")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection error: {str(e)}")
                    st.info("Please check that your FastAPI backend is running and accessible.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
    
    # Instructions
    with st.expander("📖 How to use"):
        st.markdown("""
        1. **Prepare your dataset**: Take daily photos of perishable items (e.g., bananas) 
           and organize them in folders named `day_0`, `day_1`, ..., `day_5` based on days 
           remaining until spoiled.
        
        2. **Train the model**: Use the provided Jupyter notebook in `model_training/` 
           on Google Colab to train your ResNet model.
        
        3. **Deploy the backend**: Upload your trained `model.h5` file to the backend 
           directory and deploy to Render or Railway.
        
        4. **Deploy the frontend**: This app is deployed on Streamlit Cloud! Just set 
           the `API_URL` environment variable to your FastAPI backend URL.
        
        5. **Use the app**: Upload an image and click "Predict Freshness" to get the 
           prediction!
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>Built with FastAPI, TensorFlow, and Streamlit</p>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

