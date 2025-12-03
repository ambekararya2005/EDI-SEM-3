"""
Forecast & Risk Prediction Page
================================
AI-powered demand forecasting, disruption risk prediction, and hybrid purchase recommendations.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend import (
    load_main_dataset, get_unique_products, get_unique_locations,
    filter_data, forecast_demand, create_future_dataframe,
    predict_disruption, calculate_safe_purchase_window, get_risk_level_label
)

# Page config
st.set_page_config(page_title="Forecast & Risk", page_icon="🤖", layout="wide")

st.title("🤖 AI-Powered Forecast & Risk Analysis")
st.markdown("### Hybrid Decision System: Demand Forecasting + Disruption Risk + Purchase Timing")
st.markdown("---")

# Load data
with st.spinner("Loading data..."):
    df = load_main_dataset()

if df is None:
    st.error("Unable to load dataset.")
    st.stop()

# Sidebar controls
st.sidebar.header("🎯 Analysis Parameters")

products = get_unique_products(df)
locations = get_unique_locations(df)

if not products or not locations:
    st.error("No products or locations found.")
    st.stop()

selected_product = st.sidebar.selectbox("Select Product", products, index=0)
selected_location = st.sidebar.selectbox("Select Location", locations, index=0)
forecast_horizon = st.sidebar.slider("Forecast Horizon (days)", 7, 60, 30, 1)

st.sidebar.markdown("---")
risk_threshold = st.sidebar.slider("Risk Threshold (%)", 10, 50, 30, 5) / 100

st.sidebar.markdown("---")
run_analysis = st.sidebar.button("🚀 Run Analysis", type="primary", use_container_width=True)

# Filter data
filtered_df = filter_data(df, product=selected_product, location=selected_location)

if filtered_df is None or len(filtered_df) == 0:
    st.warning(f"No data for {selected_product} at {selected_location}")
    st.stop()

# Historical section
st.subheader(f"📊 Historical Sales: {selected_product} @ {selected_location}")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", f"{filtered_df['units_sold'].sum():,.0f}" if 'units_sold' in filtered_df.columns else "N/A")
with col2:
    st.metric("Avg Daily Sales", f"{filtered_df['units_sold'].mean():,.1f}" if 'units_sold' in filtered_df.columns else "N/A")
with col3:
    st.metric("Data Points", f"{len(filtered_df):,}")

# Historical chart
if 'date' in filtered_df.columns and 'units_sold' in filtered_df.columns:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'], y=filtered_df['units_sold'],
        mode='lines+markers', name='Historical Sales',
        line=dict(color='#1f77b4', width=2), marker=dict(size=4)
    ))
    fig.update_layout(title='Historical Sales Trend', xaxis_title='Date',
                     yaxis_title='Units Sold', hovermode='x unified', height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Analysis section
if run_analysis:
    st.subheader("🔮 AI Prediction Results")
    
    with st.spinner("Generating forecasts and analyzing risks..."):
        future_df = create_future_dataframe(filtered_df, forecast_horizon)
        
        if future_df is None or len(future_df) == 0:
            st.error("Unable to create future dataframe.")
            st.stop()
        
        demand_predictions = forecast_demand(future_df)
        future_df['predicted_demand'] = demand_predictions
        
        risk_predictions = predict_disruption(future_df)
        future_df['risk_probability'] = risk_predictions
        
        start_date, end_date, num_safe_days = calculate_safe_purchase_window(
            future_df['date'], future_df['risk_probability'], threshold=risk_threshold
        )
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Forecast", f"{future_df['predicted_demand'].sum():,.0f}")
    with col2:
        st.metric("Avg Daily Forecast", f"{future_df['predicted_demand'].mean():,.1f}")
    with col3:
        avg_risk = future_df['risk_probability'].mean()
        risk_color = "🟢" if avg_risk < 0.3 else "🟡" if avg_risk < 0.6 else "🔴"
        st.metric(f"{risk_color} Avg Risk", f"{avg_risk*100:.1f}%")
    with col4:
        if num_safe_days > 0:
            st.metric("Safe Days", f"{num_safe_days}", delta="Low Risk")
        else:
            st.metric("Safe Days", "0", delta="High Risk", delta_color="inverse")
    
    st.markdown("---")
    
    # Hybrid Decision Logic - Combined View
    st.subheader("🎯 Hybrid Decision System")
    
    # Create combined chart showing demand, risk, and purchase window
    fig = go.Figure()
    
    # Add demand forecast (on primary y-axis)
    fig.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['predicted_demand'],
        mode='lines+markers',
        name='Demand Forecast',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=6),
        yaxis='y'
    ))
    
    # Add risk probability (on secondary y-axis)
    fig.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['risk_probability'] * 100,
        mode='lines+markers',
        name='Risk Probability',
        line=dict(color='#e74c3c', width=2, dash='dash'),
        marker=dict(size=5),
        yaxis='y2'
    ))
    
    # Highlight safe purchase window
    if num_safe_days > 0:
        safe_mask = future_df['risk_probability'] < risk_threshold
        safe_dates = future_df[safe_mask]['date']
        safe_demand = future_df[safe_mask]['predicted_demand']
        
        fig.add_trace(go.Scatter(
            x=safe_dates,
            y=safe_demand,
            mode='markers',
            name='Safe Purchase Window',
            marker=dict(size=12, color='gold', symbol='star', line=dict(color='orange', width=2)),
            yaxis='y'
        ))
    
    # Add risk threshold line
    fig.add_hline(
        y=risk_threshold * 100,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"Risk Threshold ({risk_threshold*100:.0f}%)",
        annotation_position="right",
        yref='y2'
    )
    
    fig.update_layout(
        title='Hybrid Decision View: Demand + Risk + Purchase Window',
        xaxis_title='Date',
        yaxis=dict(title='Demand (Units)', side='left', showgrid=False),
        yaxis2=dict(title='Risk Probability (%)', side='right', overlaying='y', range=[0, 100]),
        hovermode='x unified',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Individual charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Demand Forecast")
        
        fig_demand = go.Figure()
        
        # Historical (last 90 days)
        if 'date' in filtered_df.columns and 'units_sold' in filtered_df.columns:
            fig_demand.add_trace(go.Scatter(
                x=filtered_df['date'].tail(90), y=filtered_df['units_sold'].tail(90),
                mode='lines', name='Historical',
                line=dict(color='#95a5a6', width=2), opacity=0.7
            ))
        
        # Forecast
        fig_demand.add_trace(go.Scatter(
            x=future_df['date'], y=future_df['predicted_demand'],
            mode='lines+markers', name='Forecast',
            line=dict(color='#2ecc71', width=3), marker=dict(size=6)
        ))
        
        fig_demand.update_layout(
            xaxis_title='Date', yaxis_title='Units',
            hovermode='x unified', height=350,
            legend=dict(orientation="h")
        )
        
        st.plotly_chart(fig_demand, use_container_width=True)
    
    with col2:
        st.markdown("### ⚠️ Disruption Risk")
        
        fig_risk = go.Figure()
        
        fig_risk.add_trace(go.Scatter(
            x=future_df['date'], y=future_df['risk_probability'] * 100,
            mode='lines+markers', name='Risk',
            line=dict(color='#e74c3c', width=3), marker=dict(size=6),
            fill='tozeroy', fillcolor='rgba(231, 76, 60, 0.2)'
        ))
        
        fig_risk.add_hline(
            y=risk_threshold * 100, line_dash="dash", line_color="green",
            annotation_text=f"Safe ({risk_threshold*100:.0f}%)"
        )
        
        fig_risk.update_layout(
            xaxis_title='Date', yaxis_title='Risk %',
            hovermode='x unified', height=350,
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    st.markdown("---")
    
    # Hybrid Decision Recommendation
    st.subheader("✅ Hybrid Purchase Recommendation")
    
    if num_safe_days > 0:
        # Calculate optimal purchase quantity
        safe_period_demand = future_df[future_df['risk_probability'] < risk_threshold]['predicted_demand'].sum()
        avg_safe_demand = safe_period_demand / num_safe_days
        
        st.success(f"""
        **✅ RECOMMENDED PURCHASE WINDOW IDENTIFIED**
        
        **📅 Timing:**
        - Start: {start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date}
        - End: {end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date}
        - Duration: {num_safe_days} days
        
        **📊 Demand Analysis:**
        - Expected demand during window: {safe_period_demand:.0f} units
        - Average daily demand: {avg_safe_demand:.1f} units
        - Risk level: Below {risk_threshold*100:.0f}% (SAFE)
        
        **💡 Recommendation:**
        - **Optimal action:** Place orders during this window
        - **Suggested quantity:** {safe_period_demand * 1.1:.0f} units (includes 10% safety buffer)
        - **Priority:** HIGH - Low risk period with stable demand
        """)
        
        # Risk scenario alerts
        high_risk_days = np.sum(future_df['risk_probability'] > 0.7)
        if high_risk_days > 0:
            st.warning(f"""
            ⚠️ **RISK ALERT:** {high_risk_days} days with very high disruption risk (>70%) detected.
            Consider increasing safety stock or activating backup suppliers.
            """)
    else:
        st.error(f"""
        **⚠️ NO SAFE PURCHASE WINDOW FOUND**
        
        All forecasted days have disruption risk above {risk_threshold*100:.0f}%.
        
        **🚨 Critical Recommendations:**
        1. **Immediate Action Required:**
           - Increase safety stock to 150-200% of normal levels
           - Activate backup suppliers immediately
           - Consider alternative sourcing locations
        
        2. **Risk Mitigation:**
           - Split orders across multiple time periods
           - Use expedited shipping for critical items
           - Monitor situation daily for improvements
        
        3. **Demand Management:**
           - Expected demand: {future_df['predicted_demand'].sum():.0f} units
           - Average risk: {future_df['risk_probability'].mean()*100:.1f}%
           - Consider postponing non-critical orders
        """)
    
    st.markdown("---")
    
    # Detailed forecast table
    st.subheader("📋 Detailed Forecast Data")
    
    display_df = future_df[['date', 'predicted_demand', 'risk_probability']].copy()
    display_df['risk_percentage'] = (display_df['risk_probability'] * 100).round(1)
    display_df['risk_level'] = display_df['risk_probability'].apply(get_risk_level_label)
    display_df['is_safe'] = display_df['risk_probability'] < risk_threshold
    display_df['recommendation'] = display_df['is_safe'].map({
        True: '✅ Safe to Purchase',
        False: '⚠️ High Risk - Avoid'
    })
    
    display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d')
    display_df['predicted_demand'] = display_df['predicted_demand'].round(0).astype(int)
    
    display_df = display_df.rename(columns={
        'date': 'Date',
        'predicted_demand': 'Forecasted Demand',
        'risk_percentage': 'Risk %',
        'risk_level': 'Risk Level',
        'recommendation': 'Recommendation'
    })
    
    display_df = display_df.drop('risk_probability', axis=1)
    display_df = display_df.drop('is_safe', axis=1)
    
    st.dataframe(display_df, use_container_width=True, height=400, hide_index=True)
    
    # Download
    csv = display_df.to_csv(index=False)
    st.download_button(
        "📥 Download Forecast (CSV)", data=csv,
        file_name=f"forecast_{selected_product}_{selected_location}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    st.info("""
    👈 **Configure parameters and click 'Run Analysis'**
    
    **The Hybrid AI System will:**
    1. 🔮 **Forecast demand** using XGBoost model
    2. ⚠️ **Predict disruption risk** using risk classifier
    3. ✅ **Identify safe purchase windows** where demand is high and risk is low
    4. 💡 **Provide actionable recommendations** for optimal procurement timing
    
    **Key Features:**
    - Historical sales analysis
    - AI-powered demand forecasting
    - Supply chain disruption risk assessment
    - Hybrid decision logic combining demand + risk
    - Best time to purchase recommendations
    """)

st.markdown("---")
st.caption("💡 The hybrid system combines demand forecasting with risk prediction to identify optimal purchase timing.")
