## Script to run GAMMs

library(readxl)
library(dplyr)
library(stringr)
library(mgcv)
library(nlme)
library(ggplot2)
library(ggh4x)
library(tidyverse)

## Load files
file1 <- "E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed\\coral_growth_yr_v2.xlsx"
file2 <- "E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed\\coral_lumn_yr.xlsx"
file3 <- "E:\\GDrive\\Academicos\\Articulos\\Pendientes\\Varadero growth rates\\Data_processed\\env_yr.xlsx"
coral_data <- read_excel(file1,sheet=2)
lumin_data <- read_excel(file2,sheet=1)
envir_data <- read_excel(file3,sheet=1)

## Fit coral data to 1954-2015
coral_data_fit <- coral_data %>% slice(1:62)
lumin_data_fit <- lumin_data %>% slice(1:62)

## Select columns
cols_lumin <- lumin_data_fit %>% select(Year, `G/B`)
cols_envir <- envir_data %>% select(Year,WF_Helena,WF_Calamar,HadISST,SOI,AMO)

## Merge all columns into a single data frame
df <- coral_data_fit %>% 
  left_join(cols_lumin, by = "Year") %>% 
  left_join(cols_envir, by = "Year") %>%
  arrange(Year) #sorted

## Create date and time columns
#df$Date <- as.Date(
#  paste(df$Year, df$Month, "01", sep = "-"))
df$Time <- 1:nrow(df)

# Convert to LONG format (Crucial step for subplots)
long_data <- df %>%
  pivot_longer(cols = c(Density, Extension, Calcification, `G/B`,
                        WF_Helena, WF_Calamar, HadISST, SOI, AMO), 
               names_to = "Variable", values_to = "Value")

# --- Step 2: Fit GAMM to each variable automatically ---
## to save models
models <- list()

# We split the data by "Variable", run the model, and extract the predictions
nested_plots_data <- long_data %>%
  group_by(Variable) %>%
  do({
    # Fit the exact same model configuration for the current variable group
    model <- gamm(
      Value ~ s(Time, bs = "cr", k = 62),
      data = .,
      correlation = corARMA(form = ~ Time, p = 1)
    )
    # Save model using variable name
    models[[unique(.$Variable)]] <<- model
    # Predict the trend (excluding seasonality)
    pred_df <- data.frame(Time = .$Time)
    preds <- predict(model$gam, newdata = pred_df, type = "response", se.fit = TRUE)
    # Attach predictions back to this variable's dataframe
    data.frame(
      Date = .$Year,
      Raw_Value = .$Value,
      Trend = preds$fit,
      Lower_CI = preds$fit - (1.96 * preds$se.fit),
      Upper_CI = preds$fit + (1.96 * preds$se.fit)
    )
  }) %>%
  ungroup()

### Select variables (growth or environmental)
df_growth <- nested_plots_data %>% 
  filter(Variable %in% c("Density", "Extension", "Calcification", "G/B")) %>%
  mutate(Variable = factor(Variable, levels = c("Density", "Extension", "Calcification", "G/B")))
df_envir <- nested_plots_data %>% 
  filter(Variable %in% c("WF_Helena", "WF_Calamar", "HadISST","SOI","AMO")) %>%
  mutate(Variable = factor(Variable, levels = c("WF_Helena", "WF_Calamar", "HadISST","SOI","AMO")))

### Select dataframe for plot
data_plot = df_growth

# --- Step 3: Define Aligned Grid Breaks ---
grid_breaks1 <- seq(from = min(data_plot$Date), 
                        to = max(data_plot$Date), by = 10)
grid_breaks2 <- seq(from = min(data_plot$Date), 
                        to = max(data_plot$Date), by = 5)

# --- Step 4: Plot using Facet Wrap ---
ggplot(data_plot, aes(x = Date)) +
  # Raw data per variable
  geom_line(aes(y = Raw_Value), color = "black", size = 0.2,alpha = 0.9) +
  # Shaded 95% Confidence Interval ribbon per variable
  geom_ribbon(aes(ymin = Lower_CI, ymax = Upper_CI), fill = "blue", alpha = 0.15) +
  # Trend line per variable
  geom_line(aes(y = Trend), color = "blue", size = 0.5) +
  # Aligned X-Axis (Years only, perfectly centered)
  scale_x_continuous(breaks = grid_breaks1, minor_breaks = grid_breaks2) +
  # GENERATE SUBPLOTS
  # scales = "free_y" lets every variable keep its original scale
  # ncol = 1 stacks them vertically, which makes comparing timelines easy
  facet_grid(Variable ~ .,
             scales = "free_y",
             switch = "y") + 
  labs(
    subtitle = NULL,
    x = "Year", y = NULL
  ) +
  #theme_minimal() +
  theme_bw() +
  theme(
    axis.text.x = element_text(angle = 0, hjust = 0.5, vjust = 1),
    strip.placement = "outside",
    strip.background = element_blank(),
    strip.text.y.left = element_text(
      angle = 90,
      face = "bold",
      size = 9),
    panel.border = element_rect(
      colour = "black",
      fill = NA,
      linewidth = 0.6
    )
  )

## Inspect models
summary(models$AMO$gam) # GAM model
## Check whether AR(1) was sufficient
summary(models$Density$lme) #autocorrelation
acf(residuals(models$Density$lme, type="normalized")) # plot
## Visualize the smooths
plot(models$Density$gam,
     pages=1,
     shade=TRUE)

### Save figure
ggsave(
  "GAM_growth_annual.tiff",
  width = 90,
  height = 120,
  units = "mm",
  dpi = 300
)

