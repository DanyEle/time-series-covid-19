# -*- coding: utf-8 -*-
"""
Daniele Gadler
Coronavirus time series prediction
based on ARIMA model
Updated to 15.03.2020
https://www.youtube.com/watch?v=e8Yw4alG16Q
"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
import pandas as pd
from pylab import rcParams
from datetime import datetime

rcParams['figure.figsize'] = 8, 6

df_input = pd.read_csv("TBD_Regression.csv", sep=";")

list_dates = df_input["YEAR"]

list_dates_format = [ datetime.strptime(str(x), '%Y') for x in list_dates ]

#DALY
list_totale_casi_daly = df_input["DALY"]
list_casi_converted_daly = [float(x.replace(",", ".")) for x in list_totale_casi_daly]
plt.plot(list_dates, list_casi_converted_daly)
plt.title("Cases per year - DALY")
plt.xticks(rotation=90)

#YLD
list_totale_casi_yld = df_input["YLD"]
list_casi_converted_yld = [float(x.replace(",", ".")) for x in list_totale_casi_yld]
plt.plot(list_dates, list_casi_converted_yld)
plt.title("Cases per year - YLD")
plt.xticks(rotation=90)


#Input: - list_data: a list of floating-point numbers or integers that we want to analyse
#       - list_dates: a list of strings that we want to use as daily dates
#       - days_prediction(int), the number of upcoming days for which we want to draw predictions
#Output: - fig, a figure plotting the past data and forecasted data
def arima_predict(list_data, list_dates, years_prediction, plot_title):
    df_data_frame = pd.DataFrame({"data" : list_data})
    df_data_frame.index=list_dates
    df_data_frame.index = pd.DatetimeIndex(df_data_frame.index).to_period('Y')

    #ARIMA model forforecasting upcoming values
    model = ARIMA(df_data_frame, order=(2, 1, 0))
    results_ARIMA = model.fit(disp=-1)
    
    fig = results_ARIMA.plot_predict(1, years_prediction)
    fig.suptitle(plot_title)
    
arima_predict(list_casi_converted_daly, list_dates_format, 18, "Number cases predicted DALY")
arima_predict(list_casi_converted_yld, list_dates_format, 18, "Number cases predicted YLD")




