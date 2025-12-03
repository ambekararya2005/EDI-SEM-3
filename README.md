# 🛒 SmartRetail Hybrid Dashboard

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-orange?style=for-the-badge)](https://xgboost.readthedocs.io/)

**AI-Powered Retail Demand Forecasting & Supply Chain Risk Management Platform**

A comprehensive multipage Streamlit application that combines demand forecasting, disruption risk prediction, and hybrid decision logic to optimize retail supply chain decisions.

---

## 🎯 Key Features

### 🤖 AI & Machine Learning
- **XGBoost Demand Forecasting**: Gradient boosting model for accurate demand prediction
- **Risk Classification**: Disruption probability analysis with contextual factors
- **Baseline Model Comparison**: Performance benchmarking (ARIMA, Prophet, LSTM, XGBoost)
- **Advanced Feature Engineering**: Time features, lag features, rolling statistics, one-hot encoding

### 📊 Analytics & Insights
- **Historical Sales Analysis**: Trends, patterns, and distributions
- **Context Dependency Analysis**: Weather, promotions, congestion impact
- **Performance Benchmarking**: Multi-metric model comparison
- **Interactive Visualizations**: Plotly charts with drill-down capabilities

### 🎯 Decision Support
- **Hybrid Recommendation System**: Combines demand + risk for optimal timing
- **Safe Purchase Windows**: Identifies low-risk, high-demand periods
- **Risk Mitigation Strategies**: Scenario-specific recommendations
- **What-If Scenario Planning**: Simulate business conditions

---

## 📱 Dashboard Pages

### 1️⃣ Overview Dashboard
- Key performance indicators (KPIs)
- Sales trends (daily/weekly/monthly/yearly)
- Top products and location analysis
- Context dependency (weather, promotions, congestion)
- Interactive filters for deep-dive analysis

### 2️⃣ Forecast & Risk Prediction
- AI-powered demand forecasting using XGBoost
- Disruption risk probability prediction
- **Hybrid decision logic**: Best time to purchase recommendations
- Safe purchase window identification
- Risk alerts and mitigation strategies

### 3️⃣ Sales Data Explorer
- Advanced filtering (17 products, 531 locations)
- Multi-select product filter
- Searchable location filter
- Category, region, and segment filters
- Sales range and date range filters
- Distribution analysis and data export

### 4️⃣ Model Performance & Insights
- Performance metrics (RMSE, MAE, MAPE, R²)
- Model comparison: XGBoost vs ARIMA vs Prophet vs LSTM
- Visual performance analysis (bar charts, radar charts)
- Best model recommendations

### 5️⃣ Scenario Simulation
- What-if analysis for proactive planning
- 5 business scenarios:
  - Festival demand spikes
  - Bad weather conditions
  - Logistics delays
  - Promotional campaigns
  - Competitor actions
- Impact visualization on demand and risk
- Scenario-specific recommendations

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/smartretail-hybrid-dashboard.git
cd smartretail-hybrid-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Add your data and models**
   - Place your dataset in `data/` folder:
     - `Retail-Supply-Chain-Sales-Dataset-With-Weather.xlsx`
   - Place your trained models in `models/` folder:
     - `xgboost_forecast.pkl`
     - `risk_classifier.pkl`

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
   - Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
smartretail_app/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── SETUP_GUIDE.md                 # Detailed setup instructions
│
├── backend/                        # Backend logic
│   ├── __init__.py
│   ├── model_loader.py            # Model loading utilities
│   ├── data_utils.py              # Data preprocessing
│   ├── forecasting.py             # Demand forecasting
│   ├── disruption.py              # Risk prediction
│   ├── model_comparison.py        # Model performance comparison
│   └── scenario_simulation.py     # Scenario simulation logic
│
├── models/                         # ML models (gitignored)
│   ├── .gitkeep
│   ├── xgboost_forecast.pkl       # XGBoost demand model
│   └── risk_classifier.pkl        # Risk classification model
│
├── data/                           # Dataset (gitignored)
│   ├── .gitkeep
│   └── Retail-Supply-Chain-Sales-Dataset-With-Weather.xlsx
│
└── pages/                          # Streamlit pages
    ├── 1_📊_Overview.py
    ├── 2_🤖_Forecast_and_Risk.py
    ├── 3_📈_Sales_Explorer.py
    ├── 4_📊_Model_Performance.py
    └── 5_🧪_Scenario_Simulation.py
```

---

## 🔧 Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly |
| **ML Models** | XGBoost, Scikit-learn |
| **Data Processing** | Pandas, NumPy |
| **Features** | Time series, Weather data, Contextual factors |

---

## 📊 Dataset Requirements

The application expects an Excel file with the following columns:

| Column | Description | Type |
|--------|-------------|------|
| `Order Date` | Transaction date | Date |
| `Sub-Category` | Product name | String |
| `City` | Location | String |
| `Sales` | Sales amount | Numeric |
| `Category` | Product category | String |
| `Region` | Geographic region | String |
| `Segment` | Customer segment | String |
| `Temperature` | Temperature (°C) | Numeric |
| `Rainfall` | Rainfall (mm) | Numeric |
| `Holiday Flag` | Holiday indicator | Binary (0/1) |
| `Promotion Flag` | Promotion indicator | Binary (0/1) |
| `Congestion Index` | Traffic congestion | Numeric (0-1) |

---

## 🎓 Academic Context

**Project:** SmartRetail Hybrid  
**Institution:** VIT SY  
**Course:** EDI SEM_3  
**Year:** 2025

---

## 📝 License

This project is created for academic purposes.

---

## 🤝 Contributing

This is an academic project. For suggestions or issues, please open an issue on GitHub.

---

## 📧 Contact

For questions or collaboration:
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

## 🙏 Acknowledgments

- **XGBoost**: For the powerful gradient boosting framework
- **Streamlit**: For the amazing web app framework
- **Plotly**: For interactive visualizations
- **VIT SY**: For academic support

---

**Built with ❤️ using Streamlit and XGBoost**
