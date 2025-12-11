"""
FastAPI Backend for Freshness Predictor
High-performance API endpoint for serving the trained model
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import os
import hashlib
from contextlib import asynccontextmanager

# Global model variable
model = None
demo_mode = False

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH", "model.h5")
IMG_SIZE = (224, 224)
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load model on startup and clean up on shutdown.
    This ensures zero-latency predictions after initial load.
    """
    global model, demo_mode
    
    # Load model on startup
    print(f"Loading model from {MODEL_PATH}...")
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"⚠️  Model file not found at {MODEL_PATH}")
            print("🔄 Running in DEMO MODE - returning mock predictions")
            print("   To use real predictions, train a model and place model.h5 in the backend directory")
            demo_mode = True
        else:
            model = keras.models.load_model(MODEL_PATH)
            print("✅ Model loaded successfully!")
            print(f"   Model input shape: {model.input_shape}")
            print(f"   Model output shape: {model.output_shape}")
            demo_mode = False
    except Exception as e:
        print(f"⚠️  Error loading model: {str(e)}")
        print("🔄 Running in DEMO MODE - returning mock predictions")
        demo_mode = True
    
    yield
    
    # Cleanup on shutdown (if needed)
    model = None
    print("Model unloaded.")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Freshness Predictor API",
    description="Computer Vision API for predicting days remaining until spoiled",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware to allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Streamlit Cloud URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def preprocess_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess image for model inference.
    Resizes to IMG_SIZE and normalizes pixel values.
    """
    # Resize image
    image = image.resize(IMG_SIZE)
    
    # Convert to RGB if needed
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    # Convert to array and normalize
    img_array = np.array(image) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Freshness Predictor API is running",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "demo_mode": demo_mode,
        "model_path": MODEL_PATH if model else None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict days remaining until spoiled from uploaded image.
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with prediction: {"days_remaining": float}
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Demo mode: return mock prediction based on image characteristics
        if demo_mode or model is None:
            # Simple heuristic: analyze image brightness/color to estimate freshness
            # In demo mode, we'll return a random-ish value based on image hash
            img_array = np.array(image)
            # Simple heuristic: calculate average brightness
            if len(img_array.shape) == 3:
                brightness = np.mean(img_array)
            else:
                brightness = np.mean(img_array)
            
            # Mock prediction: fresher items tend to be brighter (for bananas)
            # This is just for demo - real model would be much more sophisticated
            img_hash = int(hashlib.md5(contents).hexdigest()[:8], 16)
            days_remaining = 2.5 + (img_hash % 100) / 50.0  # Random between 2.5-4.5
            days_remaining = max(0.0, min(5.0, days_remaining))
            
            return JSONResponse(content={
                "days_remaining": round(days_remaining, 2),
                "status": "success",
                "demo_mode": True,
                "message": "⚠️ Demo mode: This is a mock prediction. Train a model for real predictions."
            })
        
        # Real mode: use actual model
        # Preprocess image
        img_array = preprocess_image(image)
        
        # Make prediction
        prediction = model.predict(img_array, verbose=0)
        days_remaining = float(prediction[0][0])
        
        # Clamp prediction to reasonable range (0-5 days)
        days_remaining = max(0.0, min(5.0, days_remaining))
        
        return JSONResponse(content={
            "days_remaining": round(days_remaining, 2),
            "status": "success",
            "demo_mode": False
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

