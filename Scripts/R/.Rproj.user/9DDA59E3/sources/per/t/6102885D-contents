## Script to run GAMMs

library(readxl)
library(dplyr)
library(stringr)
library(mgcv)
library(nlme)


file1 <- "E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed\\coral_growth_monthly_v2.xlsx"
file2 <- "E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed\\coral_lumn_monthly.xlsx"
file3 <- "E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed\\env_monthly.xlsx"
coral_data <- read_excel(file1,sheet=2)
lumin_data <- read_excel(file2,sheet=2)
envir_data <- read_excel(file3,sheet=1)

## Fit coral data to 1954-2015
coral_data_fit <- coral_data %>% slice(1:744)

## Select columns
cols_lumin <- lumin_data %>% select(Y.M., `G/B`)
cols_envir <- envir_data %>% select(Y.M.,WF_Helena,WF_Calamar,HadISST,SOI,AMO)

## Merge all columns into a single data frame
df <- coral_data_fit %>% 
  left_join(cols_lumin, by = "Y.M.") %>% 
  left_join(cols_envir, by = "Y.M.") %>%
  arrange(Y.M.) #sorted

## Create date and time columns
df$Date <- as.Date(
  paste(df$Year, df$Month, "01", sep = "-"))
df$Time <- 1:nrow(df)

## Fit a GAM (without autocorrelation)
gam1 <- gam(
  Density ~
    s(Time) +
    s(Month, bs = "cc", k = 12) +
    s(WF_Helena) +
    s(WF_Calamar) +
    s(HadISST) +
    s(SOI) + s(AMO),
  method = "REML",
  data = df
)

summary(gam1)

## Check residual autocorrelation
acf(residuals(gam1))

## Fit the GAMM
## This estimates an AR(1) correlation in the residuals.
gamm1 <- gamm(
  (`G/B`) ~
    s(Time) +
    s(Month, bs="cc", k=12) +
    s(WF_Helena) +
    s(WF_Calamar) +
    s(HadISST) +
    s(SOI) + s(AMO),
  correlation = corAR1(),
  data=df,
  method="REML"
)

## Check whether AR(1) was sufficient
acf(residuals(gamm1$lme, type="normalized"))

## Visualize the smooths
plot(gamm1$gam,
     pages=1,
     shade=TRUE)

summary(gamm1$gam) #smooth
summary(gamm1$lme) #autocorrelation