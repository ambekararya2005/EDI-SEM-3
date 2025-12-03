"""
Model Conversion Script
=======================
Converts the XGBoost JSON model to pickle format and creates a placeholder risk model.
"""

import joblib
import numpy as np
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
ARTIFACTS_DIR = PROJECT_ROOT.parent / "project" / "artifacts"
MODELS_DIR = PROJECT_ROOT / "models"

print("=" * 60)
print("SmartRetail Model Conversion Script")
print("=" * 60)

# 1. Load and convert XGBoost forecast model
print("\n1. Converting XGBoost forecast model...")
xgb_json_path = ARTIFACTS_DIR / "xgb_model.json"

if xgb_json_path.exists():
    try:
        # Load the XGBoost model from JSON
        forecast_model = XGBRegressor()
        forecast_model.load_model(str(xgb_json_path))
        
        # Save as pickle
        forecast_pkl_path = MODELS_DIR / "xgboost_forecast.pkl"
        joblib.dump(forecast_model, forecast_pkl_path)
        
        print(f"   ✅ Forecast model converted successfully!")
        print(f"   📁 Saved to: {forecast_pkl_path}")
    except Exception as e:
        print(f"   ❌ Error converting forecast model: {e}")
else:
    print(f"   ⚠️  XGBoost model not found at: {xgb_json_path}")

# 2. Create a placeholder risk classifier
print("\n2. Creating placeholder risk classifier...")
print("   ⚠️  NOTE: This is a DUMMY model for demonstration only!")
print("   You should replace this with your actual trained risk model.")

try:
    # Create a simple random forest classifier as placeholder
    # This will predict random risk probabilities
    risk_model = RandomForestClassifier(
        n_estimators=50,
        max_depth=5,
        random_state=42
    )
    
    # Train on dummy data (just to make it functional)
    # In reality, you should use your actual training data
    np.random.seed(42)
    X_dummy = np.random.randn(100, 9)  # 9 features (matching placeholder in disruption.py)
    y_dummy = np.random.randint(0, 2, 100)  # Binary classification
    
    risk_model.fit(X_dummy, y_dummy)
    
    # Save the placeholder model
    risk_pkl_path = MODELS_DIR / "risk_classifier.pkl"
    joblib.dump(risk_model, risk_pkl_path)
    
    print(f"   ✅ Placeholder risk model created!")
    print(f"   📁 Saved to: {risk_pkl_path}")
    print(f"   ⚠️  IMPORTANT: Replace this with your actual risk model!")
except Exception as e:
    print(f"   ❌ Error creating risk model: {e}")

print("\n" + "=" * 60)
print("Conversion Complete!")
print("=" * 60)
print("\nNext steps:")
print("1. ✅ Dataset is already in data/ folder")
print("2. ✅ Forecast model converted to models/ folder")
print("3. ⚠️  Replace the placeholder risk model with your actual trained model")
print("4. ⚠️  Update feature engineering in backend/forecasting.py")
print("5. ⚠️  Update feature engineering in backend/disruption.py")
print("6. 🚀 Run: streamlit run app.py")
print("=" * 60)
