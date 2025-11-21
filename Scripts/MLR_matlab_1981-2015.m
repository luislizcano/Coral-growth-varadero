% 1981-2015


% Import the data:
growth         = importdata('coral_growth_yr.xlsx');
lumin          = importdata('coral_lumn_yr.xlsx');
env            = importdata('env_yr.xlsx');

% Parse the dataset into working variables (PERIOD 1982-2015):

%% Coral Growth Means
den        = growth.data(1:35,2);        % Density
ext        = growth.data(1:35,3);        % Extension
cal        = growth.data(1:35,4);        % Calcification
lum        = lumin.data(1:35,2);         % Luminescence

%% Environmental variables
envar       = env.data(1:35,2:5);   % ENV Variables (m3/s,°C,SOI,AMO)
envar_txt   = env.textdata(1,2:5);  % Variable LABELS


%% Standardize biological data
% Standardize the predictors using z-Scores {[X - mean(X)]/std(X)}:
envarS       = (envar - repmat(mean(envar),size(envar,1),1)) ./ repmat(std(envar),size(envar,1),1);

% Center the response variable [Y - mean(Y)]:
% Mean
denC        = (den - repmat(mean(den),size(den,1),1)) ./ repmat(std(den),size(den,1),1);
extC        = (ext - repmat(mean(ext),size(ext,1),1)) ./ repmat(std(ext),size(ext,1),1);
calC        = (cal - repmat(mean(cal),size(cal,1),1)) ./ repmat(std(cal),size(cal,1),1);
lumC        = (lum - repmat(mean(lum),size(lum,1),1)) ./ repmat(std(lum),size(lum,1),1);

%% MULTIPLE REGRESSION ANALYSIS
% Perform multiple regression analysis using standardized and centered 
% variables:

% Density:
MLR_den  = bmt_MLR(envarS,denC,1000,0)
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.14607      
R2adj = 0.03221      
F     = 1.28293      
p     = 0.28700      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       0.12700       
            1 0.17418       0.61126       0.55800       
            2 0.30203       1.13437       0.26700       
            3 0.11217       0.44484       0.65400       
            4 -0.59599      -2.10748      0.04800       
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
R2    = 0.09973      
R2adj = -0.02031     
F     = 0.83080      
p     = 0.52000      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       0.88300       
            1 0.03087       0.10550       0.91000       
            2 0.15643       0.57219       0.59300       
            3 0.20325       0.78498       0.44600       
            4 0.10073       0.34690       0.74300       
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
R2    = 0.08075      
R2adj = -0.04181     
F     = 0.65886      
p     = 0.63500      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       0.91900       
            1 0.03763       0.12729       0.90500       
            2 0.26546       0.96095       0.35600       
            3 0.33044       1.26300       0.22600       
            4 -0.29203      -0.99528      0.32700       
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
R2    = 0.47629      
R2adj = 0.40647      
F     = 6.82100      
p     = 0.00200      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00000      -0.00000      0.27800       
            1 -0.01165      -0.05221      0.96300       
            2 -0.60952      -2.92322      0.00500       
            3 -0.04549      -0.23037      0.79800       
            4 -0.13793      -0.62279      0.52100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}


%%
% Show regression coefficients, SE's, t-stats, and p-values using the
% 'table' command:

% Density:
table(MLR_den.b, MLR_den.b_SE, MLR_den.t, MLR_den.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    DENSITY
        b          b_SE        tStat      pVal           Var      
    __________    _______    _________    _____    _______________

    4.3867e-15    0.16629    2.638e-14    0.127    {'Intercept'  }
       0.17418    0.28495      0.61126    0.558    {'WaterFlow'  }
       0.30203    0.26625       1.1344    0.267    {'Temperature'}
       0.11217    0.25217      0.44484    0.654    {'SOI'        }
      -0.59599     0.2828      -2.1075    0.048    {'AMO'        }  
 %}

%Extension
table(MLR_ext.b, MLR_ext.b_SE, MLR_ext.t, MLR_ext.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
        b          b_SE        tStat      pVal           Var      
    __________    _______    _________    _____    _______________

    3.4677e-16    0.17074    2.031e-15    0.883    {'Intercept'  }
      0.030866    0.29258       0.1055     0.91    {'WaterFlow'  }
       0.15643    0.27338      0.57219    0.593    {'Temperature'}
       0.20325    0.25892      0.78498    0.446    {'SOI'        }
       0.10073    0.29037       0.3469    0.743    {'AMO'        }
 %}

%Calcification
table(MLR_cal.b, MLR_cal.b_SE, MLR_cal.t, MLR_cal.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b          b_SE        tStat      pVal           Var      
    __________    _______    _________    _____    _______________

    3.0296e-16    0.17253    1.756e-15    0.919    {'Intercept'  }
      0.037632    0.29564      0.12729    0.905    {'WaterFlow'  }
       0.26546    0.27625      0.96095    0.356    {'Temperature'}
       0.33044    0.26163        1.263    0.226    {'SOI'        }
      -0.29203    0.29341     -0.99528    0.327    {'AMO'        }
 %}

%Luminescence
table(MLR_lum.b, MLR_lum.b_SE, MLR_lum.t, MLR_lum.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
         b          b_SE         tStat       pVal           Var      
    ___________    _______    ___________    _____    _______________

    -2.4789e-15    0.13022    -1.9036e-14    0.278    {'Intercept'  }
      -0.011651    0.22315      -0.052211    0.963    {'WaterFlow'  }
       -0.60952    0.20851        -2.9232    0.005    {'Temperature'}
      -0.045494    0.19748       -0.23037    0.798    {'SOI'        }
       -0.13793    0.22147       -0.62279    0.521    {'AMO'        }
 %}



%%
% AIC MODEL SELECTION
    
% Examine the results of the Marginal Tests based on AIC to get an initial
% ranking of variables:

[mod_den,marg_den]    = bmt_MLR_AIC(envarS,denC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'    }    {'R2'        }    {'R2adj'  }    {'AIC'    }    {'delta' }    {'wts'   }    {'ratio' }    {'var'        }
    {[30.5444]}    {[    0.1016]}    {[ 0.0744]}    {[-0.3909]}    {[     0]}    {[0.5059]}    {[     1]}    {'AMO'        }
    {[34.0000]}    {[       NaN]}    {[    NaN]}    {[ 1.1066]}    {[1.4975]}    {[0.2393]}    {[2.1144]}    {'none'       }
    {[33.6258]}    {[    0.0110]}    {[-0.0190]}    {[ 2.9731]}    {[3.3639]}    {[0.0941]}    {[5.3761]}    {'Temperature'}
    {[33.8696]}    {[    0.0038]}    {[-0.0264]}    {[ 3.2260]}    {[3.6168]}    {[0.0829]}    {[6.1008]}    {'WaterFlow'  }
    {[33.9942]}    {[1.6955e-04]}    {[-0.0301]}    {[ 3.3545]}    {[3.7454]}    {[0.0778]}    {[6.5058]}    {'SOI'        }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'    }    {'R2'    }    {'R2adj' }    {'AIC'    }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[30.5444]}    {[0.1016]}    {[0.0744]}    {[-0.3909]}    {[0.5059]}    {[1.4975]}    {'AMO' }    {[       4]}
    {[30.5444]}    {[   NaN]}    {[   NaN]}    {[-0.3909]}    {[0.3976]}    {[     0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_ext,marg_ext]    = bmt_MLR_AIC(envarS,extC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'    }    {'R2'    }    {'R2adj'  }    {'AIC'   }    {'delta' }    {'wts'   }    {'ratio' }    {'var'        }
    {[31.6706]}    {[0.0685]}    {[ 0.0403]}    {[0.8764]}    {[     0]}    {[0.2837]}    {[     1]}    {'AMO'        }
    {[34.0000]}    {[   NaN]}    {[    NaN]}    {[1.1066]}    {[0.2303]}    {[0.2529]}    {[1.1220]}    {'none'       }
    {[32.4369]}    {[0.0460]}    {[ 0.0171]}    {[1.7132]}    {[0.8368]}    {[0.1867]}    {[1.5196]}    {'SOI'        }
    {[32.8181]}    {[0.0348]}    {[ 0.0055]}    {[2.1221]}    {[1.2457]}    {[0.1522]}    {[1.8643]}    {'WaterFlow'  }
    {[33.1978]}    {[0.0236]}    {[-0.0060]}    {[2.5248]}    {[1.6484]}    {[0.1244]}    {[2.2800]}    {'Temperature'}

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'    }    {'R2'    }    {'R2adj' }    {'AIC'   }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[31.6706]}    {[0.0685]}    {[0.0403]}    {[0.8764]}    {[0.2837]}    {[0.2303]}    {'AMO' }    {[       4]}
    {[31.6706]}    {[   NaN]}    {[   NaN]}    {[0.8764]}    {[0.3350]}    {[     0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calC,1,2,envar_txt);
%{
Conditional Tests skipped: No variable is better than a null model!
%}

[mod_lum,marg_lum]    = bmt_MLR_AIC(envarS,lumC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'    }    {'R2'    }    {'R2adj'  }    {'AIC'     }    {'delta'  }    {'wts'       }    {'ratio'     }    {'var'        }
    {[18.5861]}    {[0.4533]}    {[ 0.4368]}    {[-17.7776]}    {[      0]}    {[    0.9957]}    {[         1]}    {'Temperature'}
    {[25.4298]}    {[0.2521]}    {[ 0.2294]}    {[ -6.8049]}    {[10.9728]}    {[    0.0041]}    {[  241.3813]}    {'AMO'        }
    {[34.0000]}    {[   NaN]}    {[    NaN]}    {[  1.1066]}    {[18.8843]}    {[7.8974e-05]}    {[1.2609e+04]}    {'none'       }
    {[33.8575]}    {[0.0042]}    {[-0.0260]}    {[  3.2134]}    {[20.9910]}    {[2.7542e-05]}    {[3.6153e+04]}    {'SOI'        }
    {[33.9582]}    {[0.0012]}    {[-0.0290]}    {[  3.3173]}    {[21.0950]}    {[2.6148e-05]}    {[3.8081e+04]}    {'WaterFlow'  }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'    }    {'R2'    }    {'R2adj' }    {'AIC'     }    {'wts'   }    {'deltaN' }    {'var'        }    {'idx'     }
    {[18.5861]}    {[0.4533]}    {[0.4368]}    {[-17.7776]}    {[0.9957]}    {[18.8843]}    {'Temperature'}    {[       2]}
    {[18.5861]}    {[   NaN]}    {[   NaN]}    {[-17.7776]}    {[0.3927]}    {[      0]}    {'none'       }    {0×0 double}

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
R2    = 0.10164      
R2adj = 0.07441      
F     = 3.73345      
p     = 0.06100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00000       0.00000       0.03500       
            1 -0.31880      -1.93221      0.06100       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Extension
model_ext  = bmt_MLR(envarS(:,mod_ext.idx),extC,1000,0,1,0);
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.06851      
R2adj = 0.04029      
F     = 2.42721      
p     = 0.14400      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00000      -0.00000      0.08100       
            1 0.26175       1.55795       0.14400       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%Calcification
model_cal  = bmt_MLR(envarS(:,mod_cal.idx),calC,1000,0,1,0);
%{
NONE
%}

%Luminescence
model_lum  = bmt_MLR(envarS(:,mod_lum.idx),lumC,1000,0,1,0);
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.45335      
R2adj = 0.43678      
F     = 27.36756     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00000      -0.00000      0.08100       
            1 -0.67331      -5.23140      0.00100       
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
    {'none'}
%}

mod_lum.var'
%{
    {'Temperature' }
    {'none'}
%}
