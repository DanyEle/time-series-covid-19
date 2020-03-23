# -*- coding: utf-8 -*-
"""
Daniele Gadler
Coronavirus spreading in the Province of Bolzano.
Infeced people data has been downloaded from: 
http://www.provincia.bz.it/news/it/news.asp
Coordinates data from: 
http://www.dossier.net/utilities/coordinate-geografiche/provincia-bolzano.htm
"""
import pandas as pd
import numpy as np

#Goal: have all the time series data in a unique data frame, ready to be plotted with their coordinates

######DATA 21.03.2020 - 22.03.2020
df_pab_21_22_03 = pd.read_csv("./dati_quarantena_pab_csv/21_22_03_2020.csv", sep=";")

########COORDINATES
df_coordinate_comuni_pab = pd.read_csv("./dati_quarantena_pab_csv/coordinate_comuni_alto_adige.csv", sep=";")

#Associate the coordinates to the different 'comuni via a merge
df_data_pab_coordinate = pd.merge(df_pab_21_22_03, df_coordinate_comuni_pab, on="Comune di residenza")

#Good, we have successfully assigned coordinates to 84 comuni. let's see the remaining ones and fix the data in the 
#original data for the coordinates

set(df_pab_21_22_03["Comune di residenza"]) - set(df_data_pab_coordinate["Comune di residenza"])

#Let's discard the 'Fuori Provincia' and 'nan' cases for now
df_pab_coordinate_cleaned_21_22_03 = df_data_pab_coordinate[df_data_pab_coordinate["Comune di residenza"] != "Fuori provincia"]


######DATA 19.03.2020 - 20.03.2020
df_pab_19_20_03 = pd.read_csv("./dati_quarantena_pab_csv/19_20_03_2020.csv", sep=";")

#Remove useless column 'Unnamed'
df_pab_19_20_03.drop(df_pab_19_20_03.columns[df_pab_19_20_03.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

#remove rows containing na values
df_pab_19_20_03_no_na = df_pab_19_20_03.dropna()

#Let's perform a merge on the 'Cod Istat', "Comune di residenza" and "Wohngemeinde"
df_data_pab_coordinates_cleaned_19_21_22_03 = pd.merge(df_pab_coordinate_cleaned_21_22_03, df_pab_19_20_03_no_na, how="outer", on=["Cod Istat", "Comune di residenza", "Wohngemeinde"])


