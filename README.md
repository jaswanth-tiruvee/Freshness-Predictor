# Freshness Predictor (Computer Vision Microservice)

A full-stack computer vision application that predicts the number of days remaining until a perishable item (e.g., banana) spoils. This project demonstrates a production-ready microservice architecture with a decoupled frontend and backend.

## 🏗️ Architecture

```
┌─────────────────┐         HTTP Request          ┌─────────────────┐
│  Streamlit UI   │ ────────────────────────────> │  FastAPI Backend│
│  (Frontend)     │ <──────────────────────────── │  (Model Server) │
│  Streamlit Cloud│         JSON Response         │  Render/Railway │
└─────────────────┘                                └─────────────────┘
                                                           │
                                                           ▼
                                                    ┌──────────────┐
                                                    │ ResNet Model │
                                                    │  (TensorFlow)│
                                                    └──────────────┘
```

## 📁 Project Structure

```
Freshness Predictor(Computer Vision Microservice)/
├── model_training/
│   └── train_model.ipynb          # Google Colab notebook for training
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── requirements.txt           # Python dependencies
│   └── model.h5                   # Trained model (add after training)
├── frontend/
│   ├── streamlit_app.py           # Streamlit UI application
│   └── requirements.txt           # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start Guide

### Phase 1: Model Training (Google Colab)

1. **Prepare your dataset**:
   - Take daily photos of perishable items (e.g., bananas)
   - Organize images in folders: `day_0/`, `day_1/`, ..., `day_5/`
   - Each folder contains images taken when that many days remain until spoiled

2. **Train the model**:
   - Open `model_training/train_model.ipynb` in Google Colab
   - Upload your dataset to Colab
   - Update the `DATASET_PATH` variable
   - Run all cells to train the ResNet model
   - Download the `model.h5` file when training completes

3. **Model Architecture**:
   - Base: Pre-trained ResNet50 (ImageNet weights)
   - Head: Custom regression layers (128 → 64 → 1 neuron)
   - Loss: Mean Squared Error (MSE)
   - Output: Continuous value (0-5 days)

### Phase 2: Backend Deployment (FastAPI)

#### Option A: Render (Recommended)

1. **Create a new Web Service** on [Render](https://render.com)

2. **Connect your GitHub repository** or use Render's CLI

3. **Configure the service**:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: 
     - `MODEL_PATH`: `model.h5` (default)

4. **Upload model file**:
   - Add your `model.h5` file to the `backend/` directory
   - Commit and push to trigger deployment

5. **Note your API URL**: Render will provide a URL like `https://your-app.onrender.com`

#### Option B: Railway

1. **Create a new project** on [Railway](https://railway.app)

2. **Deploy from GitHub** or upload files

3. **Configure**:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add `model.h5` to the backend directory

4. **Get your API URL** from Railway dashboard

#### Local Testing

```bash
cd backend
pip install -r requirements.txt
# Place your model.h5 file in the backend directory
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for API documentation.

### Phase 3: Frontend Deployment (Streamlit)

1. **Push code to GitHub** (if not already done)

2. **Deploy on Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Connect your GitHub repository
   - Set:
     - **Main file path**: `frontend/streamlit_app.py`
     - **Python version**: 3.9+

3. **Configure Environment Variables**:
   - Add `API_URL` = `https://your-fastapi-app.onrender.com` (your backend URL)

4. **Deploy**: Click "Deploy" and wait for the app to go live

#### Local Testing

```bash
cd frontend
pip install -r requirements.txt
export API_URL=http://localhost:8000  # or set in .env
streamlit run streamlit_app.py
```

## 🔧 API Endpoints

### `GET /`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "message": "Freshness Predictor API is running",
  "model_loaded": true
}
```

### `GET /health`
Detailed health check.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "model.h5"
}
```

### `POST /predict`
Predict days remaining from uploaded image.

**Request**:
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: Image file (JPEG, PNG, etc.)

**Response**:
```json
{
  "days_remaining": 3.4,
  "status": "success"
}
```

## 🧪 Testing the API

### Using curl:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

### Using Python:
```python
import requests

url = "http://localhost:8000/predict"
with open("test_image.jpg", "rb") as f:
    files = {"file": ("test.jpg", f, "image/jpeg")}
    response = requests.post(url, files=files)
    print(response.json())
```

## 📊 Model Performance

The model is trained to predict a continuous value (0-5 days). Expected performance:
- **Mean Absolute Error (MAE)**: < 0.5 days (with sufficient training data)
- **Inference Time**: < 100ms per image (on CPU)
- **Model Size**: ~90 MB (ResNet50 base)

## 🛠️ Technology Stack

- **Model Training**: TensorFlow/Keras, ResNet50
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Deployment**: Render/Railway (backend), Streamlit Cloud (frontend)

## 📝 Notes

- The model loads once at startup for zero-latency predictions
- Images are automatically resized to 224x224 (ResNet input size)
- Predictions are clamped to 0-5 days range
- CORS is enabled for cross-origin requests (configure for production)

## 🔒 Production Considerations

1. **Security**:
   - Restrict CORS origins to your Streamlit Cloud URL
   - Add API authentication if needed
   - Validate file sizes and types

2. **Performance**:
   - Use GPU for faster inference (if available)
   - Implement request queuing for high traffic
   - Add caching for repeated predictions

3. **Monitoring**:
   - Add logging and error tracking
   - Monitor API response times
   - Track prediction accuracy

## 📄 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve this project!

