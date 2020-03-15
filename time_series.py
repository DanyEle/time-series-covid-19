# -*- coding: utf-8 -*-
"""
Daniele Gadler
Coronavirus time series prediction
based on ARIMA model
Updated to 15.03.2020
https://www.youtube.com/watch?v=e8Yw4alG16Q
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] = 10, 10

FILE_PATH="dpc-covid19-ita-andamento-nazionale.json"


with open(FILE_PATH, 'r') as f:
    json_virus = json.load(f)
    
#Let's get all the dates in each dictionary
list_dates = [dict_date["data"] for dict_date in json_virus]

#Let's get all the 'totale casi' in each dictionary
list_totale_casi = [dict_date["totale_casi"] for dict_date in json_virus]

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

#Rolling statistics, the time window is 1, since there is no "cyclic behaviour here"
df_totale_casi = pd.DataFrame({"totale_casi" : list_totale_casi})
df_totale_casi.index=list_dates
df_totale_casi.index = pd.DatetimeIndex(df_totale_casi.index).to_period('D')
    
rolling_mean = df_totale_casi["totale_casi"].rolling(window=3).mean()

plt.xticks(rotation=90)
#Let's plot the trend every 3 days
plt.plot(list_dates, rolling_mean, list_totale_casi)

#Let's perform a test for stationarity with Dicker-Fuller
df_test = adfuller(df_totale_casi["totale_casi"], autolag="AIC")

df_output = pd.Series(df_test[0:4], index=["Test statistic", "p-value", "#Lags used", "Num. of obs used"])

#Cannot reject the null hypothesis, the data is NOT stationary!
print(df_output)

#ARIMA model forforecasting upcoming values
#Parameters for order: p-value, differentiating, Q-value
model = ARIMA(df_totale_casi, order=(2, 1, 0))
results_ARIMA = model.fit(disp=-1)

fig = results_ARIMA.plot_predict(1, 30)
fig.suptitle("Numero totale casi di Covid-19 in Italia")

   






