# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:30:10 2026

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
growth = coral_data.parse(1)#.drop([96,97,98]).reset_index(drop=True) ## Growth data
lumin = lumin_data.parse(1) ## Luminescence data
envir = envir_data.parse(0) ## Environmental data
# print('Number of rows and columns:',growth.shape)

## Check if there is missing data
growth.isna().sum()
lumin.isna().sum()
envir.isna().sum()

## Interpolate if needed
# growth = growth.interpolate()