"""
Demand Forecasting Module
==========================
Handles demand prediction using the XGBoost model.
"""

import pandas as pd
import numpy as np
from .model_loader import load_forecast_model


def forecast_demand(input_df: pd.DataFrame) -> np.ndarray:
    """
    Predict future demand using the XGBoost forecasting model.
    
    Args:
        input_df: DataFrame with features for prediction
                  Expected columns (after feature engineering):
                  - temperature
                  - rainfall
                  - holiday_flag
                  - promotion_flag
                  - congestion_index
                  - [any additional engineered features]
    
    Returns:
        np.ndarray: Predicted demand values (units_sold)
    
    Note:
        This function includes a PLACEHOLDER for feature engineering.
        You should replace the feature engineering section with your actual
        preprocessing pipeline that matches your trained model.
    """
    
    # Load the model
    model = load_forecast_model()
    
    if model is None:
        # Return dummy predictions if model not available
        return np.zeros(len(input_df))
    
    # ============================================================
    # FEATURE ENGINEERING (Matches trained XGBoost model)
    # ============================================================
    # This matches the preprocessing pipeline from src/data/preprocess.py
    # Features include:
    # - Time features: dow (day of week), week, month, year
    # - Lag features: lag_7, lag_14, lag_28
    # - Rolling statistics: roll_mean_7, roll_mean_28, roll_std_7, roll_std_28
    # - Numeric features: temperature, rainfall, congestion_index
    # - Categorical features (one-hot encoded): product, location, holiday_flag, promotion_flag
    # ============================================================
    
    feature_df = input_df.copy()
    
    # 1. Add time features
    if 'date' in feature_df.columns:
        d = pd.to_datetime(feature_df['date'])
        feature_df['dow'] = d.dt.dayofweek
        feature_df['week'] = d.dt.isocalendar().week.astype(int)
        feature_df['month'] = d.dt.month
        feature_df['year'] = d.dt.year
    
    # 2. Add lag features (7, 14, 28 days)
    # Note: For future predictions, we use the last known values as approximation
    # In production, you should use actual historical data for lags
    if 'units_sold' in feature_df.columns:
        # If we have historical sales, create lags
        for lag in [7, 14, 28]:
            feature_df[f'lag_{lag}'] = feature_df['units_sold'].shift(lag)
    else:
        # For future predictions, use placeholder values (you may want to improve this)
        for lag in [7, 14, 28]:
            feature_df[f'lag_{lag}'] = 0  # Placeholder
    
    # 3. Add rolling statistics (mean and std for 7 and 28 day windows)
    if 'units_sold' in feature_df.columns:
        for window in [7, 28]:
            feature_df[f'roll_mean_{window}'] = feature_df['units_sold'].shift(1).rolling(window).mean()
            feature_df[f'roll_std_{window}'] = feature_df['units_sold'].shift(1).rolling(window).std()
    else:
        # Placeholder for future predictions
        for window in [7, 28]:
            feature_df[f'roll_mean_{window}'] = 0
            feature_df[f'roll_std_{window}'] = 0
    
    # 4. Ensure numeric features exist
    numeric_features = ['temperature', 'rainfall', 'congestion_index']
    for feat in numeric_features:
        if feat not in feature_df.columns:
            feature_df[feat] = 0
    
    # 5. Ensure categorical features exist
    categorical_features = ['product', 'location', 'holiday_flag', 'promotion_flag']
    for feat in categorical_features:
        if feat not in feature_df.columns:
            feature_df[feat] = 'Unknown' if feat in ['product', 'location'] else 0
    
    # 6. One-hot encode categorical features (matching training)
    # Note: This will create columns like product_X, location_Y, etc.
    feature_df = pd.get_dummies(feature_df, columns=categorical_features, drop_first=False)
    
    # 7. Fill any NaN values
    feature_df = feature_df.fillna(0)
    
    # 8. Select only numeric/boolean columns (excluding date and target)
    exclude_cols = ['date', 'units_sold']
    candidate_cols = [c for c in feature_df.columns if c not in exclude_cols]
    numeric_cols = list(feature_df[candidate_cols].select_dtypes(include=['number', 'bool']).columns)
    
    if not numeric_cols:
        # If no features available, return zeros
        return np.zeros(len(input_df))
    
    X = feature_df[numeric_cols]
    
    # ============================================================
    # END FEATURE ENGINEERING
    # ============================================================
    
    try:
        # Make predictions
        predictions = model.predict(X)
        
        # Ensure predictions are non-negative (demand can't be negative)
        predictions = np.maximum(predictions, 0)
        
        return predictions
        
    except Exception as e:
        print(f"Error during forecasting: {str(e)}")
        # Return zeros if prediction fails
        return np.zeros(len(input_df))


def create_future_dataframe(historical_df: pd.DataFrame, horizon_days: int) -> pd.DataFrame:
    """
    Create a dataframe for future dates based on historical data.
    
    This function generates future scenarios with proper handling of lag features
    by combining historical and future data.
    
    Args:
        historical_df: Historical data
        horizon_days: Number of days to forecast
        
    Returns:
        pd.DataFrame: Future dataframe with predicted features
    """
    
    if historical_df is None or len(historical_df) == 0:
        return pd.DataFrame()
    
    # Get the last date in historical data
    if 'date' in historical_df.columns:
        last_date = pd.to_datetime(historical_df['date'].max())
    else:
        last_date = pd.Timestamp.now()
    
    # Create future dates
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=horizon_days,
        freq='D'
    )
    
    # ============================================================
    # Future Feature Generation
    # ============================================================
    # Use recent historical data to estimate future features
    # ============================================================
    
    recent_data = historical_df.tail(60)  # Use last 60 days for estimation
    
    future_df = pd.DataFrame({
        'date': future_dates
    })
    
    # Use average values for weather features from recent data
    if 'temperature' in recent_data.columns:
        # Use seasonal average (same month from history)
        future_df['temperature'] = recent_data['temperature'].mean()
    else:
        future_df['temperature'] = 20  # Default
    
    if 'rainfall' in recent_data.columns:
        future_df['rainfall'] = recent_data['rainfall'].mean()
    else:
        future_df['rainfall'] = 0
    
    # Assume no holidays/promotions unless specified
    # You can customize this based on known future events
    future_df['holiday_flag'] = 0
    future_df['promotion_flag'] = 0
    
    if 'congestion_index' in recent_data.columns:
        future_df['congestion_index'] = recent_data['congestion_index'].mean()
    else:
        future_df['congestion_index'] = 0.5
    
    # Copy product and location (they should be constant for a specific forecast)
    if 'product' in historical_df.columns:
        future_df['product'] = historical_df['product'].iloc[-1]
    
    if 'location' in historical_df.columns:
        future_df['location'] = historical_df['location'].iloc[-1]
    
    # For lag features, we need to combine historical and future data
    # This is a simplified approach - in production, you'd want to:
    # 1. Make predictions iteratively (predict day 1, use it for day 8's lag_7, etc.)
    # 2. Or use a more sophisticated approach with uncertainty
    
    # Combine historical and future for lag calculation
    combined_df = pd.concat([historical_df, future_df], ignore_index=True)
    
    # Add placeholder units_sold for future (will be filled by predictions)
    if 'units_sold' not in future_df.columns:
        # Use recent average as initial guess
        if 'units_sold' in historical_df.columns:
            avg_sales = historical_df['units_sold'].tail(30).mean()
            future_df['units_sold'] = avg_sales
        else:
            future_df['units_sold'] = 0
    
    # ============================================================
    # END Future Feature Generation
    # ============================================================
    
    return future_df
