"""
Overview Dashboard Page
========================
Displays high-level KPIs, sales trends, and dataset summary with filters.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend import load_main_dataset, get_unique_products, get_unique_locations, filter_data

# Page configuration
st.set_page_config(
    page_title="Overview Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Overview Dashboard")
st.markdown("### SmartRetail Hybrid - Retail Analytics & Forecasting Platform")
st.markdown("---")

# Load data
with st.spinner("Loading data..."):
    df = load_main_dataset()

if df is None:
    st.error("Unable to load dataset. Please check the data file location.")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Product filter
products = ["All"] + get_unique_products(df)
selected_product = st.sidebar.selectbox("Product", products, index=0)

# Location filter
locations = ["All"] + get_unique_locations(df)
selected_location = st.sidebar.selectbox("Location", locations, index=0)

# Date range filter
if 'date' in df.columns:
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
else:
    start_date, end_date = None, None

# Apply filters
filtered_df = filter_data(df, 
                          product=selected_product if selected_product != "All" else None,
                          location=selected_location if selected_location != "All" else None)

if filtered_df is not None and 'date' in filtered_df.columns and start_date and end_date:
    filtered_df = filtered_df[
        (filtered_df['date'].dt.date >= start_date) &
        (filtered_df['date'].dt.date <= end_date)
    ]

# Use filtered data for display
display_df = filtered_df if filtered_df is not None and len(filtered_df) > 0 else df

# ============================================================
# KPI Section
# ============================================================
st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_sales = display_df['units_sold'].sum() if 'units_sold' in display_df.columns else 0
    st.metric(
        label="Total Units Sold",
        value=f"{total_sales:,.0f}"
    )

with col2:
    num_products = display_df['product'].nunique() if 'product' in display_df.columns else 0
    st.metric(
        label="Unique Products",
        value=f"{num_products}"
    )

with col3:
    num_locations = display_df['location'].nunique() if 'location' in display_df.columns else 0
    st.metric(
        label="Locations",
        value=f"{num_locations}"
    )

with col4:
    avg_daily_sales = display_df['units_sold'].mean() if 'units_sold' in display_df.columns else 0
    st.metric(
        label="Avg Daily Sales",
        value=f"{avg_daily_sales:,.1f}"
    )

with col5:
    num_records = len(display_df)
    st.metric(
        label="Total Records",
        value=f"{num_records:,}"
    )

st.markdown("---")

# ============================================================
# Sales Trends
# ============================================================
st.subheader("📅 Sales Trends Over Time")

# Time aggregation selector
time_agg = st.selectbox(
    "Aggregation Level",
    ["Daily", "Weekly", "Monthly", "Yearly"],
    index=2
)

if 'date' in display_df.columns and 'units_sold' in display_df.columns:
    trend_df = display_df.copy()
    
    if time_agg == "Daily":
        trend_df['period'] = trend_df['date'].dt.date
    elif time_agg == "Weekly":
        trend_df['period'] = trend_df['date'].dt.to_period('W').astype(str)
    elif time_agg == "Monthly":
        trend_df['period'] = trend_df['date'].dt.to_period('M').astype(str)
    else:  # Yearly
        trend_df['period'] = trend_df['date'].dt.year
    
    sales_trend = trend_df.groupby('period')['units_sold'].sum().reset_index()
    
    fig = px.line(
        sales_trend,
        x='period',
        y='units_sold',
        title=f'{time_agg} Sales Trend',
        labels={'period': 'Period', 'units_sold': 'Units Sold'},
        markers=True
    )
    
    fig.update_layout(
        hovermode='x unified',
        xaxis_title="Period",
        yaxis_title="Units Sold",
        height=450
    )
    
    fig.update_traces(
        line_color='#1f77b4',
        line_width=3,
        marker=dict(size=8)
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Date or units_sold column not found in dataset.")

st.markdown("---")

# ============================================================
# Product & Location Analytics
# ============================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products by Sales")
    
    if 'product' in display_df.columns and 'units_sold' in display_df.columns:
        top_products = display_df.groupby('product')['units_sold'].sum().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            labels={'x': 'Units Sold', 'y': 'Product'},
            color=top_products.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Product or units_sold column not found.")

with col2:
    st.subheader("📍 Sales Distribution by Location")
    
    if 'location' in display_df.columns and 'units_sold' in display_df.columns:
        location_sales = display_df.groupby('location')['units_sold'].sum().sort_values(ascending=False)
        
        fig = px.pie(
            values=location_sales.values,
            names=location_sales.index,
            title='Sales Distribution by Location',
            hole=0.4
        )
        
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Location or units_sold column not found.")

st.markdown("---")

# ============================================================
# Context Dependency - Weather & Promotion Effects
# ============================================================
st.subheader("🌤️ Context Dependency Analysis")

tab1, tab2, tab3 = st.tabs(["Weather Impact", "Promotion Effect", "Congestion Impact"])

with tab1:
    if all(col in display_df.columns for col in ['temperature', 'units_sold', 'rainfall']):
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature vs Sales
            fig = px.scatter(
                display_df.sample(min(1000, len(display_df))),
                x='temperature',
                y='units_sold',
                title='Temperature vs Sales',
                labels={'temperature': 'Temperature (°C)', 'units_sold': 'Units Sold'},
                trendline='ols',
                opacity=0.6
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rainfall vs Sales
            fig = px.scatter(
                display_df.sample(min(1000, len(display_df))),
                x='rainfall',
                y='units_sold',
                title='Rainfall vs Sales',
                labels={'rainfall': 'Rainfall (mm)', 'units_sold': 'Units Sold'},
                trendline='ols',
                opacity=0.6,
                color_discrete_sequence=['#ff7f0e']
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Weather data not available.")

with tab2:
    if 'promotion_flag' in display_df.columns and 'units_sold' in display_df.columns:
        promo_comparison = display_df.groupby('promotion_flag')['units_sold'].agg(['mean', 'sum', 'count']).reset_index()
        promo_comparison['promotion_flag'] = promo_comparison['promotion_flag'].map({0: 'No Promotion', 1: 'With Promotion'})
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                promo_comparison,
                x='promotion_flag',
                y='mean',
                title='Average Sales: Promotion vs No Promotion',
                labels={'promotion_flag': '', 'mean': 'Avg Units Sold'},
                color='promotion_flag',
                color_discrete_map={'No Promotion': '#e74c3c', 'With Promotion': '#2ecc71'}
            )
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(
                promo_comparison,
                values='sum',
                names='promotion_flag',
                title='Total Sales Distribution',
                color='promotion_flag',
                color_discrete_map={'No Promotion': '#e74c3c', 'With Promotion': '#2ecc71'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Promotion data not available.")

with tab3:
    if 'congestion_index' in display_df.columns and 'units_sold' in display_df.columns:
        fig = px.scatter(
            display_df.sample(min(1000, len(display_df))),
            x='congestion_index',
            y='units_sold',
            title='Congestion Index vs Sales',
            labels={'congestion_index': 'Congestion Index', 'units_sold': 'Units Sold'},
            trendline='ols',
            opacity=0.6,
            color_discrete_sequence=['#9b59b6']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Congestion data not available.")

st.markdown("---")

# ============================================================
# Dataset Preview
# ============================================================
st.subheader("🔍 Dataset Preview")

col1, col2 = st.columns([1, 3])

with col1:
    date_range_str = f"{display_df['date'].min().strftime('%Y-%m-%d')} to {display_df['date'].max().strftime('%Y-%m-%d')}" if 'date' in display_df.columns else 'N/A'
    
    st.info(f"""
    **Dataset Info:**
    - Total Records: {len(display_df):,}
    - Columns: {len(display_df.columns)}
    - Date Range: {date_range_str}
    - Products: {display_df['product'].nunique() if 'product' in display_df.columns else 'N/A'}
    - Locations: {display_df['location'].nunique() if 'location' in display_df.columns else 'N/A'}
    """)

with col2:
    num_rows = st.selectbox("Rows to display:", [10, 25, 50, 100], index=0)
    st.dataframe(
        display_df.head(num_rows),
        use_container_width=True,
        height=300
    )

# Footer
st.markdown("---")
st.caption("💡 Use the sidebar filters to explore different segments of your data. Navigate to other pages for AI predictions and scenario analysis.")
