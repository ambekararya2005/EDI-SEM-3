"""
Scenario Simulation Module
===========================
Handles what-if scenario simulations for demand and risk prediction.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class ScenarioSimulator:
    """
    Simulates different business scenarios and their impact on demand and risk.
    """
    
    SCENARIOS = {
        'festival_spike': {
            'name': 'Festival Demand Spike',
            'description': 'Increased demand during festival season',
            'demand_multiplier': {'low': 1.2, 'medium': 1.5, 'high': 2.0},
            'risk_adjustment': {'low': 0.05, 'medium': 0.1, 'high': 0.15}
        },
        'bad_weather': {
            'name': 'Bad Weather Conditions',
            'description': 'Heavy rainfall or extreme temperatures',
            'demand_multiplier': {'low': 0.95, 'medium': 0.85, 'high': 0.7},
            'risk_adjustment': {'low': 0.1, 'medium': 0.2, 'high': 0.35}
        },
        'logistics_delay': {
            'name': 'Logistics Delay',
            'description': 'Supply chain disruption or delivery delays',
            'demand_multiplier': {'low': 1.0, 'medium': 1.0, 'high': 1.0},
            'risk_adjustment': {'low': 0.15, 'medium': 0.3, 'high': 0.5}
        },
        'promotion': {
            'name': 'Promotional Campaign',
            'description': 'Marketing promotion or discount offer',
            'demand_multiplier': {'low': 1.3, 'medium': 1.6, 'high': 2.2},
            'risk_adjustment': {'low': 0.0, 'medium': 0.05, 'high': 0.1}
        },
        'competitor_action': {
            'name': 'Competitor Action',
            'description': 'Competitor launches similar product or promotion',
            'demand_multiplier': {'low': 0.9, 'medium': 0.75, 'high': 0.6},
            'risk_adjustment': {'low': 0.05, 'medium': 0.1, 'high': 0.15}
        }
    }
    
    @classmethod
    def get_available_scenarios(cls) -> Dict[str, str]:
        """Get list of available scenarios with descriptions."""
        return {k: v['name'] for k, v in cls.SCENARIOS.items()}
    
    @classmethod
    def apply_scenario(cls, 
                       demand_forecast: np.ndarray,
                       risk_forecast: np.ndarray,
                       scenario_type: str,
                       severity: str = 'medium') -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply a scenario to modify demand and risk forecasts.
        
        Args:
            demand_forecast: Original demand predictions
            risk_forecast: Original risk predictions
            scenario_type: Type of scenario (e.g., 'festival_spike')
            severity: Severity level ('low', 'medium', 'high')
            
        Returns:
            tuple: (modified_demand, modified_risk)
        """
        
        if scenario_type not in cls.SCENARIOS:
            return demand_forecast, risk_forecast
        
        scenario = cls.SCENARIOS[scenario_type]
        
        # Apply demand multiplier
        demand_mult = scenario['demand_multiplier'].get(severity, 1.0)
        modified_demand = demand_forecast * demand_mult
        
        # Apply risk adjustment
        risk_adj = scenario['risk_adjustment'].get(severity, 0.0)
        modified_risk = np.clip(risk_forecast + risk_adj, 0, 1)
        
        return modified_demand, modified_risk
    
    @classmethod
    def get_scenario_description(cls, scenario_type: str, severity: str) -> str:
        """
        Get detailed description of scenario impact.
        
        Args:
            scenario_type: Type of scenario
            severity: Severity level
            
        Returns:
            str: Description of the scenario impact
        """
        
        if scenario_type not in cls.SCENARIOS:
            return "Unknown scenario"
        
        scenario = cls.SCENARIOS[scenario_type]
        demand_mult = scenario['demand_multiplier'].get(severity, 1.0)
        risk_adj = scenario['risk_adjustment'].get(severity, 0.0)
        
        demand_change = (demand_mult - 1) * 100
        risk_change = risk_adj * 100
        
        description = f"""
**{scenario['name']}** ({severity.upper()} severity)

{scenario['description']}

**Expected Impact:**
- Demand: {'+' if demand_change > 0 else ''}{demand_change:.1f}%
- Risk: +{risk_change:.1f} percentage points

**Interpretation:**
"""
        
        if demand_change > 20:
            description += "- Significant increase in demand expected\n"
        elif demand_change > 0:
            description += "- Moderate increase in demand expected\n"
        elif demand_change < -20:
            description += "- Significant decrease in demand expected\n"
        elif demand_change < 0:
            description += "- Moderate decrease in demand expected\n"
        else:
            description += "- Demand remains stable\n"
        
        if risk_change > 30:
            description += "- Very high disruption risk\n"
        elif risk_change > 15:
            description += "- Elevated disruption risk\n"
        elif risk_change > 0:
            description += "- Slightly increased disruption risk\n"
        else:
            description += "- Risk level unchanged\n"
        
        return description
    
    @classmethod
    def get_recommendation(cls,
                          modified_demand: np.ndarray,
                          modified_risk: np.ndarray,
                          dates: pd.Series,
                          risk_threshold: float = 0.3) -> str:
        """
        Generate recommendation based on scenario simulation.
        
        Args:
            modified_demand: Demand forecast after scenario
            modified_risk: Risk forecast after scenario
            dates: Corresponding dates
            risk_threshold: Threshold for safe risk level
            
        Returns:
            str: Recommendation text
        """
        
        avg_demand = np.mean(modified_demand)
        avg_risk = np.mean(modified_risk)
        max_risk = np.max(modified_risk)
        
        # Find safe periods
        safe_indices = np.where(modified_risk < risk_threshold)[0]
        
        recommendation = "**Recommended Actions:**\n\n"
        
        if len(safe_indices) == 0:
            recommendation += "⚠️ **HIGH ALERT**: No safe purchase window found in this scenario.\n\n"
            recommendation += "**Suggested Actions:**\n"
            recommendation += "- Increase safety stock immediately\n"
            recommendation += "- Activate backup suppliers\n"
            recommendation += "- Consider postponing non-critical orders\n"
            recommendation += "- Monitor situation closely for improvements\n"
        else:
            start_idx = safe_indices[0]
            end_idx = safe_indices[-1]
            start_date = dates.iloc[start_idx] if hasattr(dates, 'iloc') else dates[start_idx]
            end_date = dates.iloc[end_idx] if hasattr(dates, 'iloc') else dates[end_idx]
            
            recommendation += f"✅ **Safe purchase window identified:**\n"
            recommendation += f"- From: {start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date}\n"
            recommendation += f"- To: {end_date.strftime('%Y-%m-%d') if hasattr(end_date, 'strftime') else end_date}\n"
            recommendation += f"- Duration: {len(safe_indices)} days\n\n"
            
            recommendation += "**Suggested Actions:**\n"
            recommendation += f"- Place orders during the safe window\n"
            recommendation += f"- Expected average demand: {avg_demand:.1f} units/day\n"
            
            if avg_risk > 0.5:
                recommendation += "- Maintain higher safety stock due to elevated overall risk\n"
            
            if max_risk > 0.7:
                recommendation += "- Prepare contingency plans for high-risk periods\n"
        
        return recommendation
