# Brent Oil Price Analysis Plan

## Part 1: Data Analysis Workflow

### Step 1: Data Loading & Preprocessing
- Load the Brent oil prices dataset (Date, Price columns)
- Parse 'Date' as datetime and set as DataFrame index
- Check for missing values and handle using forward-fill (max 5 consecutive missing)
- Create derived columns:
  - **Daily Returns**: `(Price_t / Price_{t-1}) - 1`
  - **Log Returns**: `log(Price_t / Price_{t-1})`
  - **Rolling Averages**: 50-day and 200-day moving averages

### Step 2: Exploratory Data Analysis (EDA)
- **Trend Analysis**: 
  - Plot raw Brent prices with 50-day and 200-day moving averages
  - Identify long-term upward/downward trends
- **Stationarity Testing**:
  - Augmented Dickey-Fuller (ADF) test on raw prices
  - ADF test on daily returns (which should be stationary)
  - Discuss implications for modeling
- **Volatility Patterns**:
  - Plot daily returns to visualize volatility clustering
  - Compute rolling 30-day standard deviation
  - Identify periods of high/low volatility (e.g., 2014 crash, 2020 COVID shock)

### Step 3: Event Data Integration
- Load `data/brent_events.csv` containing 15 major events
- Overlay event dates on price and volatility plots
- Visually inspect price behavior around each event (pre-event, immediate reaction, post-event)

### Step 4: Change Point Detection (Bayesian)
- **Model Specification**:
  - Use PyMC to implement a Bayesian change point model
  - Assume time series follows a piecewise linear trend or mean-shift process
  - Define prior distributions:
    - Number of change points: Poisson prior
    - Location of change points: Uniform over time range
    - Segment parameters (mean/variance): Weakly informative Normal/Half-Cauchy priors
- **Sampling**:
  - Use MCMC with NUTS sampler (4 chains, 2000 warmup, 4000 draws)
  - Check convergence using R-hat (< 1.01) and effective sample size

### Step 5: Quantifying Event Impact
- For each detected change point:
  - Calculate average price in 30-day window before and after
  - Compute percentage change
  - Match to nearest event in `brent_events.csv`
- Produce table: Event | Change Date | Price Before | Price After | % Change

### Step 6: Reporting & Visualization
- Plot Brent price series with detected change points highlighted
- Create summary table of all events and their estimated impacts
- Write 1-2 page executive summary for policymakers:
  - Key findings
  - Most impactful events
  - Recommendations for risk management and policy

---

## Part 2: Time Series Properties Analysis

### Trend Analysis
- **Long-term trend**: Brent oil prices show a general upward trend from 1987-2022, with significant structural breaks.
- **Moving averages**: 50-day MA captures short-term momentum; 200-day MA indicates long-term trend direction.
- **Crossovers**: When 50-day MA crosses above 200-day MA (golden cross), indicates bullish sentiment; opposite (death cross) indicates bearish.

### Stationarity Testing
- **Raw Prices**: Non-stationary (ADF p-value > 0.05) – trending behavior present.
- **Daily Returns**: Stationary (ADF p-value < 0.05) – mean-reverting around zero.
- **Implication for Modeling**: Change point models can work on raw prices (with trend component) or returns (mean-shift detection). We will model log-prices with piecewise linear trend.

### Volatility Patterns
- **Volatility clustering**: Periods of high volatility tend to cluster (e.g., 2014-2016, 2020-2022).
- **Key volatile periods**:
  - 2014: Oil price crash (supply glut)
  - 2020: COVID-19 demand shock + Saudi-Russia price war
  - 2022: Russia-Ukraine war and sanctions
- **Implication for Modeling**: Use Student-t distribution for returns to account for heavy tails, or model volatility explicitly via GARCH.

---

## Part 3: Understanding Change Point Models

### Purpose of Change Point Models
Change point models identify structural breaks in time series – points where the underlying data-generating process changes. In oil price analysis:

- **Why use them?** Oil prices are driven by discrete events (wars, OPEC decisions, sanctions). Change points help identify when the "regime" shifted.
- **How they work**: The time series is divided into segments, each with its own parameters (mean, trend, variance). The model estimates both the number of change points and their locations.
- **Types**: 
  - Mean-shift model: Change in average price level
  - Trend-shift model: Change in slope (price trajectory)
  - Variance-shift model: Change in volatility

### Expected Outputs
1. **Number of change points** – how many structural breaks occurred
2. **Locations (dates)** – when each break happened
3. **Segment parameters**:
   - Mean price level in each segment
   - Trend (slope) in each segment
   - Volatility (variance) in each segment
4. **Posterior uncertainty** – credible intervals around change point locations
5. **Probability of change** – likelihood that a change occurred at each time point

### Limitations of Change Point Analysis
1. **Cannot prove causation**: A change point aligning with an event does not mean the event *caused* the change – correlation ≠ causation.
2. **Confounding variables**: Other simultaneous factors (macroeconomic conditions, currency fluctuations, demand shifts) are not controlled for.
3. **Model specification**: Results depend on assumed number of change points and prior distributions.
4. **Data quality**: Daily data misses intra-day reactions; monthly data may smooth over shocks.
5. **Forward-looking markets**: Prices often react *before* events based on expectations, making precise dating difficult.

---

## Part 4: Assumptions & Limitations

| Assumption | Limitation | Mitigation |
|------------|------------|------------|
| Events are the primary drivers of structural breaks | Confounding macro factors (USD strength, inflation, global demand) also affect prices | Include event dates in model; discuss confounders in report |
| Price series is piecewise stationary between change points | If number of change points is mis-specified, results are biased | Use model comparison (WAIC, LOO) to select optimal number |
| Events have a discrete start date (not gradual) | Many events unfold over weeks/months (e.g., sanctions) | Use approximate start dates; discuss uncertainty in timing |
| Bayesian priors are weakly informative | Choice of prior affects posterior; sensitive analysis required | Test different priors; report robustness checks |
| Daily prices capture market reactions accurately | Intra-day volatility and speculative trading are missed | Acknowledge as limitation in final report |

---

## Part 5: Correlation vs. Causation

**Critical Distinction**:

- **Statistical Correlation**: A change point occurs at approximately the same time as an event. This shows association but does not prove the event caused the price change.

- **Causal Impact**: To prove causality, we would need a counterfactual – what would have happened to oil prices *without* the event? This requires methods like:
  - Synthetic Control (construct a "control" time series from unaffected assets)
  - Difference-in-Differences (compare treated vs. control periods)
  - Bayesian Structural Time Series (CausalImpact package)

**Our Approach**: We will identify change points and match them to events, but we will clearly state that we are identifying *statistical associations*, not proving causation. We will recommend follow-up studies using causal inference methods for definitive policy recommendations.

---

## Deliverables Summary
1. ✅ Events CSV: `data/brent_events.csv` (15 events)
2. ✅ Analysis Plan: This document (`docs/analysis_plan.md`)
3. ✅ Assumptions/Limitations: Documented within (Correlation vs. Causation discussed)