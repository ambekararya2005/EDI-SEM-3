"""
Disruption Risk Prediction Module
==================================
Handles supply chain disruption risk prediction using classification model.
"""

import pandas as pd
import numpy as np
from .model_loader import load_risk_model


def predict_disruption(input_df: pd.DataFrame) -> np.ndarray:
    """
    Predict disruption risk probability using the classification model.
    
    Args:
        input_df: DataFrame with features for prediction
                  Expected columns (after feature engineering):
                  - temperature
                  - rainfall
                  - congestion_index
                  - [any additional engineered features]
    
    Returns:
        np.ndarray: Disruption risk probabilities (0.0 to 1.0)
                   Higher values indicate higher risk of disruption
    
    Note:
        This function includes a PLACEHOLDER for feature engineering.
        You should replace the feature engineering section with your actual
        preprocessing pipeline that matches your trained model.
    """
    
    # Load the model
    model = load_risk_model()
    
    if model is None:
        # Return dummy predictions if model not available
        return np.random.uniform(0.1, 0.4, len(input_df))
    
    # ============================================================
    # PLACEHOLDER: FEATURE ENGINEERING
    # ============================================================
    # TODO: Replace this section with your actual feature engineering
    # that matches what you used during model training.
    #
    # Examples of features you might create:
    # - Weather severity indicators (extreme temp, heavy rain)
    # - Congestion level categories
    # - Historical disruption patterns
    # - Interaction features (rainfall * congestion_index)
    # - Time-based features (rush hour, peak season)
    # ============================================================
    
    feature_df = input_df.copy()
    
    # Example: Create some basic derived features
    if 'temperature' in feature_df.columns:
        # Flag for extreme temperatures
        feature_df['extreme_temp'] = (
            (feature_df['temperature'] < 0) | 
            (feature_df['temperature'] > 35)
        ).astype(int)
    
    if 'rainfall' in feature_df.columns:
        # Flag for heavy rainfall
        feature_df['heavy_rain'] = (feature_df['rainfall'] > 50).astype(int)
    
    if 'congestion_index' in feature_df.columns:
        # Categorize congestion levels
        feature_df['high_congestion'] = (feature_df['congestion_index'] > 0.7).astype(int)
    
    # Extract date features if available
    if 'date' in feature_df.columns:
        feature_df['day_of_week'] = pd.to_datetime(feature_df['date']).dt.dayofweek
        feature_df['month'] = pd.to_datetime(feature_df['date']).dt.month
        feature_df['is_weekend'] = feature_df['day_of_week'].isin([5, 6]).astype(int)
    
    # Define expected feature columns (modify based on your model)
    # This is a PLACEHOLDER - adjust to match your actual model features
    expected_features = [
        'temperature',
        'rainfall',
        'congestion_index',
        'extreme_temp',
        'heavy_rain',
        'high_congestion',
        'day_of_week',
        'month',
        'is_weekend'
    ]
    
    # Select only the features that exist in the dataframe
    available_features = [col for col in expected_features if col in feature_df.columns]
    
    if not available_features:
        # If no features available, return moderate risk
        return np.full(len(input_df), 0.3)
    
    X = feature_df[available_features]
    
    # Handle any remaining missing values
    X = X.fillna(0)
    
    # ============================================================
    # END PLACEHOLDER
    # ============================================================
    
    try:
        # Make predictions
        # Check if model has predict_proba method (for classifiers)
        if hasattr(model, 'predict_proba'):
            # Get probability of positive class (disruption)
            predictions = model.predict_proba(X)[:, 1]
        else:
            # If no predict_proba, use predict and normalize
            predictions = model.predict(X)
            # Ensure values are between 0 and 1
            predictions = np.clip(predictions, 0, 1)
        
        return predictions
        
    except Exception as e:
        print(f"Error during disruption prediction: {str(e)}")
        # Return moderate risk if prediction fails
        return np.full(len(input_df), 0.3)


def calculate_safe_purchase_window(dates, risk_probabilities, threshold=0.3):
    """
    Calculate the safe purchase window based on risk probabilities.
    
    A safe purchase window is a continuous period where disruption risk
    is below the specified threshold.
    
    Args:
        dates: Array or Series of dates
        risk_probabilities: Array of risk probabilities
        threshold: Risk threshold (default 0.3 = 30%)
        
    Returns:
        tuple: (start_date, end_date, num_safe_days) or (None, None, 0) if no safe window
    """
    
    if len(dates) == 0 or len(risk_probabilities) == 0:
        return None, None, 0
    
    # Find indices where risk is below threshold
    safe_indices = np.where(risk_probabilities < threshold)[0]
    
    if len(safe_indices) == 0:
        return None, None, 0
    
    # Find the longest continuous sequence of safe days
    # Group consecutive indices
    groups = np.split(safe_indices, np.where(np.diff(safe_indices) != 1)[0] + 1)
    
    # Find the longest group
    longest_group = max(groups, key=len)
    
    if len(longest_group) == 0:
        return None, None, 0
    
    # Get start and end dates
    start_idx = longest_group[0]
    end_idx = longest_group[-1]
    
    start_date = dates.iloc[start_idx] if hasattr(dates, 'iloc') else dates[start_idx]
    end_date = dates.iloc[end_idx] if hasattr(dates, 'iloc') else dates[end_idx]
    num_safe_days = len(longest_group)
    
    return start_date, end_date, num_safe_days


def get_risk_level_label(risk_prob):
    """
    Convert risk probability to human-readable label.
    
    Args:
        risk_prob: Risk probability (0.0 to 1.0)
        
    Returns:
        str: Risk level label
    """
    if risk_prob < 0.2:
        return "🟢 Very Low"
    elif risk_prob < 0.4:
        return "🟡 Low"
    elif risk_prob < 0.6:
        return "🟠 Moderate"
    elif risk_prob < 0.8:
        return "🔴 High"
    else:
        return "⛔ Very High"
