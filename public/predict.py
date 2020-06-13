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

def parseDate(date):
    format_str = "%m/%d/%y" # The format
    datetime_obj = datetime.datetime.strptime(date, format_str).date().isoformat()
    print(datetime_obj)
    return datetime_obj





def forecast(ma1,ma2,ticker,from_date,to_date):
    plt.clf()
  
    # start_date = datetime.datetime(2016, 5, 10)
    if to_date == '0':
        end_date = datetime.datetime.now().date().isoformat()
    else:
        end_date = to_date

    start_date = parseDate(from_date)
    
    # end_date = parseDate(to_date) 

    stocks_df = web.DataReader(ticker, 'yahoo', start_date, end_date)

    closing_price_df= stocks_df['Adj Close']

    closing_price_df.index = pd.to_datetime(closing_price_df.index)

    print(closing_price_df.tail(1))

    ## calc moving averages
    ## temp


    ## Calculate 50 day Moving Average
    ma_1 = closing_price_df.rolling(window=ma1).mean()
    ma_1.index = pd.to_datetime(ma_1.index)
    ma_1.dropna(inplace=True)

    ma_2 = closing_price_df.rolling(window=ma2).mean()
    ma_2.index = pd.to_datetime(ma_2.index)
    ma_2.dropna(inplace=True)

    # mas=[ma_1.tail(1).squeeze(),ma_2.tail(1).squeeze()]
    # def mac(smas):
    # #outputs
    #     sma1 = smas[0]
    #     sma2 = smas[1]
    #     # print(max(ma1,ma2))
    #     if ma1 != ma2:
    #         maps = {
    #             ma1:smas[0],
    #             ma2:smas[1]
    #         }
    #         if ma1 < ma2:
    #             # cross up
    #             if maps[ma1] > maps[ma2]:
    # #                 print('cross up')
    #                 return 'Up'
    #             else:
    #                 return 'Down'
    # #                 print('cross down')
    #         elif ma2 > ma1:
    #             if maps[ma2] < maps[ma1]:
    #                 return 'Up'
    #             else: 
    #                 return 'Down'
                    
    #         else:
    #             return 'Undetermined'
    # crossover = mac(mas)




    #high low percentage 
    dfreg = stocks_df.loc[:,['Adj Close','Volume']]
    dfreg['HL_PCT'] = (stocks_df['High'] - stocks_df['Low']) / stocks_df['Close'] * 100.0
    #percentage change 
    dfreg['PCT_change'] = (stocks_df['Close'] - stocks_df['Open']) / stocks_df['Open']  * 100.0

    #drop missing value 
    dfreg.fillna(value=99999, inplace = True)
    forecast_out = int(math.ceil(0.01*len(dfreg)))

    forecast_col = 'Adj Close'
    dfreg['label'] = dfreg[forecast_col].shift(-forecast_out)
    X = np.array(dfreg.drop(['label'], 1))

    #linear regression
    #X = preprocessing.scale(X)

    #train for model generation and evaluation 
    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]

    y = np.array(dfreg['label'])
    y = y[:-forecast_out]


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    #linear regression
    clfreg = LinearRegression(n_jobs=-1)
    clfreg.fit(X_train, y_train)
    #quadratic regression
    clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge())
    clfpoly2.fit(X_train, y_train)

    clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge())
    clfpoly3.fit(X_train, y_train)

    #KNN Regression 
    clfknn = KNeighborsRegressor(n_neighbors=2)
    clfknn.fit(X_train, y_train)

    #evaluation 
    conf_reg = clfreg.score(X_test, y_test)
    confpoly2 = clfpoly2.score(X_test, y_test)
    confpoly3 = clfpoly3.score(X_test, y_test)
    confidenceknn = clfknn.score(X_test, y_test)

    forecast_set = clfreg.predict(X_lately)
    dfreg['Forecast'] = np.nan

    np.array([191.54990963, 188.1837365 , 185.22907692, 191.73701731,
        202.68987939, 201.99275306, 204.57470538, 204.22774733,
        206.14309605, 207.74508456, 208.88960301])
    #plotting prediciton 
    last_date = dfreg.iloc[-1].name
    last_unix = last_date
    next_unix = last_unix + datetime.timedelta(days=1)

    for i in forecast_set:
        next_date = next_unix
        next_unix += datetime.timedelta(days=1)
        dfreg.loc[next_date] = [np.nan for _ in range(len(dfreg.columns)-1)]+[i]


    dfreg['Adj Close'].tail(500).plot(color='black')
    dfreg['Forecast'].tail(500).plot(color='orange',label='Forecast')

    forecastHTML = pd.DataFrame(dfreg['Forecast'].tail(8)).to_html()
    

    def trend():
        forecastDF = dfreg['Forecast'].tail(500).dropna()
        if forecastDF.tail(1).squeeze() > forecastDF.head(1).squeeze(): 
            return 'Bullish'
        elif forecastDF.tail(1).squeeze() < forecastDF.head(1).squeeze():
            return 'Bearish'
        else:
            return 'Neutral'
    forecastedTrend = trend()

    

    plt.title(ticker)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.plot(ma_1, label=f'{ma1} Day SMA', linewidth = 1.5,color='pink')
    plt.plot(ma_2, label=f'{ma2} Day SMA', linewidth = 1.5,color='aqua')
    plt.legend(loc='best')
    # plt.show()

    plt.savefig('public/static/predict.png')
    plt.close()

    results = {
        'trend':forecastedTrend,
        'html':forecastHTML
    }

    return results



# forecast(50,200,'AAPL')