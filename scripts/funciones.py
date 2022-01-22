# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:25:09 2021

@author: maialen
"""
import pandas as pd  
import os
import numpy as np
import datetime as dt # para gestión de fechas
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure
from datetime import datetime
import locale
from scipy import stats
import re
import os
import glob

#Funcion para quitar filas duplicadas
def eliminar_duplicados(df):
    df.drop_duplicates(ignore_index= True, inplace= True)


#Función para identificar columnas duplicadas
def columnas_duplicadas(df):
    duplicates = []
    for col in range(df.shape[1]):
        contents = df.iloc[:, col]
        
    for comp in range(col + 1, df.shape[1]):
        if contents.equals(df.iloc[:, comp]):
            duplicates.append(comp)

    duplicates = np.unique(duplicates).tolist()
    print(duplicates)

#funcion para quitar columnas Unnamed
def eliminar_unnamed(df):
    df = df[df.columns[~df.columns.str.contains('Unnamed:')]] 

#funcion para eliminar missings
def identificar_missings(df):
    missing_data = df.isnull()
    for column in missing_data.columns.values.tolist():
        print(column)
        print(missing_data[column].value_counts())
        print('')

#funcion para cambiar el tipo 
def corregir_tipo(df, columnas, tipo):
    for col in columnas:
        df[col] = df[col].astype(tipo)

#Funcion para quitar columnas
def eliminar_columnas(df, columnas):
    df.drop(columns = columnas, inplace = True)

#Funcion para quitar dias de la semana
def eliminar_dias(df, columna):
    for i in range(len(df[columna])):
        dias = ["lunes, ", "martes, ", "miércoles, ", "jueves, ", "viernes, ", "sábado, ", "domingo, "]
        for dia in dias:
            df[columna] = df[columna].str.replace(dia, '') 

    
#Funcion para convertir la fecha de texto a numerico
def fecha_texto(df, columna):
    for index, value in enumerate(df[columna]):
        if value != '--':
            df.loc[index, columna]= datetime.strptime(value, '%d de %B de %Y, %H:%M')
        else:
            df.loc[index,columna] =  None

#Funcion para eliminar el DNI de program_name
def eliminar_dni(df,columna):
    for num, i in enumerate(df[columna]):
        i = str(i)
        if re.findall('TÉCNICO DEMO|TECNICO DEMO|TecnicoDemo', i, re.IGNORECASE):
            i = i.replace("TÉCNICO DEMO", "TECNICODEMO").replace("TECNICO DEMO", "TECNICODEMO").replace(' 2 ', '_2 ')
            i = i.split(' ')[0]
            df.loc[num, columna] = i


#Funcion para descargar los dataframes como csv
def convertir_csv(df, filename, path_dataset):
    #file_name1 = nombrecsv
    #path_dataset1 = '..\\datosTransformados\\'
    ruta_completa1 = path_dataset + filename
    df.to_csv(path_or_buf= str(ruta_completa1))

#Función para Eliminar los .csv existentes (antiguos) en la carpeta 
def eliminar_csv(path_dataset):
    for f in os.listdir(path_dataset):
        if not f.endswith(".csv"):
            continue
        os.remove(os.path.join(path_dataset, f))



