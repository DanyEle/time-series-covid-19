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



def load_clean_df(input_file_path):
    df_loaded = pd.read_csv(input_file_path, sep=";")

    #Remove useless column 'Unnamed'
    df_loaded.drop(df_loaded.columns[df_loaded.columns.str.contains('unnamed',case = False)], axis = 1, inplace = True)
    
    #remove rows containing na values
    df_loaded_no_na = df_loaded.dropna()
    
    return(df_loaded_no_na)
    
    
        

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

#######DATA 19.03.2020 - 20.03.2020
df_pab_19_20_03 = load_clean_df("./dati_quarantena_pab_csv/19_20_03_2020.csv")

#Let's perform a merge on the 'Cod Istat', "Comune di residenza" and "Wohngemeinde"
df_pab_coordinates_cleaned_19_20_21_22_03 = pd.merge(df_pab_coordinate_cleaned_21_22_03, df_pab_19_20_03, how="outer", on=["Cod Istat", "Comune di residenza", "Wohngemeinde"])

#####DATA 18.03.2020
df_pab_18_03 = load_clean_df("./dati_quarantena_pab_csv/18_03_2020.csv")
df_pab_18_03["Cod Istat"] = df_pab_18_03["Cod Istat"].astype("object")
#let's convert every single codice istat to a string
df_pab_18_03["Cod Istat"] = [str(x) for x in df_pab_18_03["Cod Istat"]]

#Let's perform a merge
df_data_pab_coordinates_cleaned_18_19_20_21_22_03 = pd.merge(df_pab_18_03, df_pab_coordinates_cleaned_19_20_21_22_03,how="outer",on=["Cod Istat"])

#Let's remove the useless resulting columns
df_data_pab_coordinates_cleaned_18_19_20_21_22_03["Comune di residenza"] = df_data_pab_coordinates_cleaned_18_19_20_21_22_03["Comune di residenza_y"]

df_data_pab_coordinates_cleaned_18_19_20_21_22_03.drop(columns=["Comune di residenza_x", "Comune di residenza_y"], inplace=True)


#######DATA 16.03.2020
df_pab_16_03 = load_clean_df("./dati_quarantena_pab_csv/16_03_2020.csv")

#Let's remove all the values that have a "Cod Istat" == 0 (located outside Alto Adige)
df_pab_16_03_cleaned = df_pab_16_03[df_pab_16_03["Cod Istat"] != 0]

#Let's perform a cast to integer and string of every single code
df_pab_16_03_cleaned["Cod Istat"] = [str(int(x)) for x in df_pab_16_03_cleaned["Cod Istat"]]

#Let's perform a merge
df_data_pab_coordinates_cleaned_16_18_19_20_21_22_03 = pd.merge(df_pab_16_03_cleaned, df_data_pab_coordinates_cleaned_18_19_20_21_22_03,how="outer",on=["Cod Istat"])
df_data_pab_coordinates_cleaned_16_18_19_20_21_22_03["Comune di residenza"] = df_data_pab_coordinates_cleaned_16_18_19_20_21_22_03["Comune di residenza_y"]
df_data_pab_coordinates_cleaned_16_18_19_20_21_22_03.drop(columns=["Comune di residenza_x", "Comune di residenza_y"], inplace=True)

df_out = df_data_pab_coordinates_cleaned_16_18_19_20_21_22_03

#Remove useless columns
df_out_cleaned = df_out.drop(columns=["aumento di casi dal giorno precedente_x", "aumento di casi dal giorno precedente_y"])

#Let's remove all the rows that have NAs in them, namely the ones with cod istat == 42068 and 42082 
df_out_no_na = df_out_cleaned[df_out_cleaned["Cod Istat"] != "42082"]
df_out_no_na = df_out_no_na[df_out_no_na["Cod Istat"] != "42068"]
df_out_no_na = df_out_no_na[df_out_no_na["Cod Istat"] != "42068"]

#Great, let's now rename the columns before outputting them
df_out_no_na["16-03-2020"] = df_out_no_na["Numero casi al 16-03-2020"]
df_out_no_na["18-03-2020"] = df_out_no_na["Numero casi al 18-03-2020"]
df_out_no_na["19-03-2020"] = df_out_no_na["Numero casi al 19-03-2020"]
df_out_no_na["20-03-2020"] = df_out_no_na["Numero casi al 20-03-2020"]
df_out_no_na["21-03-2020"] = df_out_no_na["Numero casi al 21-03-2020"]
df_out_no_na["22-03-2020"] = df_out_no_na["Numero casi al 22-03-2020"]

df_out_ready = df_out_no_na.drop(columns=["Numero casi al 16-03-2020","Numero casi al 18-03-2020",
                                          "Numero casi al 19-03-2020", "Numero casi al 20-03-2020",
                                          "Numero casi al 21-03-2020","Numero casi al 22-03-2020" ])
    
df_out_ready.to_csv("PAB_time_series_16_22_03_2020.csv", index=False)





