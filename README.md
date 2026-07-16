# Brent Oil Change Point Analysis

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.2+-blue.svg)](https://reactjs.org/)
[![PyMC](https://img.shields.io/badge/PyMC-5.0+-orange.svg)](https://www.pymc.io/)

## Overview

This project analyzes how major geopolitical events, OPEC decisions, and economic shocks affect Brent oil prices (1987-2022) using **Bayesian change point detection**.

**Key Findings:**
- **Major structural break detected:** July 12, 2004 – prices shifted from $19.86 to $69.98 per barrel (**+252%**)
- **Biggest negative impact:** 2020 Saudi-Russia price war (**-52.85%**)
- **Biggest positive impact:** 2016 OPEC+ Vienna Agreement (**+19.38%**)
- **Model convergence:** All r_hat = 1.00 (perfect)

---

## Project Structure

brent-oil-change-point-analysis/
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .vscode/
│   └── settings.json
├── .gitignore
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   └── eda.py
│
├── scripts/
│   ├── 02_change_point.py
│   ├── task1b_eda.py
│   └── create_events_csv.py
│
├── notebooks/
│   └── task2_change_point.ipynb
│
├── tests/
│   └── __init__.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   │   └── brent_clean.csv
│   └── brent_events.csv
│
├── docs/
│   ├── analysis_plan.md
│   ├── interim_report.md
│   ├── final_report.md
│   └── brent_*.png
│
├── backend/
│   ├── app.py
│   ├── data_loader.py
│   └── requirements.txt
│
└── frontend/
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        ├── App.css
        ├── index.js
        ├── index.css
        ├── api.js
        └── components/
            ├── Dashboard.js
            ├── Dashboard.css
            ├── PriceChart.js
            ├── EventList.js
            ├── StatsCards.js
            └── StatsCards.css
```

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/brent-oil-change-point-analysis.git
cd brent-oil-change-point-analysis
```

### 2. Set Up Python Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Analysis

```bash
# EDA (Task 1)
python scripts/task1b_eda.py

# Bayesian Change Point Model (Task 2)
python scripts/02_change_point.py
```

### 4. Run the Dashboard

```bash
# Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python app.py
```

```bash
# Frontend (Terminal 2)
cd frontend
npm install
npm start
```

---

## Dashboard Features

| Feature | Description |
|----------|-------------|
| Statistics Cards | Total observations, price range, average price, volatility |
| Price Chart | Brent prices with moving averages and volatility |
| Event List | 15 events with impact percentages |
| Change Points | Detected structural breaks |
| Date Filters | Filter data by date range |
| Responsive Design | Works on desktop, tablet, and mobile |

---

## API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/health` | GET | Health check |
| `/api/prices` | GET | Price data with date filtering |
| `/api/events` | GET | Event dataset |
| `/api/change-points` | GET | Detected change points |
| `/api/statistics` | GET | Summary statistics |
| `/api/event-impact` | GET | Event impact quantification |
| `/api/event-correlation` | GET | Event correlation data |

---

## Results

### Detected Change Point

| Metric | Value |
|----------|----------|
| Date | July 12, 2004 |
| Before Mean Price | $19.86 per barrel |
| After Mean Price | $69.98 per barrel |
| Absolute Change | +$50.12 per barrel |
| Percentage Change | +252% |
| Probability of Increase | 100% |

### Event Impacts

| Event | Date | Impact |
|---------|---------|---------|
| Saudi-Russia price war | 2020-03-06 | -52.85% |
| OPEC decides not to cut production | 2014-11-27 | -21.22% |
| OPEC+ Historic production cut | 2020-04-12 | -19.05% |
| OPEC+ Vienna Agreement | 2016-11-30 | +19.38% |
| Russia-Ukraine War begins | 2022-02-24 | +17.15% |
| US bans Russian oil imports | 2022-03-08 | +14.23% |
| OPEC Algiers Accord | 2016-09-28 | +6.09% |
| US withdraws from Iran Nuclear Deal | 2018-05-08 | +4.65% |
| Attack on Saudi Aramco | 2019-09-14 | +2.18% |

---

## Technology Stack

| Category | Technologies |
|------------|-------------|
| Data Analysis | Python, Pandas, NumPy, Matplotlib, Seaborn, Statsmodels |
| Bayesian Modeling | PyMC, ArviZ |
| Backend | Flask, Flask-CORS |
| Frontend | React, Recharts, Axios, Bootstrap |
| Version Control | Git, GitHub Actions |



