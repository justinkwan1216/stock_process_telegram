import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from ta.volatility import AverageTrueRange
import yfinance as yf

def low_open(user_id="",ticker="AAPL",period="5y",interval="1wk",short_percent=0.045,rank=0.9):
    df = yf.download(ticker, period=period,interval=interval)
    def take_first(array_like):
        return array_like[0]
    def take_last(array_like):
        return array_like[-1]
    #df = df.resample('W-MON').agg(
    #{'Open'  :'first',
    # 'High'  :'max',
    # 'Low'   :'min',
    # 'Close' :'last',
    # 'Volume':'sum'
    #})
    df['Low-Open'] = df['Low']-df['Open']
    df['Low-Open_percent'] = df['Low-Open']/df['Open']
    df = df.sort_values('Low-Open_percent')
    a = df['Low-Open_percent'].values
    a = a[~np.isnan(a)]
    try:
        za = (a > -short_percent).sum()/len(a)
        p = np.nanpercentile(a, 100-rank*100) # return 50th percentile, e.g median.
    except:
        pass
    ar = np.arange(len(a)) # just as an example array
    # evaluate the histogram
    values, base = np.histogram(a, bins=40)
    #evaluate the cumulative
    cumulative = np.cumsum(values)
    # plot the cumulative function

    #fig, ax = plt.subplots()
    #fig2, ax2 = plt.subplots()
    #ax.plot(base[:-1], cumulative, c='blue')
    #plot the survival function
    #ax.plot(base[:-1], len(a)-cumulative, c='green')
    #ax.hist(a[:-1],bins=40)
    #ax2.plot(ar, a, '.')
    #extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    #extent2 = ax2.get_window_extent().transformed(fig2.dpi_scale_trans.inverted())
    #fig.savefig(user_id+'/ax2_figure.png')
    #fig2.savefig(user_id+'/ax_figure.png')

    return za,p,df

def high_open(user_id="",ticker="AAPL",period="5y",interval="1wk",long_percent=0.045,rank=0.9):
    df = yf.download(ticker, period=period,interval=interval)
    def take_first(array_like):
        return array_like[0]
    def take_last(array_like):
        return array_like[-1]
    #df = df.resample('W-MON').agg(
    #{'Open'  :'first',
    # 'High'  :'max',
    # 'Low'   :'min',
    # 'Close' :'last',
    # 'Volume':'sum'
    #})
    df['High-Open'] = df['High']-df['Open']
    df['High-Open_percent'] = df['High-Open']/df['Open']
    df = df.sort_values('High-Open_percent')
    a = df['High-Open_percent'].values
    a = a[~np.isnan(a)]
    try:
        za = (a < long_percent).sum()/len(a)
        p = np.nanpercentile(a, rank*100) # return 50th percentile, e.g median.
    except:
        pass
    ar = np.arange(len(a)) # just as an example array
    # evaluate the histogram
    values, base = np.histogram(a, bins=40)
    #evaluate the cumulative
    cumulative = np.cumsum(values)
    # plot the cumulative function

    #fig, ax = plt.subplots()
    #fig2, ax2 = plt.subplots()
    #ax.plot(base[:-1], cumulative, c='blue')
    #plot the survival function
    #ax.plot(base[:-1], len(a)-cumulative, c='green')
    #ax.hist(a[:-1],bins=40)
    #ax2.plot(ar, a, '.')
    #extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    #extent2 = ax2.get_window_extent().transformed(fig2.dpi_scale_trans.inverted())
    #fig.savefig(user_id+'/ax2_figure.png')
    #fig2.savefig(user_id+'/ax_figure.png')

    return za,p,df
