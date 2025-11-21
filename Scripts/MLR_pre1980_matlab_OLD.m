

% Import the data:
growth         = importdata('coral_growth.xlsx');
lum            = importdata('coral_lumn_yr.xlsx');
env            = importdata('env_yr.xlsx');

% Parse the dataset into working variables (PERIOD 1954-1980):
%% VAR2
den2        = growth.data(70:96,2);        % Density
ext2        = growth.data(70:96,3);        % Extension
cal2        = growth.data(70:96,4);        % Calcification
lum2        = lum.data(70:96,2);           % Luminescence 1980-1954
%% VAR3
den3        = growth.data(135:161,2);        % Density
ext3        = growth.data(135:161,3);        % Extension
cal3        = growth.data(135:161,4);        % Calcification
lum3        = lum.data(132:158,2);           % Luminescence
%% VAR4
den4        = growth.data(209:235,2);        % Density
ext4        = growth.data(209:235,3);        % Extension
cal4        = growth.data(209:235,4);        % Calcification
lum4        = lum.data(197:223,2);           % Luminescence
%% Environmental variables
envar       = env.data(36:62,3:5);   % ENV Variables (m3/s,°C,SOI,AMO)
envar_txt   = env.textdata(1,3:5);  % Variable LABELS

%% Mean values
den_mean = (den2+den3+den4)/4
ext_mean = (ext2+ext3+ext4)/4
cal_mean = (cal2+cal3+cal4)/4
lum_mean = (lum2+lum3+lum4)/4

%% Standardize biological data
% Standardize the predictors using z-Scores {[X - mean(X)]/std(X)}:
envarS       = (envar - repmat(mean(envar),size(envar,1),1)) ./ repmat(std(envar),size(envar,1),1);

% Center the response variable [Y - mean(Y)]:
% VAR2:
den2C        = (den2 - repmat(mean(den2),size(den2,1),1));
ext2C        = (ext2 - repmat(mean(ext2),size(ext2,1),1));
cal2C        = (cal2 - repmat(mean(cal2),size(cal2,1),1));
lum2C        = (lum2 - repmat(mean(lum2),size(lum2,1),1));

% VAR3:
den3C        = (den3 - repmat(mean(den3),size(den3,1),1));
ext3C        = (ext3 - repmat(mean(ext3),size(ext3,1),1));
cal3C        = (cal3 - repmat(mean(cal3),size(cal3,1),1));
lum3C        = (lum3 - repmat(mean(lum3),size(lum3,1),1));

% VAR4:
den4C        = (den4 - repmat(mean(den4),size(den4,1),1));
ext4C        = (ext4 - repmat(mean(ext4),size(ext4,1),1));
cal4C        = (cal4 - repmat(mean(cal4),size(cal4,1),1));
lum4C        = (lum4 - repmat(mean(lum4),size(lum4,1),1));

% Mean
denmC        = (den_mean - repmat(mean(den_mean),size(den_mean,1),1));
extmC        = (ext_mean - repmat(mean(ext_mean),size(ext_mean,1),1));
calmC        = (cal_mean - repmat(mean(cal_mean),size(cal_mean,1),1));
lummC        = (lum_mean - repmat(mean(lum_mean),size(lum_mean,1),1));
%% MULTIPLE REGRESSION ANALYSIS
% Perform multiple regression analysis using standardized and centered 
% variables:

% VAR 2:
MLR_den2  = bmt_MLR(envarS,den2C,1000,1) %Density
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.3573
       SSr: 0.0979
       SSe: 0.2595
       MSr: 0.0326
       MSe: 0.0113
         F: 2.8913
       p_F: 0.0430
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.2739
    R2adj1: 0.1791
%}
MLR_ext2  = bmt_MLR(envarS,ext2C,1000,0) %Extension
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.5926
       SSr: 0.1876
       SSe: 0.4050
       MSr: 0.0625
       MSe: 0.0176
         F: 3.5508
       p_F: 0.0350
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.3165
    R2adj1: 0.2274
%}
MLR_cal2  = bmt_MLR(envarS,cal2C,1000,0) %Calcification
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.9240
       SSr: 0.1118
       SSe: 0.8122
       MSr: 0.0373
       MSe: 0.0353
         F: 1.0556
       p_F: 0.4000
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1210
    R2adj1: 0.0064
%}
MLR_lum2  = bmt_MLR(envarS,lum2C,1000,0) %Luminescence
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.0071
       SSr: 0.0031
       SSe: 0.0040
       MSr: 0.0010
       MSe: 1.7256e-04
         F: 6.0708
       p_F: 0.0020
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.4419
    R2adj1: 0.3691
%}

% VAR 3:
MLR_den3  = bmt_MLR(envarS,den3C,1000,1) %Density
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.3369
       SSr: 0.1219
       SSe: 0.2150
       MSr: 0.0406
       MSe: 0.0093
         F: 4.3456
       p_F: 0.0160
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.3618
    R2adj1: 0.2785
%}
MLR_ext3  = bmt_MLR(envarS,ext3C,1000,0) %Extension
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.6928
       SSr: 0.1113
       SSe: 0.5815
       MSr: 0.0371
       MSe: 0.0253
         F: 1.4679
       p_F: 0.2220
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1607
    R2adj1: 0.0512
%}
MLR_cal3  = bmt_MLR(envarS,cal3C,1000,0) %Calcification
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.9731
       SSr: 0.2904
       SSe: 0.6827
       MSr: 0.0968
       MSe: 0.0297
         F: 3.2610
       p_F: 0.0320
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.2984
    R2adj1: 0.2069
%}
MLR_lum3  = bmt_MLR(envarS,lum3C,1000,0) %Luminescence
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.0087
       SSr: 0.0014
       SSe: 0.0073
       MSr: 4.7572e-04
       MSe: 3.1799e-04
         F: 1.4960
       p_F: 0.2410
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1633
    R2adj1: 0.0541
%}

% VAR 4:
MLR_den4  = bmt_MLR(envarS,den4C,1000,1) %Density
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.7408
       SSr: 0.0826
       SSe: 0.6581
       MSr: 0.0275
       MSe: 0.0286
         F: 0.9625
       p_F: 0.4320
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1115
    R2adj1: -0.0043
%}
MLR_ext4  = bmt_MLR(envarS,ext4C,1000,0) %Extension
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.9986
       SSr: 0.0913
       SSe: 0.9073
       MSr: 0.0304
       MSe: 0.0394
         F: 0.7716
       p_F: 0.5280
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.0914
    R2adj1: -0.0271
%}
MLR_cal4  = bmt_MLR(envarS,cal4C,1000,0) %Calcification
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.6297
       SSr: 0.0908
       SSe: 0.5389
       MSr: 0.0303
       MSe: 0.0234
         F: 1.2916
       p_F: 0.2900
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1442
    R2adj1: 0.0325
%}
MLR_lum4  = bmt_MLR(envarS,lum4C,1000,0) %Luminescence
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.0039
       SSr: 5.9246e-04
       SSe: 0.0033
       MSr: 1.9749e-04
       MSe: 1.4427e-04
         F: 1.3689
       p_F: 0.3050
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1515
    R2adj1: 0.0408
%}

% MEAN
MLR_denM  = bmt_MLR(envarS,denmC,1000,0) %Density
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.0776
       SSr: 0.0096
       SSe: 0.0680
       MSr: 0.0032
       MSe: 0.0030
         F: 1.0815
       p_F: 0.3800
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1236
    R2adj1: 0.0093
%}
MLR_extM  = bmt_MLR(envarS,extmC,1000,0) %Extension
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.1741
       SSr: 0.0606
       SSe: 0.1135
       MSr: 0.0202
       MSe: 0.0049
         F: 4.0907
       p_F: 0.0160
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.3479
    R2adj1: 0.2629
%}
MLR_calM  = bmt_MLR(envarS,calmC,1000,0) %Calcification
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.1230
       SSr: 0.0405
       SSe: 0.0825
       MSr: 0.0135
       MSe: 0.0036
         F: 3.7650
       p_F: 0.0200
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.3293
    R2adj1: 0.2419
%}
MLR_lumM  = bmt_MLR(envarS,lummC,1000,0) %Luminescence
%{
         b: [4×1 double]
      b_SE: [4×1 double]
       SSt: 0.0017
       SSr: 3.1413e-04
       SSe: 0.0014
       MSr: 1.0471e-04
       MSe: 6.1004e-05
         F: 1.7165
       p_F: 0.1990
         t: [4×1 double]
       p_t: [4×1 double]
        R2: 0.1829
    R2adj1: 0.0764
%}
%%
% Show regression coefficients, SE's, t-stats, and p-values using the
% 'table' command:

  
% VAR 2:
table(MLR_den2.b, MLR_den2.b_SE, MLR_den2.t, MLR_den2.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    DENSITY
        b           b_SE        tStat       pVal          Var     
    __________    ________    __________    _____    _____________

    2.5608e-16    0.020441    1.2528e-14    0.321    'Intercept'  
       0.02889    0.022536         1.282    0.201    'Temperature'
      0.022253    0.022638       0.98298    0.331    'SOI'        
     -0.053991    0.021094       -2.5595    0.017    'AMO'        
 %}
table(MLR_ext2.b, MLR_ext2.b_SE, MLR_ext2.t, MLR_ext2.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
         b           b_SE         tStat       pVal          Var     
    ___________    ________    ___________    _____    _____________

    -3.7051e-16    0.025538    -1.4508e-14     0.29    'Intercept'  
      -0.024884    0.028155       -0.88383    0.391    'Temperature'
       0.048688    0.028283         1.7215    0.114    'SOI'        
       0.068219    0.026354         2.5886    0.017    'AMO'        
 %}
table(MLR_cal2.b, MLR_cal2.b_SE, MLR_cal2.t, MLR_cal2.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b           b_SE        tStat       pVal          Var     
    __________    ________    __________    _____    _____________

    2.3588e-16    0.036164    6.5226e-15    0.618    'Intercept'  
     0.0089804     0.03987       0.22524    0.821    'Temperature'
      0.067247    0.040051         1.679    0.119    'SOI'        
    -0.0064111    0.037319      -0.17179    0.862    'AMO'        
 %}
table(MLR_lum2.b, MLR_lum2.b_SE, MLR_lum2.t, MLR_lum2.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
         b           b_SE          tStat       pVal          Var     
    ___________    _________    ___________    _____    _____________

    -1.8451e-16     0.002528    -7.2983e-14    0.185    'Intercept'  
     0.00075671    0.0027871        0.27151    0.815    'Temperature'
      0.0084345    0.0027997         3.0126    0.006    'SOI'        
      0.0085794    0.0026088         3.2887    0.004    'AMO'        
 %}

% VAR 3:
table(MLR_den3.b, MLR_den3.b_SE, MLR_den3.t, MLR_den3.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    DENSITY
         b           b_SE         tStat       pVal          Var     
    ___________    ________    ___________    _____    _____________

    -2.0796e-16    0.018607    -1.1176e-14      0.4    'Intercept'  
      -0.012315    0.020514       -0.60031    0.563    'Temperature'
      0.0007223    0.020607       0.035051    0.957    'SOI'        
       0.068779    0.019202          3.582    0.001    'AMO'        
 %}
table(MLR_ext3.b, MLR_ext3.b_SE, MLR_ext3.t, MLR_ext3.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
         b           b_SE         tStat       pVal          Var     
    ___________    ________    ___________    _____    _____________

    -7.0009e-17      0.0306    -2.2879e-15    0.834    'Intercept'  
      -0.006134    0.033735       -0.18183    0.841    'Temperature'
     -0.0036627    0.033889       -0.10808    0.914    'SOI'        
       0.065322    0.031577         2.0686    0.039    'AMO'        
 %}
table(MLR_cal3.b, MLR_cal3.b_SE, MLR_cal3.t, MLR_cal3.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
         b           b_SE         tStat       pVal          Var     
    ___________    ________    ___________    _____    _____________

    -3.0464e-16    0.033157    -9.1878e-15    0.486    'Intercept'  
      -0.012969    0.036555       -0.35478    0.726    'Temperature'
     -0.0031053    0.036721      -0.084567     0.93    'SOI'        
        0.10597    0.034216         3.0971    0.005    'AMO'        
 %}
table(MLR_lum3.b, MLR_lum3.b_SE, MLR_lum3.t, MLR_lum3.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
         b           b_SE          tStat       pVal          Var     
    ___________    _________    ___________    _____    _____________

    -3.0958e-17    0.0034318    -9.0208e-15    0.468    'Intercept'  
     -0.0024495    0.0037834       -0.64741    0.513    'Temperature'
    -0.00080064    0.0038006       -0.21066    0.839    'SOI'        
      0.0072085    0.0035414         2.0355    0.066    'AMO'        
 %}

% VAR 4:
table(MLR_den4.b, MLR_den4.b_SE, MLR_den4.t, MLR_den4.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    DENSITY
        b           b_SE        tStat       pVal          Var     
    __________    ________    __________    _____    _____________

    6.1392e-16    0.032554    1.8858e-14    0.145    'Intercept'  
      0.051284     0.03589        1.4289    0.179    'Temperature'
      0.046924    0.036053        1.3015    0.207    'SOI'        
     -0.011644    0.033594      -0.34661    0.743    'AMO'        
 %}
table(MLR_ext4.b, MLR_ext4.b_SE, MLR_ext4.t, MLR_ext4.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
         b           b_SE         tStat       pVal          Var     
    ___________    ________    ___________    _____    _____________

    -1.0248e-16    0.038223    -2.6812e-15     0.83    'Intercept'  
      -0.005332     0.04214       -0.12653    0.893    'Temperature'
     -0.0047791    0.042331        -0.1129     0.91    'SOI'        
       0.058886    0.039444         1.4929    0.152    'AMO'        
 %}
table(MLR_cal4.b, MLR_cal4.b_SE, MLR_cal4.t, MLR_cal4.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b           b_SE        tStat       pVal          Var     
    __________    ________    __________    _____    _____________

    4.2867e-16    0.029458    1.4552e-14    0.249    'Intercept'  
      0.044259    0.032476        1.3628    0.187    'Temperature'
      0.041856    0.032624         1.283    0.212    'SOI'        
      0.035547    0.030399        1.1694     0.24    'AMO'        
 %}
table(MLR_lum4.b, MLR_lum4.b_SE, MLR_lum4.t, MLR_lum4.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
         b           b_SE          tStat       pVal          Var     
    ___________    _________    ___________    _____    _____________

    -1.0167e-16    0.0023115    -4.3985e-14    0.222    'Intercept'  
     -0.0017502    0.0025484       -0.68678    0.505    'Temperature'
      0.0002236      0.00256       0.087346    0.924    'SOI'        
     -0.0041814    0.0023854        -1.7529    0.108    'AMO'        
 %}

% MEAN
table(MLR_denM.b, MLR_denM.b_SE, MLR_denM.t, MLR_denM.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    DENSITY
        b           b_SE        tStat       pVal          Var     
    __________    ________    __________    _____    _____________

    2.4724e-16    0.010465    2.3625e-14    0.099    'Intercept'  
      0.016965    0.011537        1.4704    0.166    'Temperature'
      0.017475     0.01159        1.5078    0.155    'SOI'        
    0.00078599    0.010799      0.072781    0.942    'AMO'        
    %}
table(MLR_extM.b, MLR_extM.b_SE, MLR_extM.t, MLR_extM.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
         b           b_SE         tStat       pVal          Var     
    ___________    ________    ___________    _____    _____________

    -2.4677e-16    0.013519    -1.8253e-14    0.254    'Intercept'  
     -0.0090876    0.014905       -0.60972    0.525    'Temperature'
       0.010062    0.014972        0.67201    0.487    'SOI'        
       0.048107    0.013951         3.4482    0.002    'AMO'        
  %}
table(MLR_calM.b, MLR_calM.b_SE, MLR_calM.t, MLR_calM.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b           b_SE        tStat       pVal          Var     
    __________    ________    __________    _____    _____________

    3.0997e-16    0.011525    2.6896e-14    0.178    'Intercept'  
      0.010068    0.012706       0.79238    0.436    'Temperature'
      0.026499    0.012763        2.0762    0.044    'SOI'        
      0.033777    0.011893        2.8401    0.007    'AMO'        
    %}
table(MLR_lumM.b, MLR_lumM.b_SE, MLR_lumM.t, MLR_lumM.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
         b           b_SE         tStat       pVal          Var     
    ___________    _________    __________    _____    _____________

     1.9622e-16    0.0015031    1.3054e-13    0.461    'Intercept'  
    -0.00086073    0.0016572       -0.5194    0.598    'Temperature'
      0.0019644    0.0016647          1.18    0.256    'SOI'        
      0.0029016    0.0015512        1.8706    0.083    'AMO'        
   %}
    
%%
% AIC MODEL SELECTION
    
% Examine the results of the Marginal Tests based on AIC to get an initial
% ranking of variables:
[mod_den,marg_den]    = bmt_MLR_AIC(envarS,denmC,1,2,envar_txt);
%{
Conditional Tests skipped: No variable is better than a null model!
%}
[mod_ext,marg_ext]    = bmt_MLR_AIC(envarS,extmC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    'RSS'       'R2'        'R2adj'      'AIC'          'delta'     'wts'       'ratio'       'var'        
    [0.1199]    [0.3111]    [ 0.2835]    [-141.7534]    [     0]    [0.9657]    [       1]    'AMO'        
    [0.1741]    [   NaN]    [    NaN]    [-134.0327]    [7.7207]    [0.0203]    [ 47.4818]    'none'       
    [0.1726]    [0.0085]    [-0.0311]    [-131.9238]    [9.8296]    [0.0071]    [136.2895]    'Temperature'
    [0.1730]    [0.0063]    [-0.0335]    [-131.8630]    [9.8904]    [0.0069]    [140.5003]    'SOI'        

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    'RSS'       'R2'        'R2adj'     'AIC'          'wts'       'deltaN'    'var'     'idx'
    [0.1199]    [0.3111]    [0.2835]    [-141.7534]    [0.9657]    [7.7207]    'AMO'     [  3]
    [0.1199]    [   NaN]    [   NaN]    [-141.7534]    [0.5133]    [     0]    'none'       []

--------------------------------------------------

RSS    = residual sum-of-squares 
R2     = fraction of total variance explained 
R2adj  = fraction of adjusted total variance explained 
deltaN = delta associated with NO variable addition 
wts    = AIC weights 
var    = variable labels 
idx    = index to selected variables 

(Note: RSS, R2, and R2adj in Conditional tests are CUMULATIVE) 
%}
[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calmC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    'RSS'       'R2'        'R2adj'      'AIC'          'delta'     'wts'       'ratio'      'var'        
    [0.0979]    [0.2036]    [ 0.1718]    [-147.2189]    [     0]    [0.7605]    [      1]    'AMO'        
    [0.1230]    [   NaN]    [    NaN]    [-143.4116]    [3.8074]    [0.1133]    [ 6.7105]    'none'       
    [0.1148]    [0.0669]    [ 0.0295]    [-142.9398]    [4.2791]    [0.0895]    [ 8.4958]    'SOI'        
    [0.1226]    [0.0031]    [-0.0368]    [-141.1545]    [6.0644]    [0.0367]    [20.7425]    'Temperature'

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    'RSS'       'R2'        'R2adj'     'AIC'          'wts'       'deltaN'    'var'     'idx'
    [0.0979]    [0.2036]    [0.1718]    [-147.2189]    [0.7605]    [3.8074]    'AMO'     [  3]
    [0.0979]    [   NaN]    [   NaN]    [-147.2189]    [0.2931]    [1.3685]    'none'       []

--------------------------------------------------

RSS    = residual sum-of-squares 
R2     = fraction of total variance explained 
R2adj  = fraction of adjusted total variance explained 
deltaN = delta associated with NO variable addition 
wts    = AIC weights 
var    = variable labels 
idx    = index to selected variables 

(Note: RSS, R2, and R2adj in Conditional tests are CUMULATIVE) 
%}
[mod_lum,marg_lum]    = bmt_MLR_AIC(envarS,lummC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    'RSS'       'R2'        'R2adj'      'AIC'          'delta'     'wts'       'ratio'     'var'        
    [0.0016]    [0.0962]    [ 0.0600]    [-259.1278]    [     0]    [0.3687]    [     1]    'AMO'        
    [0.0017]    [   NaN]    [    NaN]    [-258.7377]    [0.3901]    [0.3034]    [1.2154]    'none'       
    [0.0016]    [0.0528]    [ 0.0149]    [-257.8612]    [1.2665]    [0.1957]    [1.8838]    'SOI'        
    [0.0017]    [0.0248]    [-0.0142]    [-257.0765]    [2.0513]    [0.1322]    [2.7889]    'Temperature'

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    'RSS'       'R2'        'R2adj'     'AIC'          'wts'       'deltaN'    'var'     'idx'
    [0.0016]    [0.0962]    [0.0600]    [-259.1278]    [0.3687]    [0.3901]    'AMO'     [  3]
    [0.0016]    [   NaN]    [   NaN]    [-259.1278]    [0.3074]    [     0]    'none'       []

--------------------------------------------------

RSS    = residual sum-of-squares 
R2     = fraction of total variance explained 
R2adj  = fraction of adjusted total variance explained 
deltaN = delta associated with NO variable addition 
wts    = AIC weights 
var    = variable labels 
idx    = index to selected variables 

(Note: RSS, R2, and R2adj in Conditional tests are CUMULATIVE) 
%}
