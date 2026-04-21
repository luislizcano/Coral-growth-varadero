% 1954-1982 Monthly
% Data has been already centred - seasonality corrected
% x - x(mean)Month (Climatology)

% Import the data:
growth         = importdata('coral_growth_monthly_centered.xlsx');
lumin          = importdata('coral_lumn_monthly_centered.xlsx');
env            = importdata('env_monthly_centered.xlsx');

% Parse the dataset into working variables (PERIOD 1954-2015):
%% Coral Growth Means
den        = growth.data.Hoja1(34:62,4);        % Density
ext        = growth.data.Hoja1(34:62,5);        % Extension
cal        = growth.data.Hoja1(34:62,6);        % Calcification
lum        = lumin.data.Hoja1(34:62,4);         % Luminescence

%% Environmental variables (Select only those with data available for 1954-1982)
envar       = env.data.Hoja1(34:62,[5,6,8,9,10]);   % ENV Variables (m3/s,°C,SOI,AMO) - SOI and AMO are added below
envar_txt   = env.textdata.Hoja1(1,[5,6,8,9,10]);  % Variable LABELS

%% Standardize biological data
% Standardize the predictors using z-Scores {[X - mean(X)]/std(X)}:
envarS       = envar; % only deseasonalized data (i.e. centered)

% Center the response variable [Y - mean(Y)]:
denC        = den;
extC        = ext;
calC        = cal;
lumC        = lum;

%% MULTIPLE REGRESSION ANALYSIS
% Perform multiple regression analysis using standardized and centered 
% variables:

% Density:
MLR_den  = bmt_MLR(envarS,denC,1000,0)
%{
=====================================================================
                     Multiple Linear Regression:                     
---------------------------------------------------------------------
R2    = 0.64204      
R2adj = 0.56422      
F     = 8.25063      
p     = 0.00200      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.03883      -1.38018      0.37200       
            1 0.00003       5.60041       0.00100       
            2 -0.03064      -0.93632      0.35000       
            3 0.07695       1.13783       0.29200       
            4 -0.01717      -1.22162      0.22700       
            5 0.24694       2.45077       0.02000       
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
R2    = 0.55126      
R2adj = 0.45370      
F     = 5.65081      
p     = 0.00300      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.03709       2.88578       0.08900       
            1 0.00001       2.78138       0.00800       
            2 0.06378       4.26544       0.00200       
            3 -0.05150      -1.66677      0.13300       
            4 -0.00800      -1.24614      0.22000       
            5 -0.04179      -0.90768      0.38200       
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
R2    = 0.57437      
R2adj = 0.48185      
F     = 6.20763      
p     = 0.00300      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.01753       2.52404       0.19300       
            1 0.00000       3.41353       0.00300       
            2 0.03283       4.06487       0.00100       
            3 -0.03204      -1.91956      0.06600       
            4 -0.00375      -1.08225      0.28100       
            5 0.00502       0.20195       0.83200       
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
R2    = 0.77181      
R2adj = 0.72221      
F     = 15.55879     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.03911      -8.74007      0.00100       
            1 0.00001       5.65541       0.00100       
            2 -0.01035      -1.98880      0.06500       
            3 -0.01035      -0.96210      0.36600       
            4 0.00397       1.77668       0.08500       
            5 0.07688       4.79757       0.00100       
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
        b           b_SE        tStat      pVal             Var        
    __________    _________    ________    _____    ___________________

      -0.03883     0.028134     -1.3802    0.372    {'Intercept'      }
    3.2163e-05    5.743e-06      5.6004    0.001    {'WF_Calamar'     }
     -0.030642     0.032726    -0.93632     0.35    {'Air_Temperature'}
       0.07695     0.067629      1.1378    0.292    {'HadISST'        }
     -0.017174     0.014058     -1.2216    0.227    {'SOI'            }
       0.24694      0.10076      2.4508     0.02    {'AMO'            }

 %}

%Extension
table(MLR_ext.b, MLR_ext.b_SE, MLR_ext.t, MLR_ext.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
        b            b_SE        tStat      pVal             Var        
    __________    __________    ________    _____    ___________________

      0.037094      0.012854      2.8858    0.089    {'Intercept'      }
    7.2979e-06    2.6238e-06      2.7814    0.008    {'WF_Calamar'     }
      0.063777      0.014952      4.2654    0.002    {'Air_Temperature'}
       -0.0515      0.030898     -1.6668    0.133    {'HadISST'        }
    -0.0080039      0.006423     -1.2461     0.22    {'SOI'            }
     -0.041786      0.046036    -0.90768    0.382    {'AMO'            }
 %}

%Calcification
table(MLR_cal.b, MLR_cal.b_SE, MLR_cal.t, MLR_cal.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b            b_SE        tStat     pVal             Var        
    __________    __________    _______    _____    ___________________

      0.017526     0.0069435      2.524    0.193    {'Intercept'      }
    4.8382e-06    1.4174e-06     3.4135    0.003    {'WF_Calamar'     }
      0.032831     0.0080769     4.0649    0.001    {'Air_Temperature'}
     -0.032039      0.016691    -1.9196    0.066    {'HadISST'        }
     -0.003755     0.0034696    -1.0823    0.281    {'SOI'            }
     0.0050221      0.024868    0.20195    0.832    {'AMO'            }
 %}

%Luminescence
table(MLR_lum.b, MLR_lum.b_SE, MLR_lum.t, MLR_lum.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
        b            b_SE        tStat     pVal             Var        
    __________    __________    _______    _____    ___________________

     -0.039107     0.0044745    -8.7401    0.001    {'Intercept'      }
    5.1655e-06    9.1337e-07     5.6554    0.001    {'WF_Calamar'     }
     -0.010351     0.0052048    -1.9888    0.065    {'Air_Temperature'}
     -0.010348      0.010756    -0.9621    0.366    {'HadISST'        }
     0.0039724     0.0022359     1.7767    0.085    {'SOI'            }
      0.076882      0.016025     4.7976    0.001    {'AMO'            }
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
  Columns 1 through 7

    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta'  }    {'wts'       }    {'ratio'     }
    {[0.1140]}    {[    0.4876]}    {[ 0.4686]}    {[-156.1571]}    {[      0]}    {[    0.9993]}    {[         1]}
    {[0.2044]}    {[    0.0813]}    {[ 0.0473]}    {[-139.2272]}    {[16.9298]}    {[2.1059e-04]}    {[4.7453e+03]}
    {[0.2225]}    {[       NaN]}    {[    NaN]}    {[-139.0814]}    {[17.0757]}    {[1.9577e-04]}    {[5.1044e+03]}
    {[0.2086]}    {[    0.0626]}    {[ 0.0279]}    {[-138.6423]}    {[17.5148]}    {[1.5718e-04]}    {[6.3575e+03]}
    {[0.2199]}    {[    0.0120]}    {[-0.0246]}    {[-137.1180]}    {[19.0390]}    {[7.3354e-05]}    {[1.3623e+04]}
    {[0.2224]}    {[4.0994e-04]}    {[-0.0366]}    {[-136.7799]}    {[19.3772]}    {[6.1943e-05]}    {[1.6133e+04]}

  Column 8

    {'var'            }
    {'WF_Calamar'     }
    {'Air_Temperature'}
    {'none'           }
    {'SOI'            }
    {'HadISST'        }
    {'AMO'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var'       }    {'idx'     }
    {[0.1140]}    {[0.4876]}    {[0.4686]}    {[-156.1571]}    {[0.9993]}    {[17.0757]}    {'WF_Calamar'}    {[       1]}
    {[0.0898]}    {[0.5966]}    {[0.5656]}    {[-160.5990]}    {[0.7922]}    {[ 4.4419]}    {'AMO'       }    {[       5]}
    {[0.0898]}    {[   NaN]}    {[   NaN]}    {[-160.5990]}    {[0.4594]}    {[      0]}    {'none'      }    {0×0 double}

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
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'  }    {'var'            }
    {[0.0273]}    {[0.2632]}    {[ 0.2359]}    {[-197.6135]}    {[     0]}    {[0.8739]}    {[      1]}    {'Air_Temperature'}
    {[0.0333]}    {[0.1006]}    {[ 0.0673]}    {[-191.8314]}    {[5.7821]}    {[0.0485]}    {[18.0123]}    {'HadISST'        }
    {[0.0371]}    {[   NaN]}    {[    NaN]}    {[-191.0700]}    {[6.5435]}    {[0.0332]}    {[26.3580]}    {'none'           }
    {[0.0354]}    {[0.0442]}    {[ 0.0088]}    {[-190.0685]}    {[7.5450]}    {[0.0201]}    {[43.4897]}    {'SOI'            }
    {[0.0364]}    {[0.0177]}    {[-0.0187]}    {[-189.2741]}    {[8.3394]}    {[0.0135]}    {[64.6966]}    {'WF_Calamar'     }
    {[0.0370]}    {[0.0023]}    {[-0.0347]}    {[-188.8226]}    {[8.7909]}    {[0.0108]}    {[81.0819]}    {'AMO'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var'            }    {'idx'     }
    {[0.0273]}    {[0.2632]}    {[0.2359]}    {[-197.6135]}    {[0.8739]}    {[6.5435]}    {'Air_Temperature'}    {[       2]}
    {[0.0214]}    {[0.4213]}    {[0.3768]}    {[-202.1224]}    {[0.6779]}    {[4.5089]}    {'WF_Calamar'     }    {[       1]}
    {[0.0181]}    {[0.5108]}    {[0.4521]}    {[-204.2860]}    {[0.5553]}    {[2.1636]}    {'HadISST'        }    {[       3]}
    {[0.0181]}    {[   NaN]}    {[   NaN]}    {[-204.2860]}    {[0.5576]}    {[     0]}    {'none'           }    {0×0 double}

--------------------------------------------------
%}

[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'  }    {'var'            }
    {[0.0086]}    {[0.2433]}    {[ 0.2152]}    {[-231.0249]}    {[     0]}    {[0.8126]}    {[      1]}    {'Air_Temperature'}
    {[0.0102]}    {[0.1072]}    {[ 0.0742]}    {[-226.2309]}    {[4.7940]}    {[0.0739]}    {[10.9904]}    {'HadISST'        }
    {[0.0114]}    {[   NaN]}    {[    NaN]}    {[-225.2547]}    {[5.7702]}    {[0.0454]}    {[17.9053]}    {'none'           }
    {[0.0109]}    {[0.0396]}    {[ 0.0040]}    {[-224.1125]}    {[6.9125]}    {[0.0256]}    {[31.6971]}    {'WF_Calamar'     }
    {[0.0111]}    {[0.0305]}    {[-0.0054]}    {[-223.8400]}    {[7.1849]}    {[0.0224]}    {[36.3231]}    {'SOI'            }
    {[0.0111]}    {[0.0233]}    {[-0.0129]}    {[-223.6252]}    {[7.3998]}    {[0.0201]}    {[40.4424]}    {'AMO'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var'            }    {'idx'     }
    {[0.0086]}    {[0.2433]}    {[0.2152]}    {[-231.0249]}    {[0.8126]}    {[5.7702]}    {'Air_Temperature'}    {[       2]}
    {[0.0062]}    {[0.4562]}    {[0.4143]}    {[-238.1074]}    {[0.8889]}    {[7.0825]}    {'WF_Calamar'     }    {[       1]}
    {[0.0051]}    {[0.5501]}    {[0.4961]}    {[-240.8983]}    {[0.6364]}    {[2.7909]}    {'HadISST'        }    {[       3]}
    {[0.0051]}    {[   NaN]}    {[   NaN]}    {[-240.8983]}    {[0.5712]}    {[     0]}    {'none'           }    {0×0 double}

--------------------------------------------------
%}

[mod_lum,marg_lum]    = bmt_MLR_AIC(envarS,lumC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
  Columns 1 through 7

    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta'  }    {'wts'       }    {'ratio'     }
    {[0.0042]}    {[0.5293]}    {[ 0.5119]}    {[-252.2013]}    {[      0]}    {[    0.9987]}    {[         1]}
    {[0.0067]}    {[0.2428]}    {[ 0.2148]}    {[-238.4155]}    {[13.7858]}    {[    0.0010]}    {[  985.2665]}
    {[0.0076]}    {[0.1376]}    {[ 0.1057]}    {[-234.6429]}    {[17.5584]}    {[1.5370e-04]}    {[6.4978e+03]}
    {[0.0088]}    {[   NaN]}    {[    NaN]}    {[-232.6625]}    {[19.5388]}    {[5.7103e-05]}    {[1.7490e+04]}
    {[0.0088]}    {[0.0053]}    {[-0.0315]}    {[-230.5031]}    {[21.6982]}    {[1.9397e-05]}    {[5.1489e+04]}
    {[0.0088]}    {[0.0013]}    {[-0.0357]}    {[-230.3875]}    {[21.8138]}    {[1.8308e-05]}    {[5.4551e+04]}

  Column 8

    {'var'            }
    {'WF_Calamar'     }
    {'SOI'            }
    {'Air_Temperature'}
    {'none'           }
    {'AMO'            }
    {'HadISST'        }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var'            }    {'idx'     }
    {[0.0042]}    {[0.5293]}    {[0.5119]}    {[-252.2013]}    {[0.9987]}    {[19.5388]}    {'WF_Calamar'     }    {[       1]}
    {[0.0027]}    {[0.6897]}    {[0.6659]}    {[-261.7909]}    {[0.9836]}    {[ 9.5896]}    {'AMO'            }    {[       5]}
    {[0.0023]}    {[0.7378]}    {[0.7064]}    {[-263.9676]}    {[0.5240]}    {[ 2.1767]}    {'Air_Temperature'}    {[       2]}
    {[0.0023]}    {[   NaN]}    {[   NaN]}    {[-263.9676]}    {[0.4470]}    {[      0]}    {'none'           }    {0×0 double}

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
R2    = 0.59663      
R2adj = 0.56561      
F     = 19.22883     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.03159      -1.51182      0.45400       
            1 0.00003       6.19929       0.00100       
            2 0.24420       2.65143       0.01700       
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
R2    = 0.51080      
R2adj = 0.45210      
F     = 8.70131      
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.02923       2.67174       0.20200       
            1 0.06216       4.49754       0.00100       
            2 0.00001       2.74118       0.01100       
            3 -0.06359      -2.13814      0.05300       
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
R2    = 0.55008      
R2adj = 0.49609      
F     = 10.18864     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.01720       2.95494       0.15900       
            1 0.03502       4.76394       0.00100       
            2 0.00000       3.33028       0.00500       
            3 -0.03614      -2.28436      0.03500       
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
R2    = 0.73783      
R2adj = 0.70636      
F     = 23.45211     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.03890      -11.36010     0.00100       
            1 0.00001       7.03996       0.00100       
            2 0.07163       4.42263       0.00100       
            3 -0.01135      -2.14127      0.04900       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%% SHOW BEST VARIABLES

mod_den.var'
%{
    {'WF_Calamar'}
    {'AMO'       }
    {'none'      }
%}

mod_ext.var'
%{
    {'Air_Temperature'}
    {'WF_Calamar'     }
    {'HadISST'        }
    {'none'           }
%}

mod_cal.var'
%{
    {'Air_Temperature'}
    {'WF_Calamar'     }
    {'HadISST'        }
    {'none'           }
%}

mod_lum.var'
%{
    {'WF_Calamar'     }
    {'AMO'            }
    {'Air_Temperature'}
    {'none'           }
%}