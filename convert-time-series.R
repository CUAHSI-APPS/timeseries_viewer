# wps.des: convert-time-series, title = Convert time series to weekly, 
# abstract = Convert time series to new time frame; 
# wps.in: url, string;
# wps.in: interval, string;
# wps.in: stat, string;
# wps.out: output, text;
library(WaterML)
library(xts)
library(lubridate)
#water ml 2 test
#server <- 'http://worldwater.byu.edu/app/index.php/byu_test_justin/services/cuahsi_1_1.asmx/GetValues?location=byu_test_justin:B-Lw&variable=byu_test_justin:WATER&startDate=&endDate='
#url <-'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location!CHMI-H:140~variable!CHMI-H:TEPLOTA~startDate!2015-07-01~endDate!2015-07-10~authToken!'
#TEST
#server <- 'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:140&variable=CHMI-H:TEPLOTA&startDate=2015-07-01&endDate=2015-07-10&authToken='
#server <- 'http://worldwater.byu.edu/app/index.php/byu_test_justin/services/cuahsi_1_1.asmx/GetValuesObject?location=byu_test_justin:B-Lw&variable=byu_test_justin:WATER&startDate=&endDate='

#server <- 'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:841&variable=CHMI-H:SRAZKY&startDate=2015-07-01&endDate=2015-07-10&authToken='
#NA values
server <-'http://hydrodata.info/chmi-d/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-D:171&variable=CHMI-D:PRUTOK&startDate=2014-07-01&endDate=2015-07-30&authToken='
#stat <- 'mean'
interval <- "weekly"
#url <- 'http://worldwater.byu.edu/app/index.php/byu_test_justin/services/cuahsi_1_1.asmx/GetValues?location=byu_test_justin:B-Lw&variable=byu_test_justin:WATER&startDate=&endDate='

server <- gsub("!", "=", url)
server <- gsub("~", "&", server)
values <- GetValues(server)
#get time series object
ts <- xts(values$DataValue, order.by = values$time)
#convert to weekly

if (interval == "daily"){
  ts_daily <-apply.daily(ts,stat)
  date<- as.Date(as.POSIXlt(time(ts_daily)))
  value <- as.double(ts_daily)
  daily_data <- data.frame(date,value)
  final_ts <- xts(daily_data$value, order.by = date)
  
}
if (interval == "weekly")
{
  ts_weekly <- apply.weekly(ts,stat)
  date<- as.Date(as.POSIXlt(time(ts_weekly)))
  value <- as.double(ts_weekly)
  weekly_data <- data.frame(date,value)
  final_ts <- xts(weekly_data$value, order.by = date)
}
#convert to monthly
if (interval == "monthly")
{
  ts_monthly<- apply.monthly(ts, stat)
  #Converting the time so it displays as the first day of the month and trimming time of day off
  date<- as.Date(as.yearmon(time(ts_monthly)))
  value <- as.double(ts_monthly)
  monthly_data <- data.frame(date,value)
  final_ts <- xts(monthly_data$value, order.by = date)
}
if (interval == "yearly")
{
  ts_yearly <- apply.yearly(ts,stat)
  date<- as.Date(as.POSIXlt(time(ts_yearly)))
  value <- as.double(ts_yearly)
  yearly_data <- data.frame(date,value)
  final_ts <- xts(yearly_data$value, order.by = date)
}

#plot(ts_weekly)
#plot(ts)
#plot(ts_monthly)
#plot(ts_daily)
#plot(final_ts)
#rm(list=ls())
#write the output
output <- "Weekly Values"
write.zoo(final_ts,output)
