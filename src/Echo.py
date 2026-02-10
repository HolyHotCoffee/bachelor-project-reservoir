# Reservoir function

import reservoirpy as rpy
from reservoirpy.nodes import Reservoir, Ridge, FORCE, ESN
from reservoirpy.observables import nrmse, rsquare
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# import data
from reservoirpy.hyper import research
import json
import analyze
import plotting
import data

###### CHECK ISS #########


def myESN(
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
    i_c,
):
    # Creating our reservoir
    reservoir = Reservoir(
        neurons,
        lr=lr,
        sr=sr,
        seed=seed,
        rc_connectivity=rc_connectivity,
        input_connectivity=i_c,
        iss=10000,
        learning_algo="FORCE",
    )

    # Creating the data
    stock_data = data.stock_price(ticker, START, END)
    n_training = len(stock_data) - n_prediction

    X_train = stock_data[:n_training]
    Y_train = stock_data[10 : n_training + 10]
    train_states = reservoir.run(X_train, reset=True)

    readout = Ridge(ridge=1e-7)  # 1e-7, secure overfitting
    readout = readout.fit(train_states, Y_train, warmup=warmup)  #

    # =========================
    # CREATING THE ESN MODEL ==
    # =========================

    # Give the reservoir acces to the readouts last activation using feedback
    reservoir <<= readout
    esn_model = reservoir >> readout
    # force = FORCE() ??? Maybe later for online

    # Shift_fb: forced feedback timeseries should be shifted in tyme by one time step
    esn_model = esn_model.fit(X_train, Y_train, warmup=warmup, force_teachers=True)

    my_pred = esn_model.run(
        stock_data[n_training:], forced_feedbacks=Y_train, shift_fb=True, reset=False
    )

    x = my_pred[-1].reshape(1, -1)
    # x_pred = np.empty((100, 1))
    Y_pred = np.empty((99, 1))

    # The prediction is feed into itself

    for i in range(99):
        # Use initial warm-uo period
        if i < warmup:
            x = esn_model(x)
        else:
            x = Y_pred[i - warmup].reshape(1, -1)

        x = esn_model(x)
        Y_pred[i] = x

    # for i in range(99):
    #      x = esn_model(x)
    #      Y_pred[i] = x
    #

    # Y_pred = my_pred
    # esn_model(X[0].reshape(1, -1))

    table = plotting.datatable(
        START, END, n_prediction, seed, lr, sr, warmup, neurons, rc_connectivity, i_c
    )
    plotting.plot_prediction2(stock_data[n_training:], Y_pred, ticker, table)
