"""
Model Comparison Module
========================
Handles comparison of different forecasting models and performance metrics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


def get_model_performance_metrics() -> Dict[str, Dict[str, float]]:
    """
    Get performance metrics for all models.
    
    Returns placeholder metrics if actual model evaluations aren't available.
    Replace these with your actual model evaluation results.
    
    Returns:
        dict: Model names mapped to their metrics (RMSE, MAE, MAPE)
    """
    
    # ============================================================
    # PLACEHOLDER: Model Performance Metrics
    # ============================================================
    # TODO: Replace these with actual metrics from your model evaluation
    # These are sample values for demonstration
    # ============================================================
    
    metrics = {
        'XGBoost': {
            'RMSE': 12.5,
            'MAE': 9.2,
            'MAPE': 15.3,
            'R2': 0.89,
            'available': True
        },
        'ARIMA': {
            'RMSE': 18.7,
            'MAE': 14.1,
            'MAPE': 22.5,
            'R2': 0.72,
            'available': False  # Set to True if you have this model
        },
        'Prophet': {
            'RMSE': 16.2,
            'MAE': 12.3,
            'MAPE': 19.8,
            'R2': 0.78,
            'available': False  # Set to True if you have this model
        },
        'LSTM': {
            'RMSE': 14.8,
            'MAE': 10.9,
            'MAPE': 17.2,
            'R2': 0.84,
            'available': False  # Set to True if you have this model
        }
    }
    
    return metrics


def compare_models_on_sample(historical_df: pd.DataFrame, test_size: int = 30) -> pd.DataFrame:
    """
    Compare all available models on a test sample.
    
    Args:
        historical_df: Historical data
        test_size: Number of days to use for testing
        
    Returns:
        DataFrame with predictions from each model
    """
    
    # This is a placeholder implementation
    # In production, you would:
    # 1. Split data into train/test
    # 2. Make predictions with each model
    # 3. Return comparison dataframe
    
    if historical_df is None or len(historical_df) < test_size:
        return pd.DataFrame()
    
    test_df = historical_df.tail(test_size).copy()
    
    # Placeholder predictions (replace with actual model predictions)
    if 'units_sold' in test_df.columns:
        actual = test_df['units_sold'].values
        
        # Simulate predictions with some noise
        test_df['actual'] = actual
        test_df['xgboost_pred'] = actual * (1 + np.random.normal(0, 0.1, len(actual)))
        test_df['arima_pred'] = actual * (1 + np.random.normal(0, 0.15, len(actual)))
        test_df['prophet_pred'] = actual * (1 + np.random.normal(0, 0.12, len(actual)))
        test_df['lstm_pred'] = actual * (1 + np.random.normal(0, 0.11, len(actual)))
    
    return test_df


def get_best_model() -> Tuple[str, str]:
    """
    Determine the best performing model based on metrics.
    
    Returns:
        tuple: (model_name, reason)
    """
    metrics = get_model_performance_metrics()
    
    # Find model with lowest RMSE
    available_models = {k: v for k, v in metrics.items() if v.get('available', False)}
    
    if not available_models:
        return "XGBoost", "Only available model"
    
    best_model = min(available_models.items(), key=lambda x: x[1]['RMSE'])
    
    reason = f"Lowest RMSE ({best_model[1]['RMSE']:.2f}) and highest R² ({best_model[1]['R2']:.2f})"
    
    return best_model[0], reason
