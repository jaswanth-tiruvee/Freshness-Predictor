"""
Streamlit Frontend for Freshness Predictor
Entry point for Streamlit Cloud deployment
"""
import sys
import os

# Add frontend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend'))

# Import and run the main app
from streamlit_app import main

if __name__ == "__main__":
    main()

