"""
Streamlit Frontend for Freshness Predictor
Interactive UI for uploading images and viewing predictions
"""

import streamlit as st
import requests
from PIL import Image
import io
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
PREDICT_ENDPOINT = f"{API_URL}/predict"

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
        st.write(f"**API URL:** {API_URL}")
        
        # Check API health
        try:
            response = requests.get(f"{API_URL}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                st.success("✅ API is healthy")
                st.write(f"**Model loaded:** {health_data.get('model_loaded', False)}")
            else:
                st.warning("⚠️ API returned unexpected status")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Cannot connect to API: {str(e)}")
            st.info("Make sure your FastAPI backend is running!")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=['jpg', 'jpeg', 'png'],
        help="Upload an image of a perishable item (e.g., banana)"
    )
    
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
                    response = requests.post(PREDICT_ENDPOINT, files=files, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        days_remaining = result.get("days_remaining", 0)
                        
                        # Display prediction
                        st.markdown("---")
                        st.markdown(f"""
                            <div class="prediction-box">
                                <h2>Prediction Result</h2>
                                <div class="prediction-value">{days_remaining:.1f}</div>
                                <h3>Days Remaining</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
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
        
        4. **Deploy the frontend**: Deploy this Streamlit app to Streamlit Cloud with 
           the `API_URL` environment variable set to your FastAPI backend URL.
        
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

