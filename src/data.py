# Creating training data
import yfinance as yf
import numpy


# Making chances just for fun

def stock_price(ticker, START, END):
    df = yf.download(ticker, start=START, end=END)
    price = df['Adj Close'].to_numpy().reshape(-1, 1)
    return price
    
    

