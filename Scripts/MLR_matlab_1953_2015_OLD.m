% 1954-2015
% Import the data:
growth         = importdata('coral_growth_yr.xlsx');
lumin          = importdata('coral_lumn_yr.xlsx');
env            = importdata('env_yr.xlsx');

% Parse the dataset into working variables (PERIOD 1954-2015):
%% Coral Growth Means
den        = growth.data(1:62,2);        % Density
ext        = growth.data(1:62,3);        % Extension
cal        = growth.data(1:62,4);        % Calcification
lum        = lumin.data(1:62,2);         % Luminescence

%% Environmental variables (Select only those with data available for 1954-2015)
envar       = env.data(1:62,[3,4,6]);   % ENV Variables (m3/s,°C,SOI,AMO) - SOI and AMO are added below
envar_txt   = env.textdata(1,[3,4,6,7,8]);  % Variable LABELS

%% Standardize biological data
% Standardize the predictors using z-Scores {[X - mean(X)]/std(X)}:
envarS       = (envar - repmat(mean(envar),size(envar,1),1)) ./ repmat(std(envar),size(envar,1),1);
% Append the SOI and AMO data, which were already an index
envarS = [envarS, env.data(1:62,7:8)];

% Center the response variable [Y - mean(Y)]:
denC        = (den - repmat(mean(den),size(den,1),1));
extC        = (ext - repmat(mean(ext),size(ext,1),1));
calC        = (cal - repmat(mean(cal),size(cal,1),1));
lumC        = (lum - repmat(mean(lum),size(lum,1),1));

%% MULTIPLE REGRESSION ANALYSIS
% Perform multiple regression analysis using standardized and centered 
% variables:

% Density:
MLR_den  = bmt_MLR(envarS,denC,1000,0)
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.16441      
R2adj = 0.08980      
F     = 2.20370      
p     = 0.07000      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.01135      -1.16636      0.01700       
            1 -0.01088      -0.81773      0.44100       
            2 0.00901       0.77498       0.44100       
            3 0.01478       0.81820       0.41600       
            4 0.04654       2.07668       0.05000       
            5 -0.20117      -2.31709      0.02100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Extension
MLR_ext  = bmt_MLR(envarS,extC,1000,0)
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.19765      
R2adj = 0.12601      
F     = 2.75895      
p     = 0.02300      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00591       0.34147       0.46700       
            1 -0.00510      -0.21533      0.82000       
            2 -0.00522      -0.25236      0.79000       
            3 -0.01132      -0.35209      0.74600       
            4 0.01478       0.37063       0.69300       
            5 0.35502       2.29868       0.02900       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Calcification
MLR_cal  = bmt_MLR(envarS,calC,1000,0) 
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.08613      
R2adj = 0.00454      
F     = 1.05562      
p     = 0.41500      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00784      -0.56232      0.20800       
            1 -0.01506      -0.79016      0.44100       
            2 0.00473       0.28400       0.77900       
            3 -0.00003      -0.00120      0.99900       
            4 0.05952       1.85421       0.05600       
            5 0.03671       0.29522       0.76100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Luminescence
MLR_lum  = bmt_MLR(envarS,lumC,1000,0) 
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.25772      
R2adj = 0.21933      
F     = 6.71266      
p     = 0.00200      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       0.98700       
            1 -0.00619      -2.84072      0.00600       
            2 0.00127       0.62802       0.51700       
            3 -0.00334      -1.62536      0.10900       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}


%% Tables
% Show regression coefficients, SE's, t-stats, and p-values using the
% 'table' command:

  
% Density:
table(MLR_den.b, MLR_den.b_SE, MLR_den.t, MLR_den.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    DENSITY
         b           b_SE          tStat       pVal           Var      
    ___________    _________    ___________    _____    _______________

    -9.7946e-18    0.0085834    -1.1411e-15    0.926    {'Intercept'  }
       0.014338     0.010026         1.4301    0.162    {'Temperature'}
       0.019263      0.00933         2.0647    0.043    {'SOI'        }
      -0.026212    0.0094704        -2.7677    0.008    {'AMO'        }    
 %}

%Extension
table(MLR_ext.b, MLR_ext.b_SE, MLR_ext.t, MLR_ext.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
         b           b_SE         tStat       pVal           Var      
    ___________    ________    ___________    _____    _______________

    -4.6828e-17    0.015168    -3.0872e-15    0.268    {'Intercept'  }
      -0.007898    0.017717       -0.44578    0.662    {'Temperature'}
      0.0066032    0.016488        0.40049    0.685    {'SOI'        }
       0.058607    0.016736         3.5018    0.001    {'AMO'        }
 %}

%Calcification
table(MLR_cal.b, MLR_cal.b_SE, MLR_cal.t, MLR_cal.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b          b_SE        tStat       pVal           Var      
    _________    ________    __________    _____    _______________

    6.702e-17    0.012263    5.4651e-15    0.318    {'Intercept'  }
    0.0062918    0.014324       0.43925    0.649    {'Temperature'}
      0.02575     0.01333        1.9317    0.054    {'SOI'        }
    0.0080704    0.013531       0.59646    0.552    {'AMO'        }
 %}

%Luminescence
table(MLR_lum.b, MLR_lum.b_SE, MLR_lum.t, MLR_lum.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
        b           b_SE         tStat       pVal           Var      
    __________    _________    __________    _____    _______________

    4.1803e-18    0.0018641    2.2425e-15    0.987    {'Intercept'  }
    -0.0061852    0.0021773       -2.8407    0.006    {'Temperature'}
     0.0012725    0.0020262       0.62802    0.517    {'SOI'        }
    -0.0033429    0.0020567       -1.6254    0.109    {'AMO'        }
 %}

    
%% AIC MODEL SELECTION
    
% Examine the results of the Marginal Tests based on AIC to get an initial
% ranking of variables:

[mod_den,marg_den]    = bmt_MLR_AIC(envarS,denC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'  }    {'var'        }
    {[0.2867]}    {[    0.0795]}    {[ 0.0641]}    {[-329.1303]}    {[     0]}    {[0.6510]}    {[      1]}    {'AMO'        }
    {[0.3004]}    {[    0.0354]}    {[ 0.0194]}    {[-326.2324]}    {[2.8980]}    {[0.1529]}    {[ 4.2587]}    {'SOI'        }
    {[0.3115]}    {[       NaN]}    {[    NaN]}    {[-326.1321]}    {[2.9982]}    {[0.1454]}    {[ 4.4777]}    {'none'       }
    {[0.3113]}    {[5.4874e-04]}    {[-0.0161]}    {[-324.0294]}    {[5.1009]}    {[0.0508]}    {[12.8129]}    {'Temperature'}

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.2867]}    {[0.0795]}    {[0.0641]}    {[-329.1303]}    {[0.6510]}    {[2.9982]}    {'AMO' }    {[       3]}
    {[0.2867]}    {[   NaN]}    {[   NaN]}    {[-329.1303]}    {[0.3377]}    {[0.5429]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_ext,marg_ext]    = bmt_MLR_AIC(envarS,extC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta'  }    {'wts'   }    {'ratio'   }    {'var'        }
    {[0.8355]}    {[0.1861]}    {[ 0.1726]}    {[-262.8214]}    {[      0]}    {[0.9909]}    {[       1]}    {'AMO'        }
    {[1.0266]}    {[   NaN]}    {[    NaN]}    {[-252.1879]}    {[10.6335]}    {[0.0049]}    {[203.7168]}    {'none'       }
    {[1.0184]}    {[0.0080]}    {[-0.0085]}    {[-250.5500]}    {[12.2714]}    {[0.0021]}    {[462.0512]}    {'SOI'        }
    {[1.0186]}    {[0.0078]}    {[-0.0087]}    {[-250.5393]}    {[12.2821]}    {[0.0021]}    {[464.5433]}    {'Temperature'}

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var' }    {'idx'     }
    {[0.8355]}    {[0.1861]}    {[0.1726]}    {[-262.8214]}    {[0.9909]}    {[10.6335]}    {'AMO' }    {[       3]}
    {[0.8355]}    {[   NaN]}    {[   NaN]}    {[-262.8214]}    {[0.5494]}    {[      0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio' }    {'var'        }
    {[0.5493]}    {[    0.0601]}    {[ 0.0445]}    {[-288.8276]}    {[     0]}    {[0.5567]}    {[     1]}    {'SOI'        }
    {[0.5844]}    {[       NaN]}    {[    NaN]}    {[-287.1196]}    {[1.7080]}    {[0.2370]}    {[2.3490]}    {'none'       }
    {[0.5764]}    {[    0.0137]}    {[-0.0028]}    {[-285.8357]}    {[2.9919]}    {[0.1247]}    {[4.4635]}    {'AMO'        }
    {[0.5844]}    {[5.9121e-05]}    {[-0.0166]}    {[-284.9865]}    {[3.8410]}    {[0.0816]}    {[6.8244]}    {'Temperature'}

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.5493]}    {[0.0601]}    {[0.0445]}    {[-288.8276]}    {[0.5567]}    {[1.7080]}    {'SOI' }    {[       2]}
    {[0.5493]}    {[   NaN]}    {[   NaN]}    {[-288.8276]}    {[0.4249]}    {[     0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_lum,marg_lum]    = bmt_MLR_AIC(envarS,lumC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'delta'  }    {'wts'   }    {'ratio'   }    {'var'        }
    {[0.0131]}    {[0.2225]}    {[0.2095]}    {[-520.5120]}    {[      0]}    {[0.9814]}    {[       1]}    {'Temperature'}
    {[0.0149]}    {[0.1123]}    {[0.0975]}    {[-512.2943]}    {[ 8.2177]}    {[0.0161]}    {[ 60.8773]}    {'AMO'        }
    {[0.0162]}    {[0.0366]}    {[0.0206]}    {[-507.2225]}    {[13.2895]}    {[0.0013]}    {[768.7329]}    {'SOI'        }
    {[0.0168]}    {[   NaN]}    {[   NaN]}    {[-507.0453]}    {[13.4667]}    {[0.0012]}    {[839.9580]}    {'none'       }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var'        }    {'idx'     }
    {[0.0131]}    {[0.2225]}    {[0.2095]}    {[-520.5120]}    {[0.9814]}    {[13.4667]}    {'Temperature'}    {[       1]}
    {[0.0131]}    {[   NaN]}    {[   NaN]}    {[-520.5120]}    {[0.4030]}    {[ 0.2440]}    {'none'       }    {0×0 double}

--------------------------------------------------
%}

%% REPEAT MLR OVER BEST VARIABLES
% Perform multiple regression analysis using standardized and centered 
% variables:

% Density:
model_den   = bmt_MLR(envarS(:,mod_den.idx),denC,1000,0,1,0);
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.07948      
R2adj = 0.06414      
F     = 5.18087      
p     = 0.02500      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00000      -0.00000      0.66500       
            1 -0.02015      -2.27615      0.02500       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Extension
model_ext  = bmt_MLR(envarS(:,mod_ext.idx),extC,1000,0,1,0);
%{
=====================================================================
model_ext  = bmt_MLR(envarS(:,mod_ext.idx),extC,1000,0,1,0);
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.18614      
R2adj = 0.17258      
F     = 13.72303     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00000      -0.00000      0.00200       
            1 0.05597       3.70446       0.00100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Calcification
model_cal  = bmt_MLR(envarS(:,mod_cal.idx),calC,1000,0,1,0);
%{
=====================================================================
model_cal  = bmt_MLR(envarS(:,mod_cal.idx),calC,1000,0,1,0);
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.06013      
R2adj = 0.04446      
F     = 3.83845      
p     = 0.06900      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       0.03800       
            1 0.02400       1.95920       0.06900       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Luminescence
model_lum  = bmt_MLR(envarS(:,mod_lum.idx),lumC,1000,0,1,0);
%{
=====================================================================
model_lum  = bmt_MLR(envarS(:,mod_lum.idx),lumC,1000,0,1,0);
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.22250      
R2adj = 0.20954      
F     = 17.17015     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       1.00000       
            1 -0.00784      -4.14369      0.00100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%% SHOW BEST VARIABLES

mod_den.var'
%{
    {'AMO' }
    {'none'}
%}

mod_ext.var'
%{
    {'AMO' }
    {'none'}
%}

mod_cal.var'
%{
    {'SOI' }
    {'none'}
%}

mod_lum.var'
%{
    {'Temperature' }
    {'none'}
%}