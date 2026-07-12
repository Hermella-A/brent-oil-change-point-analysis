# Brent Oil Price Analysis Plan

## Part 1: Data Analysis Workflow

### Step 1: Data Loading & Preprocessing
- Load Brent oil prices (Date, Price)
- Parse Date as datetime and set as index
- Handle missing values via forward-fill
- Create daily returns and log-returns

### Step 2: Exploratory Data Analysis
- **Trend Analysis**: Plot raw prices with 50-day and 200-day moving averages
- **Stationarity Testing**: ADF test on raw prices and daily returns
- **Volatility Patterns**: Plot daily returns and rolling 30-day standard deviation

### Step 3: Event Data Integration
- Load 15 events from data/brent_events.csv
- Overlay event dates on price plots

### Step 4: Change Point Detection (Bayesian)
- Use PyMC with piecewise linear trend model
- Priors: Poisson on number of change points, Uniform on locations
- MCMC sampling (NUTS, 4 chains)

### Step 5: Quantifying Impact
- Compare pre-event vs post-event average prices
- Calculate percentage changes

### Step 6: Reporting
- Visualize change points on price series
- Summary table: Event | Change Date | % Change
- Executive summary for policymakers

---

## Part 2: Time Series Properties

### Trend Analysis
- Long-term upward trend with structural breaks
- 50-day MA for short-term; 200-day MA for long-term

### Stationarity Testing
- Raw prices: Non-stationary (ADF p > 0.05)
- Daily returns: Stationary (ADF p < 0.05)
- Implication: Model log-prices with piecewise linear trend

### Volatility Patterns
- Volatility clustering observed (2014-2016, 2020-2022)
- Use Student-t distribution for heavy tails

---

## Part 3: Change Point Models

### Purpose
- Identify structural breaks where data-generating process changes
- Detect regime shifts caused by wars, OPEC decisions, sanctions

### Expected Outputs
1. Number of change points
2. Locations (dates) of changes
3. Segment parameters (mean, trend, variance)
4. Posterior uncertainty (credible intervals)
5. Probability of change at each time point

### Limitations
1. Correlation ≠ Causation – cannot prove events caused changes
2. Confounding variables (USD strength, inflation, global demand)
3. Model specification affects results
4. Daily data misses intra-day reactions

---

## Part 4: Assumptions & Limitations

| Assumption | Limitation | Mitigation |
|------------|------------|------------|
| Events drive structural breaks | Confounding macro factors | Discuss confounders in report |
| Piecewise stationarity | Mis-specified number of breaks | Use model comparison (WAIC, LOO) |
| Discrete event dates | Events unfold gradually | Use approximate dates with uncertainty |
| Weakly informative priors | Prior affects posterior | Test different priors |

---

## Part 5: Correlation vs. Causation

**Correlation**: Change point aligns with event in time.

**Causation**: Would require counterfactual (what would have happened without event).

**Our Approach**: Identify statistical associations, clearly state correlation ≠ causation. Recommend causal methods (Synthetic Control, CausalImpact) for follow-up.

---

## Deliverables
1. ✅ Events CSV: data/brent_events.csv (15 events)
2. ✅ Analysis Plan: This document
3. ✅ Assumptions & Limitations documented

**Next**: Task 1b - Python notebook with EDA, trend, stationarity, volatility
