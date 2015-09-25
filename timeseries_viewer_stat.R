# wps.des: timeseries_viewer_stat, title = Statistics for viewer, 
# abstract = Displays basic statistics; 
# wps.in: url, string;
# wps.out: output, text;
library(WaterML)
library(xts)
library(lubridate)
#url <-'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location!CHMI-H:140~variable!CHMI-H:TEPLOTA~startDate!2015-07-01~endDate!2015-07-10~authToken!'
#TEST
server <- gsub("!", "=", url)
server <- gsub("~", "&", server)

values <- GetValues(server)
#get time series object
ts <- xts(values$DataValue, order.by = values$time)
#convert to weekly

#rm(list =ls())
ts_double <- data.frame(ts)

mean_ts <- mean(ts_double$ts,na.rm=TRUE)
median_ts<- median(ts_double$ts,na.rm=TRUE)
standard_ts <- sd(ts_double$ts,na.rm=TRUE)


stat_val <-c(mean_ts,median_ts,standard_ts)


final_stat <- stat_val

output <- "Statistics Values"
write.zoo(final_stat,output)
