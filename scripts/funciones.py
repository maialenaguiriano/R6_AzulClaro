# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 18:25:09 2021

@author: maialen
"""

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

