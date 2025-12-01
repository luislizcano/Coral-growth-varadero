# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 16:06:35 2025

@author: lizca

Comparisons between air temperature and SST data
"""


import os
import sys
import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy.stats import pearsonr

# =============================================================================
## Load Excel file using pandas
## To make sure set the file path
dir = 'E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Envdata_raw'
os.chdir(dir)

## Import pre-made functions
# caution: path[0] is reserved for script path
sys.path.insert(1, 
    'E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Scripts\\python')
from functions import STDA


data = pd.ExcelFile('Temperaturas_2025.xlsx')

## Check the type of file
print('File Type:',type(data))

## Check if the file has different sheets
data.sheet_names

## You can load data by number of sheet
air = data.parse(1)[['Year', 'Air_T']].dropna().reset_index(drop=True)
aqua = data.parse(2)[['Year', 'SST_Aqua']].dropna().reset_index(drop=True)
terra = data.parse(3)[['Year', 'SST_Terra']].dropna().reset_index(drop=True)
avhrr_d = data.parse(4)[['Year', 'AVHRR_Day']].dropna().reset_index(drop=True)
avhrr_n = data.parse(4)[['Year', 'AVHRR_Night']].dropna().reset_index(drop=True)
cci = data.parse(5)[['Year', 'SST_cci']].dropna().reset_index(drop=True)
had = data.parse(6)[['Year', 'HadISST']].dropna().reset_index(drop=True)
oisst = data.parse(7)[['Year', 'OISST']].dropna().reset_index(drop=True)

### STANDARDIZATIONS (Z-Scores)
z_air = pd.concat([air['Year'],STDA(air['Air_T'])],axis=1,join='inner')
z_aqua = pd.concat([aqua['Year'],STDA(aqua['SST_Aqua'])],axis=1,join='inner')
z_terra = pd.concat([terra['Year'],STDA(terra['SST_Terra'])],axis=1,join='inner')
z_avhrr_d = pd.concat([avhrr_d['Year'],STDA(avhrr_d['AVHRR_Day'])],axis=1,join='inner')
z_avhrr_n = pd.concat([avhrr_n['Year'],STDA(avhrr_n['AVHRR_Night'])],axis=1,join='inner')
z_cci = pd.concat([cci['Year'],STDA(cci['SST_cci'])],axis=1,join='inner')
z_had = pd.concat([had['Year'],STDA(had['HadISST'])],axis=1,join='inner')
z_oisst = pd.concat([oisst['Year'],STDA(oisst['OISST'])],axis=1,join='inner')

### CORRELATIONS
## The correlation is made with the number of valid data among each pair of variables.
## nans are discarded automatically.
data = pd.concat([z_air['Air_T'],z_aqua['SST_Aqua'],z_terra['SST_Terra'],
                  z_avhrr_d['AVHRR_Day'],z_avhrr_n['AVHRR_Night'],z_cci['SST_cci'],
                  z_had['HadISST'],z_oisst['OISST']],axis=1,join='outer')
corr = data.corr(method = 'pearson')
# Function to return p-value for pearsonr
def calculate_pvalue(col1, col2):
    return pearsonr(col1, col2)[1]
# Create a DataFrame to store p-values
p_values = data.corr(method=calculate_pvalue)


# =============================================================================
# FIGURES
# =============================================================================

### FIGURE 1. Temperature time series data (°C)
fig1, axes1 = plt.subplots(1, 1, figsize=(6,3), sharex=True)
X = 'Year'
Y = ['Air_T','SST_Aqua','SST_Terra','AVHRR_Day','AVHRR_Night','SST_cci',
     'HadISST','OISST']

# plt1 = sns.lineplot(y=[0,0], x=[1980,2017],ax=axes1,color='black',alpha=0.2)
plt1 = sns.lineplot(data=air, y=Y[0], x=X,color='black',label=Y[0])
plt1 = sns.lineplot(data=aqua, y=Y[1], x=X,linewidth=0.7,label=Y[1])
plt1 = sns.lineplot(data=terra, y=Y[2], x=X,linewidth=0.7,label=Y[2])
plt1 = sns.lineplot(data=avhrr_d, y=Y[3], x=X,linewidth=0.7,label=Y[3])
plt1 = sns.lineplot(data=avhrr_n, y=Y[4], x=X,linewidth=0.7,label=Y[4])
plt1 = sns.lineplot(data=cci, y=Y[5], x=X,linewidth=0.7,label=Y[5])
plt1 = sns.lineplot(data=had, y=Y[6], x=X,linewidth=0.7,label=Y[6])
plt1 = sns.lineplot(data=oisst, y=Y[7], x=X,linewidth=0.7,label=Y[7])

## Limits
axes1.set_xlim([1950,2016])
axes1.set(ylabel='Temperature (°C)')
## Legend
handles1, labels1 = axes1.get_legend_handles_labels()
plt1.legend(handles1, labels1, loc='upper left', ncols=2, fontsize=7)
## Ticks
axes1.xaxis.set_minor_locator(ticker.MultipleLocator(5))
axes1.xaxis.set_major_locator(ticker.MultipleLocator(10))

#fig1.savefig(dir+'\\fig1_Temperatures.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================

### FIGURE 2. Temperature time series data (Z-SCORES)
fig2, axes2 = plt.subplots(1, 1, figsize=(6,3), sharex=True)
X = 'Year'
Y = ['Air_T','SST_Aqua','SST_Terra','AVHRR_Day','AVHRR_Night','SST_cci',
     'HadISST','OISST']

plt2 = sns.lineplot(y=[0,0], x=[1950,2016],ax=axes2,color='black',alpha=0.2)
plt2 = sns.lineplot(data=z_air, y=Y[0], x=X,color='black',label=Y[0])
plt2 = sns.lineplot(data=z_aqua, y=Y[1], x=X,linewidth=0.7,label=Y[1])
plt2 = sns.lineplot(data=z_terra, y=Y[2], x=X,linewidth=0.7,label=Y[2])
plt2 = sns.lineplot(data=z_avhrr_d, y=Y[3], x=X,linewidth=0.7,label=Y[3])
plt2 = sns.lineplot(data=z_avhrr_n, y=Y[4], x=X,linewidth=0.7,label=Y[4])
plt2 = sns.lineplot(data=z_cci, y=Y[5], x=X,linewidth=0.7,label=Y[5])
plt2 = sns.lineplot(data=z_had, y=Y[6], x=X,linewidth=0.7,label=Y[6])
plt2 = sns.lineplot(data=z_oisst, y=Y[7], x=X,linewidth=0.7,label=Y[7])

## Limits
axes2.set_xlim([1950,2016])
# axes2.set_ylim([-3,3])
axes2.set(ylabel='Temperature (Normalized)')
## Legend
handles2, labels2 = axes2.get_legend_handles_labels()
plt2.legend(handles2, labels2, loc='upper left', ncols=4, fontsize=7)
## Ticks
axes2.xaxis.set_minor_locator(ticker.MultipleLocator(5))
axes2.xaxis.set_major_locator(ticker.MultipleLocator(10))

#fig2.savefig(dir+'\\fig2_Temperatures_stda.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================

### FIGURE 3. CORRELATION MATRIX
fig3, axes3 = plt.subplots(1,1, figsize=(5,4), dpi=150)
plt3 = sns.heatmap(corr,annot=True,fmt=".2f", linewidth=.5)
#fig3.savefig(dir+'\\fig3_Temperatures_corr.tiff', format='tiff', dpi=300,bbox_inches = 'tight')

### FIGURE 4. CORRELATION MATRIX - P- VALUES
fig4, axes4 = plt.subplots(1,1, figsize=(5,4), dpi=150)
plt4 = sns.heatmap(p_values,annot=True,fmt=".2f", linewidth=.5, vmin=0.01,vmax=0.05,
                   cbar=False,cmap=['#6a0000','#ffffff'])
#fig4.savefig(dir+'\\fig4_Temperatures_corr_p.tiff', format='tiff', dpi=300,bbox_inches = 'tight')
