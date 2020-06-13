import pandas as pd
from flask import Flask, jsonify, render_template,redirect,request
import math 
import numpy as np
import pandas as pd
import datetime
from pandas import Series, DataFrame
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
# from analyze import generatePlot
from .analyze import generatePlot
from .predict import forecast
from .scrape import scrape
from .multistock import multiStock
from flask import Markup

app=Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    start_date = datetime.datetime(2016, 1, 1)
    ## Select today's date as end date
    end_date = datetime.datetime.now().date().isoformat() 

    stocks_df = web.DataReader('FB', 'yahoo', start_date, end_date)
    return jsonify(stocks_df.to_dict("records"))


@app.route('/prediction/',methods=['GET','POST'])
def defaultPrediction():
    return render_template('dynamicForecast.html')


@app.route('/prediction/<stock>',methods=['GET','POST'])
def prediction(stock):
    if request.method == 'POST':
        # form = request.form
        stock = request.form['ticker']
        req = request
        print(req.form)
        ticker = request.form['ticker']
        ma1 = int(request.form['ma1'])
        ma2 = int(request.form['ma2'])
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        crossover = ''

        # Parameters can now be passed through for calculations
        results = forecast(ma1,ma2,ticker,from_date,to_date)

        data = scrape(ticker)

        cap = data['cap']
        price = data['price']
        day = data['day']
        week = data['week']
        month = data['month']
        quarter = data['quarter']
        headlines = data['headlines']
        trend = results['trend']
        value=Markup(results['html'])

        # img = f'predict.png'


        return render_template("dynamicForecast.html",from_date=from_date,to_date=to_date,ma1=ma1,ma2=ma2,ticker=ticker,crossover=crossover,trend=trend,cap=cap,price=price,day=day,week=week,month=month,quarter=quarter,value=value,headlines=headlines)   
        # return render_template('dynamicForecast.html',stock=stock)
    else:
        return render_template('dynamicForecast.html')

@app.route('/multi',methods=["POST","GET"])
def multi():
    if request.method == 'POST':
        ticker1 = request.form['symbol1']
        ticker2 = request.form['symbol2']
        ticker3 = request.form['symbol3']
        ticker4 = request.form['symbol4']
        from_date = request.form['from_date']
        to_date = request.form['to_date']
        multiStock(ticker1,ticker2,ticker3,ticker4,from_date,to_date)
        return render_template('multi.html',ticker1=ticker1,ticker2=ticker2,ticker3=ticker3,ticker4=ticker4,from_date=from_date,to_date=to_date)
    else:
        return render_template('multi.html')

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html')

@app.errorhandler(500)
def notFound(error):
    return render_template('error.html')

if __name__ == "__main__":
    app.run()