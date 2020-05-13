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
from analyze1 import generatePlot
from predict import forecast
from scrape import scrape

app=Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def index():
    return render_template("index.html")



@app.route("/submit",methods=["POST","GET"])
def submit():
    if request.method == 'POST':
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

        trend = results['trend']
        img = './static/predict.png'
        return render_template("submit.html",from_date=from_date,to_date=to_date,ma1=ma1,ma2=ma2,ticker=ticker,img=img,crossover=crossover,trend=trend,cap=cap,price=price,day=day,week=week,month=month,quarter=quarter)   
    else:
        return render_template("submit.html")

@app.route('/multi')
def multi():
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


if __name__ == "__main__":
    app.run(debug=True)