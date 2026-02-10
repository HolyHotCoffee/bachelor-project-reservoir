# Making Graph for our stocks
#
import matplotlib.pyplot as plt
import pandas as pd


"""Create datatable for plot_prediction"""
def datatable(START, END, n_prediction, seed, lr, sr, warmup, neurons, rc_connectivity, i_c):
    data = {'n predicton': [n_prediction], 'Start' : START, 'End' : END, 'Neurons' : neurons}
    x = range(1)
    df = pd.DataFrame(data, index=x)
    return df 



# Old Prediction
def plot_prediction(realprice_data, prediction_data, ticker, table):
    n_prediction = len(prediction_data)

    plt.figure(figsize=(10, 3))
    ax=plt.gca()

    # Generating profit table
    col_labels=['Potential Profit']
    table_vals=[[11000]]
    the_table = plt.table(cellText=table_vals,
                      colWidths = [0.1]*3,
                      colLabels=col_labels,
                      loc='best')
    plt.title(str(n_prediction) + " Days Stock price forecasting for " + ticker)
    plt.xlabel("$t$")

    # Adding table


    plt.plot(prediction_data, label="Predicted price", color="blue")
    plt.plot(realprice_data, label="Real price", color="red")
    plt.legend()
    plt.show()


'''Plotting prediction + Table'''
def plot_prediction2(realprice_data, prediction_data, ticker, table):
    n_prediction = len(prediction_data)

    fig, axs = plt.subplots(2, figsize=(10, 7))
    fig.suptitle(str(n_prediction) + " Days Stock price forecasting for " + ticker)

    
    # Plotting graph prediction and real price
    axs[0].plot(prediction_data, label="Predicted price", color="blue")
    axs[0].plot(realprice_data, label="Real price", color="red")
    axs[0].set_xlabel("time in days")
    axs[0].legend(loc = 'upper right')


    # Adding table
    df = table 
    axs[1].axis('off')  # turn off axis ticks and labels
    axs[1].table(cellText=df.values, colLabels=df.columns, loc='center')


    plt.legend()
    plt.show()



