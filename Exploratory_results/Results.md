# Exploratory results

## Monthly time series (1954-2015)
* Skeletal density (g cm<sup>-3</sup>)
* Linear extension (cm mo<sup>-1</sup>)
* Calcification (g cm<sup>-2</sup> mo<sup>-1</sup>)
* Sea surface temperature (HadISST)
* Water discharge (Sta Helena)(data from 1954-1981 were modeled using Calamar data)
* Water discharge (Calamar)
* SOI
* AMO

## Preliminary tests using raw data (no transformations or treatments)

### Normality test (raw data)

**Test:** Shapiro-Wilk test for normality \
**Interpretation:** If p < 0.05, then the distribution is non-normal

|Variable      | Statistic | p-value  |
|--------------|-----------|----------|
|Density       |  0.99     |  0.000 * |
|Extension     |  0.96     |  0.000 * |
|Calcification |  0.97     |  0.000 * |
|G/B           |  0.99     |  0.001 * |
|WF_Helena     |  0.96     |  0.000 * |
|WF_Calamar    |  0.98     |  0.000 * |
|HadISST       |  0.97     |  0.000 * |
|SOI           |  0.99     |  0.001 * |
|AMO           |  0.99     |  0.013 * |


|Variable      | Statistic | p-value  |
|--------------|-----------|----------|
|Density       | -2.50     |  0.117   |
|Extension     | -4.61     |  0.000 * |
|Calcification | -5.00     |  0.000 * |
|G/B           | -3.26     |  0.016 * |
|WF_Helena     | -2.58     |  0.097   |
|WF_Calamar    | -6.27     |  0.000 * |
|HadISST       | -4.55     |  0.000 * |
|SOI           | -7.48     |  0.000 * |
|AMO           | -2.13     |  0.231   |