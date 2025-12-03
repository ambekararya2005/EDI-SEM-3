"""
Model Performance & Insights Page
==================================
Compares different forecasting models and displays performance metrics.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend import (
    get_model_performance_metrics,
    get_best_model,
    get_model_info,
    load_main_dataset
)

# Page config
st.set_page_config(
    page_title="Model Performance",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Model Performance & Insights")
st.markdown("---")

# Introduction
st.markdown("""
This page compares different forecasting models used in the SmartRetail Hybrid system.
We evaluate **XGBoost** (our primary model) against baseline models including **ARIMA**, **Prophet**, and **LSTM**.
""")

st.markdown("---")

# Get model information
model_info = get_model_info()
metrics = get_model_performance_metrics()

# Model Availability Section
st.subheader("🔧 Model Availability")

cols = st.columns(5)
for idx, (model_key, info) in enumerate(model_info.items()):
    with cols[idx]:
        if info['available']:
            st.success(f"✅ **{info['name']}**")
        else:
            st.warning(f"⚠️ **{info['name']}**")
        st.caption(info['description'])

st.markdown("---")

# Performance Metrics Comparison
st.subheader("📈 Performance Metrics Comparison")

# Create metrics dataframe
metrics_df = pd.DataFrame(metrics).T
metrics_df = metrics_df.reset_index()
metrics_df.columns = ['Model', 'RMSE', 'MAE', 'MAPE', 'R2', 'Available']

# Convert all numeric columns to proper numeric type
metrics_df['RMSE'] = pd.to_numeric(metrics_df['RMSE'], errors='coerce')
metrics_df['MAE'] = pd.to_numeric(metrics_df['MAE'], errors='coerce')
metrics_df['MAPE'] = pd.to_numeric(metrics_df['MAPE'], errors='coerce')
metrics_df['R2'] = pd.to_numeric(metrics_df['R2'], errors='coerce')

# Display metrics table
st.markdown("### 📋 Detailed Metrics")
display_df = metrics_df[['Model', 'RMSE', 'MAE', 'MAPE', 'R2']].copy()

# Round for display
display_df['RMSE'] = display_df['RMSE'].round(2)
display_df['MAE'] = display_df['MAE'].round(2)
display_df['MAPE'] = display_df['MAPE'].round(1)
display_df['R2'] = display_df['R2'].round(3)

st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("---")

# Visualizations
st.markdown("### 📊 Visual Comparison")

col1, col2 = st.columns(2)

with col1:
    # RMSE Comparison
    fig_rmse = go.Figure()
    
    colors = ['#2ecc71' if m == 'XGBoost' else '#3498db' for m in metrics_df['Model']]
    
    fig_rmse.add_trace(go.Bar(
        x=metrics_df['Model'],
        y=metrics_df['RMSE'],
        marker_color=colors,
        text=metrics_df['RMSE'].round(2),
        textposition='outside',
        name='RMSE'
    ))
    
    fig_rmse.update_layout(
        title='Root Mean Squared Error (RMSE)',
        xaxis_title='Model',
        yaxis_title='RMSE (lower is better)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_rmse, use_container_width=True)

with col2:
    # MAE Comparison
    fig_mae = go.Figure()
    
    fig_mae.add_trace(go.Bar(
        x=metrics_df['Model'],
        y=metrics_df['MAE'],
        marker_color=colors,
        text=metrics_df['MAE'].round(2),
        textposition='outside',
        name='MAE'
    ))
    
    fig_mae.update_layout(
        title='Mean Absolute Error (MAE)',
        xaxis_title='Model',
        yaxis_title='MAE (lower is better)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_mae, use_container_width=True)

# R² Score Comparison
st.markdown("### 🎯 Model Accuracy (R² Score)")

fig_r2 = go.Figure()

fig_r2.add_trace(go.Bar(
    x=metrics_df['Model'],
    y=metrics_df['R2'],
    marker_color=colors,
    text=metrics_df['R2'].round(3),
    textposition='outside',
    name='R² Score'
))

fig_r2.update_layout(
    title='R² Score Comparison',
    xaxis_title='Model',
    yaxis_title='R² Score (higher is better, max = 1.0)',
    height=400,
    showlegend=False,
    yaxis=dict(range=[0, 1.1])
)

st.plotly_chart(fig_r2, use_container_width=True)

st.markdown("---")

# Multi-metric Radar Chart
st.markdown("### 🎯 Multi-Metric Radar Chart")

# Normalize metrics for radar chart (0-1 scale, higher is better)
radar_df = metrics_df.copy()
radar_df['RMSE_norm'] = 1 - (radar_df['RMSE'] / radar_df['RMSE'].max())
radar_df['MAE_norm'] = 1 - (radar_df['MAE'] / radar_df['MAE'].max())
radar_df['MAPE_norm'] = 1 - (radar_df['MAPE'] / radar_df['MAPE'].max())
radar_df['R2_norm'] = radar_df['R2']

fig_radar = go.Figure()

categories = ['RMSE', 'MAE', 'MAPE', 'R²']

for idx, row in radar_df.iterrows():
    values = [row['RMSE_norm'], row['MAE_norm'], row['MAPE_norm'], row['R2_norm']]
    values.append(values[0])  # Close the polygon
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=row['Model']
    ))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]
        )),
    showlegend=True,
    title='Normalized Performance Metrics (Higher = Better)',
    height=500
)

st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# Best Model Recommendation
st.subheader("🏆 Best Model Recommendation")

best_model, reason = get_best_model()

st.success(f"""
**Recommended Model: {best_model}**

**Reason:** {reason}

**Why {best_model}?**
- Consistently low error metrics across RMSE, MAE, and MAPE
- High R² score indicating good fit to data
- Robust performance on validation set
- Handles non-linear patterns and feature interactions well
""")

st.markdown("---")

# Model Insights
st.subheader("💡 Model Insights & Interpretation")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📊 Metric Definitions:**
    
    - **RMSE (Root Mean Squared Error)**: Measures average prediction error, penalizes large errors more
    - **MAE (Mean Absolute Error)**: Average absolute difference between predictions and actual values
    - **MAPE (Mean Absolute Percentage Error)**: Average percentage error, useful for relative comparison
    - **R² Score**: Proportion of variance explained by the model (0 to 1, higher is better)
    """)

with col2:
    st.markdown("""
    **🎯 Model Characteristics:**
    
    - **XGBoost**: Gradient boosting, handles complex patterns, feature importance
    - **ARIMA**: Time series baseline, captures trends and seasonality
    - **Prophet**: Facebook's time series tool, handles holidays and events
    - **LSTM**: Neural network, learns sequential patterns
    """)

st.markdown("---")

# Performance Over Time (if data available)
st.subheader("📈 Model Performance Trends")

st.info("""
**Note:** The metrics shown above are based on validation set performance.
For production deployment, continuous monitoring of model performance is recommended.

**Placeholder:** In a production system, you would show:
- Performance metrics over time
- Drift detection
- Retraining triggers
- A/B test results
""")

# Footer
st.markdown("---")
st.caption("💡 Model performance metrics are updated after each retraining cycle. Actual metrics may vary based on data distribution.")
