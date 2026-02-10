import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import Echo
import os
from natsort import natsorted
import optimize


def read_opt_file(path):
    with open(path, "r") as f:
        data = json.loads(f.read())
        return data


"""
    Get all tickers dirs. (All the tickers with optimizer folders)

"""


def get_ticker_opt_dirs():
    ticker_dirs = [
        name
        for name in os.listdir("optimize-stocks/")
        if os.path.isdir(os.path.join("optimize-stocks", name))
    ]
    return ticker_dirs


"""
   Return file path, with best loss parameters. 
   Take a ticker as input. 
"""


def best_loss_file(ticker, long_period):
    path = "optimize-stocks/"
    if long_period == True:
        path = path + ticker + "/Long_period/results/"
    else:
        path = path + ticker + "/Short_period/results/"

    file_list = os.listdir(path)
    sort_list = natsorted(file_list)
    best_5_results = sort_list[0]
    # Open file, and call ESN on it
    return path + best_5_results


"""
    Take ticker in model, at plot prediction against actual price.

"""


def execute_best_loss_file(ticker, n_prediction, neurons, START, END, long_period):
    file_path = best_loss_file(ticker, long_period)
    BEST_OPT_ESN(file_path, n_prediction, neurons, ticker, START, END)


"""
    Optimize hyperparameters for these tickers.
    Take a list of ticker names.

"""


def optimize_ticker_list(tickers, START, END, n_prediction, long_period):
    i = 0
    while i < len(tickers):
        optimize.optimize(tickers[i], START, END, n_prediction, long_period)
        i = i + 1


"""
    Check - if SP500.csv, can be found by yahoo download.
    (ADD This tomorrow)
"""


# Not implemented yet


"""
    Read json file, we are gaining as output from optimizer.
    And set the hyperparameters.
    Return parameters as a dict.
"""


def read_opt_params(path):
    with open(path, "r") as f:
        data = json.loads(f.read())

    return data["current_params"]
    # print(data)
    # seed = data['current_params']['seed']
    # lr = data['current_params']['lr']
    # sr = data['current_params']['sr']
    # input_connectivity = data['current_params']['input_connectivity']
    # rc_connectivity = data['current_params']['rc_connectivity']
    # neurons = 900
    # warmup = 10
    # n_training = 800


"""
    Read best optimizer file, for given tick, into ESN Model.
"""


def BEST_OPT_ESN(path, n_prediction, neurons, ticker, START, END):
    with open(path, "r") as f:
        data = json.loads(f.read())

    # data = data['current_params']
    seed = 1234  # data['current_params']['seed']
    lr = data["current_params"]["lr"]
    sr = data["current_params"]["sr"]
    input_connectivity = data["current_params"]["input_connectivity"]
    rc_connectivity = data["current_params"]["rc_connectivity"]
    # neurons = 580
    warmup = 100
    # n_training = 800
    # n_training = n_data - n_prediction
    Echo.myESN(
        ticker,
        START,
        END,
        n_prediction,
        seed,
        lr,
        sr,
        warmup,
        neurons,
        rc_connectivity,
        input_connectivity,
    )


"""
    Calculating profit for ML Prediction 
    Using a simple method, where buy,
    if our prediction is over the actual price.
    Sell if prediction is lower than actual price.
"""


def ML_profit(p_var, a_var, money):
    # Money, adjust for how many stocks we want to buy
    total_profit = 0
    i = 0
    holdingStock = False
    bought_price = 0
    stocks_bought = 0
    start_money = money
    while i < len(p_var):
        if p_var[i] > a_var[i] and holdingStock == False:
            # Buy stock
            bought_price = a_var[i]
            stocks_bought = math.floor(money / bought_price)
            money = money - stocks_bought * bought_price
            holdingStock = True
        if p_var[i] < a_var[i] and holdingStock == True:
            # Sell stock
            profit = a_var[i] - bought_price - 100
            total_profit = total_profit + (profit * stocks_bought)
            money = money + (a_var[i] * stocks_bought)
            holdingStock = False
        i = i + 1
    return total_profit


"""
Using Brownian Motion + Monte Carlo Simulation,
to find the stocks, who we predict give the highest profit.
This return a df with all the simulations.

Input: 
    Stock dataframe
    number of simulations.

"""


def Mc_Simulation(df, n_simulations, boolPlot):
    # Input is yahoo data
    df = df["Adj Close"]

    SO = df[0]  # Start Price
    dt = 1  # Time increment
    T = len(df)  # Time length

    # Calculating returns in log
    t_0 = np.log(df[1:])
    t_1 = np.log(df[:-1])
    t_0 = t_0.to_numpy()
    t_1 = t_1.to_numpy()
    log_returns = t_0 - t_1
    mu = np.mean(
        log_returns
    )  # mu - sigma^2 -> Aendre parameter vejen.  -> Her divdere med dt
    # v = np.mean(log_return) / dt
    sigma = np.std(
        log_returns
    )  # Divder med kvadratrod dt, for at faa den rigtige sigma

    # m = mu + sigma^2 / 2
    np.random.seed(155)  # Generating the seed number
    St = np.exp(
        (mu - sigma**2 / 2) * dt
        ## Tager vores resultater og ganger en normal fordeling på
        + sigma * np.random.normal(0, np.sqrt(dt), size=(n_simulations, T)).T
    )

    St = np.vstack([np.ones(n_simulations), St])
    # multiply through by S0 and return the cumulative product of elements along a given simulation path (axis=0).
    St = SO * St.cumprod(axis=0)
    time = np.linspace(0, T, T + 1)
    tt = np.full(shape=(n_simulations, T + 1), fill_value=time).T

    plt.plot(tt, St)
    plt.xlabel("Days $(t)$")
    plt.ylabel("Stock Price $(S_t)$")
    plt.title("ST")

    if boolPlot == True:
        plt.show()

    # Data du pandas. All the simulations
    df = pd.DataFrame(data=St)
    return df
