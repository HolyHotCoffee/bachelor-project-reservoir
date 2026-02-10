import reservoirpy as rpy
from reservoirpy.nodes import Reservoir, Ridge, FORCE, ESN
from reservoirpy.observables import nrmse, rsquare
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
# import data
from reservoirpy.hyper import research
import json
import data
import os

# looss function: RMSE, root mean squared Error
from reservoirpy.datasets import doublescroll


def optimize(ticker, START, END, n_prediction, long_period):

    # Path to save
    path_save = ''
    if long_period == True:
        path_save = str(ticker + '/Long_period')
    else:
        path_save = str(ticker + '/Short_period')
        

    # Creating data
    stock_data = data.stock_price(ticker, START, END)
    

    X = stock_data 
    #X = X[0:len(X)].reshape(-1, 1)  # Need to reshape, so it fits rsn.py format

    n_predict = n_prediction 
    train_len = len(X) - n_predict
    
    X_train = X[:train_len]
    y_train = X[10: train_len + 10]
     
    X_test = X[train_len: -1]
    y_test = X[train_len + 1:]
    

    

    # train_len = 800 
    # X_train = X[:train_len]
    # y_train = X[1: train_len + 1]
    # 
    # X_test = X[train_len: -1]
    # y_test = X[train_len + 1:]
    
    
    hyperopt_config = {
        "exp": f"optimize-stocks/" + path_save,  # the experimentation name
        # the number of differents sets of parameters hyperopt has to try
        "hp_max_evals": 50,
        # the method used by hyperopt to chose those sets (see below)
        "hp_method": "random",
        "seed": 1234,                      # the random state seed, to ensure reproducibility
        # how many random ESN will be tried with each sets of parameters
        "instances_per_trial": 1,
        "hp_space": {                    # what are the ranges of parameters explored
            # the number of neurons is fixed to 300
            "N": ["choice", 600],
            # the spectral radius is log-uniformly distributed between 1e-6 and 10
            "sr": ["loguniform", 2.0, 15],
            # idem with the leaking rate, from 1e-3 to 1
            "lr": ["loguniform", 0.2, 1],
            "iss": ["choice", 1.1],           # the input scaling is fixed
            # and so is the regularization parameter.
            "ridge": ["choice", 1e-7],
            # an other random seed for the ESN initialization
            "seed": ["choice", 1234],
            "rc_connectivity": ["loguniform", 0.05, 0.30],
            "input_connectivity": ["loguniform", 0.05, 0.30]
            # "rc_connectivity": ["choice", 0.10],
            # "input_connectivity": ["choice", 0.10]
    
        }
    }
    
    # Objective functions accepted by ReservoirPy must respect some conventions:
    #  - dataset and config arguments are mandatory, like the empty '*' expression.
    #  - all parameters that will be used during the search must be placed after the *.
    #  - the function must return a dict with at least a 'loss' key containing the result
    # of the loss function. You can add any additional metrics or information with other
    # keys in the dict. See hyperopt documentation for more informations.
    
    
    def objective(dataset, config, *, iss, N, sr, lr, ridge, seed, rc_connectivity, input_connectivity):
    
        # This step may vary depending on what you put inside 'dataset'
        train_data, validation_data = dataset
        X_train, y_train = train_data
        X_val, y_val = validation_data
        prediction_steps = 99
        warmup = 100
    
        # You can access anything you put in the config
        # file from the 'config' parameter.
        instances = config["instances_per_trial"]
    
        # The seed should be changed across the instances,
        # to be sure there is no bias in the results
        # due to initialization.
        variable_seed = seed
    
        losses = []
        r2s = []
        for n in range(instances):
            # Build your model given the input parameters
            reservoir = Reservoir(N,
                                  sr=sr,
                                  lr=lr,
                                  inut_scaling=iss,
                                  seed=variable_seed,
                                  rc_connectivity=rc_connectivity,
                                  input_connectivity=input_connectivity)
    
            readout = Ridge(ridge=ridge)
            train_states = reservoir.run(X_train, reset=True)
            readout = readout.fit(train_states, y_train, warmup=warmup)
            reservoir <<= readout
            model = reservoir >> readout
    
            # Train your model and test your model.
            predictions = model.fit(X_train, y_train, warmup=warmup, force_teachers=True) \
                    .run(X_test)
            # predictions = model.fit(X_train, y_train, warmup=warmup, force_teachers=True) 
            
    
            warmup_y = model.run(X_train[:-prediction_steps], reset=True)

            Y_pred = np.empty((prediction_steps, 1))
            x = warmup_y[-1].reshape(1, -1)
            
            for i in range(prediction_steps):
                # Use initial warm-uo period
                if i < warmup:
                    x = model(x)
                else:
                    x = Y_pred[i - warmup].reshape(1, -1)

                x = model(x)
                Y_pred[i] = x
        
            predictions = Y_pred
    
    
            loss = nrmse(y_test, predictions, norm_value=np.ptp(X_train))
            r2 = rsquare(y_test, predictions)
    
            # Change the seed between instances
            variable_seed += 1
    
            losses.append(loss)
            r2s.append(r2)
    
        # Return a dictionnary of metrics. The 'loss' key is mandatory when
        # using hyperopt.
        # print(np.mean(losses))
        return {'loss': np.mean(losses),
                'r2': np.mean(r2s)}

    # Creating dir, if dir does not exists 
    mypath = "optimize-stocks/" + ticker + "/"
    isExists = os.path.exists(mypath) 
    if not isExists:
        os.makedirs(mypath)

    
    # we precautionously save the configuration in a JSON file
    # each file will begin with a number corresponding to the current experimentation run number.
    with open(f"{hyperopt_config['exp']}.config.json", "w+") as f:
        json.dump(hyperopt_config, f) # Dumper config filen
        # print(hyperopt_config)
        # print(type(hyperopt_config))
        # print(hyperopt_config['exp'])

        
    
    # dataset = ((X_train, y_train), (X_test, y_test))
    dataset = ((X_train, y_train), (X_test, y_test))
    # dataset = ([(X_train, y_train), (X_train, y_train)], [(X_test, y_test), (X_test, y_test)])
    
    best = research(objective, dataset,
                    f"{hyperopt_config['exp']}.config.json", ".")
    return best
