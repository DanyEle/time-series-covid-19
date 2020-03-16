# -*- coding: utf-8 -*-
"""
Daniele Gadler
Coronavirus time series prediction
based on ARIMA model
Updated to 15.03.2020
https://www.youtube.com/watch?v=e8Yw4alG16Q
"""

import urllib.request, json 
import json
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

#Let's read the JSON from the online repo so that we always get the latest version of the data
with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json") as url:
    json_data = json.loads(url.read().decode())


#Let's get all the dates in each dictionary
list_dates = [dict_date["data"] for dict_date in json_data]

#Let's get all the 'totale casi' in each dictionary
list_totale_casi = [dict_date["totale_casi"] for dict_date in json_data]

#Let's compute a diff 

list_diff_casi = []
for x, y in zip(list_totale_casi[0::], list_totale_casi[1::]): 
    list_diff_casi.append(y-x) 
    
list_diff_casi.insert(0, 0)

plt.plot(list_dates, list_diff_casi)
plt.title("Nuovi casi di Covid-19 in Italia")
plt.xticks(rotation=90)

plt.plot(list_dates, list_totale_casi)
plt.title("Numero di casi di Covid-19 in Italia")
plt.xticks(rotation=90)

#Let's take a look at the data
print(list_dates)
print(list_totale_casi)

#Input: - list_data: a list of floating-point numbers or integers that we want to analyse
#       - list_dates: a list of strings that we want to use as daily dates
#       - days_prediction(int), the number of upcoming days for which we want to draw predictions
#Output: - fig, a figure plotting the past data and forecasted data
def arima_predict(list_data, list_dates, days_prediction):
    df_data_frame = pd.DataFrame({"data" : list_data})
    df_data_frame.index=list_dates
    df_data_frame.index = pd.DatetimeIndex(df_data_frame.index).to_period('D')

    #ARIMA model forforecasting upcoming values
    model = ARIMA(df_data_frame, order=(2, 1, 0))
    results_ARIMA = model.fit(disp=-1)
    
    fig = results_ARIMA.plot_predict(1, days_prediction)
    fig.suptitle("Numero totale casi di Covid-19 in Italia")
    
    
arima_predict(list_totale_casi, list_dates, 100)


   






