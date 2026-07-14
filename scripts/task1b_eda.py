import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 1. LOAD YOUR CSV FROM data/raw/
# ============================================
file_path = "data/raw/BrentOilPrices.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"❌ File not found! Please place your CSV at {file_path}")

df = pd.read_csv(file_path, parse_dates=['Date'])
df.set_index('Date', inplace=True)

print(f"✅ Loaded {len(df)} rows from {file_path}")
print(df.head())
print(f"Date range: {df.index.min()} to {df.index.max()}")

# ============================================
# 2. CALCULATE METRICS
# ============================================
df['Returns'] = df['Price'].pct_change()
df['Log_Returns'] = np.log(df['Price'] / df['Price'].shift(1))
df['MA_50'] = df['Price'].rolling(50).mean()
df['MA_200'] = df['Price'].rolling(200).mean()
df['Volatility_30d'] = df['Returns'].rolling(30).std() * np.sqrt(252)

# ============================================
# 3. PLOTS (Trend, Returns, Volatility)
# ============================================
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Price + MAs
axes[0].plot(df.index, df['Price'], label='Brent Price', alpha=0.7)
axes[0].plot(df.index, df['MA_50'], label='50-day MA', linestyle='--')
axes[0].plot(df.index, df['MA_200'], label='200-day MA', linestyle='--')
axes[0].set_title('Trend Analysis: Brent Oil Prices with Moving Averages')
axes[0].set_ylabel('Price (USD/barrel)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Returns
axes[1].plot(df.index, df['Returns'], alpha=0.5, color='green')
axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[1].set_title('Daily Returns')
axes[1].set_ylabel('Returns')
axes[1].grid(True, alpha=0.3)

# Volatility
axes[2].plot(df.index, df['Volatility_30d'], color='red')
axes[2].set_title('30-Day Rolling Volatility (Annualized)')
axes[2].set_ylabel('Volatility')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs("docs", exist_ok=True)
plt.savefig('docs/brent_eda_plots.png', dpi=150)
print("✅ Plots saved to docs/brent_eda_plots.png")

# ============================================
# 4. STATIONARITY TESTS
# ============================================
print("\n" + "="*50)
print("STATIONARITY TESTS (Augmented Dickey-Fuller)")
print("="*50)

# Raw Prices
result = adfuller(df['Price'].dropna())
print(f"\nRaw Prices - ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
print(f"Stationary? {'✅ Yes' if result[1] < 0.05 else '❌ No (Non-Stationary)'}")

# Returns
result = adfuller(df['Returns'].dropna())
print(f"\nReturns - ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
print(f"Stationary? {'✅ Yes' if result[1] < 0.05 else '❌ No'}")

# ============================================
# 5. SAVE CLEAN DATA
# ============================================
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/brent_clean.csv")
print("\n✅ Cleaned data saved to data/processed/brent_clean.csv")
print("✅ Task 1b is COMPLETE!")
