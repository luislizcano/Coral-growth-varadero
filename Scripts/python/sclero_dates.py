# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 10:59:59 2026

@author: lizca
"""



import os
import pandas as pd
import numpy as np

# =============================================================================
## Load Excel file using pandas
## To make sure set the file path
dir = 'E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Sclerocronology'
os.chdir(dir)

# from functions import mean_yr,mean_cols,STDA,STDAidx,climat,linreg,mean_range,\
#                 stats_all,detect_changes,check_assumptions

data = pd.ExcelFile('Sclerocronology_v2.xlsx')
sheet = data.parse(0)

### Dates - according temperature climatology
hi = '-10-31'
lo = '-02-28'

# =============================================================================
# DATE INTERPOLATIONS
# =============================================================================
### Number of band pairs. Band 1 is from 2016
n_bands = sheet['Pair'].dropna().drop_duplicates()
sheet['Fecha'] = None
for i in n_bands:
    y = int(2016 + 1 - i)
    year = str(y)
    hi_date = year+hi
    lo_date = year+lo
    
    sheet.loc[(sheet['Pair'] == i) & (sheet['Banda'] == 'Alta'), 'Fecha'] = hi_date
    sheet.loc[(sheet['Pair'] == i) & (sheet['Banda'] == 'Baja'), 'Fecha'] = lo_date

### Interpolate dates:
    
## Convert Date column to datetime objects
sheet['Fecha'] = pd.to_datetime(sheet['Fecha'])
## Convert valid dates to unix timestamps (seconds), leaving NaNs as NaN
sheet['Fecha_seconds'] = sheet['Fecha'].apply(lambda x: x.timestamp() if pd.notnull(x) else np.nan)
## Linearly interpolate the missing timestamps
sheet['Fecha_seconds'] = sheet['Fecha_seconds'].interpolate(method='linear')
## Convert the filled numbers back into clean date formats
sheet['Fecha'] = pd.to_datetime(sheet['Fecha_seconds'], unit='s').dt.date
## Drop the temporary numbers column
sheet.drop(columns=['Fecha_seconds'], inplace=True)

# =============================================================================
# GROWTH PARAMETERS - ANNUAL
# =============================================================================
### Density
# 1. Asegurar que la columna "Fecha" tenga formato de fecha (datetime)
sheet['Fecha'] = pd.to_datetime(sheet['Fecha'])
# 2. Extraer el año y agrupar sumando la columna "Densidad"
density = sheet.groupby(sheet['Fecha'].dt.year)['Densidad'].mean().reset_index()
# 3. Renombrar la columna resultante para mayor claridad
density.columns = ['Year', 'Density']

### Extension
# 1. Agrupar por año y extraer el primer ('first') y último ('last') valor de Distance
extension = sheet.groupby(sheet['Fecha'].dt.year)['Distancia (cm)'].first().reset_index()
extension['Extension'] = extension['Distancia (cm)'].diff().abs()

## Calcification
growth = density
growth['Extension'] = extension['Extension']
growth['Calcification'] = growth['Density'] * growth['Extension']


# =============================================================================
# GROWTH PARAMETERS - MONTHLY
# =============================================================================
### Density
sheet['Fecha'] = pd.to_datetime(sheet['Fecha'])
density_mo = sheet.groupby([sheet['Fecha'].dt.year.rename('Year'), 
                            sheet['Fecha'].dt.month.rename('Month')])['Densidad'].mean().reset_index()
### Extension
extension_mo = sheet.groupby([sheet['Fecha'].dt.year.rename('Year'), 
                              sheet['Fecha'].dt.month.rename('Month')])['Distancia (cm)'].first().reset_index()
extension_mo['Extension'] = extension_mo['Distancia (cm)'].diff().abs()
## Calcification
growth_mo = density_mo
growth_mo['Extension'] = extension_mo['Extension']
growth_mo['Calcification'] = growth_mo['Densidad'] * growth_mo['Extension']

# =============================================================================
# COMPLETE MISSING MISSING MONTHS WITH NANS
# =============================================================================
df = growth_mo
# 1. Crear una columna temporal de tipo datetime para poder secuenciar los meses
df['Fecha_Tmp'] = pd.to_datetime(df['Year'].astype(int).astype(str) + '-' + 
                                 df['Month'].astype(int).astype(str) + '-01')

# 2. Establecer esa fecha como el índice
df.set_index('Fecha_Tmp', inplace=True)

# 3. Generar un rango mensual completo desde el primer mes hasta el último
rango_completo = pd.date_range(start=df.index.min(), end=df.index.max(), freq='MS') # 'MS' = Month Start

# 4. Reindexar el DataFrame para forzar la inclusión de los meses faltantes (se llenarán con NaN)
df_completo = df.reindex(rango_completo)

# 5. Reconstruir las columnas 'Year' y 'Month' para las nuevas filas añadidas
df_completo['Year'] = df_completo.index.year
df_completo['Month'] = df_completo.index.month

# 6. Limpiar el índice para volver a tu formato original de columnas
df_completo.reset_index(drop=True, inplace=True)
## Sort values
df_completo = df_completo.sort_values(by=['Year','Month'], ascending=False)

## Fix extension values next to missing data
## Be careful, only works with one missing values, if there are two rows or months
## without values, it should be adjusted manually dividing by 3 or more.
empty = df_completo['Extension'].shift(-1).isna()
df_completo.loc[empty, 'Extension'] = df_completo['Extension'] / 2
## Now for calcification:
empty = df_completo['Calcification'].shift(-1).isna()
df_completo.loc[empty, 'Calcification'] = df_completo['Calcification'] / 2
df_completo['interpolated'] = df_completo['Densidad'].interpolate()