"""
Backend Package
===============
Contains all backend logic for data processing, model loading, and predictions.
"""

from .data_utils import load_main_dataset, get_unique_products, get_unique_locations, filter_data
from .model_loader import load_forecast_model, load_risk_model, check_models_exist, load_baseline_models, get_model_info
from .forecasting import forecast_demand, create_future_dataframe
from .disruption import predict_disruption, calculate_safe_purchase_window, get_risk_level_label
from .model_comparison import get_model_performance_metrics, compare_models_on_sample, get_best_model
from .scenario_simulation import ScenarioSimulator

__all__ = [
    'load_main_dataset',
    'get_unique_products',
    'get_unique_locations',
    'filter_data',
    'load_forecast_model',
    'load_risk_model',
    'check_models_exist',
    'load_baseline_models',
    'get_model_info',
    'forecast_demand',
    'create_future_dataframe',
    'predict_disruption',
    'calculate_safe_purchase_window',
    'get_risk_level_label',
    'get_model_performance_metrics',
    'compare_models_on_sample',
    'get_best_model',
    'ScenarioSimulator'
]
