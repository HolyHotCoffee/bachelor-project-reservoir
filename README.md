# Reservoir Computing for Stock Time Series (Bachelor Project)

**One-liner:** Stock time series forecasting → Echo State Network style reservoir computing with hyperparameter search → prediction plots and saved optimization results.

## Why it matters
Reservoir computing can model sequential data with simpler training compared to fully trained recurrent networks.
This repo shows a practical end-to-end workflow: fetch data → optimize ESN-like hyperparameters → run a prediction → visualize outputs.

## Data
- Primary data source: historical stock prices downloaded via `yfinance` (Adjusted Close).
- Local helper data files:
  - `src/data/SP500.csv`
  - `src/data/DFMonte.csv`

Constraints:
- Results can differ over time because market data is fetched live from Yahoo Finance through `yfinance`.
- Large generated outputs are expected to be kept out of git.

## Method
- Data fetching: `src/data.py`
- Model and training logic: `src/Echo.py`
- Hyperparameter optimization: `src/optimize.py`
- Experiment utilities and evaluation tools: `src/analyze.py`
- Plotting helpers: `src/plotting.py`
- Entry script: `src/main.py`

## Results
Status: The repo contains the full pipeline code. Generated outputs are written to an `optimize-stocks/` folder during optimization runs.

## Repo structure
```text
bachelor-project-reservoir/
├─ README.md
├─ .gitignore
├─ Notes.md
├─ TODO.md
└─ src/
   ├─ analyze.py
   ├─ data.py
   ├─ data2.py
   ├─ Echo.py
   ├─ main.py
   ├─ optimize.py
   ├─ plotting.py
   └─ data/
      ├─ DFMonte.csv
      └─ SP500.csv
