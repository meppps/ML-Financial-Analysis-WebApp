import pandas as pd
import json
import requests

def scrape(stock):
    url = f'https://finviz.com/quote.ashx?t={stock}'
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    dfs = pd.read_html(r.text)

    df = dfs[5]
    col1 = df[[0,1]].set_index(0)[1]
    marketCap = col1['Market Cap']
    col2 = df[[10,11]].set_index(10)[11]
    col2
    price = col2['Price']
    dailyChange = col2['Change']
    week = col2['Perf Week']
    month = col2['Perf Month']
    quarter = col2['Perf Quarter']
    
    try:
        newsList = []
        headlines = pd.read_html(r.text,attrs={'id':'news-table'})[0][1]
        if headlines.size >= 10:
            for i in range(0,10):
                headline = headlines[i]
                newsList.append(headline)
    except:
        print('No headlines')
        
    data = {
        'cap': marketCap,
        'price': price,
        'day': dailyChange,
        'week': week,
        'month': month,
        'quarter': quarter,
        'headlines':newsList
    }
    return data