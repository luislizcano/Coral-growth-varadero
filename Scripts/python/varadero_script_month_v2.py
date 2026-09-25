^# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:16:04 2021

@author: lizca
"""


import os
import sys
import pandas as pd
import numpy as np
# from trend_classifier import Segmenter
# import ruptures as rpt
# import statistics as stats
# import math
# import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy.stats import pearsonr

### 'ruptures' package required
#python -m pip install ruptures

# =============================================================================
## Load Excel file using pandas
## To make sure set the file path
dir = 'E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates'
os.chdir(dir)

subfolder_path = os.path.abspath("Scripts\\python")
if subfolder_path not in sys.path:
    sys.path.append(subfolder_path)


from functions import mean_yr,mean_cols,STDA,STDAidx,climat,linreg,mean_range,\
                stats_all,detect_changes,check_assumptions

## Load data
coral_data = pd.ExcelFile('Data_processed\\coral_growth_monthly_v2.xlsx')
lumin_data = pd.ExcelFile('Data_processed\\coral_lumn_monthly.xlsx')
envir_data = pd.ExcelFile('Data_processed\\env_monthly.xlsx')

## Check if the file has different sheets
lumin_data.sheet_names

## You can load data by number of sheet
growth = coral_data.parse(1).iloc[0:744].sort_values('Y.M.').reset_index(drop=True)
lumin = lumin_data.parse(1).sort_values('Y.M.').reset_index(drop=True)
envir = envir_data.parse(0).sort_values('Y.M.').reset_index(drop=True)
# print('Number of rows and columns:',growth.shape)

## Check if there is missing data
growth.isna().sum()
lumin.isna().sum()
envir.isna().sum()

## Interpolate if needed
# growth = growth.interpolate()


# =============================================================================
# Examine Normality
# =============================================================================
# If p < 0.05, assume non-normal distribution.
from scipy.stats import shapiro

shapiro(growth["Density"])
shapiro(growth["Extension"])
shapiro(growth["Calcification"])
shapiro(lumin["G/B"])
shapiro(envir["WF_Helena"])
shapiro(envir["WF_Calamar"])
shapiro(envir["HadISST"])
shapiro(envir["SOI"])
shapiro(envir["AMO"])

# from scipy.stats import normaltest
# normaltest(growth["Density"])

growth[['Density','Extension','Calcification']].hist(figsize=(10,4))
lumin[['G/B']].hist(figsize=(10,4))
envir[['WF_Helena','WF_Calamar','HadISST','SOI','AMO']].hist(figsize=(10,4))
'''
Shapiro Results (1954-2015)
-------------------------------------
|Variable      | Statistic | p-value  |
|--------------|-----------|----------|
|Density       |  0.99     |  0.000 * |
|Extension     |  0.96     |  0.000 * |
|Calcification |  0.97     |  0.000 * |
|G/B           |  0.99     |  0.001 * |
|WF_Helena     |  0.96     |  0.000 * |
|WF_Calamar    |  0.98     |  0.000 * |
|HadISST       |  0.97     |  0.000 * |
|SOI           |  0.99     |  0.001 * |
|AMO           |  0.99     |  0.013 * |
-------------------------------------
*There is no normality for all variables.
'''


# =============================================================================
# Test stationary - Augmented Dickey-Fuller (ADF) test
# =============================================================================
## A stationary time series is one whose statistical properties do not change over time
## If p < 0.05, time series is stationary (there are no trends)
from statsmodels.tsa.stattools import adfuller

result = adfuller(growth["Calcification"])
# result = adfuller(lumin["G/B"])
# result = adfuller(envir["SOI"])
print('Statistic', result[0])   # statistic
print('p-value', result[1])   # p-value

'''
Stationary Results
-------------------------------------
|Variable      | Statistic | p-value  |
|--------------|-----------|----------|
|Density       | -2.50     |  0.117   |
|Extension     | -4.61     |  0.000 * |
|Calcification | -5.00     |  0.000 * |
|G/B           | -3.26     |  0.016 * |
|WF_Helena     | -2.58     |  0.097   |
|WF_Calamar    | -6.27     |  0.000 * |
|HadISST       | -4.55     |  0.000 * |
|SOI           | -7.48     |  0.000 * |
|AMO           | -2.13     |  0.231   |
|-------------------------------------|
* Stationary time-series (there is no trend or trend-stationary)
'''

# =============================================================================
# Test Seasonality
# =============================================================================
from statsmodels.tsa.seasonal import seasonal_decompose

## Select dataset and invert df
# sdata = lumin["G/B"].iloc[::-1].reset_index(drop=True)
sdata = growth["Density"].iloc[0:744].iloc[::-1].reset_index(drop=True)
## Decompose
decomp = seasonal_decompose(sdata, period=12)
fig = decomp.plot()
## Change marker size of residual plot
axes = fig.get_axes()
for line in axes[3].get_lines():
    line.set_markersize(2)
# Loop through subplots 0, 1, and 2 to change line width
for i in [0,1,2]:
    ax = axes[i]
    # Update the width for all lines inside this specific subplot
    for line in ax.get_lines():
        line.set_linewidth(1.0)  # Change 3.5 to your desired thickness
## Change format of x-axis to dates:
# 1. Generate the calendar labels matching your data length (e.g., starting Jan 2023)
date_labels = pd.date_range(start='1954-01-01', periods=len(sdata), freq='MS').strftime('%Y')
# 2. Get the bottom subplot (Index 3)
axes = fig.get_axes()
bottom_ax = axes[3]
# 3. Map your integer positions to your date strings (showing every 6th month to avoid crowding)
tick_intervals = range(0, len(sdata), 120)
bottom_ax.set_xticks(tick_intervals)
bottom_ax.set_xticklabels([date_labels[i] for i in tick_intervals], rotation=0)

plt.show()

fig.savefig(dir+'\\figE1_Calcification_monthly.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================
# Test Autocorrelations
# =============================================================================
## Blue Shaded Area: The 95% confidence interval.
## Significant Autocorrelation: If a vertical bar sticks out above or below 
## the blue area, it means that lag has a statistically significant correlation
from statsmodels.graphics.tsaplots import plot_acf

fig = plot_acf(growth["Density"], lags=36)
plt.show()

plot_acf(envir["HadISST"], lags=36)
plt.show()

fig.savefig(dir+'\\figE2_ACF_Density_monthly.tiff', format='tiff', dpi=300,bbox_inches = 'tight')

## Durbin-watson test: autocorrelation test at lag=1
from statsmodels.stats.stattools import durbin_watson

durbin_watson(growth["Extension"])
durbin_watson(lumin["G/B"])
durbin_watson(envir["AMO"])
'''
* Durbin-Watson test at lag=1, autocorrelation is important at values < 2
* Values > 2 indicates no autocorrelation.
|Variable      | d      |
|--------------|--------|
Density       = 0.004 *
Extension     = 0.080 *
Calcification = 0.072 *
G/B           = 0.000 *
WF_Helena     = 0.051 *
WF_Calamar    = 0.049 *
HadISST       = 0.000 *
SOI           = 0.690 *
AMO           = 0.141 *
'''
### Testing autocorrelation at specific lag.
# from statsmodels.stats.diagnostic import acorr_ljungbox
# lb_test = acorr_ljungbox(growth["Calcification"], lags=[1], return_df=True)
# print(lb_test)


# =============================================================================
# OPTION A - Raw data
# Time-series detrending (removing seasonality)
# =============================================================================

def detrend(df, cols):
    for c in cols:
        df[c+"_anom"] = (
            df[c] -
            df.groupby(df.Month)[c].transform("mean")
        )
    return df

growth_det = detrend(growth, ['Density','Extension','Calcification'])#.iloc[0:744,:]
lumin_det = detrend(lumin, ['G/B'])
envir_det = detrend(envir, ['WF_Helena','WF_Calamar','HadISST','SOI','AMO'])

# =============================================================================
# A. Test Autocorrelations
# =============================================================================
## plot with 36 lags
fig = plot_acf(growth_det["Density_anom"], lags=36)
plt.show()
fig.savefig(dir+'\\figE2_ACF_Density-detr_monthly.tiff', format='tiff', dpi=300,bbox_inches = 'tight')

## at lag=1
durbin_watson(growth_det["Calcification_anom"])
durbin_watson(lumin_det["G/B_anom"])
durbin_watson(envir_det["WF_Helena_anom"])
'''
* Durbin-Watson test at lag=1, autocorrelation is important at values < 2
* Values > 2 indicates no autocorrelation.
|Variable      | d      |
|--------------|--------|
Density       = 0.049 *
Extension     = 0.653 *
Calcification = 0.683 *
G/B           = 0.105 *
WF_Helena     = 0.157 *
WF_Calamar    = 0.249 *
HadISST       = 0.373 *
SOI           = 0.703 *
AMO           = 0.136 *
'''

# =============================================================================
# A. Examine Normality
# =============================================================================
# If p < 0.05, assume non-normal distribution.
from scipy.stats import shapiro

shapiro(growth_det["Density_anom"])
shapiro(growth_det["Extension_anom"])
shapiro(growth_det["Calcification_anom"])
shapiro(lumin_det["G/B_anom"])
shapiro(envir_det["WF_Helena_anom"])
shapiro(envir_det["WF_Calamar_anom"])
shapiro(envir_det["HadISST_anom"])
shapiro(envir_det["SOI_anom"])
shapiro(envir_det["AMO_anom"])

'''
Shapiro Results (1954-2015)
-------------------------------------
|Variable      | Statistic | p-value  |
|--------------|-----------|----------|
|Density       |  0.99     |  0.000 * |
|Extension     |  0.98     |  0.000 * |
|Calcification |  0.98     |  0.000 * |
|G/B           |  0.99     |  0.001 * |
|WF_Helena     |  0.96     |  0.000 * |
|WF_Calamar    |  0.99     |  0.000 * |
|HadISST       |  0.97     |  0.168   |
|SOI           |  0.99     |  0.001 * |
|AMO           |  0.99     |  0.000 * |
-------------------------------------
*There is no normality for all variables.
'''

# =============================================================================
# MULTIPLE VARIABLE EVALUATIONS
# =============================================================================

## Variables
growth_vars = ['Density','Extension','Calcification']
lumin_vars = ['G/B']
envir_vars = ['WF_Helena','WF_Calamar','HadISST','SOI','AMO']
growth_vars2 = ['Density_anom','Extension_anom','Calcification_anom']
lumin_vars2 = ['G/B_anom']
envir_vars2 = ['WF_Helena_anom','WF_Calamar_anom','HadISST_anom','SOI_anom','AMO_anom']

## Predictor correlations
envir_det[envir_vars2].corr()

## Variance Inflation Factors (VIFs)
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif = pd.DataFrame({
    "Variable": envir_det[envir_vars2].columns,
    "VIF": [variance_inflation_factor(envir_det[envir_vars2].values, i)
            for i in range(envir_det[envir_vars2].shape[1])] })
print(vif)
'''
VIF < 5: generally acceptable
VIF between 5 and 10: moderate multicollinearity.
VIF > 10: severe multicollinearity.

|          Variable |     VIF  |
|-------------------|----------|
|   WF_Helena_anom  | 1.902295 |
|  WF_Calamar_anom  | 2.281343 |
|     HadISST_anom  | 1.975874 |
|         SOI_anom  | 1.456005 |
|         AMO_anom  | 2.056262 |
'''

# =============================================================================
# A. Pearson Correlation
# =============================================================================
from scipy.stats import pearsonr

# growth_det = growth_det.sort_values(by='Y.M.', ascending=True)
# lumin_det = lumin_det.sort_values(by='Y.M', ascending=True)
# envir_det = envir_det.sort_values(by='Y.M', ascending=True)

def corr(x_df,y_df,x_cols,y_cols):
    for x in x_cols:
        for y in y_cols:
            r_val, p_val = pearsonr(x_df[x], y_df[y])
            print(f"\n--- Final Results {x} vs {y} ---")
            print(f"Correlation Coefficient (r): {r_val:.2f}")
            print(f"Adjusted p-value: {p_val:.3f}")

## Prepare data >1984
growth_det2 = growth_det.iloc[360:,:]
lumin_det2 = lumin_det.iloc[360:,:]
envir_det2 = envir_det.iloc[360:,:]
## Prepare data <1984
growth_det3 = growth_det.iloc[0:360,:]
lumin_det3 = lumin_det.iloc[0:360,:]
envir_det3 = envir_det.iloc[0:360,:]

## Variables
growth_vars = ['Density','Extension','Calcification']
lumin_vars = ['G/B']
envir_vars = ['WF_Helena','WF_Calamar','HadISST','SOI','AMO']
growth_vars2 = ['Density_anom','Extension_anom','Calcification_anom']
lumin_vars2 = ['G/B_anom']
envir_vars2 = ['WF_Helena_anom','WF_Calamar_anom','HadISST_anom','SOI_anom','AMO_anom']

## Correlations of raw data
growth_corrs = corr(envir_det, growth_det, envir_vars, growth_vars)
lumin_corrs = corr(envir_det,lumin_det, envir_vars, lumin_vars)

## test post 1984 [0:384,:]
growth_corrs2 = corr(envir_det2,growth_det2, envir_vars, growth_vars)
lumin_corrs2 = corr(envir_det2,lumin_det2, envir_vars, lumin_vars)

## test pre 1983 [384:,:]. Sta Helena data is modeled
growth_corrs3 = corr(envir_det3,growth_det3, envir_vars, growth_vars)
lumin_corrs3 = corr(envir_det3,lumin_det3, envir_vars, lumin_vars)
'''
USING RAW DATA
------------------------------------------------------------------------------------
 1954-2015    | WF_Helena   | WF_Calamar  | HadISST     | SOI        | AMO         |
------------------------------------------------------------------------------------
Density       | 0.08,0.026  | 0.43,<0.001 | 0.45,<0.001 | 0.05,0.146 |-0.12,0.001  |
Extension     | 0.17,<0.001 | 0.10,0.004  |-0.20,<0.001 | 0.05,0.178 | 0.08,0.023  |
Calcification | 0.18,<0.001 | 0.31,<0.001 | 0.01,0.845  | 0.07,0.062 | 0.01,0.829  |
G/B           | 0.22,<0.001 | 0.53,<0.001 | 0.04,0.258  | 0.10,0.005 |-0.19,<0.001 |
------------------------------------------------------------------------------------

------------------------------------------------------------------------------------
1984-2015     | WF_Helena   | WF_Calamar  | HadISST     | SOI        | AMO         |
------------------------------------------------------------------------------------
Density       | 0.39,<0.001 | 0.48,<0.001 | 0.53,<0.001 |-0.04,0.396 |-0.03,0.542  |
Extension     | 0.16,0.002  | 0.08,0.122  |-0.20,<0.001 | 0.14,0.006 |-0.07,0.542  |
Calcification | 0.33,<0.001 | 0.30,<0.001 | 0.04,0.412  | 0.11,0.035 |-0.07,0.156  |
G/B           | 0.49,<0.001 | 0.55,<0.001 | 0.02,0.689  | 0.11,0.027 |-0.12,0.016  |
------------------------------------------------------------------------------------

------------------------------------------------------------------------------------
1954-1983     | WF_Helena   | WF_Calamar  | HadISST     | SOI        | AMO         |
------------------------------------------------------------------------------------
Density       | 0.40,<0.001 | 0.45,<0.001 | 0.54,<0.001 | 0.09,0.079 | 0.01,0.864  |
Extension     | 0.10,0.051  | 0.13,0.012  |-0.25,<0.001 |-0.01,0.860 | 0.16,0.002  |
Calcification | 0.27,<0.001 | 0.32,<0.001 |-0.00,0.942  | 0.03,0.561 | 0.16,0.002  |
G/B           | 0.47,<0.001 | 0.55,<0.001 | 0.16,0.002  | 0.05,0.321 | 0.11,0.046  |
------------------------------------------------------------------------------------
'''

## Correlations of detrended data
growth_corrs = corr(envir_det, growth_det, envir_vars2, growth_vars2)
lumin_corrs = corr(envir_det,lumin_det, envir_vars2, lumin_vars2)

## test post 1984 [0:384,:]
growth_corrs2 = corr(envir_det2,growth_det2, envir_vars2, growth_vars2)
lumin_corrs2 = corr(envir_det2,lumin_det2, envir_vars2, lumin_vars2)

## test pre 1983 [384:,:]. Sta Helena data is modeled
growth_corrs3 = corr(envir_det3,growth_det3, envir_vars2, growth_vars2)
lumin_corrs3 = corr(envir_det3,lumin_det3, envir_vars2, lumin_vars2)
'''
USING DETRENDED DATA
------------------------------------------------------------------------------------
 1954-2015    | WF_Helena   | WF_Calamar  | HadISST     | SOI        | AMO         |
------------------------------------------------------------------------------------
Density       |-0.31,<0.001 | 0.12,0.002  |-0.14,<0.001 | 0.12,0.001 |-0.21,<0.001 |
Extension     | 0.13,<0.001 |-0.01,0.847  | 0.18,<0.001 | 0.09,0.011 | 0.24,<0.001 |
Calcification |-0.07,0.054  | 0.05,0.178  | 0.06,0.080  | 0.15,<0.001| 0.09,0.013  |
G/B           |-0.13,0.001  | 0.33,<0.001 |-0.36,<0.001 | 0.21,<0.001|-0.25,<0.001 |
------------------------------------------------------------------------------------

------------------------------------------------------------------------------------
1984-2015     | WF_Helena   | WF_Calamar  | HadISST     | SOI        | AMO         |
------------------------------------------------------------------------------------
Density       | 0.01,0.825  | 0.18,<0.001 |-0.08,0.138  |-0.01,0.919 |-0.22,<0.001 |
Extension     | 0.03,0.516  |-0.04,0.465  | 0.16,0.002  | 0.15,0.004 | 0.10,0.056  |
Calcification | 0.01,0.797  | 0.03,0.584  | 0.05,0.307  | 0.12,0.016 |-0.05,0.326  |
G/B           | 0.24,<0.001 | 0.40,<0.001 |-0.44,<0.001 | 0.18,<0.001|-0.38,<0.001 |
------------------------------------------------------------------------------------

------------------------------------------------------------------------------------
1954-1983     | WF_Helena   | WF_Calamar  | HadISST     | SOI        | AMO         |
------------------------------------------------------------------------------------
Density       | 0.02,0.679  | 0.08,0.125  | 0.05,0.326  | 0.19,<0.001| 0.07,0.208  |
Extension     |-0.01,0.833  | 0.03,0.536  | 0.11,0.033  | 0.07,0.199 | 0.30,<0.001 |
Calcification | 0.00,0.927  | 0.07,0.170  | 0.15,0.004  | 0.16,0.003 | 0.32,<0.001 |
G/B           | 0.17,0.001  | 0.30,<0.001 |-0.04,0.442  | 0.23,<0.001| 0.23,<0.001 |
------------------------------------------------------------------------------------
'''
plt.scatter(envir_det2['WF_Helena_anom'], lumin_det2['G/B_anom'])



# =============================================================================
# =============================================================================
# # PLOTS OF WATER DISCHARGE
# =============================================================================
# =============================================================================

# =============================================================================
# ### Scatter plot of before and after 1984
# =============================================================================
fig, ax = plt.subplots(1,1,figsize=(5, 3),sharex=True)
ax.scatter(envir['WF_Calamar'].iloc[324:372], envir['WF_Helena'].iloc[324:372], 
           color='#f0aa71', label='Before 1984', s=10, alpha = 0.8)
ax.scatter(envir['WF_Calamar'].iloc[372:], envir['WF_Helena'].iloc[372:], 
           color='#73a1f0', label='After 1984', s=10, alpha = 0.8)
ax.plot(envir['WF_Calamar'].iloc[324:372], 0.0329*(envir['WF_Calamar'].iloc[324:372])-33.8,
        color='#EB5406', lw=2,alpha = 1)
ax.plot(envir['WF_Calamar'].iloc[372:], 0.0497*(envir['WF_Calamar'].iloc[372:])+13.271,
        color='#256ce6', lw=2,alpha = 1)

fig.legend(fontsize=9,bbox_to_anchor=(0.44, 0.94),handletextpad=0.1)
ax.text(11000, 100, 'y = 0.0329x - 33.8 \n $R^{2}$ = 0.76',fontsize=8,color='#EB5406')
ax.text(3000, 500, 'y = 0.0497x + 13.271 \n $R^{2}$ = 0.85',fontsize=8,color='#256ce6')
## Edit axes
ax.set(ylabel='Water flow \n at Sta Helena ($m^{3}$ $s^{-1}$)')
ax.set(xlabel='Water flow at Calamar ($m^{3}$ $s^{-1}$)')
fig.tight_layout()
# fig.savefig(dir+'\\fig0_waterflow-scatter.tiff', format='tiff', dpi=600,bbox_inches = 'tight')


# =============================================================================
# ### Time series with modeled before data.
# =============================================================================
fig, ax = plt.subplots(2,1,figsize=(8, 5),sharex=True)
x = envir['Y.M.']
ax[0].plot(x, envir['WF_Calamar'], '-', color='gray',
            label='Calamar',lw=1,alpha = 1)
## Second Y-axis
ax_2 = ax[0].twinx()
ax_2.plot(x.iloc[0:373], envir['WF_Helena'].iloc[0:373], '-', color='#FF8000',
            label='Sta Helena (Before 1984)',lw=1,alpha = 1)
ax_2.plot(x.iloc[372:], envir['WF_Helena'].iloc[372:], '-', color='red',
            label='Sta Helena (After 1984)',lw=1,alpha = 1)
## Ratio
ax[1].plot(x, envir['WF_Helena']/envir['WF_Calamar']*100, '-', color='gray',
            lw=1,alpha = 1)

fig.legend(fontsize=9,bbox_to_anchor=(0.82, 0.95),ncol=3)
## Edit axes
ax[1].set_xlim([1954,2015])
ax[0].set_ylim([1500,20000])
ax[0].xaxis.set_minor_locator(ticker.MultipleLocator(5))
# axes3[3,0].xaxis.set_major_locator(ticker.MultipleLocator(10))
ax[0].set(ylabel='Water flow \n at Calamar ($m^{3}$ $s^{-1}$)')
ax_2.set(ylabel='Water flow \n at Santa Helena ($m^{3}$ $s^{-1}$)')
ax[1].set(ylabel='Santa Helena-Calamar \nflow ratio (%)')
fig.text(0.86, 0.9, 'A', fontsize=10)
fig.text(0.15, 0.44, 'B', fontsize=10)

fig.tight_layout()
# fig.savefig(dir+'\\fig0_waterflow-timeseries.tiff', format='tiff', dpi=600,bbox_inches = 'tight')



# =============================================================================
# ###### PLOTS (INCLUDED IN MANUSCRIPT)
# =============================================================================

###### FIG 0. CORAL TIMESPAN RECORDED
fig0, axes0 = plt.subplots(figsize=(4.2,1), sharex=True)
plt0 = sns.lineplot(y=[4,4], x=[1982,2015], ax=axes0) #VAR1
plt0 = sns.lineplot(y=[3,3], x=[1951,2015]) #VAR2
plt0 = sns.lineplot(y=[2,2], x=[1942,2015]) #VAR3
plt0 = sns.lineplot(y=[1,1], x=[1950,2015]) #VAR4
plt0 = sns.lineplot(y=[0,0], x=[1954,2015],color='black') #MEAN

axes0.set_yticks([0,1,2,3,4])
axes0.set_yticklabels(['Mean','VAR4','VAR3','VAR2','VAR1'])

axes0.xaxis.set_minor_locator(ticker.MultipleLocator(1))
axes0.xaxis.set_major_locator(ticker.MultipleLocator(10))

axes0.set_xlim([1940,2015])
axes0.set_ylim([-0.8,4.8])

#fig0.tight_layout()
# fig0.savefig(dir+'\\fig0_timespan_full.tiff', format='tiff', dpi=600,bbox_inches = 'tight')


# =============================================================================
####### FIG 3. STDA Growth data (All data)
## for original units/values
plt_gr = coral_data.parse(0)#.drop
plt_lu = lumin_data.parse(0)

plt.style.use('seaborn-v0_8')
# plt.style.use('default')
fig3, axes3 = plt.subplots(4, 2, figsize=(8,7), sharex=True)

## for STDA values
# plt_gr = stda_growth_all
# plt_lu = stda_lumin_all
# plt_wf = stda_wf_all
# plt_te = stda_temp_all
# plt_soi= stda_soi_all
# plt_amo = stda_amo_all
# plt_gr_mn = stda_growth_mean_full
# plt_lu_mn = stda_lumin_mean_full

## for programmatic coding of subplots
axx = [0,0,0,0,1,1,1,1]
axy = [0,1,2,3,0,1,2,3]

## Draw a guide line along y = 0:
for i in (range(len(axx))):
    plt3 = sns.lineplot(y=[0,0], x=[1940,2017],ax=axes3[axy[i],axx[i]],
                        color='black',alpha=0.2)
## Growth per core:
lbl_gr = ['Density','Extension','Calcification']
for i in (range(len(lbl_gr))):
    plt3 = sns.lineplot(data=plt_gr, y=lbl_gr[i], x="Year",hue='Core',
                        ax=axes3[axy[i],0],linewidth=0.7)
    ## Mean:
    plt3 = sns.lineplot(data=growth,y=lbl_gr[i],x="Year",
                        ax=axes3[axy[i],0],color='black',label='Mean')

## Luminescence per core:
plt3 = sns.lineplot(data=plt_lu, y="G/B", x="Year",hue='Core',
                    ax=axes3[3,0],linewidth=0.7)
## Luminescence Mean:
plt3 = sns.lineplot(data=lumin, y="G/B", x="Year",color='black',
                    ax=axes3[3,0],label='Mean')

## Environmental data:
lbl_env = ['WF_Helena','HadISST','SOI','AMO']
for i in (range(len(lbl_env))):
    ## Mean
    plt3 = sns.lineplot(data=envir, y=lbl_env[i], x="Year",
                        ax=axes3[axy[i],1])

## Draw lines of Change point detection
## Here are all the years with changing points
pd_yr = [1982,1986,1966,1961,2011,2001,1996,1956,2011,2006,2001,1981,1971,
         1996,1991,1976,1971,1996,1976,1971,1961]
pd_axy = [0,1,1,2,3,3,3,3,0,0,1,1,1,2,2,2,2,3,3,3,3]
pd_axx = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1]
pd_ylim1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,-3,-3,-3,-3,-3,-3,-3,-3]
pd_ylim2 = [5,5,5,5,5,5,5,5,800,800,32,32,32,3,3,3,3,3,3,3,3]
for i in (range(len(pd_yr))):
    plt3 = sns.lineplot(y=[pd_ylim1[i],pd_ylim2[i]], x=[pd_yr[i],pd_yr[i]],
                        ax=axes3[pd_axy[i],pd_axx[i]],estimator=None,
                         linestyle='--',color='black',lw=1,alpha=0.8)

## Regression lines
regline = {"color": "#ff6c00",'alpha':0.6}
regdot = {"color": "#1f77b4", 's':0}
plt3 = sns.regplot(data=plt_gr_mn, y="Density", x="Year",ci=None,
                   scatter_kws=regdot,line_kws=regline,ax=axes3[0,0])
plt3 = sns.regplot(data=plt_gr_mn, y="Calcification", x="Year",ci=None,
                   scatter_kws=regdot,line_kws=regline,ax=axes3[2,0])
plt3 = sns.regplot(data=plt_lu_mn, y="G/B", x="Year",ci=None,
                   scatter_kws=regdot,line_kws=regline,ax=axes3[3,0])
plt3 = sns.regplot(data=plt_wf, y="WaterFlow", x="Year",ci=None,
                   scatter_kws=regdot,line_kws=regline,ax=axes3[0,1])
plt3 = sns.regplot(data=plt_amo, y="AMO", x="Year",ci=None,
                   scatter_kws=regdot,line_kws=regline,ax=axes3[3,1])

## Plot customization
axes3[3,0].set_xlim([1940,2015]) #x-axis limit
## x-axis ticks
axes3[3,0].xaxis.set_minor_locator(ticker.MultipleLocator(2))
axes3[3,0].xaxis.set_major_locator(ticker.MultipleLocator(10))
## Legend
axes3[3,0].legend(fontsize=6,loc='lower left')
# axes6[3,0].legend().set_visible(False)
axes3[1,0].legend().set_visible(False)
axes3[2,0].legend().set_visible(False)
axes3[0,0].legend().set_visible(False)
## Set axis limits
axes3[0,0].set_ylim([0.2,1.2])
axes3[1,0].set_ylim([0.2,2.2])
axes3[2,0].set_ylim([0.2,1.5])
axes3[3,0].set_ylim([0.95,1.1])
axes3[0,1].set_ylim([50,700])
axes3[1,1].set_ylim([26,30])
axes3[2,1].set_ylim([-2.5,2.5])
axes3[3,1].set_ylim([-0.55,0.5])
## Axis titles
axes3[0,0].set(ylabel='Skeletal density \n($g$ $m^{-3}$)')
axes3[1,0].set(ylabel='Linear extension \n($cm$ $yr^{-1}$)')
axes3[2,0].set(ylabel='Calcification \n($g$ $cm^{-2}$ $yr^{-1}$)')
axes3[3,0].set(ylabel='Luminescence \n($G/B$)')
axes3[0,1].set(ylabel='Water Flow \n($m^{3}$ $s^{-1}$)')
axes3[1,1].set(ylabel='Temperature \n($°C$)')

## Adjust space between subplots
fig3.tight_layout()

#fig3.savefig(dir+'\\fig3_growth-full_er_lines.tiff', format='tiff', dpi=600,bbox_inches = 'tight')


# =============================================================================
####### FIG 4. BEFORE VS AFTER 1981
plt.style.use('seaborn-v0_8')
fig4, axes4 = plt.subplots(2, 2, figsize=(6,3.5), sharex=True)

## DOTS WITH ERROR
## Error STD
# axes4[0,0].errorbar([1,2],[growth_mean_before.iloc[1],growth_mean_after.iloc[1]],
#     yerr=[growth_std_before.iloc[1],growth_std_after.iloc[1]],
#     fmt='o',color='#1f77b4',ecolor='black')
# axes4[0,1].errorbar([1,2],[growth_mean_before.iloc[2],growth_mean_after.iloc[2]],
#     yerr=[growth_std_before.iloc[2],growth_std_after.iloc[2]],
#     fmt='o',color='#1f77b4',ecolor='black')
# axes4[1,0].errorbar([1,2],[growth_mean_before.iloc[3],growth_mean_after.iloc[3]],
#     yerr=[growth_std_before.iloc[3],growth_std_after.iloc[3]],
#     fmt='o',color='#1f77b4',ecolor='black')
# axes4[1,1].errorbar([1,2],[lumin_mean_before.iloc[1],lumin_mean_after.iloc[1]],
#     yerr=[lumin_std_before.iloc[1],lumin_std_after.iloc[1]],
#     fmt='o',color='#1f77b4',ecolor='black')

## Calculate Error CI 95%
ci_den_be = growth_mean_before.iloc[1] - 1.96*(growth_std_before.iloc[1]/np.sqrt(31))
ci_den_af = growth_mean_after.iloc[1] - 1.96*(growth_std_after.iloc[1]/np.sqrt(35))
ci_ext_be = growth_mean_before.iloc[2] - 1.96*(growth_std_before.iloc[2]/np.sqrt(31))
ci_ext_af = growth_mean_after.iloc[2] - 1.96*(growth_std_after.iloc[2]/np.sqrt(35))
ci_cal_be = growth_mean_before.iloc[3] - 1.96*(growth_std_before.iloc[3]/np.sqrt(31))
ci_cal_af = growth_mean_after.iloc[3] - 1.96*(growth_std_after.iloc[3]/np.sqrt(35))
ci_lum_be = lumin_mean_before.iloc[1] - 1.96*(lumin_std_before.iloc[1]/np.sqrt(31))
ci_lum_af = lumin_mean_after.iloc[1] - 1.96*(lumin_std_after.iloc[1]/np.sqrt(35))
## Add error to plot
axes4[0,0].errorbar([1,2],[growth_mean_before.iloc[1],growth_mean_after.iloc[1]],
    yerr=[growth_mean_before.iloc[1]-ci_den_be, growth_mean_after.iloc[1]-ci_den_af],
    fmt='o',color='#1f77b4',ecolor='black')
axes4[0,1].errorbar([1,2],[growth_mean_before.iloc[2],growth_mean_after.iloc[2]],
    yerr=[growth_mean_before.iloc[2]-ci_ext_be, growth_mean_after.iloc[2]-ci_ext_af],
    fmt='o',color='#1f77b4',ecolor='black')
axes4[1,0].errorbar([1,2],[growth_mean_before.iloc[3],growth_mean_after.iloc[3]],
    yerr=[growth_mean_before.iloc[3]-ci_cal_be, growth_mean_after.iloc[3]-ci_cal_af],
    fmt='o',color='#1f77b4',ecolor='black')
axes4[1,1].errorbar([1,2],[lumin_mean_before.iloc[1],lumin_mean_after.iloc[1]],
    yerr=[lumin_mean_before.iloc[1]-ci_lum_be, lumin_mean_after.iloc[1]-ci_lum_af],
    fmt='o',color='#1f77b4',ecolor='black')

## Modify axes labels
axes4[0,0].set(ylabel='Skeletal density \n($g$ $m^{-3}$)')
axes4[0,1].set(ylabel='Linear extension \n($cm$ $yr^{-1}$)')
axes4[1,0].set(ylabel='Calcification \n($g$ $cm^{-2}$ $yr^{-1}$)')
axes4[1,1].set(ylabel='Luminescence \n($G/B$)')
axes4[1,0].xaxis.set_major_locator(ticker.MultipleLocator(1))
axes4[1,0].set_xticks([1,2])
axes4[1,0].set_xticklabels(['1951-1981','1981-2015'], fontsize=10,rotation=0)
axes4[0,0].set_xlim([0.5,2.5])
fig4.tight_layout()

#fig4.savefig(dir+'\\fig8_before-after-ci95.tiff', format='tiff', dpi=600,bbox_inches = 'tight')

#print((sns.color_palette("tab10")).as_hex()) #Extract seaborn color codes


# =============================================================================
####### FIG 4b. BEFORE VS AFTER 1981 (BOXPLOT VERSION)
plt.style.use('seaborn-v0_8')
fig4b, axes4b = plt.subplots(2, 2, figsize=(8,5), sharex=True)

## BOXPLOTS
## Error FIRST COLUMN
flier = dict(marker='o',markerfacecolor='b',markersize=2,linestyle='none',markeredgecolor='black')
axes4b[0,0].boxplot([growth_mean_all.iloc[34:64,1],growth_mean_all.iloc[0:34,1]],
                    flierprops=flier)
axes4b[0,1].boxplot([growth_mean_all.iloc[34:64,2],growth_mean_all.iloc[0:34,2]],
                    flierprops=flier)
axes4b[1,0].boxplot([growth_mean_all.iloc[34:64,3],growth_mean_all.iloc[0:34,3]],
                    flierprops=flier)
axes4b[1,1].boxplot([lumin_mean_all.iloc[34:64,1],lumin_mean_all.iloc[0:34,1]],
                    flierprops=flier)

## Modify axes labels
axes4b[0,0].set(ylabel='Skeletal density \n($g$ $m^{-3}$)')
axes4b[0,1].set(ylabel='Linear extension \n($cm$ $yr^{-1}$)')
axes4b[1,0].set(ylabel='Calcification \n($g$ $cm^{-2}$ $yr^{-1}$)')
axes4b[1,1].set(ylabel='Luminescence \n($G/B$)')
## Set xtick labels
axes4b[1,0].set_xticks([1,2])
axes4b[1,0].set_xticklabels(['1951-1981','1981-2015'], fontsize=10,rotation=0)
axes4b[1,0].set_xlabel('Period')#periods, fontsize=8)
axes4b[1,1].set_xticks([1,2])
axes4b[1,1].set_xticklabels(['1951-1981','1981-2015'], fontsize=10,rotation=0)
axes4b[1,1].set_xlabel('Period')#periods, fontsize=8)
## Adjust space between subplots
fig4b.tight_layout()

#fig4b.savefig(dir+'\\fig4b_growth-boxplot.tiff', format='tiff', dpi=600,bbox_inches = 'tight')



# =============================================================================
# ###### EXPLORATORY PLOTS (NOT INCLUDED IN MANUSCRIPT)
# =============================================================================

###### FIG E1. Annual Skeletal Growth data (Master Mean + std) 1981-2015
figE1, axesE1 = plt.subplots(3, 1, figsize=(4,7), sharex=True)
pltE1 = sns.lineplot(data=growth_period, y="Density", x="Year", ax=axesE1[0])
pltE1 = sns.lineplot(data=growth_period,y="Extension", x="Year",ax=axesE1[1])
pltE1 = sns.lineplot(data=growth_period,y="Calcification", x="Year",ax=axesE1[2])

## Axis-Y Labels
axesE1[0].set(ylabel='Density \n($g$ $m^{-3}$)')
axesE1[1].set(ylabel='Extension \n($cm$ $yr^{-1}$)')
axesE1[2].set(ylabel='Calcification \n($g$ $cm^{-2}$ $yr{-1}$)')


# =============================================================================
####### FIG E2. Skeletal Growth data (all 4 cores in a plot) 1981-2015
figE2, axesE2 = plt.subplots(3, 1, figsize=(4,7), sharex=True)
pltE2 = sns.lineplot(data=growth_period, y="Density", x="Year",hue='Core',ax=axesE2[0])
pltE2 = sns.lineplot(data=growth_period,y="Extension", x="Year",hue='Core',ax=axesE2[1])
pltE2 = sns.lineplot(data=growth_period,y="Calcification", x="Year",hue='Core',ax=axesE2[2])

## Axis-Y Labels
axesE2[0].set(ylabel='Density \n($g$ $m^{-3}$)')
axesE2[1].set(ylabel='Extension \n($cm$ $yr^{-1}$)')
axesE2[2].set(ylabel='Calcification \n($g$ $cm^{-2}$ $yr^{-1}$)')
## Legend
axesE2[0].legend(fontsize=5,loc=2)
axesE2[1].legend().set_visible(False)
axesE2[2].legend().set_visible(False)
## ticks
axesE2[2].xaxis.set_minor_locator(ticker.MultipleLocator(1))
axesE2[2].xaxis.set_major_locator(ticker.MultipleLocator(5))

# figE2.savefig(dir+'\\figE2_growth-all.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================
####### FIG E3. Lumin data (all 4 cores in a plot) 1981-2015
# sns.reset_orig()
figE3, axesE3 = plt.subplots(1, 1, figsize=(6,3), sharex=True)
pltE3 = sns.lineplot(y=[0,0], x=[1980,2017],ax=axesE3,color='black',alpha=0.2)
pltE3 = sns.lineplot(data=stda_lumin, y="G/B", x="Year",hue='Core',linewidth=0.7)
pltE3 = sns.lineplot(data=stda_lumin_mean, y="G/B", x="Year",color='black',label='Mean')

## Second Y-axis
axesE3_2 = axesE3.twinx()
sns.lineplot(data=stda_wf, x='Year', y='WaterFlow', label='Water Flow',
            color = '#0600ff', ax=axesE3_2)
axesE3_2.set_ylabel(None)
axesE3_2.legend(fontsize=8,loc=2).set_visible(True)
# axesE3_2.yaxis.set_major_formatter(formatter)
# axesE3_2.spines['right'].set_color(palette_dic['Forest'])
# axesE3_2.tick_params(axis='y', colors=palette_dic['Forest'])

## Limits
axesE3.set_xlim([1981,2016])
axesE3.set_ylim([-2.5,2.5])
axesE3_2.set_xlim([1981,2016])
axesE3_2.set_ylim([-2.5,2.5])
## Legend
handlesE3, labelsE3 = axesE3.get_legend_handles_labels()
pltE3.legend(handlesE3, labelsE3, loc='upper right', fontsize=7)
## Ticks
axesE3.xaxis.set_minor_locator(ticker.MultipleLocator(1))
axesE3.xaxis.set_major_locator(ticker.MultipleLocator(5))

#figE3.savefig(dir+'\\figE3_lumin-all.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================
####### FIG E3B. Lumin data (all 4 cores in a plot) 1981-2015
### CORRELATIONS
## The correlation is made with the number of valid data among each pair of variables.
## nans are discarded automatically.
lum_data = pd.concat([
    lumin.loc[lumin['Core'] == 'VAR1']['G/B'].reset_index(drop=True).rename('VAR1'),
    lumin.loc[lumin['Core'] == 'VAR2']['G/B'].reset_index(drop=True).rename('VAR2'),
    lumin.loc[lumin['Core'] == 'VAR3']['G/B'].reset_index(drop=True).rename('VAR3'),
    lumin.loc[lumin['Core'] == 'VAR4']['G/B'].reset_index(drop=True).rename('VAR4'),
    lumin_mean['G/B'].rename('Mean'),wf_all['WaterFlow']],
    axis=1,join='outer')
corr_lum = lum_data.corr(method = 'pearson')

## STDA
lum_stda_data = pd.concat([
    stda_lumin.loc[stda_lumin['Core'] == 'VAR1']['G/B'].reset_index(drop=True).rename('VAR1'),
    stda_lumin.loc[stda_lumin['Core'] == 'VAR2']['G/B'].reset_index(drop=True).rename('VAR2'),
    stda_lumin.loc[stda_lumin['Core'] == 'VAR3']['G/B'].reset_index(drop=True).rename('VAR3'),
    stda_lumin.loc[stda_lumin['Core'] == 'VAR4']['G/B'].reset_index(drop=True).rename('VAR4'),
    stda_lumin_mean['G/B'].rename('Mean'),stda_wf['WaterFlow']],
    axis=1,join='outer')
corr_lum_stda = lum_stda_data.corr(method = 'pearson')
# Function to return p-value for pearsonr
def calculate_pvalue(col1, col2):
    return pearsonr(col1, col2)[1]
# Create a DataFrame to store p-values
p_values = lum_stda_data.corr(method=calculate_pvalue)

## PLOT
figE3b, axesE3b = plt.subplots(1,1, figsize=(5,4), dpi=150)
pltE3b = sns.heatmap(corr_lum_stda,annot=True,fmt=".2f",linewidth=.5,vmin=0.0,vmax=1,
                   cbar=False)
axesE3b.set_title('Correlations Luminescence vs WaterFlow (Normalized)')
#figE3b.savefig(dir+'\\figE3b_Lumin_corr_stda.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================
####### FIG E4. DECADAL TRENDS STDA Growth data (All cores)
figE4, axesE4 = plt.subplots(3, 1, figsize=(6,7), sharex=True)
x4 = 'Period'
y4 = 'slope'
pltE4 = sns.lineplot(y=[0,0], x=[-1,6],ax=axesE4[0],color='black',alpha=0.2)
pltE4 = sns.lineplot(y=[0,0], x=[-1,6],ax=axesE4[1],color='black',alpha=0.2)
pltE4 = sns.lineplot(y=[0,0], x=[-1,6],ax=axesE4[2],color='black',alpha=0.2)

pltE4 = sns.barplot(data=reg_den_dec,x='Period', y='slope',ax=axesE4[0],color='#1f77b4')
pltE4 = sns.barplot(data=reg_ext_dec,x='Period', y='slope',ax=axesE4[1],color='#1f77b4')
pltE4 = sns.barplot(data=reg_cal_dec,x='Period', y='slope',ax=axesE4[2],color='#1f77b4')

## Modify axes labels
axesE4[0].set_ylabel('Density')
axesE4[1].set_ylabel('Extension')
axesE4[2].set_ylabel('Calcification')
## Ticks
axesE4[2].set_xticks([0,1,2,3,4,5])
axesE4[2].set_xticklabels(periods, fontsize=8)
## Set axis limits
axesE4[0].set_ylim([-0.25,0.25])
axesE4[1].set_ylim([-0.07,0.07])
axesE4[2].set_ylim([-0.12,0.12])

## Adjust space between subplots
#figE4.tight_layout()

#figE4.savefig(dir+'\\figE4_growth-slope.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================
####### FIG E5. DECADAL MEAN Growth data (All cores)
plt.style.use('seaborn-v0_8')
figE5, axesE5 = plt.subplots(4, 2, figsize=(8,7), sharex=True)

## BOXPLOTS
## Error FIRST COLUMN
flier = dict(marker='o',markerfacecolor='b',markersize=2,linestyle='none',markeredgecolor='black')
axesE5[0,0].boxplot([stda_growth_mean_full.iloc[50:60,1],stda_growth_mean_full.iloc[40:50,1],
                    stda_growth_mean_full.iloc[30:40,1],stda_growth_mean_full.iloc[20:30,1],
                    stda_growth_mean_full.iloc[10:20,1],stda_growth_mean_full.iloc[0:10,1]],
                    flierprops=flier)
axesE5[1,0].boxplot([stda_growth_mean_full.iloc[50:60,2],stda_growth_mean_full.iloc[40:50,2],
                    stda_growth_mean_full.iloc[30:40,2],stda_growth_mean_full.iloc[20:30,2],
                    stda_growth_mean_full.iloc[10:20,2],stda_growth_mean_full.iloc[0:10,2]],
                    flierprops=flier)
axesE5[2,0].boxplot([stda_growth_mean_full.iloc[50:60,3],stda_growth_mean_full.iloc[40:50,3],
                    stda_growth_mean_full.iloc[30:40,3],stda_growth_mean_full.iloc[20:30,3],
                    stda_growth_mean_full.iloc[10:20,3],stda_growth_mean_full.iloc[0:10,3]],
                    flierprops=flier)
axesE5[3,0].boxplot([stda_lumin_mean_full.iloc[50:60,1],stda_lumin_mean_full.iloc[40:50,1],
                    stda_lumin_mean_full.iloc[30:40,1],stda_lumin_mean_full.iloc[20:30,1],
                    stda_lumin_mean_full.iloc[10:20,1],stda_lumin_mean_full.iloc[0:10,1]],
                    flierprops=flier)
## Error SECOND COLUMN
axesE5[0,1].boxplot([[],[],[],stda_wf_all.iloc[20:30,1],
                    stda_wf_all.iloc[10:20,1],stda_wf_all.iloc[0:10,1]],
                    flierprops=flier)
axesE5[1,1].boxplot([stda_temp_all.iloc[50:60,1],stda_temp_all.iloc[40:50,1],
                    stda_temp_all.iloc[30:40,1],stda_temp_all.iloc[20:30,1],
                    stda_temp_all.iloc[10:20,1],stda_temp_all.iloc[0:10,1]],
                    flierprops=flier)
axesE5[2,1].boxplot([stda_soi_all.iloc[50:60,1],stda_soi_all.iloc[40:50,1],
                    stda_soi_all.iloc[30:40,1],stda_soi_all.iloc[20:30,1],
                    stda_soi_all.iloc[10:20,1],stda_soi_all.iloc[0:10,1]],
                    flierprops=flier)
axesE5[3,1].boxplot([stda_amo_all.iloc[50:60,1],stda_amo_all.iloc[40:50,1],
                    stda_amo_all.iloc[30:40,1],stda_amo_all.iloc[20:30,1],
                    stda_amo_all.iloc[10:20,1],stda_amo_all.iloc[0:10,1]],
                    flierprops=flier)

## Column 1
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[0,0],color='black',alpha=0.2)
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[1,0],color='black',alpha=0.2)
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[2,0],color='black',alpha=0.2)
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[3,0],color='black',alpha=0.2)
##Column 2
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[0,1],color='black',alpha=0.2)
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[1,1],color='black',alpha=0.2)
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[2,1],color='black',alpha=0.2)
pltE5 = sns.lineplot(y=[0,0], x=[-1,7],ax=axesE5[3,1],color='black',alpha=0.2)

## Modify axes labels
axesE5[0,0].set(ylabel='Density')
axesE5[1,0].set(ylabel='Extension')
axesE5[2,0].set(ylabel='Calcification')
axesE5[3,0].set(ylabel='Luminescence')
axesE5[0,1].set(ylabel='Water Flow')
axesE5[1,1].set(ylabel='Temperature')
axesE5[2,1].set(ylabel='SOI')
axesE5[3,1].set(ylabel='AMO')
## Set axis limits
axesE5[0,0].set_ylim([-1.5,1.5])
axesE5[1,0].set_ylim([-1.3,1.3])
axesE5[2,0].set_ylim([-1.4,1.4])
axesE5[3,0].set_ylim([-2.1,2.1])
axesE5[3,0].set_xlim([0.5,6.5])
## Set axis limits
axesE5[0,1].set_ylim([-2.5,2.5])
axesE5[1,1].set_ylim([-2.3,2.3])
axesE5[2,1].set_ylim([-2.3,2.3])
axesE5[3,1].set_ylim([-2.5,2.5])
axesE5[3,1].set_xlim([0.5,6.5])
## Set xtick labels
axesE5[3,0].set_xticks([1,2,3,4,5,6])
axesE5[3,0].set_xticklabels(periods, fontsize=8,rotation=35)
axesE5[3,0].set_xlabel('Period')#periods, fontsize=8)
axesE5[3,1].set_xticks([1,2,3,4,5,6])
axesE5[3,1].set_xticklabels(periods, fontsize=8,rotation=35)
axesE5[3,1].set_xlabel('Period')#periods, fontsize=8)

## Adjust space between subplots
figE5.tight_layout()

#figE5.savefig(dir+'\\figE5_stda-growth-change.tiff', format='tiff', dpi=300,bbox_inches = 'tight')


# =============================================================================
####### FIG E6. Cross-Wavelet Transform (THIS WAS FOR ANNUAL DATA)
import pyleoclim as pyleo

# Load your data
y = lumin_det['G/B'].values
ty = lumin_det["Y.M."].values
x = growth_det['Density'].values
tx = growth_det["Y.M."].values

ts_gb = pyleo.Series(time=tx, value=x, time_unit='yr', label='Density',verbose=False,
                     value_name = r'$Density$',value_unit='STDA')
ts_wf = pyleo.Series(time=ty, value=y, time_unit='yr', label='G/B',verbose=False,
                     value_name = r'$Luminescence$',value_unit=r'$STDA$')

## Plot wavelet transform
ts_gb.wavelet(method='cwt').plot()
ts_wf.wavelet(method='cwt').plot()

## It change the scales of the scalogram.
## First arg changes the Amplitude scale, the second arg changes the Y-scale
## Say we wanted to focus on oscillations in the 0.7-10kyr range
ts_wf_scl = ts_wf.wavelet(freq_kwargs={'fmin':1/30,'fmax':1,'nf':100})
ts_wf_scl.plot()

## Plot significance
ts_wf_sig = ts_wf_scl.signif_test(method='CN',number = 1000)
ts_wf_sig.plot()

## Spectral plot
psd = ts_wf.spectral(method='wwz')
psd.beta_est().plot()

#### Wavelet transform coherence between two series
wf_gb = ts_wf.wavelet_coherence(ts_gb,method='wwz')
fig, ax = wf_gb.plot()

## Significance
wf_gb_sig = wf_gb.signif_test(method='CN',number=100)
fig, ax = wf_gb_sig.plot()

## Dashboard
wf_gb_sig.dashboard()

## Save figure
wf_gb_sig.dashboard(savefig_settings={'path':'./gb-Den_dash_Calamar_yr.tif','dpi':600})



# =============================================================================
####### FIG E7. Cross-Wavelet Transform - MONTHLY DATA
import pyleoclim as pyleo

# Load your data (it must be sorted from oldest to recent dates)
x = growth_det['Extension_anom'].values
y = envir_det['HadISST_anom'].values
tx = lumin_det["Y.M."].values
ty = envir_det["Y.M."].values


ts1 = pyleo.Series(time=tx, value=x, time_unit='yr', label='Extension',verbose=False,
                     value_name = '$Extension$',value_unit='$cm yr^{-1}$')
ts2 = pyleo.Series(time=ty, value=y, time_unit='yr', label='SST',verbose=False,
                     value_name = r'$HadISST$',value_unit=r'$^{o}C$')
# ts2.plot()

## Plot wavelet transform (CWT)
ts1.wavelet(method='cwt').plot()
ts2.wavelet(method='cwt').plot()

## It change the scales of the scalogram.
## First arg changes the Amplitude scale, the second arg changes the Y-scale
## Use fmax = 2 if data is deseasonalized, fmax = 12 for seasonalized data.
## The scales of interest are determined by fmin, if want to focus on
## scales of 1-10 year cycles use fmin = 1/10. The higher nf, the smoother the plot.
ts2_scl = ts2.wavelet(freq_kwargs={'fmin':1/20,'fmax':6,'nf':100})
ts2_scl.plot()

## Plot significance of scalogram
ts2_sig = ts2_scl.signif_test(method='CN',number = 1000)
ts2_sig.plot()

## Power spectral plot
'''PSD shows how much variability (or power) a single time series contains at 
different frequencies or periods. A high value means that a relatively large 
proportion of the variance in the time series occurs around that frequency/timescale.'''
psd = ts2.spectral(method='wwz')
psd.beta_est().plot()

#### Weighted Wavelet Z-transform coherence between two series (WTC)
'''This help to visualize where the two time series covary consistenly.
It measures the localized correlation/coherence and it is useful to find 
relationships. The arrows provide information about the phase, if they are pointing
to the right the ts are in phase, if they are to the left then they are anti-phase.'''
wwz = ts2.wavelet_coherence(ts1,method='wwz')
fig, ax = wwz.plot()

## WWZ Significance
''' NOTE: This line can take about 40 min to complete, using n 200 (surrogate models).
number=200 is good for exploration, but min 500 or 1000 is recommended for 
stronger inferences. The significance determines determines which of those 
regions are stronger than expected under the specified null/surrogate model?'''
wwz_sig = wwz.signif_test(method='CN',number=200)
fig, ax = wwz_sig.plot()

## Dashboard (it shows the WTC and cross-wavelet transform XWT plots)
'''The WTC show how consistently the two series are related at a particular time 
and timescale. The XWT indicate when the two series have strong common oscillatory 
power at the same timescale. A high-power region means that both series have 
strong variability at that period and time. However, high XWT power does not 
necessarily mean strong correlation'''
wwz_sig.dashboard()

## Save figure
wwz_sig.dashboard(savefig_settings={'path':'./HadISST-Extension_dash_monthly_detr.tif','dpi':300})
