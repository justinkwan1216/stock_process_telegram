import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import pandas_datareader.data as web
file = "260780380/nasdaq_all.csv"
df = pd.read_csv(file, parse_dates=True, index_col=0)
df = df[(df['current_price'] < 100) & (df['current_price'] > 0) & (df['ATR_2'] < 1000) & \
        (df['ATR_2'] > 0) & (df['peak_difference'] < 1000) & (df['peak_difference'] > 0) & \
        (df['bot_difference'] < 1000) & (df['bot_difference'] > 0)]
print(df)
