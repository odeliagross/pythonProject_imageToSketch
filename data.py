import pandas as pd

def get_sample_data():
    return pd.DataFrame({
        'Thickness': [1, 2, 3, 4, 5, 6],
        'Quality': [7.5, 8.0, 8.2, 7.8, 8.5, 7.9],
        'Upload Date': pd.date_range(start='2025-01-01', periods=6, freq='D'),
        'Creation Date': pd.date_range(start='2025-01-02', periods=6, freq='D')
    })
