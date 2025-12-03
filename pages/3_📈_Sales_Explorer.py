"""
Sales Explorer Page
===================
Interactive data exploration with advanced filtering capabilities.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend import load_main_dataset

# Page configuration
st.set_page_config(
    page_title="Sales Explorer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Data Explorer")
st.markdown("### Advanced Filtering and Analytics")
st.markdown("---")

# Load data
with st.spinner("Loading data..."):
    df = load_main_dataset()

if df is None:
    st.error("Unable to load dataset. Please check the data file location.")
    st.stop()

# ============================================================
# Advanced Sidebar Filters
# ============================================================
st.sidebar.header("🔍 Filter Options")

# Product filter (multi-select)
if 'product' in df.columns:
    all_products = sorted(df['product'].unique().tolist())
    
    st.sidebar.markdown(f"**Select Products** ({len(all_products)} available)")
    
    # Multi-select for products - always visible
    selected_products = st.sidebar.multiselect(
        "Choose products to analyze:",
        options=all_products,
        default=all_products,  # All selected by default
        help=f"Select from {len(all_products)} products. Clear all and reselect to filter."
    )
    
    # If nothing selected, use all products
    if not selected_products:
        selected_products = all_products
        st.sidebar.warning("⚠️ No products selected - showing all")
else:
    selected_products = []

st.sidebar.markdown("---")

# Location filter with search
if 'location' in df.columns:
    all_locations = sorted(df['location'].unique().tolist())
    
    st.sidebar.markdown(f"**Select Locations** ({len(all_locations)} available)")
    
    # Search box for locations
    location_search = st.sidebar.text_input(
        "🔎 Search cities:",
        placeholder="Type to filter cities...",
        help="Search for specific cities"
    )
    
    # Filter locations based on search
    if location_search:
        filtered_locations = [loc for loc in all_locations if location_search.lower() in loc.lower()]
        st.sidebar.info(f"Found {len(filtered_locations)} matching cities")
    else:
        filtered_locations = all_locations
    
    # Multi-select for locations - always visible
    # Show top 50 by default or search results
    default_locs = filtered_locations[:50] if len(filtered_locations) >= 50 else filtered_locations
    
    selected_locations = st.sidebar.multiselect(
        "Choose locations to analyze:",
        options=filtered_locations,
        default=default_locs,
        help=f"Select from {len(filtered_locations)} locations. Use search to find specific cities."
    )
    
    # If nothing selected, use all locations
    if not selected_locations:
        selected_locations = all_locations
        st.sidebar.warning("⚠️ No locations selected - showing all")
else:
    selected_locations = []

st.sidebar.markdown("---")

# Category filter (if available)
if 'category' in df.columns:
    all_categories = ["All"] + sorted(df['category'].unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Product Category",
        options=all_categories,
        index=0
    )
else:
    selected_category = "All"

# Region filter (if available)
if 'region' in df.columns:
    all_regions = ["All"] + sorted(df['region'].unique().tolist())
    selected_region = st.sidebar.selectbox(
        "Region",
        options=all_regions,
        index=0
    )
else:
    selected_region = "All"

# Customer Segment filter (if available)
if 'segment' in df.columns:
    all_segments = ["All"] + sorted(df['segment'].unique().tolist())
    selected_segment = st.sidebar.selectbox(
        "Customer Segment",
        options=all_segments,
        index=0
    )
else:
    selected_segment = "All"

st.sidebar.markdown("---")

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

st.sidebar.markdown("---")

# Sales range filter
if 'units_sold' in df.columns:
    min_sales = float(df['units_sold'].min())
    max_sales = float(df['units_sold'].max())
    
    sales_range = st.sidebar.slider(
        "Sales Range",
        min_value=min_sales,
        max_value=max_sales,
        value=(min_sales, max_sales),
        help="Filter by sales amount"
    )
else:
    sales_range = None

# Apply filters button
st.sidebar.markdown("---")
apply_filters = st.sidebar.button("🔄 Apply Filters", type="primary", use_container_width=True)
reset_filters = st.sidebar.button("🔃 Reset All Filters", use_container_width=True)

# ============================================================
# Apply Filters
# ============================================================
if reset_filters:
    st.rerun()

if apply_filters or 'filtered_df' not in st.session_state:
    filtered_df = df.copy()
    
    # Apply product filter
    if selected_products and 'product' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['product'].isin(selected_products)]
    
    # Apply location filter
    if selected_locations and 'location' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_locations)]
    
    # Apply category filter
    if selected_category != "All" and 'category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Apply region filter
    if selected_region != "All" and 'region' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    # Apply segment filter
    if selected_segment != "All" and 'segment' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['segment'] == selected_segment]
    
    # Apply date range filter
    if 'date' in filtered_df.columns and start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= start_date) &
            (filtered_df['date'].dt.date <= end_date)
        ]
    
    # Apply sales range filter
    if sales_range and 'units_sold' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['units_sold'] >= sales_range[0]) &
            (filtered_df['units_sold'] <= sales_range[1])
        ]
    
    st.session_state.filtered_df = filtered_df
else:
    filtered_df = st.session_state.filtered_df

# Use filtered data for display
display_df = filtered_df if filtered_df is not None and len(filtered_df) > 0 else df

# ============================================================
# Display Active Filters
# ============================================================
st.subheader("🎯 Active Filters")

filter_tags = []

# Check if products are filtered
if 'product' in df.columns:
    all_products_count = df['product'].nunique()
    if len(selected_products) < all_products_count:
        filter_tags.append(f"**Products:** {len(selected_products)}/{all_products_count} selected")

# Check if locations are filtered  
if 'location' in df.columns:
    all_locations_count = df['location'].nunique()
    if len(selected_locations) < all_locations_count:
        filter_tags.append(f"**Locations:** {len(selected_locations)}/{all_locations_count} selected")

if selected_category != "All":
    filter_tags.append(f"**Category:** {selected_category}")
if selected_region != "All":
    filter_tags.append(f"**Region:** {selected_region}")
if selected_segment != "All":
    filter_tags.append(f"**Segment:** {selected_segment}")
if start_date and end_date:
    filter_tags.append(f"**Date:** {start_date} to {end_date}")

if filter_tags:
    st.info(" | ".join(filter_tags))
else:
    st.info("**No filters applied** - Showing all data")

st.markdown("---")

# ============================================================
# Summary Metrics
# ============================================================
st.subheader("📊 Summary Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_records = len(display_df)
    st.metric("Total Records", f"{total_records:,}")

with col2:
    if 'units_sold' in display_df.columns:
        total_sales = display_df['units_sold'].sum()
        st.metric("Total Sales", f"${total_sales:,.2f}")

with col3:
    if 'units_sold' in display_df.columns:
        avg_sales = display_df['units_sold'].mean()
        st.metric("Avg Sales", f"${avg_sales:,.2f}")

with col4:
    if 'product' in display_df.columns:
        unique_products = display_df['product'].nunique()
        st.metric("Unique Products", f"{unique_products}")

with col5:
    if 'location' in display_df.columns:
        unique_locations = display_df['location'].nunique()
        st.metric("Unique Locations", f"{unique_locations}")

st.markdown("---")

# ============================================================
# Sales Trend Over Time
# ============================================================
st.subheader("📅 Sales Trend Over Time")

if 'date' in display_df.columns and 'units_sold' in display_df.columns:
    # Time aggregation selector
    time_agg = st.selectbox(
        "Aggregation Level",
        ["Daily", "Weekly", "Monthly"],
        index=2
    )
    
    trend_df = display_df.copy()
    
    if time_agg == "Daily":
        trend_df['period'] = trend_df['date'].dt.date
    elif time_agg == "Weekly":
        trend_df['period'] = trend_df['date'].dt.to_period('W').astype(str)
    else:  # Monthly
        trend_df['period'] = trend_df['date'].dt.to_period('M').astype(str)
    
    sales_trend = trend_df.groupby('period')['units_sold'].sum().reset_index()
    
    fig = px.line(
        sales_trend,
        x='period',
        y='units_sold',
        title=f'{time_agg} Sales Trend',
        labels={'period': 'Period', 'units_sold': 'Sales ($)'},
        markers=True
    )
    
    fig.update_layout(
        hovermode='x unified',
        height=450
    )
    
    fig.update_traces(line_color='#1f77b4', line_width=2)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Date or sales column not found.")

st.markdown("---")

# ============================================================
# Distribution Analysis
# ============================================================
st.subheader("📊 Distribution Analysis")

tab1, tab2, tab3 = st.tabs(["By Product", "By Location", "By Category"])

with tab1:
    if 'product' in display_df.columns and 'units_sold' in display_df.columns:
        product_sales = display_df.groupby('product')['units_sold'].sum().sort_values(ascending=False).head(15)
        
        fig = px.bar(
            x=product_sales.values,
            y=product_sales.index,
            orientation='h',
            title='Top 15 Products by Sales',
            labels={'x': 'Total Sales ($)', 'y': 'Product'},
            color=product_sales.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(showlegend=False, height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Product or sales data not available.")

with tab2:
    if 'location' in display_df.columns and 'units_sold' in display_df.columns:
        location_sales = display_df.groupby('location')['units_sold'].sum().sort_values(ascending=False).head(20)
        
        fig = px.bar(
            x=location_sales.index,
            y=location_sales.values,
            title='Top 20 Locations by Sales',
            labels={'x': 'Location', 'y': 'Total Sales ($)'},
            color=location_sales.values,
            color_continuous_scale='Greens'
        )
        
        fig.update_layout(showlegend=False, height=500, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Location or sales data not available.")

with tab3:
    if 'category' in display_df.columns and 'units_sold' in display_df.columns:
        category_sales = display_df.groupby('category')['units_sold'].sum().sort_values(ascending=False)
        
        fig = px.pie(
            values=category_sales.values,
            names=category_sales.index,
            title='Sales Distribution by Category',
            hole=0.4
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Category data not available.")

st.markdown("---")

# ============================================================
# Data Table
# ============================================================
st.subheader("🔍 Filtered Data Preview")

# Show number of rows selector
num_rows = st.selectbox(
    "Number of rows to display:",
    options=[10, 25, 50, 100, 200, "All"],
    index=0
)

if num_rows == "All":
    preview_df = display_df
else:
    preview_df = display_df.head(num_rows)

st.dataframe(
    preview_df,
    use_container_width=True,
    height=400
)

# Download button
csv = display_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name=f"sales_data_filtered_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption(f"💡 Showing {len(display_df):,} records out of {len(df):,} total records. Use filters to refine your analysis.")
