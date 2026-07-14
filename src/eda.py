"""
Module: eda.py
Brent Oil Price Exploratory Data Analysis
Modular functions for loading, processing, plotting, and testing.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import os
import warnings
warnings.filterwarnings('ignore')


def load_data(filepath):
    """
    Load Brent oil price data from CSV.
    
    Parameters:
        filepath (str): Path to the raw CSV file.
    
    Returns:
        pd.DataFrame: DataFrame with DateTime index.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    print(f"✅ Loaded {len(df)} rows from {filepath}")
    return df


def compute_features(df):
    """
    Compute derived features: returns, moving averages, volatility.
    
    Parameters:
        df (pd.DataFrame): Raw price data with 'Price' column.
    
    Returns:
        pd.DataFrame: Original DataFrame with new feature columns.
    """
    df = df.copy()
    df['Returns'] = df['Price'].pct_change()
    df['Log_Returns'] = np.log(df['Price'] / df['Price'].shift(1))
    df['MA_50'] = df['Price'].rolling(50).mean()
    df['MA_200'] = df['Price'].rolling(200).mean()
    df['Volatility_30d'] = df['Returns'].rolling(30).std() * np.sqrt(252)
    return df


def plot_analysis(df, save_path="docs/brent_eda_plots.png"):
    """
    Generate EDA plots: trend, returns, and volatility.
    
    Parameters:
        df (pd.DataFrame): DataFrame with computed features.
        save_path (str): Where to save the plot image.
    
    Returns:
        str: The path where the plot was saved.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    fig, axes = plt.subplots(3, 1, figsize=(14, 12))
    
    # Plot 1: Price with moving averages
    axes[0].plot(df.index, df['Price'], label='Brent Price', alpha=0.7)
    axes[0].plot(df.index, df['MA_50'], label='50-day MA', linestyle='--')
    axes[0].plot(df.index, df['MA_200'], label='200-day MA', linestyle='--')
    axes[0].set_title('Trend Analysis: Brent Oil Prices with Moving Averages')
    axes[0].set_ylabel('Price (USD/barrel)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Plot 2: Daily returns
    axes[1].plot(df.index, df['Returns'], alpha=0.5, color='green')
    axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    axes[1].set_title('Daily Returns')
    axes[1].set_ylabel('Returns')
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: Rolling volatility
    axes[2].plot(df.index, df['Volatility_30d'], color='red')
    axes[2].set_title('30-Day Rolling Volatility (Annualized)')
    axes[2].set_ylabel('Volatility')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()  # Close to prevent hanging
    print(f"✅ Plots saved to {save_path}")
    return save_path


def test_stationarity(series, name):
    """
    Perform Augmented Dickey-Fuller test.
    
    Parameters:
        series (pd.Series): Time series to test.
        name (str): Name of the series (for printing).
    
    Returns:
        tuple: (adf_statistic, p_value, is_stationary)
    """
    result = adfuller(series.dropna())
    adf_stat = result[0]
    p_val = result[1]
    is_stat = p_val < 0.05
    status = "✅ Yes" if is_stat else "❌ No"
    print(f"{name} - ADF: {adf_stat:.4f}, p-value: {p_val:.4f}, Stationary? {status}")
    return adf_stat, p_val, is_stat


def save_processed_data(df, save_path="data/processed/brent_clean.csv"):
    """
    Save the processed DataFrame to CSV.
    
    Parameters:
        df (pd.DataFrame): DataFrame with computed features.
        save_path (str): Where to save the CSV.
    
    Returns:
        str: The path where the CSV was saved.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path)
    print(f"✅ Cleaned data saved to {save_path}")
    return save_path


def run_full_analysis(raw_path="data/raw/BrentOilPrices.csv",
                      processed_path="data/processed/brent_clean.csv",
                      plot_path="docs/brent_eda_plots.png"):
    """
    Run the complete EDA pipeline.
    
    Parameters:
        raw_path (str): Path to raw CSV.
        processed_path (str): Path to save processed CSV.
        plot_path (str): Path to save plots.
    """
    print("=" * 50)
    print("BRENT OIL EDA PIPELINE")
    print("=" * 50)
    
    # 1. Load
    df = load_data(raw_path)
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    
    # 2. Compute features
    df = compute_features(df)
    
    # 3. Plot
    plot_analysis(df, plot_path)
    
    # 4. Stationarity tests
    print("\n" + "=" * 50)
    print("STATIONARITY TESTS")
    print("=" * 50)
    test_stationarity(df['Price'], "Raw Prices")
    test_stationarity(df['Returns'], "Returns")
    
    # 5. Save processed data
    save_processed_data(df, processed_path)
    
    print("\n✅ Task 1b EDA pipeline complete!")
    return df


# If run as standalone script
if __name__ == "__main__":
    run_full_analysis()