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
     WF_Calamar -0.01088      -0.81773      0.44100       
Air_Temperature 0.00901       0.77498       0.44100       
        HadISST 0.01478       0.81820       0.41600       
            SOI 0.04654       2.07668       0.05000       
            AMO -0.20117      -2.31709      0.02100       
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
R2    = 0.30679      
R2adj = 0.24490      
F     = 4.95672      
p     = 0.00200      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.00073       0.35588       0.41600       
            1 0.00520       1.84652       0.06800       
            2 -0.00421      -1.70980      0.10100       
            3 -0.00505      -1.32095      0.16400       
            4 -0.00451      -0.95098      0.34000       
            5 0.00334       0.18159       0.81500       
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
        b          b_SE        tStat      pVal             Var        
    _________    _________    ________    _____    ___________________

     -0.01135    0.0097308     -1.1664    0.017    {'Intercept'      }
    -0.010883     0.013309    -0.81773    0.441    {'WF_Calamar'     }
    0.0090117     0.011628     0.77498    0.441    {'Air_Temperature'}
     0.014782     0.018066      0.8182    0.416    {'HadISST'        }
     0.046537     0.022409      2.0767     0.05    {'SOI'            }
     -0.20117     0.086818     -2.3171    0.021    {'AMO'            }
 %}

%Extension
table(MLR_ext.b, MLR_ext.b_SE, MLR_ext.t, MLR_ext.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
        b           b_SE       tStat      pVal             Var        
    __________    ________    ________    _____    ___________________

     0.0059111    0.017311     0.34147    0.467    {'Intercept'      }
    -0.0050982    0.023677    -0.21533     0.82    {'WF_Calamar'     }
    -0.0052204    0.020686    -0.25236     0.79    {'Air_Temperature'}
     -0.011316    0.032139    -0.35209    0.746    {'HadISST'        }
      0.014775    0.039865     0.37063    0.693    {'SOI'            }
       0.35502     0.15445      2.2987    0.029    {'AMO'            }
 %}

%Calcification
table(MLR_cal.b, MLR_cal.b_SE, MLR_cal.t, MLR_cal.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
         b           b_SE        tStat      pVal             Var        
    ___________    ________    _________    _____    ___________________

     -0.0078382    0.013939     -0.56232    0.208    {'Intercept'      }
      -0.015064    0.019065     -0.79016    0.441    {'WF_Calamar'     }
      0.0047307    0.016657        0.284    0.779    {'Air_Temperature'}
    -3.1082e-05    0.025879    -0.001201    0.999    {'HadISST'        }
       0.059521      0.0321       1.8542    0.056    {'SOI'            }
       0.036715     0.12436      0.29522    0.761    {'AMO'            }
 %}

%Luminescence
table(MLR_lum.b, MLR_lum.b_SE, MLR_lum.t, MLR_lum.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
        b           b_SE        tStat      pVal             Var        
    __________    _________    ________    _____    ___________________

    0.00073327    0.0020604     0.35588    0.416    {'Intercept'      }
     0.0052038    0.0028182      1.8465    0.068    {'WF_Calamar'     }
    -0.0042099    0.0024622     -1.7098    0.101    {'Air_Temperature'}
    -0.0050532    0.0038254      -1.321    0.164    {'HadISST'        }
    -0.0045124     0.004745    -0.95098     0.34    {'SOI'            }
     0.0033381     0.018383     0.18159    0.815    {'AMO'            }
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
    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'  }    {'var'            }
    {[0.2867]}    {[    0.0795]}    {[ 0.0641]}    {[-329.1303]}    {[     0]}    {[0.5342]}    {[      1]}    {'AMO'            }
    {[0.3004]}    {[    0.0354]}    {[ 0.0194]}    {[-326.2324]}    {[2.8980]}    {[0.1254]}    {[ 4.2587]}    {'SOI'            }
    {[0.3007]}    {[    0.0346]}    {[ 0.0185]}    {[-326.1806]}    {[2.9498]}    {[0.1222]}    {[ 4.3705]}    {'HadISST'        }
    {[0.3115]}    {[       NaN]}    {[    NaN]}    {[-326.1321]}    {[2.9982]}    {[0.1193]}    {[ 4.4777]}    {'none'           }
    {[0.3082]}    {[    0.0106]}    {[-0.0058]}    {[-324.6586]}    {[4.4717]}    {[0.0571]}    {[ 9.3547]}    {'WF_Calamar'     }
    {[0.3113]}    {[5.4874e-04]}    {[-0.0161]}    {[-324.0294]}    {[5.1009]}    {[0.0417]}    {[12.8129]}    {'Air_Temperature'}

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.2867]}    {[0.0795]}    {[0.0641]}    {[-329.1303]}    {[0.5342]}    {[2.9982]}    {'AMO' }    {[       5]}
    {[0.2867]}    {[   NaN]}    {[   NaN]}    {[-329.1303]}    {[0.2668]}    {[0.5429]}    {'none'}    {0×0 double}

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

[mod_ext,marg_ext]    = bmt_MLR_AIC(envarS,extC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
  Columns 1 through 7

    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta'  }    {'wts'   }    {'ratio'   }
    {[0.8355]}    {[    0.1861]}    {[ 0.1726]}    {[-262.8214]}    {[      0]}    {[0.9647]}    {[       1]}
    {[0.9403]}    {[    0.0841]}    {[ 0.0688]}    {[-255.4958]}    {[ 7.3256]}    {[0.0248]}    {[ 38.9711]}
    {[1.0266]}    {[       NaN]}    {[    NaN]}    {[-252.1879]}    {[10.6335]}    {[0.0047]}    {[203.7168]}
    {[1.0184]}    {[    0.0080]}    {[-0.0085]}    {[-250.5500]}    {[12.2714]}    {[0.0021]}    {[462.0512]}
    {[1.0186]}    {[    0.0078]}    {[-0.0087]}    {[-250.5393]}    {[12.2821]}    {[0.0021]}    {[464.5433]}
    {[1.0264]}    {[2.1737e-04]}    {[-0.0164]}    {[-250.0647]}    {[12.7567]}    {[0.0016]}    {[588.9570]}

  Column 8

    {'var'            }
    {'AMO'            }
    {'HadISST'        }
    {'none'           }
    {'SOI'            }
    {'Air_Temperature'}
    {'WF_Calamar'     }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var' }    {'idx'     }
    {[0.8355]}    {[0.1861]}    {[0.1726]}    {[-262.8214]}    {[0.9647]}    {[10.6335]}    {'AMO' }    {[       5]}
    {[0.8355]}    {[   NaN]}    {[   NaN]}    {[-262.8214]}    {[0.3825]}    {[      0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio' }    {'var'            }
    {[0.5493]}    {[    0.0601]}    {[ 0.0445]}    {[-288.8276]}    {[     0]}    {[0.4699]}    {[     1]}    {'SOI'            }
    {[0.5844]}    {[       NaN]}    {[    NaN]}    {[-287.1196]}    {[1.7080]}    {[0.2000]}    {[2.3490]}    {'none'           }
    {[0.5764]}    {[    0.0137]}    {[-0.0028]}    {[-285.8357]}    {[2.9919]}    {[0.1053]}    {[4.4635]}    {'AMO'            }
    {[0.5807]}    {[    0.0063]}    {[-0.0103]}    {[-285.3729]}    {[3.4547]}    {[0.0835]}    {[5.6257]}    {'WF_Calamar'     }
    {[0.5834]}    {[    0.0017]}    {[-0.0150]}    {[-285.0870]}    {[3.7406]}    {[0.0724]}    {[6.4901]}    {'HadISST'        }
    {[0.5844]}    {[5.9121e-05]}    {[-0.0166]}    {[-284.9865]}    {[3.8410]}    {[0.0689]}    {[6.8244]}    {'Air_Temperature'}

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var' }    {'idx'     }
    {[0.5493]}    {[0.0601]}    {[0.0445]}    {[-288.8276]}    {[0.4699]}    {[1.7080]}    {'SOI' }    {[       4]}
    {[0.5493]}    {[   NaN]}    {[   NaN]}    {[-288.8276]}    {[0.2985]}    {[     0]}    {'none'}    {0×0 double}

--------------------------------------------------
%}

[mod_lum,marg_lum]    = bmt_MLR_AIC(envarS,lumC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
  Columns 1 through 7

    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'delta'  }    {'wts'       }    {'ratio'   }
    {[0.0131]}    {[0.2225]}    {[0.2095]}    {[-520.5120]}    {[      0]}    {[    0.7955]}    {[       1]}
    {[0.0137]}    {[0.1843]}    {[0.1707]}    {[-517.5402]}    {[ 2.9718]}    {[    0.1800]}    {[  4.4190]}
    {[0.0149]}    {[0.1123]}    {[0.0975]}    {[-512.2943]}    {[ 8.2177]}    {[    0.0131]}    {[ 60.8773]}
    {[0.0151]}    {[0.1029]}    {[0.0880]}    {[-511.6438]}    {[ 8.8682]}    {[    0.0094]}    {[ 84.2773]}
    {[0.0162]}    {[0.0366]}    {[0.0206]}    {[-507.2225]}    {[13.2895]}    {[    0.0010]}    {[768.7329]}
    {[0.0168]}    {[   NaN]}    {[   NaN]}    {[-507.0453]}    {[13.4667]}    {[9.4707e-04]}    {[839.9580]}

  Column 8

    {'var'            }
    {'Air_Temperature'}
    {'HadISST'        }
    {'AMO'            }
    {'WF_Calamar'     }
    {'SOI'            }
    {'none'           }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var'            }    {'idx'     }
    {[0.0131]}    {[0.2225]}    {[0.2095]}    {[-520.5120]}    {[0.7955]}    {[13.4667]}    {'Air_Temperature'}    {[       2]}
    {[0.0131]}    {[   NaN]}    {[   NaN]}    {[-520.5120]}    {[0.2000]}    {[ 0.8621]}    {'none'           }    {0×0 double}

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
p     = 0.02600      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00246      -0.27791      0.02600       
            1 -0.10823      -2.27615      0.02600       
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
    intercept 0.00683       0.45231       0.00100       
            1 0.30068       3.70446       0.00100       
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
R2    = 0.06013      
R2adj = 0.04446      
F     = 3.83845      
p     = 0.07200      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.00581      -0.46424      0.07200       
            1 0.03985       1.95920       0.07200       
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
    {'Air_Temperature'}
    {'none'}
%}