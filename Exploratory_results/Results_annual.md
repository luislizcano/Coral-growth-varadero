# Exploratory results (Annual data)

## Annual time series (1954-2015)
* Skeletal density (g cm<sup>-3</sup>)
* Linear extension (cm yr<sup>-1</sup>)
* Calcification (g cm<sup>-2</sup> yr<sup>-1</sup>)
* Sea surface temperature (HadISST)
* Water discharge (Sta Helena)(data from 1954-1981 were modeled using Calamar data)
* Water discharge (Calamar) (m<sup>3</sup> s<sup>-1</sup>)
* SOI
* AMO

## Preliminary tests using raw data (no transformations or treatments)

### Normality test
**Test:** Shapiro-Wilk test for normality \
**Hypothesis:** If p < 0.05, then the distribution is non-normal \
**Result:** The distribution of all variables are normal, except WF_Helena*

|Variable      | W-Statistic | p-value  |
|--------------|-------------|----------|
|Density       |  0.98       |  0.51    |
|Extension     |  0.97       |  0.14    |
|Calcification |  0.98       |  0.76    |
|G/B           |  0.97       |  0.13    |
|WF_Helena     |  0.93       |  0.002* (0.72 for 1981-2015) | 
|WF_Calamar    |  0.98       |  0.49    |
|HadISST       |  0.99       |  0.89    |
|SOI           |  0.98       |  0.28    |
|AMO           |  0.99       |  0.77    |

### Stationary test
**Test:** Augmented Dickey-Fuller (ADF) test \
**Hypothesis:** If p < 0.05, then the time series is stationary (no long-term trends) \
**Result:** WF_Helena and AMO are non-stationary time series (statistical properties change over time).

|Variable      | DF-Statistic | p-value  |
|--------------|--------------|----------|
|Density       | -3.22        |  0.019 * |
|Extension     | -3.07        |  0.029 * |
|Calcification | -3.85        |  0.002 * |
|G/B           | -3.30        |  0.015 * |
|WF_Helena     | -1.25        |  0.650 (0.019* for 1981-2015) | 
|WF_Calamar    | -5.87        |  0.000 * |
|HadISST       | -4.93        |  0.000 * |
|SOI           | -5.27        |  0.000 * |
|AMO           | -1.95        |  0.308   |

### Autocorrelation at lag 1
**Test:** Durbin–Watson test \
**Hypothesis:** The d value lies between 0 and 4. Autocorrelation is higher as it gets closer to zero. As a rule of thumb values < 2 indicate that autocorrelation exist \
**Result:** All values are < 2, indicating high autocorrelations at lag=1.

|Variable      | d      |
|--------------|--------|
|Density       | 0.006 *|
|Extension     | 0.020 *|
|Calcification | 0.026 *|
|G/B           | 0.000 *|
|WF_Helena     | 0.060 *|
|WF_Calamar    | 0.047 *|
|HadISST       | 0.000 *|
|SOI           | 1.301 *|
|AMO           | 0.576 *|



## Data treatment

## Detrending (Z-scores)
The time series data were detrended or standardized (z-scores or STDA) to remove the long-term trend, visualize anomalies, and try to reduce autocorrelations.

### Normality
The normality test showed identical results to those from raw data above. Only WF_Helena is not normal.

|Variable      | W-Statistic | p-value  |
|--------------|-------------|----------|
|Density       |  0.98       |  0.51    |
|Extension     |  0.97       |  0.14    |
|Calcification |  0.98       |  0.76    |
|G/B           |  0.97       |  0.13    |
|WF_Helena     |  0.93       |  0.002 * | 0.72 (1981-2015)
|WF_Calamar    |  0.98       |  0.49    |
|HadISST       |  0.99       |  0.89    |
|SOI           |  0.98       |  0.28    |
|AMO           |  0.99       |  0.77    |

### Autocorrelation at lag 1
**Test:** Durbin–Watson test \
**Hypothesis:** The d value lies between 0 and 4. Autocorrelation is higher as it gets closer to zero. As a rule of thumb values < 2 indicate that autocorrelation exist \
**Result:** The d values were higher than using raw data. However, all values are still below < 2, indicating high autocorrelations at lag=1.

|Variable      | d      |
|--------------|--------|
|Density       | 0.637 *|
|Extension     | 1.586 *|
|Calcification | 1.851 *|
|G/B           | 0.526 *|
|WF_Helena     | 0.490 *|
|WF_Calamar    | 1.419 *|
|HadISST       | 1.115 *|
|SOI           | 1.301 *|
|AMO           | 0.576 *|

### Collinearity
The group of environmental variables were tested for multicollinearity using the variance inflation factor (VIF).
The VIF values were below 5, indicating there is no strong collinearity among variables.

|     Variable | VIF  |
|--------------|------|
|   WF_Helena  | 1.94 |
|  WF_Calamar  | 2.83 |
|     HadISST  | 3.03 |
|         SOI  | 2.12 |
|         AMO  | 3.19 |

However, the data **violates** the normality and autocorrelations (and potentially the homoscedasticity) assumptions for OLS linear regression (or Multiple linear regressions).

### Long-term trends
**Test:** General additive mixed models (GAMM) \
The GAMM allows to fit non-linear trends to data, accounting for autocorrelated data.

The response variable was modeled as a smooth function of time using a cubic regression spline, allowing nonlinear temporal trajectories. 
Temporal dependence among residuals was accounted for using a first-order autoregressive [AR(1)] correlation structure. 
The model was specified as $$\(Y_t=\beta_0+f(t)+\epsilon_t\)$$, where $$\(f(t)\)$$ represents the smooth temporal function and residuals 
followed $$\(\epsilon_t=\phi\epsilon_{t-1}+\eta_t\)$$. The degree of smoothness was estimated from the data using penalized regression splines.

* $$Y_t$$ = observed annual value at year $$\(t\)$$
* $$beta_0$$ = intercept
* $$f(t)$$ = smooth nonlinear function of time estimated using a cubic regression spline
* $$epsilon_t$$ = residual error

The AR(1) structure is:

$$ \epsilon_t = \phi\epsilon_{t-1}+\eta_t $$

where $$\(\phi\)$$ is the estimated lag-1 autocorrelation parameter and $$\(\eta_t\)$$ is an independent error term.


<p align="center">
<img src="https://github.com/luislizcano/Coral-growth-varadero/blob/main/Figures/Exploratorias/figE4_GAM_growth_annual.svg" width="400">
<img src="https://github.com/luislizcano/Coral-growth-varadero/blob/main/Figures/Exploratorias/figE4_GAM_envir_annual.svg" width="400">
</p>

For the long-term trends using GAM, each variable's trend is depending on the time (years). 
The table of results are indicating that many variables tend to be linear (see edf (estimated degrees of freedom), if edf = 1.0, the trend is linear),
and the p-value indicates if that trend is significant over time. \

Variables such as Extension, G/B, WF_Helena, and AMO have clearly nonlinear trends. It would be interesting keep doing further analysis with pre- and post- the dredging event of 1984.

|Variable      | Intercept | Time            |  R2   |
|--------------|-----------|-----------------|-------|
|Density       |  0.73     | edf=1.0; p=0.026|  0.21 |
|Extension     |  1.07     | edf=9.2; p<0.001|  0.35 |
|Calcification |  0.77     | edf=2.7; p=0.018|  0.12 |
|G/B           |  1.02     | edf=4.0; p<0.001|  0.63 |
|WF_Helena     |  292.7    | edf=3.1; p<0.001|  0.60 |
|WF_Calamar    |  7273.7   | edf=1.0; p=0.91 |  0.01 |
|HadISST       |  28.1     | edf=2.7; p<0.001|  0.35 |
|SOI           |  0.14     | edf=1.5; p=0.52 |  0.03 |
|AMO           | -0.02     | edf=4.7; p<0.001|  0.63 |

### Pearson correlations
For exploratory purposes, the correlations were ran using detrended monthly data for three periods: the whole period 1954-2015, and the before and after the dredging 
events of 1984 (assuming linearity).
Interpretations may be biased due to some assumptions are not met. Left value is correlation and right value is p-value.

 1954-2015    | WF_Helena      | WF_Calamar     | HadISST         | SOI            | AMO             |
--------------|----------------|----------------|-----------------|----------------|-----------------|
Density       |-0.39, **0.002**| 0.11, 0.374    |-0.20, 0.126     | 0.20, 0.114    |-0.28, **0.026** |
Extension     | 0.29, **0.023**|-0.03, 0.830    | 0.28, **0.025** | 0.09, 0.470    | 0.45, **<0.001**|
Calcification |-0.09, 0.481    | 0.09, 0.487    | 0.01, 0.927     | 0.27, **0.034**| 0.10, 0.427     |
G/B           |-0.27, **0.032**| 0.32, **0.011**|-0.43, **<0.001**| 0.19, 0.136    |-0.34, **0.008** |

1954-1983     | WF_Helena    | WF_Calamar   | HadISST      | SOI            | AMO             |
--------------|--------------|--------------|--------------|----------------|-----------------|
Density       | 0.09, 0.651  | 0.09, 0.619  | 0.02, 0.905  | 0.31, 0.099    | 0.03, 0.886     |
Extension     |-0.05, 0.807  |-0.01, 0.977  | 0.17, 0.366  | 0.17, 0.369    | 0.55, **<0.002**|
Calcification | 0.05, 0.780  | 0.10, 0.600  | 0.16, 0.404  | 0.40, **0.030**| 0.46, **0.010** |
G/B           | 0.23, 0.229  | 0.25, 0.184  | 0.06, 0.772  | 0.28, 0.135    | 0.29, 0.114     |

1984-2015     | WF_Helena    | WF_Calamar     | HadISST        | SOI         | AMO            |
--------------|--------------|----------------|----------------|-------------|----------------|
Density       |-0.01, 0.970  | 0.18, 0.336    |-0.06, 0.736    | 0.00, 0.995 |-0.31, 0.085    |
Extension     | 0.14, 0.447  |-0.04, 0.824    | 0.22, 0.231    | 0.11, 0.550 | 0.24, 0.182    |
Calcification | 0.12, 0.514  | 0.08, 0.648    | 0.03, 0.889    | 0.12, 0.511 |-0.07, 0.697    |
G/B           | 0.16, 0.388  | 0.42, **0.018**|-0.52, **0.002**| 0.09, 0.625 |-0.49, **0.005**|

In this case, it is interesting to see that the correlations for the long-term, and the periods before and after 1984, are different.
The most interesting result is that G/B is not correlated with water discharge at Sta Helena, but it is with the Calamar station after 1984.
Water flow at Sta Helena increases over time after 1984 as the WF at Calamar is stable, but after 1984 there is more water coming from
Calamar (and the Magdalena River) to Sta Helena and into the Bay.

This is a strong evidence to continue analysis per periods.

### Water flows of the Canal del Dique
The Canal del Dique have water flow data available from 1941 to the present at the Calamar station, which is located at the Canal del Dique
bifurcation from the Magdalena river. A closer station to Cartagena Bay is Santa Helena, which have data from 1981 to the present.
This station was born in the same year that the dredging works started. So there is not much data available from this station before 1984,
the year that the dredging works finished.

The regression of Calamar and Sta Helena water flow data before and after 1984 show different slopes, being higher after 1984. In average,
the water flow from 1984-2015 at Sta Helena increased 73%, in comparison to the flow from 1981-1983.

<p align="center">
<img src="https://github.com/luislizcano/Coral-growth-varadero/blob/main/Figures/Exploratorias/figE0_waterflow-scatter.png" width="500">
</p>

Monthly data from 1981 to 1983 from Sta Helena was used to model water flow from 1954 to 1980, 
assuming that the data from 1981 to 1983 at Sta Helena represents the water flow before the canal expansion of 1984, with minimal dredging impact.

<p align="center">
<img src="https://github.com/luislizcano/Coral-growth-varadero/blob/main/Figures/Exploratorias/figE0_waterflow-timeseries.png" width="700">
</p>

The plots show evidence that water flow at Sta Helena increases over time after 1984. Before the dredging events, water flow at Sta Helena
represented 2-3% of the flow at Calamar. In contrast, this ratio increases up to 6% in average after 1984.

This modeled data was averaged annually for the respective annual analyses.

### GAMM 
#### Individual comparisons
We will use individual comparisons among growth parameters and environmental variables (added to time; e.g. time series showed above), 
using GAMMs accounting for autocorrelations and potential non-linearities.

Here, we are not testing for temporal patterns, but for association between environmental variables and growth parameters.

**Water flow at Santa Helena 1954-2015** \
Both time and WF_Helena are significantly associated with G/B, after accounting for the other variable. The temporal relationship estimated 
by the GAM is essentially linear (edf = 1.0). This model establishes an association, not causation. The model explains approximately 48% 
of the variation in G/B, after accounting for model complexity. The linear trend of G/B is decreasing and WF_Helena is increasing.

|Variable      | Intercept | Time            |  WF_Helena      |  R2  | AIC  |
|--------------|-----------|-----------------|-----------------|------|------|
|Density       |  0.73     | edf=1.0; p=0.037| edf=1.0; p=0.846| 0.19 | -179 |
|Extension     |  1.07     | edf=7.5; p<0.001| edf=1.0; p=0.553| 0.35 |  -84 |
|Calcification |  0.77     | edf=1.0; p=0.029| edf=1.0; p=0.251| 0.05 | -110 |
|G/B           |  1.02     | edf=1.0; p<0.001| edf=1.0; p<0.001| 0.48 | -400 |

**Water flow at Calamar 1954-2015** \
Not much difference from what was observed with Sta Helena data.

|Variable      | Intercept | Time            |  WF_Calamar     |  R2  | AIC  |
|--------------|-----------|-----------------|-----------------|------|------|
|Density       |  0.73     | edf=1.0; p=0.026| edf=1.0; p=0.693| 0.20 | -179 |
|Extension     |  1.07     | edf=7.5; p<0.001| edf=1.0; p=0.556| 0.35 |  -84 |
|Calcification |  0.77     | edf=1.9; p=0.034| edf=1.0; p=0.421| 0.10 | -109 |
|G/B           |  1.02     | edf=1.0; p<0.001| edf=1.0; p<0.001| 0.48 | -405 |

**HadISST 1954-2015** \
R2 for G/B was higher than with waterflow data. There is still an independent temporal pattern (non-linear), but no
association with the added HadISST data.

|Variable      | Intercept | Time            |  HadISST        |  R2  | AIC  |
|--------------|-----------|-----------------|-----------------|------|------|
|Density       |  0.73     | edf=1.0; p=0.023| edf=1.0; p=0.591| 0.19 | -179 |
|Extension     |  1.07     | edf=7.7; p<0.001| edf=1.0; p=0.284| 0.33 |  -85 |
|Calcification |  0.77     | edf=1.9; p=0.017| edf=1.0; p=0.215| 0.05 | -110 |
|G/B           |  1.02     | edf=3.2; p<0.001| edf=1.0; p=0.564| 0.61 | -376 |

**SOI 1954-2015** \
R2 for G/B was higher than above variables. G/B exhibited a significant nonlinear temporal pattern over the 
study period (edf = 3.4, p < 0.001). SOI was significantly associated with G/B (edf = 1.0, p < 0.001), 
with the fitted relationship being approximately linear (G/B increases as SOI increases??).
The model explains approximately 67% of the variation in G/B.

|Variable      | Intercept | Time            |  SOI            |  R2  | AIC  |
|--------------|-----------|-----------------|-----------------|------|------|
|Density       |  0.73     | edf=1.0; p=0.029| edf=1.0; p=0.288| 0.22 | -180 |
|Extension     |  1.07     | edf=7.5; p<0.001| edf=1.0; p=0.512| 0.35 |  -84 |
|Calcification |  0.77     | edf=3.2; p=0.081| edf=1.0; p=0.038| 0.09 | -113 |
|G/B           |  1.02     | edf=3.4; p<0.001| edf=1.0; p<0.001| 0.67 | -389 |

**AMO 1954-2015** \
Adding AMO changed the observed patterns.
For Extension, the result suggests that AMO and the temporal structure of Extension are related, showing a significant
linear association.

|Variable      | Intercept | Time            |  AMO            |  R2  | AIC  |
|--------------|-----------|-----------------|-----------------|------|------|
|Density       |  0.73     | edf=1.0; p=0.029| edf=1.0; p=0.884| 0.19 | -178 |
|Extension     |  1.07     | edf=1.0; p=0.533| edf=1.0; p<0.001| 0.18 |  -87 |
|Calcification |  0.77     | edf=1.0; p<0.001| edf=1.0; p=0.072| 0.07 | -111 |
|G/B           |  1.02     | edf=3.3; p<0.001| edf=1.0; p=0.376| 0.62 | -376 |

**In conclusion** \
Four comparisons were found significants: \
* Extension ~ s(Year) + s(AMO)
* G_B ~ s(Year) + s(WF_Helena)
* G_B ~ s(Year) + s(WF_Calamar)
* G_B ~ s(Year) + s(SOI)

First, I tested the relationship between discharge and coral growth following the 1984 dredging, using
a pre/post-1984 interaction model: \

* G_B ~ s(Year) + WF_Helena * After ,

The WF_Helena had a significant positive association with G/B (p = 0.016) before 1984, and the change of G/B 
units per m<sup>3</sup> s<sup>-1</sup> was 9.9x10<sup>-5</sup>. Whereas, the post-1984 slope was not statistically
different from the pre-1984 (p = 0.902), where the change of G/B units per m<sup>3</sup> s<sup>-1</sup> was 
9.4x10<sup>-5</sup>. There was a decrease in the slope, but not significant according to these results.
There is a temporal effect on G/B, after accounting for water discharge (edf=1.9, p<0.001). The model showed an R2 of 0.61.
Therefore, we can say that there is an overall association between Santa Helena discharge and G/B, but not any
significant changes after 1984.

At this point, it is interesting to test if there is any lagged relationship among these variables to find
any potential delayed responses (for example lag1 and lag2):

|Relationship         | Intercept | Time            |  AMO            |  R2  | AIC  |
|---------------------|-----------|-----------------|-----------------|------|------|
|Extension-AMO(lag0)  |  1.07     | edf=1.0; p=0.533| edf=1.0; p<0.001| 0.18 |  -87 |
|Extension-AMO(lag1)  |  1.07     | edf=1.0; p=0.373| edf=1.0; p<0.001| 0.21 |  -87 |
|Extension-AMO(lag2)  |  1.07     | edf=3.3; p=0.068| edf=1.0; p=0.189| 0.25 |  -80 |

|Relationship         | Intercept | Time            |  AMO            |  R2  | AIC  |
|---------------------|-----------|-----------------|-----------------|------|------|
|G/B-SOI(lag0)        |  1.02     | edf=3.4; p<0.001| edf=1.0; p<0.001| 0.67 | -389 |
|G/B-SOI(lag1)        |  1.02     | edf=2.4; p<0.001| edf=1.0; p=0.229| 0.56 | -370 |
|G/B-SOI(lag2)        |  1.02     | edf=2.7; p<0.001| edf=1.0; p=0.213| 0.58 | -363 |

|Relationship         | Intercept | Time            |  WF_Helena      |  R2  | AIC  |
|---------------------|-----------|-----------------|-----------------|------|------|
|G/B-WF_Helena(lag0)  |  1.02     | edf=1.0; p<0.001| edf=1.0; p<0.001| 0.48 | -400 |
|G/B-WF_Helena(lag1)  |  1.02     | edf=2.9; p<0.001| edf=1.0; p=0.891| 0.59 | -368 |
|G/B-WF_Helena(lag2)  |  1.02     | edf=2.9; p<0.001| edf=1.0; p=0.214| 0.59 | -363 |

|Relationship         | Intercept | Time            |  WF_Calamar     |  R2  | AIC  |
|---------------------|-----------|-----------------|-----------------|------|------|
|G/B-WF_Calamar(lag0) |  1.02     | edf=1.0; p<0.001| edf=1.0; p<0.001| 0.48 | -405 |
|G/B-WF_Calamar(lag1) |  1.02     | edf=2.6; p<0.001| edf=1.0; p=0.165| 0.57 | -370 |
|G/B-WF_Calamar(lag2) |  1.02     | edf=3.0; p<0.001| edf=1.0; p=0.138| 0.61 | -364 |

These results did not show significant associations with variables at lag1 and lag2. Only the Extension and AMO at lag1 was 
sginificant, but given that AMO is a multidecadal oscillation pattern it is not clear if at lag1 is of consideration.

Now, we can continue and elaborate more complex questions, like *Does SOI still matter after accounting for discharge?*
Then we will have to test a model like this: \
* G_B ~ s(Year) + s(SOI) + s(WF_Helena)
* G_B ~ s(Year) + s(SOI) + s(WF_Calamar)

|Variable   | Intercept | Time            |  SOI            |  WF             |  R2  | AIC  |
|-----------|-----------|-----------------|-----------------|-----------------|------|------|
|G/B-Helena |  1.01     | edf=1.8; p<0.001| edf=1.0; p=0.366| edf=1.0; p<0.001| 0.61 | -397 |
|G/B-Calamar|  1.02     | edf=1.0; p<0.001| edf=1.6; p=0.462| edf=1.0; p<0.001| 0.49 | -402 |
