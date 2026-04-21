% 1954-1982
% Import the data:
growth         = importdata('coral_growth_yr.xlsx');
lumin          = importdata('coral_lumn_yr.xlsx');
env            = importdata('env_yr.xlsx');

% Parse the dataset into working variables (PERIOD 1954-2015):
%% Coral Growth Means
den        = growth.data(34:62,2);        % Density
ext        = growth.data(34:62,3);        % Extension
cal        = growth.data(34:62,4);        % Calcification
lum        = lumin.data(34:62,2);         % Luminescence

%% Environmental variables (Select only those with data available for 1954-1982)
envar       = env.data(34:62,[3,4,6]);   % ENV Variables (m3/s,°C,SOI,AMO) - SOI and AMO are added below
envar_txt   = env.textdata(1,[3,4,6,7,8]);  % Variable LABELS

%% Standardize biological data
% Standardize the predictors using z-Scores {[X - mean(X)]/std(X)}:
envarS       = (envar - repmat(mean(envar),size(envar,1),1)) ./ repmat(std(envar),size(envar,1),1);
% Append the SOI and AMO data, which were already an index
envarS = [envarS, env.data(34:62,7:8)];

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
R2    = 0.18243      
R2adj = 0.00470      
F     = 1.02643      
p     = 0.43100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.02356      -1.11567      0.18800       
            1 -0.01837      -0.95520      0.34100       
            2 0.01769       1.13550       0.27100       
            3 0.01338       0.60846       0.56200       
            4 0.06726       1.96127       0.06200       
            5 -0.07188      -0.59875      0.55500       
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
R2    = 0.39565      
R2adj = 0.26428      
F     = 3.01154      
p     = 0.02800      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.05329       1.81147       0.02800       
            1 0.02630       0.98175       0.34800       
            2 0.00683       0.31463       0.77500       
            3 -0.04237      -1.38334      0.18500       
            4 -0.00466      -0.09754      0.92400       
            5 0.56526       3.37973       0.00100       
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
R2    = 0.36531      
R2adj = 0.22734      
F     = 2.64769      
p     = 0.05100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.01370       0.52649       0.53200       
            1 0.00280       0.11836       0.91800       
            2 0.02254       1.17420       0.26600       
            3 -0.01718      -0.63425      0.58600       
            4 0.06449       1.52624       0.17500       
            5 0.32466       2.19475       0.04300       
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
R2    = 0.21857      
R2adj = 0.04869      
F     = 1.28662      
p     = 0.27300      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00286       0.89273       0.25300       
            1 0.00370       1.27003       0.21800       
            2 -0.00057      -0.24252      0.80700       
            3 -0.00116      -0.34815      0.73700       
            4 0.00011       0.02143       0.97900       
            5 0.03128       1.71980       0.10000       
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
        b          b_SE       tStat      pVal             Var        
    _________    ________    ________    _____    ___________________

    -0.023559    0.021116     -1.1157    0.188    {'Intercept'      }
     -0.01837    0.019232     -0.9552    0.341    {'WF_Calamar'     }
     0.017694    0.015583      1.1355    0.271    {'Air_Temperature'}
     0.013377    0.021984     0.60846    0.562    {'HadISST'        }
     0.067261    0.034295      1.9613    0.062    {'SOI'            }
    -0.071885     0.12006    -0.59875    0.555    {'AMO'            }

 %}

%Extension
table(MLR_ext.b, MLR_ext.b_SE, MLR_ext.t, MLR_ext.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
        b           b_SE        tStat      pVal             Var        
    __________    ________    _________    _____    ___________________

      0.053288    0.029417       1.8115    0.028    {'Intercept'      }
      0.026303    0.026792      0.98175    0.348    {'WF_Calamar'     }
       0.00683    0.021708      0.31463    0.775    {'Air_Temperature'}
     -0.042366    0.030626      -1.3833    0.185    {'HadISST'        }
    -0.0046599    0.047776    -0.097537    0.924    {'SOI'            }
       0.56526     0.16725       3.3797    0.001    {'AMO'            }
 %}

%Calcification
table(MLR_cal.b, MLR_cal.b_SE, MLR_cal.t, MLR_cal.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b          b_SE       tStat      pVal             Var        
    _________    ________    ________    _____    ___________________

     0.013698    0.026018     0.52649    0.532    {'Intercept'      }
    0.0028046    0.023696     0.11836    0.918    {'WF_Calamar'     }
     0.022545      0.0192      1.1742    0.266    {'Air_Temperature'}
     -0.01718    0.027087    -0.63425    0.586    {'HadISST'        }
     0.064492    0.042256      1.5262    0.175    {'SOI'            }
      0.32466     0.14793      2.1947    0.043    {'AMO'            }
 %}

%Luminescence
table(MLR_lum.b, MLR_lum.b_SE, MLR_lum.t, MLR_lum.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
         b           b_SE        tStat      pVal             Var        
    ___________    _________    ________    _____    ___________________

      0.0028557    0.0031989     0.89273    0.253    {'Intercept'      }
      0.0037001    0.0029134        1.27    0.218    {'WF_Calamar'     }
    -0.00057249    0.0023606    -0.24252    0.807    {'Air_Temperature'}
     -0.0011595    0.0033303    -0.34815    0.737    {'HadISST'        }
     0.00011134    0.0051953    0.021432    0.979    {'SOI'            }
       0.031279     0.018187      1.7198      0.1    {'AMO'            }
 %}

    
%% AIC MODEL SELECTION
    
% Examine the results of the Marginal Tests based on AIC to get an initial
% ranking of variables:

[mod_den,marg_den]    = bmt_MLR_AIC(envarS,denC,1,2,envar_txt);
%{
Conditional Tests skipped: No variable is better than a null model!
%}

[mod_ext,marg_ext]    = bmt_MLR_AIC(envarS,extC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
  Columns 1 through 7

    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'   }
    {[0.2639]}    {[    0.2914]}    {[ 0.2651]}    {[-131.8191]}    {[     0]}    {[0.9473]}    {[       1]}
    {[0.3725]}    {[       NaN]}    {[    NaN]}    {[-124.1434]}    {[7.6757]}    {[0.0204]}    {[ 46.4264]}
    {[0.3613]}    {[    0.0300]}    {[-0.0059]}    {[-122.7137]}    {[9.1054]}    {[0.0100]}    {[ 94.8900]}
    {[0.3632]}    {[    0.0250]}    {[-0.0111]}    {[-122.5643]}    {[9.2549]}    {[0.0093]}    {[102.2523]}
    {[0.3719]}    {[    0.0016]}    {[-0.0353]}    {[-121.8773]}    {[9.9418]}    {[0.0066]}    {[144.1573]}
    {[0.3724]}    {[2.8592e-04]}    {[-0.0367]}    {[-121.8383]}    {[9.9808]}    {[0.0064]}    {[146.9977]}

  Column 8

    {'var'            }
    {'AMO'            }
    {'none'           }
    {'HadISST'        }
    {'SOI'            }
    {'Air_Temperature'}
    {'WF_Calamar'     }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.2639]}    {[0.2914]}    {[0.2651]}    {[-131.8191]}    {[0.9473]}    {[7.6757]}    {'AMO' }    {[       5]}
    {[0.2639]}    {[   NaN]}    {[   NaN]}    {[-131.8191]}    {[0.2525]}    {[0.3054]}    {'none'}    {0×0 double}

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

[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'  }    {'var'            }
    {[0.2233]}    {[0.1953]}    {[ 0.1655]}    {[-136.6743]}    {[     0]}    {[0.6592]}    {[      1]}    {'AMO'            }
    {[0.2479]}    {[0.1066]}    {[ 0.0735]}    {[-133.6404]}    {[3.0339]}    {[0.1446]}    {[ 4.5583]}    {'SOI'            }
    {[0.2774]}    {[   NaN]}    {[    NaN]}    {[-132.6849]}    {[3.9894]}    {[0.0897]}    {[ 7.3499]}    {'none'           }
    {[0.2690]}    {[0.0304]}    {[-0.0055]}    {[-131.2670]}    {[5.4073]}    {[0.0441]}    {[14.9344]}    {'HadISST'        }
    {[0.2748]}    {[0.0096]}    {[-0.0271]}    {[-130.6498]}    {[6.0245]}    {[0.0324]}    {[20.3327]}    {'Air_Temperature'}
    {[0.2763]}    {[0.0041]}    {[-0.0328]}    {[-130.4904]}    {[6.1839]}    {[0.0299]}    {[22.0199]}    {'WF_Calamar'     }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.2233]}    {[0.1953]}    {[0.1655]}    {[-136.6743]}    {[0.6592]}    {[3.9894]}    {'AMO' }    {[       5]}
    {[0.1869]}    {[0.3264]}    {[0.2746]}    {[-139.3312]}    {[0.5871]}    {[2.6569]}    {'SOI' }    {[       4]}
    {[0.1869]}    {[   NaN]}    {[   NaN]}    {[-139.3312]}    {[0.5005]}    {[     0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_lum,marg_lum]    = bmt_MLR_AIC(envarS,lumC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio' }    {'var'            }
    {[0.0031]}    {[0.0923]}    {[ 0.0587]}    {[-260.7789]}    {[     0]}    {[0.2941]}    {[     1]}    {'AMO'            }
    {[0.0034]}    {[   NaN]}    {[    NaN]}    {[-260.2845]}    {[0.4944]}    {[0.2297]}    {[1.2804]}    {'none'           }
    {[0.0032]}    {[0.0531]}    {[ 0.0181]}    {[-259.5544]}    {[1.2245]}    {[0.1594]}    {[1.8446]}    {'SOI'            }
    {[0.0032]}    {[0.0460]}    {[ 0.0107]}    {[-259.3369]}    {[1.4420]}    {[0.1430]}    {[2.0565]}    {'WF_Calamar'     }
    {[0.0034]}    {[0.0140]}    {[-0.0225]}    {[-258.3808]}    {[2.3981]}    {[0.0887]}    {[3.3170]}    {'Air_Temperature'}
    {[0.0034]}    {[0.0112]}    {[-0.0255]}    {[-258.2970]}    {[2.4819]}    {[0.0850]}    {[3.4590]}    {'HadISST'        }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.0031]}    {[0.0923]}    {[0.0587]}    {[-260.7789]}    {[0.2941]}    {[0.4944]}    {'AMO' }    {[       5]}
    {[0.0031]}    {[   NaN]}    {[   NaN]}    {[-260.7789]}    {[0.1843]}    {[1.3840]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

%% REPEAT MLR OVER BEST VARIABLES
% Perform multiple regression analysis using standardized and centered 
% variables:

% Density:
model_den   = bmt_MLR(envarS(:,mod_den.idx),denC,1000,0,1,0);
%{
NONE
%}

%Extension
model_ext  = bmt_MLR(envarS(:,mod_ext.idx),extC,1000,0,1,0);
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.29139      
R2adj = 0.26515      
F     = 11.10287     
p     = 0.00300      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.03291       1.57853       0.00300       
            1 0.35695       3.33210       0.00300       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Calcification
model_cal  = bmt_MLR(envarS(:,mod_cal.idx),calC,1000,0,1,0);
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.32639      
R2adj = 0.27458      
F     = 6.29905      
p     = 0.00500      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00871       0.45812       0.42300       
            1 0.26837       2.91266       0.01100       
            2 0.06369       2.24907       0.03100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Luminescence
model_lum  = bmt_MLR(envarS(:,mod_lum.idx),lumC,1000,0,1,0);
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.09228      
R2adj = 0.05866      
F     = 2.74487      
p     = 0.12100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00177       0.78487       0.12100       
            1 0.01921       1.65676       0.12100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%% SHOW BEST VARIABLES

mod_den.var'
%{
    {'none'}
%}

mod_ext.var'
%{
    {'AMO' }
    {'none'}
%}

mod_cal.var'
%{
    {'AMO' }
    {'SOI' }
    {'none'}
%}

mod_lum.var'
%{
    {'AMO' }
    {'none'}
%}