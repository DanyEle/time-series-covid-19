# -*- coding: utf-8 -*-
"""
Daniele Gadler
Coronavirus time series prediction
based on ARIMA model
Updated to 15.03.2020
https://www.youtube.com/watch?v=e8Yw4alG16Q
"""



import pandas as pd
import io
import requests
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
import pandas as pd
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

#Let's read the JSON for all province
URL="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv"
url_content=requests.get(URL).content
df_province=pd.read_csv(io.StringIO(url_content.decode('utf-8')))

#Let's get the different columns making up the data frame
print(df_province.columns)

#Let's get the unique province codes
print(set(df_province["denominazione_provincia"]))

df_bz_provincia = df_province[df_province["denominazione_provincia"] == "Bolzano"]

list_dates = df_bz_provincia["data"]

list_totale_casi = df_bz_provincia["totale_casi"]

plt.plot(list_dates, list_totale_casi)
plt.title("Numero di casi di Covid-19 in Italia")
plt.xticks(rotation=90)

#Input: - list_data: a list of floating-point numbers or integers that we want to analyse
#       - list_dates: a list of strings that we want to use as daily dates
#       - days_prediction(int), the number of upcoming days for which we want to draw predictions
#Output: - fig, a figure plotting the past data and forecasted data
def arima_predict(list_data, list_dates, days_prediction, plot_title):
    df_data_frame = pd.DataFrame({"data" : list_data})
    df_data_frame.index=list_dates
    df_data_frame.index = pd.DatetimeIndex(df_data_frame.index).to_period('D')

    #ARIMA model forforecasting upcoming values
    model = ARIMA(df_data_frame, order=(2, 1, 0))
    results_ARIMA = model.fit(disp=-1)
    
    fig = results_ARIMA.plot_predict(1, days_prediction)
    fig.suptitle(plot_title)


arima_predict(list_totale_casi, list_dates, 50, "Numero totale casi di Covid-19 nella Provincia Autonoma di Bolzano")


