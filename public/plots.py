# Importing dependencies
import math 
import numpy as np
import pandas as pd
import datetime
from pandas import Series, DataFrame
## Note: Install pandas_datareader
## pip install pandas-datareader
import pandas_datareader.data as web
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

## Loading Yahoo Finance data set form 2016
# Get start and end dates 
start_date = datetime.datetime(2016, 1, 1)
## Select today's date as end date
end_date = datetime.datetime.now().date().isoformat() 

stocks_df = web.DataReader('FB', 'yahoo', start_date, end_date)

# Displaying letest 5 records
stocks_df.tail()

## Getting Final Closing price
closing_price_df= stocks_df['Adj Close']

closing_price_df.index = pd.to_datetime(closing_price_df.index)

closing_price_df.tail()

closing_price_df.head()

## Calculate 50 day Moving Average
ma_50day= closing_price_df.rolling(window=50).mean()

ma_50day.index = pd.to_datetime(ma_50day.index)

## Removing NULL Coulumns
ma_50day.dropna(inplace=True)
ma_50day.head()

ma_50day.head()

## Calculate 200 day Moving Average
ma_200day= closing_price_df.rolling(window=200).mean()

ma_200day.index = pd.to_datetime(ma_200day.index)

## Removing NULL Coulumns
ma_200day.dropna(inplace=True)
ma_200day.head()

rets = closing_price_df / closing_price_df.shift(1) - 1
rets.plot(label='return')
plt.show()