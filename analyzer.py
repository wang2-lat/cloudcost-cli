import pandas as pd
import numpy as np

def analyze_costs(df: pd.DataFrame) -> dict:
    """Analyze costs and identify optimization opportunities"""
    
    # Total cost
    total_cost = df['cost'].sum()
    
    # Cost by service
    service_costs = df.groupby('service')['cost'].sum().sort_values(ascending=False)
    
    # Identify idle resources (cost near zero but resource exists)
    if 'resource_id' in df.columns:
        resource_costs = df.groupby('resource_id')['cost'].sum()
        idle_resources = resource_costs[resource_costs < resource_costs.mean() * 0.1].index.tolist()
    else:
        idle_resources = []
    
    # Detect cost spikes (anomalies)
    daily_costs = df.groupby('date')['cost'].sum()
    mean_cost = daily_costs.mean()
    std_cost = daily_costs.std()
    threshold = mean_cost + 2 * std_cost
    
    spikes = daily_costs[daily_costs > threshold]
    
    # Top expensive services
    top_services = service_costs.head(5).to_dict()
    
    return {
        'total_cost': total_cost,
        'service_costs': service_costs.to_dict(),
        'top_services': top_services,
        'idle_resources': idle_resources[:10],
        'cost_spikes': spikes.to_dict(),
        'avg_daily_cost': daily_costs.mean(),
        'max_daily_cost': daily_costs.max()
    }
