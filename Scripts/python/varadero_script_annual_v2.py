# -*- coding: utf-8 -*-
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
growth = coral_data.parse(1).iloc[0:744]#.drop([96,97,98]).reset_index(drop=True) ## Growth data
lumin = lumin_data.parse(1) ## Luminescence data
envir = envir_data.parse(0) ## Environmental data
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
Variable      | Statistic | p-value
--------------|----------------------
Density       |  0.99     |  0.000 *
Extension     |  0.96     |  0.000 *
Calcification |  0.97     |  0.000 *
G/B           |  0.99     |  0.001 *
WF_Helena     |  0.96     |  0.000 *
WF_Calamar    |  0.98     |  0.000 *
HadISST       |  0.97     |  0.000 *
SOI           |  0.99     |  0.001 *
AMO           |  0.99     |  0.013 *
-------------------------------------
*There is no normality for all variables.
'''


# =============================================================================
# Test stationary
# =============================================================================
## A stationary time series is one whose statistical properties do not change over time
## If p < 0.05, time series is stationary (there are trends)
from statsmodels.tsa.stattools import adfuller

result = adfuller(growth["Calcification"])
# result = adfuller(lumin["G/B"])
# result = adfuller(envir["SOI"])
print('Statistic', result[0])   # statistic
print('p-value', result[1])   # p-value

'''
Stationary Results
-------------------------------------
Variable      | Statistic | p-value
--------------|----------------------
Density       | -2.50     |  0.117
Extension     | -4.61     |  0.000 *
Calcification | -5.00     |  0.000 *
G/B           | -3.26     |  0.016 *
WF_Helena     | -2.58     |  0.097
WF_Calamar    | -6.27     |  0.000 *
HadISST       | -4.55     |  0.000 *
SOI           | -7.48     |  0.000 *
AMO           | -2.13     |  0.231
-------------------------------------
* Non stationary time-series
'''

# =============================================================================
# Test Seasonality
# =============================================================================
from statsmodels.tsa.seasonal import seasonal_decompose

## Select dataset and invert df
# sdata = lumin["G/B"].iloc[::-1].reset_index(drop=True)
sdata = growth["Calcification"].iloc[0:744].iloc[::-1].reset_index(drop=True)
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

plot_acf(growth["Density"], lags=36)
plt.show()

plot_acf(envir["HadISST"], lags=36)
plt.show()

## Durbin-watson test: autocorrelation test at lag=1
from statsmodels.stats.stattools import durbin_watson

durbin_watson(growth["Calcification"])
durbin_watson(lumin["G/B"])
durbin_watson(envir["AMO"])
'''
* Durbin-Watson test at lag=1, autocorrelation is important at values < 2
* Values > 2 indicates no autocorrelation.

Density       = 0.005 *
Extension     = 0.090 *
Calcification = 0.085 *
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

growth_det = detrend(growth, ['Density','Extension','Calcification']).iloc[0:744,:]
lumin_det = detrend(lumin, ['G/B'])
envir_det = detrend(envir, ['WF_Helena','WF_Calamar','HadISST','SOI','AMO'])

# =============================================================================
# Pearson Correlation
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
growth_det2 = growth_det.iloc[0:384,:]
lumin_det2 = lumin_det.iloc[0:384,:]
envir_det2 = envir_det.iloc[0:384,:]
## Prepare data <1984
growth_det3 = growth_det.iloc[384:,:]
lumin_det3 = lumin_det.iloc[384:,:]
envir_det3 = envir_det.iloc[384:,:]

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
# OPTION B - Residuals
# Time-series detrending (removing seasonality)
# =============================================================================

from statsmodels.tsa.stattools import acf

def resid_det(df, cols):
    df_residuals = pd.DataFrame(index=df.index)
    
    for col in cols:
        # Using multiplicative or additive decomposition depending on your data structure
        decomposition = seasonal_decompose(df[col], model='additive', period=12)
        # Extract the residual component (un-autocorrelated anomaly)
        df_residuals[col] = decomposition.resid
    
    # Drop NaNs created at the edges by the decomposition window
    df_residuals.dropna(inplace=True)
    return df_residuals

growth_resid = resid_det(growth.iloc[0:744,:],['Density','Extension','Calcification'])
lumin_resid = resid_det(lumin,['G/B'])
envir_resid = resid_det(envir,['WF_Helena','WF_Calamar','HadISST','SOI','AMO'])
# Test if residuals still have autocorrelation using Autocorrelation Function (ACF)
print("Residual Autocorrelation (Lag 1):", acf(envir_resid['AMO'], nlags=1)[1])
# Values close to 0 mean autocorrelation has been successfully mitigated.

'''
Autocorrelation values from -1 to +1.
Values close to 0 mean autocorrelation has been successfully mitigated.
Autocorrelation after removing seasonality on residuals:
    Density       = 0.644
    Extension     = 0.388
    Calcification = 0.389
    G/B           = 0.071
    WF_Helena     = 0.561
    WF_Calamar    = 0.595
    HadISST       = 0.338
    SOI           = 0.134
    AMO           = 0.609
*** Autocorrelation is still high.
'''

# =============================================================================
# Pearson Correlation
# =============================================================================

def corr(x_df,y_df,x_cols,y_cols):
    for x in x_cols:
        for y in y_cols:
            r_val, p_val = pearsonr(x_df[x], y_df[y])
            print(f"\n--- Final Results {x} vs {y} ---")
            print(f"Correlation Coefficient (r): {r_val:.4f}")
            print(f"Adjusted p-value: {p_val:.4e}")

growth_corrs = corr(envir_resid,growth_resid,
                    ['WF_Helena','WF_Calamar','HadISST','SOI','AMO'],
                    ['Density','Extension','Calcification'])
lumin_corrs = corr(envir_resid,lumin_resid,
                    ['WF_Helena','WF_Calamar','HadISST','SOI','AMO'],['G/B'])

plt.scatter(envir_resid['HadISST'], growth_resid['Density'])
'''
-------------------------------------------------------------------------------------
              | WF_Helena   | WF_Calamar  | HadISST     | SOI         | AMO         |
-------------------------------------------------------------------------------------
Density       |-0.03,<0.001 | 0.10,<0.001 |-0.03,<0.001 |-0.05,<0.001 | 0.05,<0.001 |
Extension     |-0.08,<0.001 |-0.05,<0.001 | 0.13,<0.001 | 0.03,<0.001 | 0.12,<0.001 |
Calcification |-0.09,<0.001 |-0.02,<0.001 | 0.13,<0.001 | 0.02,<0.001 | 0.01,<0.001 |
G/B           | 0.07,<0.001 | 0.07,<0.001 |-0.06,<0.001 |-0.04,<0.001 | 0.06,<0.001 |
-------------------------------------------------------------------------------------
Correlations with High sginificance, but low coefficient. 
'''

# =============================================================================
# Cross-correlations
# =============================================================================
from statsmodels.tsa.stattools import ccf

cross = ccf(envir_det["HadISST"], growth_det["Density"])


# =============================================================================
# MULTIPLE VARIABLE EVALUATIONS
# =============================================================================

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

          Variable       VIF
0   WF_Helena_anom  1.902295
1  WF_Calamar_anom  2.281343
2     HadISST_anom  1.975874
3         SOI_anom  1.456005
4         AMO_anom  2.056262
'''

# =============================================================================
# MULTIPLE LINEAR REGRESSION
# =============================================================================
import statsmodels.api as sm

def mlr(x_df, y_df, x_vars, y_vars):
    X = sm.add_constant(x_df[x_vars])
    for i in y_vars:
        y = y_df[i]
        model = sm.OLS(y, X).fit()
        print("\n \n Response Variable: "+i)
        print(model.summary())
        
        ## Check autocorrelation of residuals
        plot_acf(model.resid, lags=36)

mlr(envir_det, growth_det, envir_vars2, growth_vars2)
'''
Residuals are autocorrelated. So, go to the next step
'''

# =============================================================================
# GLSAR (Generalized Least Squares with AR errors)
# =============================================================================
'''
The rho value determines the autoregressive order (AR(rho)). This order can be
determined not only with the ACF, but looking at the AIC an BIC values, with
lower values prefered.
Here, the Density showed autocorrelations at lag ~16, but the extension and 
calcification at lag ~5. The Density may required AR with rho ~5, maybe.
'''

from statsmodels.regression.linear_model import GLSAR

def glsar_run(x_df, y_df, x_vars, y_vars):
    X = sm.add_constant(x_df[x_vars])
    for i in y_vars:
        y = y_df[i]
        glsar = GLSAR(y, X, rho=1)
        results = glsar.iterative_fit(maxiter=10)
        print(results.summary())

glsar_run(envir_det.sort_values(by='Y.M', ascending=False), 
          growth_det.sort_values(by='Y.M.', ascending=False), 
          envir_vars2, growth_vars2)
'''
The coefficients and R2 are very small, although there are some variables with
p < 0.05. This suggest is better to inspect GAMM in R.
'''


# =============================================================================
# SARIMAX
# =============================================================================
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarimax_run(x_df, y_df, x_vars, y_vars):
    X = sm.add_constant(x_df[x_vars])
    for i in y_vars:
        y = y_df[i]      
        model = SARIMAX(
            endog=y,
            exog=X,
            order=(1,0,0), # rho=1
            seasonal_order=(0,0,0,0) )
        sarimax = model.fit()
        print(sarimax.summary())
        print('AIC', sarimax.aic)

sarimax_run(envir_det.sort_values(by='Y.M', ascending=False), 
          growth_det.sort_values(by='Y.M.', ascending=False), 
          envir_vars2, growth_vars2)


# =============================================================================
# Generalized Additive Model (GAM)
# =============================================================================
## Suppose the effect of env vars are nonlinear.
from pygam import LinearGAM, s

def gam_run(x_df, y_df, x_vars, y_vars):
    X = x_df[x_vars].values
    for i in y_vars:
        y = y_df[i].values
        gam = LinearGAM(s(0)+s(1)+s(2)+s(3)+s(4)).fit(X,y)
        print("GAM {i}", gam.summary())
    
    # XX = gam.generate_X_grid(term=0)
    # plt.plot(
    #     XX[:,0],
    #     gam.partial_dependence(term=0))
        
gam_run(envir_det.sort_values(by='Y.M', ascending=False), 
          growth_det.sort_values(by='Y.M.', ascending=False), 
          envir_vars2, growth_vars2)



##### Hasta aqui hice, lo de abajo son cosas viejas....


# =============================================================================
# ## Get data for the respective period 1982-2015:
  ## PER CORE
# =============================================================================
period = list(range(1982,2016))
growth_period = []
lumin_period = []
for i in period:
    yr = growth.loc[growth['Year'] == i]
    lumyr = lumin.loc[lumin['Year'] == i]
    growth_period.append(yr)
    lumin_period.append(lumyr)

## Skeletal growth and luminescence
growth_period = pd.concat(growth_period).sort_values(['Core','Year'],ascending=(True,False)).reset_index(drop=True)
lumin_period = pd.concat(lumin_period).sort_values(['Core','Year'],ascending=(True,False)).reset_index(drop=True)

### Parse environmental variables 1981-2015
dateEnv = envir.iloc[0:35,0]#['Year','Month','Y.M']
wf = envir.loc[0:35,:]['WF_Helena']#.interpolate()
wf2 = envir.loc[0:35,:]['WF_Calamar']#.interpolate()
temp = envir.loc[0:35,:]['Air_Temperature']
soi = envir.loc[0:35,:]['SOI']
amo = envir.loc[0:35,:]['AMO']
wf_std = envir.loc[0:35,:]['WF_std']#.interpolate()
temp_std = envir.loc[0:35,:]['Temp_std']
soi_std = envir.loc[0:35,:]['SOI_std']
amo_std = envir.loc[0:35,:]['AMO_std']

wf_all = pd.concat([dateEnv,wf,wf_std],axis=1,join='inner')
temp_all = pd.concat([dateEnv,temp,temp_std],axis=1,join='inner')
soi_all = pd.concat([dateEnv,soi,soi_std],axis=1,join='inner')
amo_all = pd.concat([dateEnv,amo,amo_std],axis=1,join='inner')


# =============================================================================
# ## Overall mean FULL TIMESERIES (Master)
# =============================================================================
growth_mean_all = growth.groupby(['Year']).mean(numeric_only=True).reset_index()
growth_mean_all = growth_mean_all.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
growth_std_all = growth.groupby(['Year']).std(ddof=0,numeric_only=True).reset_index()
growth_std_all = growth_std_all.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
lumin_mean_all = lumin.groupby(['Year']).mean(numeric_only=True).reset_index().drop(['G/B_std'],axis=1)
lumin_mean_all = lumin_mean_all.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
lumin_std_all = lumin.groupby(['Year']).std(ddof=0,numeric_only=True).reset_index().drop(['G/B_std'],axis=1)
lumin_std_all = lumin_std_all.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
wf_mean_all = envir[['Year','WF_Helena','WF_std']].dropna()
temp_mean_all = envir[['Year','Air_Temperature','Temp_std']].dropna()
soi_mean_all = envir[['Year','SOI','SOI_std']].dropna()
amo_mean_all = envir[['Year','AMO','AMO_std']].dropna()


# =============================================================================
# ## Overall mean of Coral growth For Period 1982-2015
# =============================================================================
growth_mean = growth_period.groupby(['Year']).mean(numeric_only=True).reset_index()
growth_mean = growth_mean.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
growth_std = growth_period.groupby(['Year']).std(ddof=0,numeric_only=True).reset_index()
growth_std = growth_std.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
lumin_mean = lumin_period.groupby(['Year']).mean(numeric_only=True).reset_index().drop(['G/B_std'],axis=1)
lumin_mean = lumin_mean.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
lumin_std = lumin_period.groupby(['Year']).std(ddof=0,numeric_only=True).reset_index().drop(['G/B_std'],axis=1)
lumin_std = lumin_std.sort_values(['Year'],ascending=(False)).reset_index(drop=True)


# =============================================================================
# ## STANDARDIZED NORMALIZATIONS (Z-SCORES)
# =============================================================================
growth_var = ['Density','Extension','Calcification']
core_index = ['VAR1','VAR2','VAR3','VAR4']
envir_var = ['WF_Helena','WF_Calamar','Air_Temperature','SOI','AMO']

## FOR EACH CORE:
stda_growth = pd.concat([growth_period[['Core','Year']],STDAidx(growth_period,growth_var,'Core',core_index)],axis=1)
stda_lumin = pd.concat([lumin_period[['Core','Year']],STDAidx(lumin_period,['G/B'],'Core',core_index)],axis=1)
stda_wf = pd.concat([dateEnv,STDA(wf)],axis=1,join='inner')
stda_wf2 = pd.concat([dateEnv,STDA(wf2)],axis=1,join='inner')
stda_temp = pd.concat([dateEnv,STDA(temp)],axis=1,join='inner')
stda_soi = pd.concat([dateEnv,STDA(soi)],axis=1,join='inner')
stda_amo = pd.concat([dateEnv,STDA(amo)],axis=1,join='inner')

## For the overall mean (master):
stda_growth_mean = stda_growth.groupby(['Year']).mean(numeric_only=True).reset_index()
stda_growth_mean = stda_growth_mean.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
stda_lumin_mean = stda_lumin.groupby(['Year']).mean(numeric_only=True).reset_index()
stda_lumin_mean = stda_lumin_mean.sort_values(['Year'],ascending=(False)).reset_index(drop=True)

## For the full timeseries
stda_growth_all = pd.concat([growth[['Core','Year']],STDAidx(growth,growth_var,'Core',core_index)],axis=1)
stda_lumin_all = pd.concat([lumin[['Core','Year']],STDAidx(lumin,['G/B'],'Core',core_index)],axis=1)
stda_wf_all = pd.concat([envir['Year'],STDA(envir['WF_Helena'])],axis=1,join='inner')
stda_wf2_all = pd.concat([envir['Year'],STDA(envir['WF_Calamar'])],axis=1,join='inner')
stda_temp_all = pd.concat([envir['Year'],STDA(envir['Air_Temperature'])],axis=1,join='inner')
stda_soi_all = pd.concat([envir['Year'],STDA(envir['SOI'])],axis=1,join='inner')
stda_amo_all = pd.concat([envir['Year'],STDA(envir['AMO'])],axis=1,join='inner')

# Period 1951-2015
stda_growth_mean_full = stda_growth_all.groupby(['Year']).mean(numeric_only=True).reset_index()
stda_growth_mean_full = stda_growth_mean_full.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
stda_growth_mean_full = stda_growth_mean_full.loc[0:64,:]
stda_lumin_mean_full = stda_lumin_all.groupby(['Year']).mean(numeric_only=True).reset_index()
stda_lumin_mean_full = stda_lumin_mean_full.sort_values(['Year'],ascending=(False)).reset_index(drop=True)
stda_lumin_mean_full = stda_lumin_mean_full.loc[0:64,:]

# =============================================================================
# REGRESSIONS
# =============================================================================
### Check normality and Homoscedasticity
check_assumptions(growth_mean_all,'Density','Year') ## Normal / Not Homogeneous
check_assumptions(growth_mean_all,'Extension','Year') ## Not normal / Homogeneous
check_assumptions(growth_mean_all,'Calcification','Year') ## Not Normal / Not Homogeneous
check_assumptions(lumin_mean_all,'G/B','Year') ## Normal / Homogeneous
check_assumptions(wf_mean_all,'WF_Helena','Year') ## Normal / Homogeneous
check_assumptions(temp_mean_all,'Air_Temperature','Year') ## Normal / Homogeneous
check_assumptions(soi_mean_all,'SOI','Year') ## Normal  / Homogeneous
check_assumptions(amo_mean_all,'AMO','Year') ## Normal / Not Homogeneous
check_assumptions(stda_growth_all,'Calcification','Year') ## Normal / Not Homogeneous

### Regression total (1951-2015)
dates_list = list(range(1951,2016))
reg_den = stats_all(growth_mean_all,'Density','Year',dates_list)
reg_ext = stats_all(growth_mean_all,'Extension','Year',dates_list)
reg_cal = stats_all(growth_mean_all,'Calcification','Year',dates_list)
reg_lum = stats_all(lumin_mean_all,'G/B','Year',dates_list)
reg_wf = stats_all(wf_mean_all,'WF_Helena','Year',dates_list)
reg_temp = stats_all(temp_mean_all,'Air_Temperature','Year',dates_list)
reg_soi = stats_all(soi_mean_all,'SOI','Year',dates_list)
reg_amo = stats_all(amo_mean_all,'AMO','Year',dates_list)

## Detect point changes in time series data (1951-2015)
dates_list = list(range(1954,2016))
det_change = detect_changes(growth_mean_all,'Calcification',dates_list)
det_change = detect_changes(lumin_mean_all,'G/B',dates_list)
det_change = detect_changes(amo_mean_all,'AMO',dates_list)
det_change = detect_changes(temp_mean_all,'Air_Temperature',dates_list)
det_change = detect_changes(soi_mean_all,'SOI',dates_list)
det_change = detect_changes(wf_mean_all,'WF_Helena',dates_list)

## Trend detections
# seg_data = growth_mean_all[growth_mean_all['Year'].isin(dates_list)]['Extension']
# seg = Segmenter(dates_list, seg_data.tolist(), n=10)
# seg.calculate_segments()
# seg.plot_segments()

# =============================================================================
# REGRESSIONS PER DECADES (NOT USED)
# =============================================================================
### Regression per decades
# dates_list = stda_growth_mean_full['Year'].tolist()
# periods = ['1956-1965','1966-1975','1976-1985','1986-1995','1996-2005','2006-2015']
# reg_den_dec = linreg(stda_growth_mean_full.loc[0:59],'Density',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_ext_dec = linreg(stda_growth_mean_full.loc[0:59],'Extension',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_cal_dec = linreg(stda_growth_mean_full.loc[0:59],'Calcification',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_lum_dec = linreg(stda_lumin_mean_full.loc[0:59],'G/B',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_wf_dec = linreg(stda_wf_all.loc[0:29],'WaterFlow',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_temp_dec = linreg(stda_temp_all.loc[0:59],'Temperature',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_soi_dec = linreg(stda_soi_all.loc[0:59],'SOI',dates_list,'Year',10).sort_values(['Period'],ascending=(True))
# reg_amo_dec = linreg(stda_amo_all.loc[0:59],'AMO',dates_list,'Year',10).sort_values(['Period'],ascending=(True))

# ## Mean per decades:
# [growth_mean_deca,growth_std_deca] = mean_range(growth_mean_all.loc[0:65,:],growth_mean_all.loc[0:65,:]['Year'],'Year',10)
# [lumin_mean_deca,lumin_std_deca] = mean_range(lumin_mean_all,lumin_mean_all['Year'],'Year',10)
# [wf_mean_deca,wf_std_deca] = mean_range(wf_mean_all,wf_mean_all['Year'],'Year',10)
# [temp_mean_deca,temp_std_deca] = mean_range(temp_mean_all,temp_mean_all['Year'],'Year',10)
# [soi_mean_deca,soi_std_deca] = mean_range(soi_mean_all,soi_mean_all['Year'],'Year',10)
# [amo_mean_deca,amo_std_deca] = mean_range(amo_mean_all,amo_mean_all['Year'],'Year',10)

# ## Mean per decades // STANDARDIZED:
# [stda_growth_mean_deca,stda_growth_std_deca] = mean_range(stda_growth_mean_full.loc[0:65,:],stda_growth_mean_full.loc[0:65,:]['Year'],'Year',10)
# [stda_lumin_mean_deca,stda_lumin_std_deca] = mean_range(stda_lumin_mean_full,stda_lumin_mean_full['Year'],'Year',10)
# [stda_wf_mean_deca,stda_wf_std_deca] = mean_range(stda_wf_all,stda_wf_all['Year'],'Year',10)
# [stda_temp_mean_deca,stda_temp_std_deca] = mean_range(stda_temp_all,stda_temp_all['Year'],'Year',10)
# [stda_soi_mean_deca,stda_soi_std_deca] = mean_range(stda_soi_all,stda_soi_all['Year'],'Year',10)
# [stda_amo_mean_deca,stda_amo_std_deca] = mean_range(stda_amo_all,stda_amo_all['Year'],'Year',10)

# =============================================================================
# Mean and Stdv of growth variables, before and after 1981
# =============================================================================
## Mean Of period 1981-2015:
growth_mean_after = (growth_mean_all.loc[0:34,:]).mean(numeric_only=True)
growth_std_after = (growth_mean_all.loc[0:34,:]).std(ddof=0,numeric_only=True)
lumin_mean_after = (lumin_mean_all.loc[0:34,:]).mean(numeric_only=True)
lumin_std_after = (lumin_mean_all.loc[0:34,:]).std(ddof=0,numeric_only=True)
## Mean Of period 1951-1981:
growth_mean_before = (growth_mean_all.loc[34:64,:]).mean(numeric_only=True)
growth_std_before = (growth_mean_all.loc[34:64,:]).std(ddof=0,numeric_only=True)
lumin_mean_before = (lumin_mean_all.loc[34:64,:]).mean(numeric_only=True)
lumin_std_before = (lumin_mean_all.loc[34:64,:]).std(ddof=0,numeric_only=True)


# =============================================================================
# ###### PLOTS (INCLUDED IN MANUSCRIPT)
# =============================================================================

###### FIG 0. CORAL TIMESPAN RECORDED
fig0, axes0 = plt.subplots(figsize=(4.2,1), sharex=True)
plt0 = sns.lineplot(y=[4,4], x=[1982,2015], ax=axes0) #VAR1
plt0 = sns.lineplot(y=[3,3], x=[1951,2015]) #VAR2
plt0 = sns.lineplot(y=[2,2], x=[1942,2015]) #VAR3
plt0 = sns.lineplot(y=[1,1], x=[1950,2015]) #VAR4
plt0 = sns.lineplot(y=[0,0], x=[1950,2015],color='black') #MEAN

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

## for original units/values
plt_gr = growth
plt_lu = lumin
plt_wf = wf_all
plt_te = temp_mean_all
plt_soi= soi_mean_all
plt_amo = amo_mean_all
plt_gr_mn = growth_mean_all[0:66]
plt_lu_mn = lumin_mean_all
## Put all the env vars in a list
plt_env_vars = [plt_wf,plt_te,plt_soi,plt_amo]

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
    plt3 = sns.lineplot(data=plt_gr_mn,y=lbl_gr[i],x="Year",
                        ax=axes3[axy[i],0],color='black',label='Mean')

## Luminescence per core:
plt3 = sns.lineplot(data=plt_lu, y="G/B", x="Year",hue='Core',
                    ax=axes3[3,0],linewidth=0.7)
## Luminescence Mean:
plt3 = sns.lineplot(data=plt_lu_mn, y="G/B", x="Year",color='black',
                    ax=axes3[3,0],label='Mean')

## Environmental data:
lbl_env = ['WaterFlow','Temperature','SOI','AMO']
lbl_std = ['WF_std','Temp_std','SOI_std','AMO_std']
for i in (range(len(lbl_env))):
    ## Mean
    plt3 = sns.lineplot(data=plt_env_vars[i], y=lbl_env[i], x="Year",
                        ax=axes3[axy[i],1])
    ## Add Error of Environmental variables:
    axes3[axy[i],1].fill_between(
        plt_env_vars[i]['Year'],plt_env_vars[i][lbl_env[i]]+plt_env_vars[i][lbl_std[i]],
        plt_env_vars[i][lbl_env[i]]-plt_env_vars[i][lbl_std[i]],
        facecolor='#1f77b4',alpha=0.3)

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
####### FIG E6. Cross-Wavelet Transform
import pyleoclim as pyleo

# Load your data
# x = stda_lumin_mean['G/B'].values
# y = stda_wf['WF_Helena'][:-1].values
# tx = stda_lumin_mean["Year"].values
# ty = stda_wf2["Year"][:-1].values
y = stda_lumin_mean_full['G/B'].values
# y = stda_wf2_all['WF_Calamar'].values
ty = stda_lumin_mean_full["Year"].values
# ty = stda_wf2_all["Year"].values
x = stda_growth_mean_full['Density'].values
tx = stda_growth_mean_full["Year"].values

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

path_env = os.path.join('E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed', 
                     'env_monthly.xlsx')
path_lum = os.path.join('E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed', 
                     'coral_lumn_monthly.xlsx')
data_env_m = pd.ExcelFile(path_env)
data_lum_m = pd.ExcelFile(path_lum)

env_m = data_env_m.parse(0).iloc[0:419,:]
env_m = data_env_m.parse(0)
lum_m = data_lum_m.parse(0)

# Load your data
x = lum_m['G/B'].values
# y = env_m['WF_Calamar'][:-1].values
y = env_m['WF_Helena'][:-1].values
tx = lum_m["Y.M"].values
ty = env_m["Y.M"][:-1].values


ts_gb = pyleo.Series(time=tx, value=x, time_unit='yr', label='G/B',verbose=False,
                     value_name = r'$Skeletal luminescence$',value_unit='G/B')
ts_wf = pyleo.Series(time=ty, value=y, time_unit='yr', label='WF',verbose=False,
                     value_name = r'$Water flow$',value_unit=r'$m_3$ $s_-1$')

## Plot wavelet transform
ts_gb.wavelet(method='cwt').plot()
ts_wf.wavelet(method='cwt').plot()

## It change the scales of the scalogram.
## First arg changes the Amplitude scale, the second arg changes the Y-scale
## Use fmax = 2 if data is deseasonalized, fmax = 12 for seasonalized data.
## The scales of interest are determined by fmin, if want to focus on
## scales of 1-10 year cycles use fmin = 1/10. The higher nf, the smoother the plot.
ts_wf_scl = ts_wf.wavelet(freq_kwargs={'fmin':1/20,'fmax':6,'nf':100})
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
wf_gb_sig = wf_gb.signif_test(method='CN',number=200)
fig, ax = wf_gb_sig.plot()

## Dashboard
wf_gb_sig.dashboard()

## Save figure
wf_gb_sig.dashboard(savefig_settings={'path':'./wf-gb_dash_Helena_monthly.tif','dpi':600})