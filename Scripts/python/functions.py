# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 08:42:36 2021

@author: lizca
"""

import pandas as pd
import statistics as stats
import numpy as np
import scipy.stats
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
import ruptures as rpt
import matplotlib.pyplot as plt

####### ANNUAL MEANS
"""
Calculate annual mean and stdev of each core's parameter'

Usage:
    output = mean_yr(df,year,var,idxName,idxCode)

Input variables: 
    df = Pandas dataframe with indexes and variable columns
    year = Name of column with year, e.g. 'Year'
    var = List of variable names, e.g. ['Density','Extension','Calcification']
    idxName = Name of column with indexes, e.g. 'Core'
    idxCode = List of indexes, e.g. ['VAR1','VAR2','VAR3','VAR4']

Output:
    Pandas dataframe with the respective mean and std values.
"""
def mean_yr(df,year,var,idxName,idxCode):
    output1 = []
    ## For each Core do:
    for i in idxCode:
        output2 = pd.Series([],dtype=pd.StringDtype()) 
        x = (df.loc[df[idxName] == i])
        date = x[year]
        datelist = date.unique()
        ## For each growth variable do:
        for y in var:
            output3 = []
            inter = x[y].interpolate()
            v = pd.concat([date,inter],axis=1,join='inner')
            ## For each year do:
            for z in datelist:
                if y == 'Extension' or y == 'Calcification':
                    d = (v.loc[v[year] == z])
                    suma = pd.Series(sum(d[y]))
                    result = pd.concat([pd.Series(i),pd.Series(z),suma],axis=1)
                    output3.append(result)                    
                else:
                    d = (v.loc[v[year] == z])
                    mean = pd.Series(stats.mean(d[y]))
                    std = pd.Series(stats.stdev(d[y]))
                    result = pd.concat([pd.Series(i),pd.Series(z),mean,std],axis=1)
                    output3.append(result)   
            result2 = pd.concat(output3,axis=0)
            output2 = pd.concat([output2,result2],axis=1)
        output1.append(output2)
    result3 = pd.concat(output1,axis=0)#.rename(columns={0:'Core',1:'Year',2:'Mean',3:'Std'})
    result3.columns = range(result3.shape[1])
    # end = result3.drop([0,5,6,9,10], axis=1)
    # end.columns = range(end.shape[1])
    # columns = ['Core','Year','Density','Den_std','Extension','Ext_std','Calcification','Cal_std']
    # end.columns= columns
    # end = end.reset_index(drop=True)
    return result3




####### TOTAL MEAN BY PARAMETER
"""
Calculate mean and stdev of each parameter'

Usage:
    [mean,std] = mean_cols(df,yr,varidx,coreidx)

Input variables: 
    df = Pandas dataframe with indexes and variable columns
    yr = Name of column with years, e.g. 'Year'
    core = Name of column containin core labels, e.g. 'Core'
    varidx = List of variable names, e.g. ['Density','Extension','Calcification']
    coreidx = List of core indexes, e.g. ['VAR1','VAR2','VAR3','VAR4']

Output:
    Pandas dataframe with the respective mean and std values, in two
    separate dataframes.
"""
def mean_cols(df,yr,core,varidx,coreidx):
    year = pd.Series(sorted(df[yr].unique(),reverse=True)).rename('Year')
    output1 = []
    output2 = []
    for i in varidx:
        x1 = df[[yr,core,i]]
        x1 = x1.sort_values(by=[core,yr],ascending=False)
        xcore = []
        for a in coreidx:       
            x2 = (x1.loc[x1[core] == a]).reset_index()#.drop(['index'])
            xcore.append(x2[i].rename(a))
        x3 = pd.concat(xcore,axis=1,ignore_index=False)
        x4 = x3.mean(axis=1).rename(i)
        x5 = x3.std(axis=1).rename(i)
        output1.append(x4)
        output2.append(x5)
    mean = pd.concat(output1,axis=1,ignore_index=False)
    mean = pd.concat([year,mean],axis=1)
    std = pd.concat(output2,axis=1,ignore_index=False)
    std = pd.concat([year,std],axis=1)
    return [mean,std]
    



####### STANDARDIZED NORMALIZATIONS
"""
Calculate standardized normalizations

Usage:
    output = STDA(df)

Input variables: 
    df = Pandas dataframe of a single column

Output:
    Pandas dataframe with the respective STDA values.
"""
def STDA(df):
    # Drop nan values if any
    if 'nan' in str(list(df)):
        x = df.dropna()
    else:
        x = df
    mean = stats.mean(x)
    std = stats.stdev(x)
    stda = pd.DataFrame((x-mean)/std)#.rename_axis(var[y])
    return stda



####### STANDARDIZED NORMALIZATIONS FOR INDEXES
"""
Calculate standardized normalizations of density, extension and
calcification to every coral core.

Usage:
    output = STDAidx(df,var,idxName,idxCode)

Input variables: 
    df = Pandas dataframe with indexes and variable columns
    var = List of variable names, e.g. ['Density','Extension','Calcification']
    idxName = Name of column with indexes, e.g. 'Core'
    idxCode = List of indexes, e.g. ['VAR1','VAR2','VAR3','VAR4']

Output:
    Pandas dataframe with the respective STDA values.
"""

def STDAidx(df,var,idxName,idxCode):
    output2 = []
    for i in range(len(idxCode)):
        output1 = []
        x = (df.loc[df[idxName] == idxCode[i]])#.reset_index(drop=True)
        for y in var:
            m = x[y].interpolate()
            mean = stats.mean(m)
            std = stats.stdev(m)
            stda = pd.DataFrame((m-mean)/std)#.rename_axis(var[y])
            output1.append(stda)
            result = pd.concat(output1,axis=1)
        output2.append(result)
    result2 = pd.concat(output2,axis=0)
    return result2



######## CLIMATOLOGY
"""
Calculate montly mean (climatology) of input variables.

Usage:
    output = climat(df,date,col)

Input variables: 
    df = Pandas dataframe with indexes and variable columns
    date = Pandas dataframe or series including the date labels/index
    col = Column name of the input date including indexes, e.g. 'Month'

Output:
    Pandas dataframe with the respective monthly values.
"""
def climat(df,date,col):
    months = sorted(date[col].unique())
    merge = pd.concat([date[col],df],axis=1)
    output = []
    for i in months:
        if 'nan' in str(list(df)):
            x = df.dropna()
        else:
            x = df
        data = x.loc[merge[col]==i]
        mean = pd.Series(stats.mean(data))
        std = pd.Series(stats.stdev(data))
        clim = pd.concat([mean,std],axis=1)
        result = pd.concat([pd.Series(i),clim],axis=1)
        output.append(result)
    result2 = pd.concat(output,axis=0).set_axis(
        ['Months', 'Mean', 'Std'], axis=1,)# inplace=False)
    #result2 = pd.concat(output,axis=0)
    return result2



######## LINEAR REGRESSIONS
"""
Calculate linear regression per time range of input variables.

Usage:
    output = linreg(df,var,dates,col_date,t_range)

Input variables: 
    df = Pandas dataframe with indexes and variable columns.
    var = List of variable names to look for in the input df.
    dates = list of date labels (years) to include in the regression.
    col_date = Name of the column including date labels.
    t_range = integer indicating the time window (years) of the regression, eg.10, for regression every 10 years.
Output:
    Pandas dataframe with the regression values.
"""
def linreg(df,var,dates,col_date,t_range):
    data = df.loc[df[col_date].isin(dates)].reset_index(drop=True)
    drop_t = list(range(t_range))
    nperiods = list(range(data.shape[0] // t_range))
    nranges = [t_range]*len(nperiods)
    period_label = []
    for num1, num2 in zip(nperiods, nranges):
        product = num1 * num2
        period_label.append(dates[product])
        
    slp_list = []
    p_list = []
    r2_list = []
    plabel = []
    for i in nperiods:
        subset = data.loc[drop_t]
        regr = scipy.stats.linregress(subset[col_date], subset[var])
        slp = pd.Series(regr.slope)
        p = pd.Series(regr.pvalue)
        r2 = pd.Series(regr.rvalue)
        per = pd.Series(period_label[i])
        slp_list.append(slp)
        p_list.append(p)
        r2_list.append(r2)
        plabel.append(per)
        data = data.drop(drop_t).reset_index(drop=True)
    slp_list = pd.concat(slp_list,axis=0)
    p_list = pd.concat(p_list,axis=0)
    r2_list = pd.concat(r2_list,axis=0)
    plabel = pd.concat(plabel,axis=0)
    concat = pd.concat([plabel,slp_list,r2_list,p_list],axis=1).rename(columns={0:'Period',1:'slope',2:'r',3:'p'})
    return concat


######## MEAN PER TIME RANGE 
"""
Calculate Mean and std per time range of input variables.

Usage:
    [mean,std] = mean_range(df,var,dates,col_date,t_range)

Input variables: 
    df = Pandas dataframe with indexes and variable columns.
    dates = list of date labels (years) to include in the regression.
    col_date = Name of the column including date labels.
    t_range = integer indicating the time window (years) of the regression, eg.10, for regression every 10 years.
Output:
    Two Pandas dataframe, one with the mean and other with std values.
"""
def mean_range(df,dates,col_date,t_range):
    data = df.loc[df[col_date].isin(dates)].reset_index(drop=True)
    drop_t = list(range(t_range))
    nperiods = list(range(data.shape[0] // t_range))
    nranges = [t_range]*len(nperiods)
    period_label = []
    for num1, num2 in zip(nperiods, nranges):
        product = num1 * num2
        period_label.append(dates[product])
        
    mean_list = []
    std_list = []
    plabel = []
    for i in nperiods:
        subset = data.loc[drop_t]
        mean = pd.DataFrame(subset.mean()).transpose()
        std = pd.DataFrame(subset.std()).transpose()
        per = pd.Series(period_label[i])
        mean_list.append(mean)
        std_list.append(std)
        plabel.append(per)
        data = data.drop(drop_t).reset_index(drop=True)
    mean_list = pd.concat(mean_list,axis=0)
    std_list = pd.concat(std_list,axis=0)
    plabel = pd.concat(plabel,axis=0)
    concat_mean = pd.concat([plabel,mean_list],axis=1).rename(columns={0:'Period'})
    concat_std = pd.concat([plabel,std_list],axis=1).rename(columns={0:'Period'})
    return [concat_mean,concat_std]


#### GET ALL STATS ######
"""
Calculate Mean, std, regressions per time range of input variables.

Usage:
    stats = stats_all(df,y_name,x_name,t_list)

Input variables: 
    df = Pandas dataframe with indexes and variable columns.
    y_name = Dependent variable.
    x_name = Independent variable.
    t_list = list of integers indicating time span of the data.
Output:
    Pandas dataframe with stats values.
"""
def stats_all(df,y_name,x_name,t_list):
    stats = []
    data = df[df[x_name].isin(t_list)]
    
    if data.size != 0:
        x = data[[x_name]]
        x = sm.add_constant(x)
        y = data[[y_name]]
        
        ## Run OLS
        model = sm.OLS(y,x)
        results = model.fit()
        
        ## Extract all values of interest
        ini = data[x_name].min()
        end = data[x_name].max()
        n = data[x_name].size
        b = results.params[0] #intercept
        m = results.params[1] #slope
        r2 = results.rsquared
        pval = results.f_pvalue
        fval = results.fvalue
        mean = data[y_name].mean()
        std = data[y_name].std()
        print(results.params[0])

        # Concatenate values
        concat = pd.concat([
                            pd.Series(ini), pd.Series(end),
                            pd.Series(n), pd.Series(mean),
                            pd.Series(std), pd.Series(b),
                            pd.Series(m), pd.Series(r2),
                            pd.Series(fval), pd.Series(pval)],
                           axis=1,join='outer')
            
        # Append to dataframe
        stats.append(concat)
    
    ## Get final output and rename columns
    output = pd.concat(stats).rename(columns={
        0:'ini', 1:'end', 2:'n', 3:'mean', 4:'std', 
        5:'intercept', 6:'slope', 7:'r2', 8:'F', 9:'p'}).reset_index(drop=True)
    return output


#### DETECT TIME SERIES TREND CHANGES ######
"""
Calculate location trend changes and plot

Usage:
    var = detect_changes(df,'Variable',[1991,1992,1993..])

Input variables: 
    time_series = Pandas dataframe with time series data.
    x_name = Independent variable.
    t_list = list of integers indicating time span of the data.
Output:
    Pandas dataframe with location of trend change.
    Plot
"""
def detect_changes(time_series,y_name,t_list):
    
    data = time_series[time_series['Year'].isin(t_list)][y_name]
    
    # Convert time series to a numpy array
    signal = data.values

    # Perform change point detection using the Pelt algorithm
    algo = rpt.Pelt(model="rbf", min_size=1, jump=5).fit(signal)
    result = algo.predict(pen=1)

    # remove location if equal to len(signal)
    change_points = [i for i in result if i < len(signal)]

    rpt.display(signal, result)
    plt.show()

    # Return the list of change point locations
    return change_points

def check_assumptions(df, y, x):
    # Ordinary Least Squares (OLS) regression
    constant = sm.add_constant(df[x])
    model = sm.OLS(df[y], constant).fit()
    
    # Residuals
    residuals = model.resid
    
    # Predicted values
    predictions = model.predict(constant)
    
    # Q-Q plot for normality check
    fig = sm.qqplot(residuals, line ='45', fit=True)
    plt.title ("Q-Q Plot of Residuals "+y)
    plt.show()
    
    # Shapiro-Wilk test for normality
    shapiro_test = scipy.stats.shapiro(residuals)
    print("Shapiro-Wilk Test:")
    print("Test statistic:", shapiro_test[0])
    print("p-value:", shapiro_test[1])
    
    # Interpretation
    if shapiro_test[1] < 0.05:
        print("Residuals are not normally distributed (Reject H0)")
    else:
        print("Residuals are normally distributed (Fail to reject H0)")
    
    ## Homocedasticity
    # Scatter plot for residuals (for visual inspection)
    plt.scatter(predictions, residuals)
    plt.title('Residuals vs Predicted Values')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.show()
    
    # The Breusch-Pagan test for heteroscedasticity
    bp_test = het_breuschpagan(residuals, constant)
    labels = ['Lagrange Multiplier statistic', 'p-value', 'f-value', 'f p-value']
    print(dict(zip(labels, bp_test)))
    
    # Interpretation
    if bp_test[1] < 0.05:
        print("Indication of heteroscedasticity (Reject H0)")
    else:
        print("No indication of heteroscedasticity (Fail to reject H0)")
    
    return shapiro_test