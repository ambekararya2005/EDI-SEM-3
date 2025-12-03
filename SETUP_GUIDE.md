# SmartRetail Hybrid - Quick Setup Guide

## Step-by-Step Setup

### 1. Install Dependencies
```bash
cd smartretail_app
pip install -r requirements.txt
```

### 2. Add Your Files

**Dataset:**
- Copy `Retail-Supply-Chain-Sales-Dataset-With-Weather.xlsx` to the `data/` folder

**Models:**
- Copy `xgboost_forecast.pkl` to the `models/` folder
- Copy `risk_classifier.pkl` to the `models/` folder

### 3. Customize Feature Engineering

Open these files and replace the PLACEHOLDER sections:

**For Demand Forecasting:**
```
backend/forecasting.py
```
- Find the `forecast_demand()` function
- Replace the feature engineering section (marked with PLACEHOLDER comments)
- Match the features you used when training your XGBoost model

**For Risk Prediction:**
```
backend/disruption.py
```
- Find the `predict_disruption()` function
- Replace the feature engineering section (marked with PLACEHOLDER comments)
- Match the features you used when training your risk classifier

### 4. Run the App
```bash
streamlit run app.py
```

The app will open at: http://localhost:8501

## Quick Test

To verify everything works:

1. Navigate to "Overview" page - should show your data
2. Navigate to "Sales Explorer" - should allow filtering
3. Navigate to "Forecast & Risk" - select product/location and run analysis

## Common Issues

**"Dataset not found"**
→ Check that the Excel file is in `data/` folder with exact filename

**"Model not found"**
→ Check that .pkl files are in `models/` folder with exact filenames

**Prediction errors**
→ Update the feature engineering in backend files to match your models

## Need Help?

Check the full README.md for detailed documentation.
