"""
SmartRetail Hybrid Dashboard - Main Entry Point
================================================
This is the landing page for the multipage Streamlit application.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SmartRetail Hybrid Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main landing page
st.title("🛒 SmartRetail Hybrid Dashboard")
st.markdown("### AI-Powered Retail Demand Forecasting & Supply Chain Risk Management")
st.markdown("---")

# Project description
st.markdown("""
## Welcome to the SmartRetail Hybrid Intelligence Platform

This application combines **demand forecasting**, **disruption risk prediction**, and **hybrid decision logic** 
to help you make smarter retail supply chain decisions.

### 🎯 Key Capabilities:
- **AI-Powered Forecasting**: XGBoost model for accurate demand prediction
- **Risk Assessment**: Disruption probability analysis with contextual factors
- **Hybrid Decision System**: Combines demand + risk for optimal purchase timing
- **Scenario Simulation**: What-if analysis for proactive planning
- **Model Comparison**: Performance benchmarking across multiple algorithms
""")

st.markdown("---")

# Page overview
st.markdown("## 📱 Dashboard Pages")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 1️⃣ 📊 Overview Dashboard
    **Get a bird's-eye view of your retail operations**
    - Key performance indicators (KPIs)
    - Sales trends (daily/weekly/monthly/yearly)
    - Top products and location analysis
    - Context dependency (weather, promotions, congestion)
    - Interactive filters for deep-dive analysis
    """)
    
    st.markdown("""
    ### 2️⃣ 🤖 Forecast & Risk Prediction
    **AI-powered predictions and recommendations**
    - Demand forecasting using XGBoost
    - Disruption risk probability
    - **Hybrid decision logic**: Best time to purchase
    - Safe purchase window identification
    - Risk alerts and mitigation strategies
    """)
    
    st.markdown("""
    ### 3️⃣ 📈 Sales Data Explorer
    **Interactive data exploration and analytics**
    - Advanced filtering (product, location, date)
    - Sales trend visualization
    - Distribution analysis
    - Data export capabilities
    """)

with col2:
    st.markdown("""
    ### 4️⃣ 📊 Model Performance & Insights
    **Compare and evaluate forecasting models**
    - Performance metrics (RMSE, MAE, MAPE, R²)
    - Model comparison: XGBoost vs ARIMA vs Prophet vs LSTM
    - Visual performance analysis
    - Best model recommendations
    - Radar charts and multi-metric views
    """)
    
    st.markdown("""
    ### 5️⃣ 🧪 Scenario Simulation
    **What-if analysis for proactive planning**
    - Simulate business scenarios:
      - Festival demand spikes
      - Bad weather conditions
      - Logistics delays
      - Promotional campaigns
      - Competitor actions
    - See impact on demand and risk
    - Get scenario-specific recommendations
    """)

st.markdown("---")

# Feature highlights
st.markdown("## ✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    **🤖 AI & Machine Learning**
    
    - XGBoost gradient boosting
    - Risk classification models
    - Baseline model comparisons
    - Feature engineering pipeline
    """)

with col2:
    st.success("""
    **📊 Analytics & Insights**
    
    - Historical sales analysis
    - Trend identification
    - Context dependency analysis
    - Performance benchmarking
    """)

with col3:
    st.warning("""
    **🎯 Decision Support**
    
    - Hybrid recommendation system
    - Safe purchase windows
    - Risk mitigation strategies
    - Scenario planning
    """)

st.markdown("---")

# Technology stack
st.markdown("## 🔧 Technology Stack")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **Frontend**
    - Streamlit
    - Plotly
    """)

with col2:
    st.markdown("""
    **ML Models**
    - XGBoost
    - Scikit-learn
    """)

with col3:
    st.markdown("""
    **Data Processing**
    - Pandas
    - NumPy
    """)

with col4:
    st.markdown("""
    **Features**
    - Time series
    - Weather data
    - Contextual factors
    """)

st.markdown("---")

# Getting started
st.markdown("## 🚀 Getting Started")

st.markdown("""
1. **Explore Overview** → Understand your current sales patterns and trends
2. **Run Forecasts** → Get AI predictions for demand and risk
3. **Analyze Scenarios** → Simulate different business conditions
4. **Compare Models** → Evaluate forecasting performance
5. **Make Decisions** → Use hybrid recommendations for optimal procurement

👈 **Use the sidebar to navigate between pages**
""")

st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>SmartRetail Hybrid © 2025</strong></p>
    <p>Powered by XGBoost, Streamlit & Advanced Analytics</p>
    <p>🎓 VIT SY | EDI SEM_3 Project</p>
</div>
""", unsafe_allow_html=True)
