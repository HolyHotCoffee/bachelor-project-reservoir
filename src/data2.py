import pandas as pd
import yfinance as yf
import os
import csv
import analyze

# 500 Days
START = '2018-01-05'
END = '2020-01-01'


def timeseries_to_csv(ticker, START, END):
    stock = yf.download(ticker, start=START, end=END)
    stock.to_csv(ticker + '.csv', index=False)


def csv_to_pd(tickers):
    data = {}
    df = pd.DataFrame(data)
    for ticker in tickers:
        data = df + pd.read_csv(ticker + '.csv')
    return data


def csv_to_df(ticker):
    data = pd.read_csv('data/timeseries' + ticker + '.csv')
    return data


"""
Automating: Saving all timeseries to csv.
Used to generate the timeseries folder.
"""


def fetch_all_timeseries_to_csv(tickers, START, END):
    for ticker in tickers:
        if os.path.exists('data/timeseries/' + ticker + '.csv'):
            pass
        else:
            stock = yf.download(ticker, start=START, end=END)
            stock.to_csv('data/timeseries/' + ticker + '.csv', index=True)

# Get all S&P Tickers
# file = open("SP500.csv", "r")
# data = list(csv.reader(file, delimiter="\n"))
# # data = pd.read_csv("SP500.csv")
# file.close()
# # df = pd.DataFrame(data)
#
# flat_list = [item for sublist in data for item in sublist]
#
# # print(data)
#
# # Fetchin S&P500 to csv files (Faster to load)
# fetch_all_timeseries_to_csv(flat_list, START, END)

# ad a
#
#
# adadad


########################################
###### Creating sorted profit DF #######
########################################
tickers = ['AOS', 'AMZN', 'TSLA', 'AAPL', 'ABT', 'ABBV', 'ACN']

# Finding the stocks we want to invest in
i = 0
datatable = pd.DataFrame(index=['Start price', 'Exspected price', 'Profit'])
# datatable[0] = ['1', '2', '3']
# tickers = data.flat_list

# tickers = next(walk('data/timeseries'), (None, None, []))[2]
# Get all S&P Tickers
file = open("SP500.csv", "r")
data = list(csv.reader(file, delimiter="\n"))
# # data = pd.read_csv("SP500.csv")
file.close()
# # df = pd.DataFrame(data)
# #
flat_list = [item for sublist in data for item in sublist]
tickers = flat_list
#
#
#
while i < len(tickers):
    try:
        df_training = yf.download(tickers[i], start=START, end=END)
        n_simulations = 100

        df = analyze.Mc_Simulation(df_training, n_simulations)

        total = 0
        j = 0
        while j < n_simulations:
            total = total + df[i][len(df) - 1]
            j = j + 1
#
        start_price = df_training['Adj Close']
        start_price = start_price[len(df_training) - 1]
        exspected_price = total / n_simulations  # Exspected end price.
        exspected_profit = exspected_price - start_price
        datatable[tickers[i]] = [start_price,
                                 exspected_price, exspected_profit]
        i = i + 1
    except:
        i = i + 1
        pass
#
# Sorting tickets by profits
df = datatable.sort_values(by='Profit', ascending=False, axis=1)
df.to_csv('out.csv')
#
# Take n, best performing companies
# # print(df.iloc[:, : 3])


def MC_sorted_tickers(tickers):

    global df, start_price
    i = 0
    while i < len(tickers):
        try:
            df_training = yf.download(tickers[i], start=START, end=END)
            n_simulations = 100
            total = 0
            j = 0
            while j < n_simulations:
                total = total + df[i][len(df) - 1]
                j = j + 1
#
            start_price = df_training['Adj Close']
            start_price = start_price[len(df_training) - 1]
            exspected_price = total / n_simulations  # Exspected end price.
            exspected_profit = exspected_price - start_price
            datatable[tickers[i]] = [start_price,
                                     exspected_price, exspected_profit]
            i = i + 1
        except:
            i = i + 1
            pass
