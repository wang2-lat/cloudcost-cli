import pandas as pd
from pathlib import Path

def parse_bill(csv_file: Path) -> pd.DataFrame:
    """Parse cloud bill CSV file
    
    Expected columns: date, service, cost, resource_id
    """
    df = pd.read_csv(csv_file)
    
    required_columns = ['date', 'service', 'cost']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain columns: {required_columns}")
    
    df['date'] = pd.to_datetime(df['date'])
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
    
    return df.sort_values('date')
