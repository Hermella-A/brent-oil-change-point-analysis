"""
Data loader for Flask backend.
Loads processed data and prepares API responses.
"""

import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/brent_clean.csv')
EVENTS_PATH = os.path.join(os.path.dirname(__file__), '../data/brent_events.csv')


def load_price_data():
    """Load Brent oil price data with features."""
    df = pd.read_csv(DATA_PATH, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    return df


def load_events_data():
    """Load events dataset."""
    df = pd.read_csv(EVENTS_PATH, parse_dates=['Date'])
    return df


def get_price_series():
    """Return price series as dict for JSON response."""
    df = load_price_data()
    return {
        'dates': df.index.strftime('%Y-%m-%d').tolist(),
        'prices': df['Price'].tolist(),
        'ma50': df['MA_50'].tolist(),
        'ma200': df['MA_200'].tolist(),
        'volatility': df['Volatility_30d'].tolist()
    }


def get_events():
    """Return events as dict for JSON response."""
    df = load_events_data()
    return {
        'events': df.to_dict(orient='records')
    }


def get_change_points():
    """
    Return change point data.
    Since we don't have multiple change points from Task 2,
    we return a single detected change point (from your output: 2004-07-12).
    """
    # From Task 2 results
    change_point_date = '2004-07-12'
    
    df = load_price_data()
    
    # Find the price at the change point
    if change_point_date in df.index:
        price_at_change = df.loc[change_point_date, 'Price']
    else:
        # Find nearest
        idx = df.index.get_indexer([pd.to_datetime(change_point_date)], method='nearest')[0]
        price_at_change = df.iloc[idx]['Price']
    
    return {
        'change_points': [
            {
                'date': change_point_date,
                'price_at_change': float(price_at_change)
            }
        ]
    }


def get_statistics():
    """Return summary statistics."""
    df = load_price_data()
    
    return {
        'total_observations': len(df),
        'date_range': {
            'start': df.index.min().strftime('%Y-%m-%d'),
            'end': df.index.max().strftime('%Y-%m-%d')
        },
        'price_stats': {
            'min': float(df['Price'].min()),
            'max': float(df['Price'].max()),
            'mean': float(df['Price'].mean()),
            'std': float(df['Price'].std())
        },
        'volatility_stats': {
            'mean': float(df['Volatility_30d'].mean()),
            'max': float(df['Volatility_30d'].max())
        }
    } 