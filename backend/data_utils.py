"""
Data Utilities Module
=====================
Handles data loading, preprocessing, and standardization.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


@st.cache_data
def load_main_dataset():
    """
    Load and preprocess the main retail supply chain dataset.
    
    This function:
    - Loads the Excel file from data/ directory
    - Standardizes column names
    - Handles missing values
    - Converts date columns to datetime
    
    Returns:
        pd.DataFrame: Preprocessed dataset with standardized columns
    """
    data_path = PROJECT_ROOT / "data" / "Retail-Supply-Chain-Sales-Dataset-With-Weather.xlsx"
    
    if not data_path.exists():
        st.error(f"⚠️ Dataset not found at: {data_path}")
        st.info("Please ensure 'Retail-Supply-Chain-Sales-Dataset-With-Weather.xlsx' is placed in the data/ directory")
        return None
    
    try:
        # Load the Excel file
        df = pd.read_excel(data_path)
        
        # Column mapping for standardization
        # The actual dataset has these columns:
        # Order Date, Sub-Category (product), City (location), Sales (units_sold)
        column_mapping = {
            'Order Date': 'date',
            'Date': 'date',
            'order_date': 'date',
            'Sub-Category': 'product',
            'Product': 'product',
            'product_name': 'product',
            'Category': 'category',
            'City': 'location',
            'Location': 'location',
            'location_name': 'location',
            'State': 'state',
            'Region': 'region',
            'Sales': 'units_sold',
            'units_sold': 'units_sold',
            'sales': 'units_sold',
            'Quantity': 'quantity',
            'Temperature': 'temperature',
            'temp': 'temperature',
            'Rainfall': 'rainfall',
            'rain': 'rainfall',
            'Holiday Flag': 'holiday_flag',
            'holiday': 'holiday_flag',
            'Promotion Flag': 'promotion_flag',
            'promotion': 'promotion_flag',
            'Congestion Index': 'congestion_index',
            'congestion': 'congestion_index',
            'Customer Name': 'customer_name',
            'Segment': 'segment'
        }
        
        # Rename columns based on mapping
        df.rename(columns=column_mapping, inplace=True)
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Handle missing values
        # For numeric columns: fill with median
        numeric_cols = ['units_sold', 'temperature', 'rainfall', 'congestion_index']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # For categorical flags: fill with 0 (no holiday/promotion)
        flag_cols = ['holiday_flag', 'promotion_flag']
        for col in flag_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Drop rows with missing critical data (date, product, location)
        critical_cols = ['date', 'product', 'location']
        existing_critical = [col for col in critical_cols if col in df.columns]
        df.dropna(subset=existing_critical, inplace=True)
        
        # Sort by date
        if 'date' in df.columns:
            df.sort_values('date', inplace=True)
        
        df.reset_index(drop=True, inplace=True)
        
        st.success(f"✅ Dataset loaded successfully! {len(df)} records found.")
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None


def get_unique_products(df):
    """
    Get list of unique products from dataset.
    
    Args:
        df: DataFrame with 'product' column
        
    Returns:
        list: Sorted list of unique products
    """
    if df is None or 'product' not in df.columns:
        return []
    return sorted(df['product'].unique().tolist())


def get_unique_locations(df):
    """
    Get list of unique locations from dataset.
    
    Args:
        df: DataFrame with 'location' column
        
    Returns:
        list: Sorted list of unique locations
    """
    if df is None or 'location' not in df.columns:
        return []
    return sorted(df['location'].unique().tolist())


def filter_data(df, product=None, location=None):
    """
    Filter dataset by product and/or location.
    
    Args:
        df: Input DataFrame
        product: Product name to filter (None for all)
        location: Location name to filter (None for all)
        
    Returns:
        pd.DataFrame: Filtered dataset
    """
    if df is None:
        return None
    
    filtered_df = df.copy()
    
    if product and product != "All":
        filtered_df = filtered_df[filtered_df['product'] == product]
    
    if location and location != "All":
        filtered_df = filtered_df[filtered_df['location'] == location]
    
    return filtered_df
