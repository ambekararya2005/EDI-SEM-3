"""
Scenario / What-If Simulation Page
===================================
Run business scenario simulations and see impact on demand and risk.
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
    load_main_dataset,
    get_unique_products,
    get_unique_locations,
    filter_data,
    forecast_demand,
    create_future_dataframe,
    predict_disruption,
    ScenarioSimulator
)

# Page config
st.set_page_config(
    page_title="Scenario Simulation",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Scenario / What-If Simulation")
st.markdown("---")

# Introduction
st.markdown("""
Simulate different business scenarios and see how they impact demand forecasts and disruption risks.
This helps in **proactive planning** and **risk mitigation**.
""")

st.markdown("---")

# Load data
with st.spinner("Loading data..."):
    df = load_main_dataset()

if df is None:
    st.error("Unable to load dataset.")
    st.stop()

# Sidebar - Scenario Configuration
st.sidebar.header("🎯 Scenario Configuration")

# Product and location selection
products = get_unique_products(df)
locations = get_unique_locations(df)

if not products or not locations:
    st.error("No products or locations found.")
    st.stop()

selected_product = st.sidebar.selectbox("Select Product", products, index=0)
selected_location = st.sidebar.selectbox("Select Location", locations, index=0)

# Forecast horizon
forecast_horizon = st.sidebar.slider("Forecast Horizon (days)", 7, 60, 30, 1)

st.sidebar.markdown("---")

# Scenario selection
st.sidebar.subheader("📋 Select Scenario")

scenarios = ScenarioSimulator.get_available_scenarios()
scenario_names = list(scenarios.values())
scenario_keys = list(scenarios.keys())

selected_scenario_name = st.sidebar.selectbox(
    "Scenario Type",
    scenario_names,
    index=0
)

selected_scenario = scenario_keys[scenario_names.index(selected_scenario_name)]

# Severity level
severity = st.sidebar.select_slider(
    "Severity Level",
    options=['low', 'medium', 'high'],
    value='medium'
)

st.sidebar.markdown("---")

# Risk threshold
risk_threshold = st.sidebar.slider(
    "Risk Threshold (%)",
    min_value=10,
    max_value=50,
    value=30,
    step=5
) / 100

st.sidebar.markdown("---")

run_simulation = st.sidebar.button("🚀 Run Simulation", type="primary", use_container_width=True)

# Main content
# Filter data
filtered_df = filter_data(df, product=selected_product, location=selected_location)

if filtered_df is None or len(filtered_df) == 0:
    st.warning(f"No data for {selected_product} at {selected_location}")
    st.stop()

# Display scenario description
st.subheader(f"📋 Scenario: {selected_scenario_name}")

scenario_desc = ScenarioSimulator.get_scenario_description(selected_scenario, severity)
st.markdown(scenario_desc)

st.markdown("---")

# Run simulation
if run_simulation:
    st.subheader("🔮 Simulation Results")
    
    with st.spinner("Running simulation..."):
        # Create future dataframe
        future_df = create_future_dataframe(filtered_df, forecast_horizon)
        
        if future_df is None or len(future_df) == 0:
            st.error("Unable to create future dataframe.")
            st.stop()
        
        # Generate baseline forecasts
        baseline_demand = forecast_demand(future_df)
        baseline_risk = predict_disruption(future_df)
        
        # Apply scenario
        scenario_demand, scenario_risk = ScenarioSimulator.apply_scenario(
            baseline_demand,
            baseline_risk,
            selected_scenario,
            severity
        )
        
        future_df['baseline_demand'] = baseline_demand
        future_df['scenario_demand'] = scenario_demand
        future_df['baseline_risk'] = baseline_risk
        future_df['scenario_risk'] = scenario_risk
    
    # Metrics comparison
    st.markdown("### 📊 Impact Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        baseline_total = baseline_demand.sum()
        scenario_total = scenario_demand.sum()
        demand_change = ((scenario_total - baseline_total) / baseline_total * 100) if baseline_total > 0 else 0
        
        st.metric(
            "Total Demand",
            f"{scenario_total:,.0f}",
            f"{demand_change:+.1f}%",
            delta_color="normal" if demand_change > 0 else "inverse"
        )
    
    with col2:
        baseline_avg_demand = baseline_demand.mean()
        scenario_avg_demand = scenario_demand.mean()
        avg_demand_change = scenario_avg_demand - baseline_avg_demand
        
        st.metric(
            "Avg Daily Demand",
            f"{scenario_avg_demand:,.1f}",
            f"{avg_demand_change:+.1f}",
            delta_color="normal" if avg_demand_change > 0 else "inverse"
        )
    
    with col3:
        baseline_avg_risk = baseline_risk.mean()
        scenario_avg_risk = scenario_risk.mean()
        risk_change = (scenario_avg_risk - baseline_avg_risk) * 100
        
        st.metric(
            "Avg Risk Level",
            f"{scenario_avg_risk*100:.1f}%",
            f"{risk_change:+.1f}pp",
            delta_color="inverse"
        )
    
    with col4:
        safe_days = np.sum(scenario_risk < risk_threshold)
        baseline_safe_days = np.sum(baseline_risk < risk_threshold)
        safe_days_change = safe_days - baseline_safe_days
        
        st.metric(
            "Safe Purchase Days",
            f"{safe_days}",
            f"{safe_days_change:+d}",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Demand Forecast Comparison
    st.markdown("### 📈 Demand Forecast: Baseline vs Scenario")
    
    fig_demand = go.Figure()
    
    # Baseline demand
    fig_demand.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['baseline_demand'],
        mode='lines+markers',
        name='Baseline Forecast',
        line=dict(color='#3498db', width=2),
        marker=dict(size=4)
    ))
    
    # Scenario demand
    fig_demand.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['scenario_demand'],
        mode='lines+markers',
        name=f'{selected_scenario_name} ({severity})',
        line=dict(color='#e74c3c', width=3, dash='dash'),
        marker=dict(size=6)
    ))
    
    fig_demand.update_layout(
        title=f'Demand Forecast Comparison',
        xaxis_title='Date',
        yaxis_title='Units',
        hovermode='x unified',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_demand, use_container_width=True)
    
    st.markdown("---")
    
    # Risk Comparison
    st.markdown("### ⚠️ Disruption Risk: Baseline vs Scenario")
    
    fig_risk = go.Figure()
    
    # Baseline risk
    fig_risk.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['baseline_risk'] * 100,
        mode='lines+markers',
        name='Baseline Risk',
        line=dict(color='#2ecc71', width=2),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.1)'
    ))
    
    # Scenario risk
    fig_risk.add_trace(go.Scatter(
        x=future_df['date'],
        y=future_df['scenario_risk'] * 100,
        mode='lines+markers',
        name=f'{selected_scenario_name} ({severity})',
        line=dict(color='#e74c3c', width=3, dash='dash'),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    # Threshold line
    fig_risk.add_hline(
        y=risk_threshold * 100,
        line_dash="dot",
        line_color="orange",
        annotation_text=f"Safe Threshold ({risk_threshold*100:.0f}%)",
        annotation_position="right"
    )
    
    fig_risk.update_layout(
        title='Disruption Risk Probability Comparison',
        xaxis_title='Date',
        yaxis_title='Risk Probability (%)',
        hovermode='x unified',
        height=450,
        yaxis=dict(range=[0, 100]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.markdown("---")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    recommendation = ScenarioSimulator.get_recommendation(
        scenario_demand,
        scenario_risk,
        future_df['date'],
        risk_threshold
    )
    
    st.markdown(recommendation)
    
    st.markdown("---")
    
    # Detailed comparison table
    st.markdown("### 📋 Detailed Comparison Data")
    
    comparison_df = future_df[['date', 'baseline_demand', 'scenario_demand', 'baseline_risk', 'scenario_risk']].copy()
    
    comparison_df['demand_change'] = comparison_df['scenario_demand'] - comparison_df['baseline_demand']
    comparison_df['demand_change_pct'] = (comparison_df['demand_change'] / comparison_df['baseline_demand'] * 100).round(1)
    comparison_df['risk_change'] = ((comparison_df['scenario_risk'] - comparison_df['baseline_risk']) * 100).round(1)
    
    comparison_df['date'] = pd.to_datetime(comparison_df['date']).dt.strftime('%Y-%m-%d')
    comparison_df['baseline_demand'] = comparison_df['baseline_demand'].round(0).astype(int)
    comparison_df['scenario_demand'] = comparison_df['scenario_demand'].round(0).astype(int)
    comparison_df['baseline_risk'] = (comparison_df['baseline_risk'] * 100).round(1)
    comparison_df['scenario_risk'] = (comparison_df['scenario_risk'] * 100).round(1)
    
    comparison_df = comparison_df.rename(columns={
        'date': 'Date',
        'baseline_demand': 'Baseline Demand',
        'scenario_demand': 'Scenario Demand',
        'demand_change': 'Demand Δ',
        'demand_change_pct': 'Demand Δ %',
        'baseline_risk': 'Baseline Risk %',
        'scenario_risk': 'Scenario Risk %',
        'risk_change': 'Risk Δ (pp)'
    })
    
    st.dataframe(comparison_df, use_container_width=True, height=400, hide_index=True)
    
    # Download button
    csv = comparison_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Simulation Results (CSV)",
        data=csv,
        file_name=f"scenario_{selected_scenario}_{severity}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

else:
    # Show instructions
    st.info("""
    👈 **Configure your scenario in the sidebar and click 'Run Simulation'**
    
    **Available Scenarios:**
    - 🎉 **Festival Demand Spike**: Increased demand during festival season
    - 🌧️ **Bad Weather Conditions**: Impact of heavy rainfall or extreme temperatures
    - 🚚 **Logistics Delay**: Supply chain disruption or delivery delays
    - 📢 **Promotional Campaign**: Marketing promotion or discount offer
    - 🏪 **Competitor Action**: Competitor launches similar product or promotion
    
    **How it works:**
    1. Select a product and location
    2. Choose a scenario type
    3. Set the severity level (low/medium/high)
    4. Run the simulation to see impact on demand and risk
    5. Review recommendations for optimal purchasing decisions
    """)

# Footer
st.markdown("---")
st.caption("💡 Scenario simulations help in proactive planning and risk mitigation. Use these insights to make informed procurement decisions.")
