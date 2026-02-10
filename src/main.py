# Main: Analyzing the stock portifolio
import Echo
import json
import pandas as pd
import optimize
import os
import analyze
from natsort import natsorted
import yfinance as yf

"""ADD Monte Carlo: DF list
### Not added #####
Function is in analyze
"""


"""Optimize hyperparameters,
for a given ticker.
"""


def optimize_stock():
    START = "2019-01-01"
    END = "2021-01-01"
    n_prediction = 100
    tickers = ["TSLA"]
    long_period = False  # If false, se short folder result

    analyze.optimize_ticker_list(tickers, START, END, n_prediction, long_period)


"""Execute Prediction 
Function take the best optimizer filer,
and take the hyperparameters, and
make our prediction.
"""


def execute_prediction():
    START = "2019-01-01"
    END = "2021-01-01"
    neurons = 1710
    n_prediction = 100
    ticker = "TSLA"
    long_period = False

    analyze.execute_best_loss_file(
        ticker, n_prediction, neurons, START, END, long_period
    )


# optimize_stock()
execute_prediction()
