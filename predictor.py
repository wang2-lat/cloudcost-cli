import pandas as pd
import numpy as np

def predict_next_month(df: pd.DataFrame) -> dict:
    """Predict next month's cost using simple trend analysis"""
    
    daily_costs = df.groupby('date')['cost'].sum()
    
    # Calculate average daily cost
    avg_daily_cost = daily_costs.mean()
    
    # Simple linear trend
    days = np.arange(len(daily_costs))
    costs = daily_costs.values
    
    if len(costs) > 1:
        # Linear regression
        slope = np.polyfit(days, costs, 1)[0]
        # Predict 30 days ahead
        predicted_daily = avg_daily_cost + slope * 30
        predicted_cost = max(predicted_daily * 30, avg_daily_cost * 30)
    else:
        predicted_cost = avg_daily_cost * 30
    
    return {
        'predicted_cost': predicted_cost,
        'avg_daily_cost': avg_daily_cost,
        'days_analyzed': len(daily_costs),
        'trend': 'increasing' if len(costs) > 1 and slope > 0 else 'stable'
    }
