% 1954-2015 Monthly
% Import the data:
growth         = importdata('coral_growth_monthly_centered.xlsx');
lumin          = importdata('coral_lumn_monthly_centered.xlsx');
env            = importdata('env_monthly_centered.xlsx');

% Parse the dataset into working variables (PERIOD 1954-2015):
%% Coral Growth Means
den        = growth.data.Hoja1(1:62,4);        % Density
ext        = growth.data.Hoja1(1:62,5);        % Extension
cal        = growth.data.Hoja1(1:62,6);        % Calcification
lum        = lumin.data.Hoja1(1:62,4);         % Luminescence

%% Environmental variables (Select only those with data available for 1954-1982)
envar       = env.data.Hoja1(1:62,[5,6,8,9,10]);   % ENV Variables (m3/s,°C,SOI,AMO) - SOI and AMO are added below
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
R2    = 0.22432      
R2adj = 0.15506      
F     = 3.23894      
p     = 0.01600      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.07281       3.93574       0.04600       
            1 0.00002       3.19270       0.00400       
            2 0.00512       0.18523       0.86000       
            3 -0.06862      -1.59937      0.13700       
            4 -0.02210      -1.78045      0.08300       
            5 0.04306       0.61470       0.51400       
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
R2    = 0.38267      
R2adj = 0.32755      
F     = 6.94260      
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.04498       5.02018       0.00400       
            1 0.00001       2.34991       0.02100       
            2 0.05496       4.10799       0.00100       
            3 -0.07728      -3.71903      0.00100       
            4 -0.00026      -0.04285      0.96300       
            5 -0.05909      -1.74182      0.08900       
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
R2    = 0.42094      
R2adj = 0.36923      
F     = 8.14153      
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.02978       6.11619       0.00200       
            1 0.00000       2.52491       0.01600       
            2 0.03034       4.17168       0.00100       
            3 -0.05040      -4.46188      0.00100       
            4 -0.00109      -0.33254      0.74000       
            5 -0.02763      -1.49841      0.13900       
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
R2    = 0.43509      
R2adj = 0.38466      
F     = 8.62631      
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.03315      -8.86502      0.01700       
            1 0.00000       3.50590       0.00100       
            2 -0.00094      -0.16873      0.85500       
            3 -0.00622      -0.71741      0.48700       
            4 0.00290       1.15723       0.22400       
            5 0.03474       2.45345       0.02200       
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
        b            b_SE        tStat     pVal             Var        
    __________    __________    _______    _____    ___________________

      0.072805      0.018499     3.9357    0.046    {'Intercept'      }
    1.7127e-05    5.3644e-06     3.1927    0.004    {'WF_Calamar'     }
     0.0051169      0.027625    0.18523     0.86    {'Air_Temperature'}
     -0.068621      0.042905    -1.5994    0.137    {'HadISST'        }
     -0.022098      0.012412    -1.7805    0.083    {'SOI'            }
      0.043056      0.070043     0.6147    0.514    {'AMO'            }

 %}

%Extension
table(MLR_ext.b, MLR_ext.b_SE, MLR_ext.t, MLR_ext.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    EXTENSION
         b           b_SE         tStat      pVal             Var        
    ___________    _________    _________    _____    ___________________

       0.044976     0.008959       5.0202    0.004    {'Intercept'      }
     6.1051e-06    2.598e-06       2.3499    0.021    {'WF_Calamar'     }
       0.054961     0.013379        4.108    0.001    {'Air_Temperature'}
      -0.077278     0.020779       -3.719    0.001    {'HadISST'        }
    -0.00025757    0.0060111    -0.042849    0.963    {'SOI'            }
      -0.059087     0.033923      -1.7418    0.089    {'AMO'            }
 %}

%Calcification
table(MLR_cal.b, MLR_cal.b_SE, MLR_cal.t, MLR_cal.p_t, ...
    ['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    CALCIFICATION
        b            b_SE        tStat      pVal             Var        
    __________    __________    ________    _____    ___________________

      0.029785     0.0048698      6.1162    0.002    {'Intercept'      }
    3.5657e-06    1.4122e-06      2.5249    0.016    {'WF_Calamar'     }
      0.030338     0.0072725      4.1717    0.001    {'Air_Temperature'}
     -0.050396      0.011295     -4.4619    0.001    {'HadISST'        }
    -0.0010865     0.0032674    -0.33254     0.74    {'SOI'            }
     -0.027629      0.018439     -1.4984    0.139    {'AMO'            }
 %}

%Luminescence
table(MLR_lum.b, MLR_lum.b_SE, MLR_lum.t, MLR_lum.p_t, ...
['Intercept' envar_txt]','VariableNames', {'b' 'b_SE' 'tStat' 'pVal' 'Var'})
%{
    LUMINESCENCE
        b            b_SE        tStat      pVal             Var        
    __________    __________    ________    _____    ___________________

     -0.033152     0.0037396      -8.865    0.017    {'Intercept'      }
     3.802e-06    1.0845e-06      3.5059    0.001    {'WF_Calamar'     }
    -0.0009423     0.0055847    -0.16873    0.855    {'Air_Temperature'}
    -0.0062225     0.0086736    -0.71741    0.487    {'HadISST'        }
     0.0029037     0.0025092      1.1572    0.224    {'SOI'            }
      0.034741       0.01416      2.4534    0.022    {'AMO'            }
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
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'  }    {'var'            }
    {[0.3096]}    {[0.1313]}    {[ 0.1168]}    {[-324.3693]}    {[     0]}    {[0.8255]}    {[      1]}    {'WF_Calamar'     }
    {[0.3327]}    {[0.0665]}    {[ 0.0510]}    {[-319.9149]}    {[4.4544]}    {[0.0890]}    {[ 9.2738]}    {'HadISST'        }
    {[0.3442]}    {[0.0342]}    {[ 0.0181]}    {[-317.8050]}    {[6.5643]}    {[0.0310]}    {[26.6330]}    {'Air_Temperature'}
    {[0.3564]}    {[   NaN]}    {[    NaN]}    {[-317.7821]}    {[6.5872]}    {[0.0306]}    {[26.9397]}    {'none'           }
    {[0.3542]}    {[0.0062]}    {[-0.0104]}    {[-316.0316]}    {[8.3377]}    {[0.0128]}    {[64.6399]}    {'SOI'            }
    {[0.3558]}    {[0.0016]}    {[-0.0151]}    {[-315.7416]}    {[8.6277]}    {[0.0110]}    {[74.7274]}    {'AMO'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var'       }    {'idx'     }
    {[0.3096]}    {[0.1313]}    {[0.1168]}    {[-324.3693]}    {[0.8255]}    {[6.5872]}    {'WF_Calamar'}    {[       1]}
    {[0.3096]}    {[   NaN]}    {[   NaN]}    {[-324.3693]}    {[0.1780]}    {[1.9294]}    {'none'      }    {0×0 double}

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
    {'RSS'   }    {'R2'    }    {'R2adj'  }    {'AIC'      }    {'delta' }    {'wts'   }    {'ratio'   }    {'var'            }
    {[0.0892]}    {[0.1510]}    {[ 0.1368]}    {[-401.5390]}    {[     0]}    {[0.8887]}    {[       1]}    {'HadISST'        }
    {[0.0975]}    {[0.0722]}    {[ 0.0567]}    {[-396.0395]}    {[5.4995]}    {[0.0568]}    {[ 15.6391]}    {'AMO'            }
    {[0.1013]}    {[0.0359]}    {[ 0.0199]}    {[-393.6617]}    {[7.8774]}    {[0.0173]}    {[ 51.3507]}    {'Air_Temperature'}
    {[0.1050]}    {[   NaN]}    {[    NaN]}    {[-393.5293]}    {[8.0097]}    {[0.0162]}    {[ 54.8642]}    {'none'           }
    {[0.1017]}    {[0.0313]}    {[ 0.0152]}    {[-393.3672]}    {[8.1718]}    {[0.0149]}    {[ 59.4964]}    {'WF_Calamar'     }
    {[0.1047]}    {[0.0028]}    {[-0.0138]}    {[-391.5661]}    {[9.9730]}    {[0.0061]}    {[146.4195]}    {'SOI'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN'}    {'var'            }    {'idx'     }
    {[0.0892]}    {[0.1510]}    {[0.1368]}    {[-401.5390]}    {[0.8887]}    {[8.0097]}    {'HadISST'        }    {[       3]}
    {[0.0796]}    {[0.2417]}    {[0.2160]}    {[-406.3379]}    {[0.7863]}    {[4.7989]}    {'Air_Temperature'}    {[       2]}
    {[0.0684]}    {[0.3491]}    {[0.3154]}    {[-413.5165]}    {[0.8620]}    {[7.1785]}    {'WF_Calamar'     }    {[       1]}
    {[0.0684]}    {[   NaN]}    {[   NaN]}    {[-413.5165]}    {[0.3466]}    {[0.9117]}    {'none'           }    {0×0 double}

--------------------------------------------------
%}

[mod_cal,marg_cal]    = bmt_MLR_AIC(envarS,calC,1,2,envar_txt);
%{
==================================================
AIC-based stepwise forward selection (MLR)         
--------------------------------------------------
Marginal (Independent) Tests: (each variable separately)
  Columns 1 through 7

    {'RSS'   }    {'R2'        }    {'R2adj'  }    {'AIC'      }    {'delta'  }    {'wts'       }    {'ratio'     }
    {[0.0264]}    {[    0.2022]}    {[ 0.1889]}    {[-477.0202]}    {[      0]}    {[    0.9852]}    {[         1]}
    {[0.0310]}    {[    0.0616]}    {[ 0.0460]}    {[-466.9580]}    {[10.0622]}    {[    0.0064]}    {[  153.1000]}
    {[0.0331]}    {[       NaN]}    {[    NaN]}    {[-465.1527]}    {[11.8675]}    {[    0.0026]}    {[  377.5667]}
    {[0.0320]}    {[    0.0332]}    {[ 0.0171]}    {[-465.1073]}    {[11.9128]}    {[    0.0026]}    {[  386.2220]}
    {[0.0321]}    {[    0.0301]}    {[ 0.0140]}    {[-464.9126]}    {[12.1075]}    {[    0.0023]}    {[  425.7101]}
    {[0.0331]}    {[6.2391e-04]}    {[-0.0160]}    {[-463.0546]}    {[13.9655]}    {[9.1399e-04]}    {[1.0779e+03]}

  Column 8

    {'var'            }
    {'HadISST'        }
    {'AMO'            }
    {'none'           }
    {'Air_Temperature'}
    {'WF_Calamar'     }
    {'SOI'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var'            }    {'idx'     }
    {[0.0264]}    {[0.2022]}    {[0.1889]}    {[-477.0202]}    {[0.9852]}    {[11.8675]}    {'HadISST'        }    {[       3]}
    {[0.0232]}    {[0.2983]}    {[0.2745]}    {[-482.7702]}    {[0.8738]}    {[ 5.7500]}    {'Air_Temperature'}    {[       2]}
    {[0.0199]}    {[0.3973]}    {[0.3661]}    {[-489.9092]}    {[0.8999]}    {[ 7.1390]}    {'WF_Calamar'     }    {[       1]}
    {[0.0199]}    {[   NaN]}    {[   NaN]}    {[-489.9092]}    {[0.4334]}    {[      0]}    {'none'           }    {0×0 double}

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
    {[0.0127]}    {[0.3639]}    {[ 0.3533]}    {[-522.2733]}    {[      0]}    {[    0.9963]}    {[         1]}
    {[0.0153]}    {[0.2374]}    {[ 0.2247]}    {[-511.0317]}    {[11.2416]}    {[    0.0036]}    {[  276.1068]}
    {[0.0171]}    {[0.1428]}    {[ 0.1285]}    {[-503.7751]}    {[18.4982]}    {[9.5843e-05]}    {[1.0395e+04]}
    {[0.0200]}    {[   NaN]}    {[    NaN]}    {[-496.3617]}    {[25.9116]}    {[2.3537e-06]}    {[4.2329e+05]}
    {[0.0196]}    {[0.0196]}    {[ 0.0032]}    {[-495.4506]}    {[26.8227]}    {[1.4925e-06]}    {[6.6753e+05]}
    {[0.0199]}    {[0.0043]}    {[-0.0123]}    {[-494.4918]}    {[27.7815]}    {[9.2410e-07]}    {[1.0781e+06]}

  Column 8

    {'var'            }
    {'WF_Calamar'     }
    {'SOI'            }
    {'Air_Temperature'}
    {'none'           }
    {'HadISST'        }
    {'AMO'            }

--------------------------------------------------

Conditional (Partial) Tests: (sequential variable addition)
    {'RSS'   }    {'R2'    }    {'R2adj' }    {'AIC'      }    {'wts'   }    {'deltaN' }    {'var'       }    {'idx'     }
    {[0.0127]}    {[0.3639]}    {[0.3533]}    {[-522.2733]}    {[0.9963]}    {[25.9116]}    {'WF_Calamar'}    {[       1]}
    {[0.0117]}    {[0.4154]}    {[0.3956]}    {[-525.3012]}    {[0.6719]}    {[ 3.0279]}    {'AMO'       }    {[       5]}
    {[0.0117]}    {[   NaN]}    {[   NaN]}    {[-525.3012]}    {[0.4117]}    {[      0]}    {'none'      }    {0×0 double}

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
R2    = 0.13126      
R2adj = 0.11678      
F     = 9.06534      
p     = 0.00200      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.05103       5.54724       0.00100       
            1 0.00001       3.01087       0.00200       
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
R2    = 0.34909      
R2adj = 0.31543      
F     = 10.36890     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.03950       4.90043       0.01900       
            1 -0.08397      -4.10008      0.00100       
            2 0.05409       4.08793       0.00100       
            3 0.00001       3.09315       0.00700       
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
R2    = 0.39729      
R2adj = 0.36611      
F     = 12.74392     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept 0.02684       6.16617       0.00400       
            1 -0.05385      -4.86834      0.00100       
            2 0.03036       4.24788       0.00100       
            3 0.00000       3.08618       0.00300       
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
R2    = 0.41543      
R2adj = 0.39562      
F     = 20.96458     
p     = 0.00100      

---------------------------------------------------------------------
Variable      b             t-stat        p
---------------------------------------------------------------------
    intercept -0.03382      -13.34043     0.00200       
            1 0.00000       6.44171       0.00100       
            2 0.03125       2.28068       0.02900       
---------------------------------------------------------------------

Number of permutations of RAW DATA =   999 
F-test is one-tailed, t-tests are two-tailed 
=====================================================================
%}

%% SHOW BEST VARIABLES

mod_den.var'
%{
    {'WF_Calamar'}
    {'none'      }

%}

mod_ext.var'
%{
    {'HadISST'        }
    {'Air_Temperature'}
    {'WF_Calamar'     }
    {'none'           }
%}

mod_cal.var'
%{
    {'HadISST'        }
    {'Air_Temperature'}
    {'WF_Calamar'     }
    {'none'           }
%}

mod_lum.var'
%{
    {'WF_Calamar'}
    {'AMO'       }
    {'none'      }
%}