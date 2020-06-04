import math 
import numpy as np
import pandas as pd
import datetime
from pandas import Series, DataFrame
## Note: Install pandas_datareader
## pip install pandas-datareader
import pandas_datareader.data as web
# %matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import style

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

def generatePlot(ma1,ma2,ticker):
    def calcDate(interval):
        
        if interval == 'month':
            time = 30
        elif interval == 'year':
            time = 365
        elif interval == 'fiveYear':
            time = 1825
        tod = datetime.datetime.now()
        d = datetime.timedelta(days = time)
        a = tod - d
        selectedDate = a.date().isoformat()
    #     print(selectedDate)
        return selectedDate

    ## Loading Yahoo Finance data set form 2016
    # Get start and end dates 

    # times = 1 year 6 month 3 month  

    start_date = datetime.datetime(2019, 5, 9)
    # start_date = calcDate('year')
    ## Select today's date as end date
    end_date = datetime.datetime.now().date().isoformat() 
    print(end_date)
    stocks_df = web.DataReader(ticker, 'yahoo', start_date, end_date)

    # Displaying letest 5 records
    # stocks_df.tail()

    ## Getting Final Closing price
    closing_price_df= stocks_df['Adj Close']

    closing_price_df.index = pd.to_datetime(closing_price_df.index)

    ## Calculate 50 day Moving Average
    ma_1 = closing_price_df.rolling(window=ma1).mean()

    ma_1.index = pd.to_datetime(ma_1.index)


    ma_1.dropna(inplace=True)


    ma_2 = closing_price_df.rolling(window=ma2).mean()

    ma_2.index = pd.to_datetime(ma_2.index)

    ma_2.dropna(inplace=True)




    #The size for our chart:
    plt.figure(figsize = (12,6))
    #Plotting price and SMA lines:
    plt.plot(closing_price_df, label='Adj Closing Price', linewidth = 2)
    plt.plot(ma_1, label=f'{ma1} Day SMA', linewidth = 1.5)
    plt.plot(ma_2, label=f'{ma2} Day SMA', linewidth = 1.5)
    #Adding title and labeles on the axes, making legend visible:
    plt.xlabel('Date')
    plt.ylabel('Adjusted Closing Price ($)')
    plt.title(ticker)
    plt.legend()
    # plt.show()
    plt.savefig('/static/mac.png')

    

# generatePlot(20,200,'MSFT')