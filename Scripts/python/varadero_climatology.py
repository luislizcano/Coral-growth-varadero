# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:16:04 2021

@author: lizca

This script calculates annual averages and STDA from monthly data.
However, this is not longer necessary.

The only output from this script used in the manuscript is the climatology
of FIGURE S2
"""


import os
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

### 'ruptures' package required
#python -m pip install ruptures

# =============================================================================
## Load Excel file using pandas
## To make sure set the file path
dir = 'E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Scripts\\python'
os.chdir(dir)

## Import pre-made functions
from functions import mean_yr,mean_cols,STDA,STDAidx,climat

## Load data
data = pd.ExcelFile('varadero.xlsx')

## Check the type of file
print('File Type:',type(data))

## Check if the file has different sheets
data.sheet_names

## Load data by number of sheet
growth = data.parse(0) ## Growth data
lumin = data.parse(1) ## Luminescence data
envir = data.parse(2) ## Environmental data
print('Number of rows and columns:',growth.shape)

## Show just the 'head' of the sheet content in the console
## This is monthly data
print(growth.head())
print('Column names:',list(growth.columns))


# =============================================================================
# ## Calculate averages for coral growth and luminescence parameters (PER CORE)
# =============================================================================
growth_var = ['Density','Extension','Calcification']
core_index = ['VAR1','VAR2','VAR3','VAR4']

## For growth parameters:
growth_yr = mean_yr(growth,'Year',growth_var,'Core',core_index)
growth_yr = growth_yr.drop([0,5,6,8,9], axis=1)
growth_yr.columns = range(growth_yr.shape[1])
growth_yr.columns= ['Core','Year','Density','Den_std','Extension','Calcification']
growth_yr = growth_yr.reset_index(drop=True)

## For luminescence:
lumin_yr = mean_yr(lumin,'Year',['G/B'],'Core',core_index)
lumin_yr = lumin_yr.drop([0], axis=1)
lumin_yr.columns = range(lumin_yr.shape[1])
lumin_yr.columns= ['Core','Year','G/B','G/B_std']
lumin_yr = lumin_yr.reset_index(drop=True)
## For Envi variables:
#envir_yr = mean_yr(envir,'Year',['WaterFlow',],'Core',core_index)


# =============================================================================
# ### Parse environmental variables
# =============================================================================
wf = envir.loc[0:419,:]['WaterFlow']#.interpolate()
# wl = envir.loc[0:382,:]['WaterLevel']#.interpolate()
# sed = envir.loc[0:382,:]['Sediment']
temp = envir.loc[0:748,:]['Air_Temperature']
sst = envir.loc[0:407,:]['SST_CCI']
soi = envir.loc[0:755,:]['SOI']
amo = envir.loc[0:755,:]['AMO']
dateEnv = envir.iloc[0:756,0:3]#['Year','Month','Y.M']

#### CLIMATOLOGY of environmental variables
clim_wf = climat(wf,dateEnv,'Month')
# clim_wl = climat(wl,dateEnv,'Month')
# clim_sed = climat(sed,dateEnv,'Month')
clim_temp = climat(temp,dateEnv,'Month')
clim_sst = climat(sst,dateEnv,'Month')


# =============================================================================
# ## STANDARDIZED NORMALIZATIONS (Z-SCORES)
# =============================================================================
envir_var = ['WaterFlow','WaterLevel','Sediment','Air_Temperature',
             'SST_CCI','SOI','AMO']

stda_growth = pd.concat([growth[['Core','Y.M']],STDAidx(growth,growth_var,'Core',core_index)],axis=1)
stda_lumin = pd.concat([lumin[['Core','Y.M']],STDAidx(lumin,['G/B'],'Core',core_index)],axis=1)
stda_growth_yr = pd.concat([growth_yr[['Core','Year']],STDAidx(growth_yr,growth_var,'Core',core_index)],axis=1)
stda_lumin_yr = pd.concat([lumin_yr[['Core','Year']],STDAidx(lumin_yr,['G/B'],'Core',core_index)],axis=1)
stda_wf = pd.concat([dateEnv[['Y.M']],STDA(wf)],axis=1,join='inner')
# stda_wl = pd.concat([dateEnv[['Y.M']],STDA(wl)],axis=1,join='inner')
# stda_sed = pd.concat([dateEnv[['Y.M']],STDA(sed)],axis=1,join='inner')
stda_temp = pd.concat([dateEnv[['Y.M']],STDA(temp)],axis=1,join='inner')


# =============================================================================
# ## Calculate total (annual) mean and stdv by parameter
# =============================================================================
[growth_yr_mean,growth_yr_std] = mean_cols(growth_yr,'Year','Core',growth_var,core_index)
[stda_growth_yr_mean,stda_growth_yr_std] = mean_cols(stda_growth_yr,'Year','Core',growth_var,core_index)
[stda_lumin_yr_mean,stda_lumin_yr_std] = mean_cols(stda_lumin_yr,'Year','Core',['G/B'],core_index)


# =============================================================================
# ### PLOTS
# =============================================================================

# =============================================================================
# ### FIG S2. Climatologies
# =============================================================================
figS2, axesS2 = plt.subplots(2, 1, figsize=(3,4), sharex=True)

## Set variables
namex = 'Month'
ax_wf = 'Water flow (m3 s-1)'
ax_wl = 'Water level (cm)'
ax_sed = 'Sediment load (Kton d-1)'
ax_temp = 'SST (°C)'
monthlabel = ['J','F','M','A','M','J','J','A','S','O','N','D']

## plots
pltS2 = sns.lineplot(data=clim_wf, y="Mean", x="Months", ax=axesS2[0])
pltS2 = sns.lineplot(data=clim_sst,y="Mean", x="Months",ax=axesS2[1])
# pltS2 = sns.lineplot(data=clim_sed,y="Mean", x="Months",ax=axesS2[2])
# pltS2 = sns.lineplot(data=clim_wl,y="Mean", x="Months",ax=axesS2[3])
## Error
axesS2[0].fill_between(
    clim_wf['Months'],clim_wf['Mean']+clim_wf['Std'],clim_wf['Mean']-clim_wf['Std'],
    facecolor='#CDECFE',alpha=0.7)
axesS2[1].fill_between(
     clim_sst['Months'],clim_sst['Mean']+clim_sst['Std'],clim_sst['Mean']-clim_sst['Std'],
    facecolor='#CDECFE',alpha=0.7)
# axesS2[2].fill_between(
#     clim_sed['Months'],clim_sed['Mean']+clim_sed['Std'],clim_sed['Mean']-clim_sed['Std'],
#     facecolor='#CDECFE',alpha=0.7)
# axesS2[3].fill_between(
#     clim_wl['Months'],clim_wl['Mean']+clim_wl['Std'],clim_wl['Mean']-clim_wl['Std'],
#     facecolor='#CDECFE',alpha=0.7)
## Axis-Y Labels
axesS2[0].set(ylabel='Water flow \n($m^3 s^{-1}$)')
axesS2[1].set(ylabel='SST \n($°C$)')
# axesS2[2].set(ylabel='Sediment load \n($Gg$ $d^{-1}$)')
# axesS2[3].set(ylabel='Water level \n($cm$)')
for ax in axesS2:
    ax.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
    ax.set_xticklabels(monthlabel)

axesS2[1].set_ylim([26,31])

# figS2.savefig(dir+'\\figS2.tiff', format='tiff', dpi=600,bbox_inches = 'tight')



# =============================================================================
# ### FIG 2. STDA Coral growth time-series per core (NOT USED IN MANUSCRIPT)
# =============================================================================
fig2, axes2 = plt.subplots(3, 1, figsize=(6,7), sharex=True)
plt2 = sns.lineplot(data=stda_growth_yr, y="Density", x="Year", hue='Core',ax=axes2[0],linewidth=0.5)
plt2 = sns.lineplot(data=stda_growth_yr,y="Extension", x="Year",hue='Core',ax=axes2[1],linewidth=0.5)
plt2 = sns.lineplot(data=stda_growth_yr,y="Calcification", x="Year",hue='Core',ax=axes2[2],linewidth=0.5)
axes2[0].get_xaxis().set_minor_locator(mpl.ticker.MultipleLocator(5))
#axes2[0].grid(b=False, which='minor', color='w', linewidth=0.5)
##Add line at y-zero
axes2[0].plot([1942,2015],[0,0],color='gray',alpha=0.5,linestyle='--',linewidth=0.8)
axes2[1].plot([1942,2015],[0,0],color='gray',alpha=0.5,linestyle='--',linewidth=0.8)
axes2[2].plot([1942,2015],[0,0],color='gray',alpha=0.5,linestyle='--',linewidth=0.8)
##Add mean 1950-2015
axes2[0].plot(stda_growth_yr_mean.loc[0:65,:]['Year'],stda_growth_yr_mean.loc[0:65,:]['Density'],color='black')
axes2[1].plot(stda_growth_yr_mean.loc[0:65,:]['Year'],stda_growth_yr_mean.loc[0:65,:]['Extension'],color='black')
axes2[2].plot(stda_growth_yr_mean.loc[0:65,:]['Year'],stda_growth_yr_mean.loc[0:65,:]['Calcification'],color='black')

for ax in axes2:
    ax.legend([],[], frameon=False)

#fig2.savefig(dir+'\\fig2.tiff', format='tiff', dpi=1200,bbox_inches = 'tight')

##### FIG.2 LEGEND
#print((sns.color_palette("tab10")).as_hex()) #Extract seaborn color codes
fig2b, axes2b = plt.subplots(1, 1, figsize=(6,1.2), sharex=True)
axes2b.plot([1982,2015],[4,4],color='#1f77b4',linestyle='-')
axes2b.plot([1951,2015],[3,3],color='#ff7f0e',linestyle='-')
axes2b.plot([1942,2015],[2,2],color='#2ca02c',linestyle='-')
axes2b.plot([1950,2015],[1,1],color='#d62728',linestyle='-')
axes2b.plot([1942,2015],[0,0],color='black',linestyle='-')
axes2b.axes.get_xaxis().set_ticks([])
axes2b.axes.get_yaxis().set_ticks([])
axes2b.get_xaxis().set_minor_locator(mpl.ticker.MultipleLocator(5))
axes2b.get_xaxis().set_major_locator(mpl.ticker.MultipleLocator(10))
axes2b.get_yaxis().set_major_locator(mpl.ticker.MultipleLocator(1))
axes2b.set_yticklabels(('','Mean','VAR4','VAR3','VAR2','VAR1'),fontsize=10)
axes2b.set_ylim([-0.5,4.5])

#fig2b.savefig(dir+'\\fig2legend.tiff', format='tiff', dpi=1200,bbox_inches = 'tight')


plt.plot(stda_growth_yr_mean.loc[0:65,:]['Year'],stda_growth_yr_mean.loc[0:65,:]['Density'],label='Density')
plt.plot(stda_lumin_yr_mean.loc[0:65,:]['Year'],stda_lumin_yr_mean.loc[0:65,:]['G/B'],label='G/B')
plt.legend()