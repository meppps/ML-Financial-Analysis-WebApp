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
from random import randrange

def multiStock(ticker1,ticker2,ticker3,ticker4,from_date,to_date):

    def parseDate(date):
        format_str = '%m/%d/%y' # The format
        datetime_obj = datetime.datetime.strptime(date, format_str).date().isoformat()
        print(datetime_obj)
        return datetime_obj

    start_date = parseDate(from_date)
    end_date = parseDate(to_date)


    tickers =[ticker1, ticker2,ticker3,ticker4]
    comp_stocks_df = web.DataReader(tickers,'yahoo',start_date,end_date)['Adj Close']

    retscomp = comp_stocks_df.pct_change()
    corr = retscomp.corr()


    plt.scatter(retscomp[ticker1], retscomp[ticker2],alpha=0.3)
    plt.xlabel(f'Returns {ticker1}')
    plt.ylabel(f'Returns {ticker2}')

    plt.title(f'Returns on {ticker1} and {ticker2}')
    # plt.legend()

    plt.savefig('public/static/scatter.png')

    plt.clf()

    plt.imshow(corr, cmap='hot', interpolation='none')
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns)
    plt.yticks(range(len(corr)), corr.columns)
    plt.savefig('public/static/heatmap.png')

    plt.clf()
    
    plt.scatter(retscomp.mean(), retscomp.std())
    plt.xlabel('Expected returns')
    plt.ylabel('Risk')
    for label, x, y in zip(retscomp.columns, retscomp.mean(), retscomp.std()):
        plt.annotate(
            label, 
            xy = (x, y), xytext = (randrange(30),50),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

    plt.savefig('public/static/riskreturn.png')

    plt.clf()

# multiStock(ticker1,ticker2,ticker3,ticker4,start_date,end_date)