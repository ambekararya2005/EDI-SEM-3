"""
Model Loader Module
===================
Handles loading of pre-trained ML models with caching for performance.
Supports XGBoost, ARIMA, Prophet, LSTM, and risk classification models.
"""

import streamlit as st
import joblib
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


@st.cache_resource
def load_forecast_model():
    """
    Load the XGBoost demand forecasting model.
    
    Returns:
        model: Loaded XGBoost model for demand forecasting
    """
    model_path = PROJECT_ROOT / "models" / "xgboost_forecast.pkl"
    
    if not model_path.exists():
        st.warning(f"⚠️ XGBoost model not found at: {model_path}")
        return None
    
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Error loading XGBoost model: {str(e)}")
        return None


@st.cache_resource
def load_risk_model():
    """
    Load the disruption risk classification model.
    
    Returns:
        model: Loaded classifier model for risk prediction
    """
    model_path = PROJECT_ROOT / "models" / "risk_classifier.pkl"
    
    if not model_path.exists():
        st.warning(f"⚠️ Risk model not found at: {model_path}")
        return None
    
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Error loading risk model: {str(e)}")
        return None


@st.cache_resource
def load_baseline_models():
    """
    Load baseline models (ARIMA, Prophet, LSTM) for comparison.
    Returns a dictionary with model names as keys.
    If models don't exist, returns None for that model.
    
    Returns:
        dict: {'arima': model, 'prophet': model, 'lstm': model}
    """
    models = {}
    model_files = {
        'arima': 'arima_model.pkl',
        'prophet': 'prophet_model.pkl',
        'lstm': 'lstm_model.pkl'
    }
    
    for name, filename in model_files.items():
        model_path = PROJECT_ROOT / "models" / filename
        if model_path.exists():
            try:
                models[name] = joblib.load(model_path)
            except Exception as e:
                models[name] = None
        else:
            models[name] = None
    
    return models


def check_models_exist():
    """
    Check if model files exist.
    
    Returns:
        dict: Status of each model type
    """
    models_status = {
        'xgboost': (PROJECT_ROOT / "models" / "xgboost_forecast.pkl").exists(),
        'risk': (PROJECT_ROOT / "models" / "risk_classifier.pkl").exists(),
        'arima': (PROJECT_ROOT / "models" / "arima_model.pkl").exists(),
        'prophet': (PROJECT_ROOT / "models" / "prophet_model.pkl").exists(),
        'lstm': (PROJECT_ROOT / "models" / "lstm_model.pkl").exists()
    }
    
    return models_status


def get_model_info():
    """
    Get information about available models.
    
    Returns:
        dict: Model availability and descriptions
    """
    status = check_models_exist()
    
    info = {
        'xgboost': {
            'available': status['xgboost'],
            'name': 'XGBoost',
            'description': 'Gradient boosting model for demand forecasting'
        },
        'risk': {
            'available': status['risk'],
            'name': 'Risk Classifier',
            'description': 'Classification model for disruption risk prediction'
        },
        'arima': {
            'available': status['arima'],
            'name': 'ARIMA',
            'description': 'Autoregressive Integrated Moving Average baseline'
        },
        'prophet': {
            'available': status['prophet'],
            'name': 'Prophet',
            'description': 'Facebook Prophet time series baseline'
        },
        'lstm': {
            'available': status['lstm'],
            'name': 'LSTM',
            'description': 'Long Short-Term Memory neural network baseline'
        }
    }
    
    return info
