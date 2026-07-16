"""
Task 2: Bayesian Change Point Model for Brent Oil Prices
Week 10 - Birhan Energies
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
from statsmodels.tsa.stattools import adfuller
import os
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("TASK 2: BAYESIAN CHANGE POINT MODEL")
print("="*60)

# ============================================================
# 1. DATA PREPARATION AND EDA
# ============================================================

print("\n📂 Loading data...")
df = pd.read_csv('data/processed/brent_clean.csv', parse_dates=['Date'])
df.set_index('Date', inplace=True)

print(f"✅ Loaded {len(df)} rows")
print(f"Date range: {df.index.min()} to {df.index.max()}")

# Plot raw prices and log returns
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

axes[0].plot(df.index, df['Price'], color='blue', alpha=0.7, linewidth=0.8)
axes[0].set_title('Brent Oil Prices (1987-2022)', fontsize=14)
axes[0].set_ylabel('Price (USD/barrel)', fontsize=12)
axes[0].grid(True, alpha=0.3)

axes[1].plot(df.index, df['Log_Returns'], color='green', alpha=0.5, linewidth=0.5)
axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[1].set_title('Log Returns (Volatility Clustering)', fontsize=14)
axes[1].set_ylabel('Log Returns', fontsize=12)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
os.makedirs('docs', exist_ok=True)
plt.savefig('docs/brent_task2_eda.png', dpi=150)
print("✅ Saved plot: docs/brent_task2_eda.png")
plt.close()

# Stationarity test on log returns
result = adfuller(df['Log_Returns'].dropna())
print("\n" + "="*50)
print("STATIONARITY TEST - Log Returns")
print("="*50)
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
print(f"Stationary? {'✅ Yes' if result[1] < 0.05 else '❌ No'}")
print("="*50)

# ============================================================
# 2. BUILD THE BAYESIAN CHANGE POINT MODEL
# ============================================================

print("\n🔄 Building Bayesian Change Point Model...")

# Prepare data
log_prices = np.log(df['Price'].values)
n_obs = len(log_prices)
time_indices = np.arange(n_obs)

print(f"Number of observations: {n_obs}")

with pm.Model() as change_point_model:
    # 1. Define the Switch Point (tau) - discrete uniform
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_obs-1)
    
    # 2. Define "Before" and "After" parameters
    mu_before = pm.Normal('mu_before', mu=np.mean(log_prices[:100]), sigma=1)
    mu_after = pm.Normal('mu_after', mu=np.mean(log_prices[-100:]), sigma=1)
    sigma = pm.HalfCauchy('sigma', beta=1)
    
    # 3. Use a Switch Function
    mu = pm.math.switch(tau >= time_indices, mu_before, mu_after)
    
    # 4. Define the Likelihood
    likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=log_prices)
    
    # 5. Run the Sampler
    print("   Sampling from posterior (this may take a few minutes)...")
    trace = pm.sample(draws=5000, tune=2000, chains=4, cores=1, random_seed=42)
    print("✅ Sampling complete!")

# ============================================================
# 3. INTERPRET THE MODEL OUTPUT
# ============================================================

print("\n" + "="*50)
print("CONVERGENCE DIAGNOSTICS (r_hat)")
print("="*50)
summary = az.summary(trace)
print(summary)

# Check r_hat - convert to numeric first
r_hat_values = pd.to_numeric(summary['r_hat'])
if np.all(r_hat_values < 1.01):
    print("\n✅ All r_hat < 1.01 - Model has converged!")
else:
    print("\n⚠️ Some r_hat > 1.01 - Consider more samples")

# Trace plots
az.plot_trace(trace, var_names=['tau', 'mu_before', 'mu_after', 'sigma'])
plt.tight_layout()
plt.savefig('docs/brent_trace_plots.png', dpi=150)
print("✅ Saved plot: docs/brent_trace_plots.png")
plt.close()

# Posterior distribution of tau
tau_samples = trace.posterior['tau'].values.flatten()
tau_median = int(np.median(tau_samples))
change_point_date = df.index[tau_median]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(tau_samples, bins=50, color='blue', alpha=0.7, edgecolor='black')
axes[0].axvline(tau_median, color='red', linestyle='--', linewidth=2, label=f'Median: {tau_median}')
axes[0].set_title('Posterior Distribution of Change Point (tau)')
axes[0].set_xlabel('Time Index')
axes[0].set_ylabel('Frequency')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Density plot using seaborn
sns.kdeplot(tau_samples, ax=axes[1], fill=True, alpha=0.5, color='blue')
axes[1].axvline(tau_median, color='red', linestyle='--', linewidth=2, label=f'Median: {tau_median}')
axes[1].set_title('Density of Change Point Location')
axes[1].set_xlabel('Time Index')
axes[1].set_ylabel('Density')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/brent_change_point_distribution.png', dpi=150)
print("✅ Saved plot: docs/brent_change_point_distribution.png")
plt.close()

print(f"\n📅 Detected Change Point: {change_point_date.strftime('%Y-%m-%d')}")

# ============================================================
# 4. QUANTIFY THE IMPACT
# ============================================================

mu_before_samples = trace.posterior['mu_before'].values.flatten()
mu_after_samples = trace.posterior['mu_after'].values.flatten()

# Convert log prices back to actual prices
price_before_samples = np.exp(mu_before_samples)
price_after_samples = np.exp(mu_after_samples)

price_before_mean = np.mean(price_before_samples)
price_after_mean = np.mean(price_after_samples)
price_change = price_after_mean - price_before_mean
price_change_pct = (price_change / price_before_mean) * 100

# FIXED: Use np.percentile instead of az.hdi (avoids version conflicts)
price_before_hdi = np.percentile(price_before_samples, [3, 97])
price_after_hdi = np.percentile(price_after_samples, [3, 97])

print("\n" + "="*50)
print("IMPACT QUANTIFICATION")
print("="*50)
print(f"\n📊 Before Change Point (μ₁):")
print(f"   Mean Price: ${price_before_mean:.2f}")
print(f"   94% HDI: ${price_before_hdi[0]:.2f} - ${price_before_hdi[1]:.2f}")
print(f"\n📊 After Change Point (μ₂):")
print(f"   Mean Price: ${price_after_mean:.2f}")
print(f"   94% HDI: ${price_after_hdi[0]:.2f} - ${price_after_hdi[1]:.2f}")
print(f"\n📈 Price Impact:")
print(f"   Absolute Change: ${price_change:+.2f}")
print(f"   Percentage Change: {price_change_pct:+.2f}%")

# Probability statements
prob_after_higher = np.mean(price_after_samples > price_before_samples)
print(f"\n📊 Probability price AFTER is higher than BEFORE: {prob_after_higher*100:.2f}%")

# ============================================================
# 5. ASSOCIATE CHANGES WITH CAUSES
# ============================================================

events_df = pd.read_csv('data/brent_events.csv', parse_dates=['Date'])

# Find closest event
events_df['Date_Diff'] = abs(events_df['Date'] - change_point_date)
closest_event = events_df.loc[events_df['Date_Diff'].idxmin()]

print("\n" + "="*50)
print("ASSOCIATED EVENT")
print("="*50)
print(f"\n📅 Detected Change Point: {change_point_date.strftime('%Y-%m-%d')}")
print(f"\n📌 Closest Event:")
print(f"   Event: {closest_event['Event_Name']}")
print(f"   Date: {closest_event['Date'].strftime('%Y-%m-%d')}")
print(f"   Category: {closest_event['Category']}")
print(f"   Days Difference: {closest_event['Date_Diff'].days} days")

# Plot change point with event
fig, ax = plt.subplots(figsize=(14, 7))

ax.plot(df.index, df['Price'], color='blue', alpha=0.6, linewidth=0.8, label='Brent Price')
ax.axvline(x=change_point_date, color='red', linestyle='--', linewidth=2, 
           label=f'Change Point: {change_point_date.strftime("%Y-%m-%d")}')

# Find price at event date (or nearest)
if closest_event['Date'] in df.index:
    event_price = df.loc[closest_event['Date'], 'Price']
else:
    # Find nearest date
    nearest_idx = df.index.get_indexer([closest_event['Date']], method='nearest')[0]
    event_price = df.iloc[nearest_idx]['Price']
    
ax.scatter(closest_event['Date'], event_price, color='red', s=200, marker='*', zorder=5,
           label=f"Event: {closest_event['Event_Name'][:30]}...")

ax.axhline(y=price_before_mean, color='green', linestyle=':', linewidth=2, alpha=0.7,
           label=f'Before Mean: ${price_before_mean:.2f}')
ax.axhline(y=price_after_mean, color='orange', linestyle=':', linewidth=2, alpha=0.7,
           label=f'After Mean: ${price_after_mean:.2f}')

ax.set_title('Brent Oil Prices with Detected Change Point and Associated Event', fontsize=14)
ax.set_ylabel('Price (USD/barrel)', fontsize=12)
ax.set_xlabel('Date', fontsize=12)
ax.legend(loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/brent_change_point_with_event.png', dpi=150)
print("✅ Saved plot: docs/brent_change_point_with_event.png")
plt.close()

# ============================================================
# 6. SUMMARY
# ============================================================

print("\n" + "="*60)
print("SUMMARY AND INTERPRETATION")
print("="*60)
print(f"\n📅 Detected Change Point: {change_point_date.strftime('%Y-%m-%d')}")
print(f"📌 Associated Event: {closest_event['Event_Name']} ({closest_event['Date'].strftime('%Y-%m-%d')})")
print(f"📊 Category: {closest_event['Category']}")
print(f"\n💵 Impact:")
print(f"   Before: ${price_before_mean:.2f} per barrel")
print(f"   After: ${price_after_mean:.2f} per barrel")
print(f"   Change: {price_change_pct:+.2f}% (${price_change:+.2f})")
print(f"\n📈 Probability of increase: {prob_after_higher*100:.2f}%")
print("\n⚠️ Note: Correlation does not imply causation. Other confounding factors")
print("   (global demand, USD strength, etc.) may have contributed.")

print("\n" + "="*60)
print("✅ TASK 2 COMPLETE!") 
print("="*60) 