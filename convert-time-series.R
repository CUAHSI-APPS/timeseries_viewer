# wps.des: timeSeriesConverter, title = Convert time series to weekly, 
# abstract = Convert time series to weekly; 
# wps.in: url, string;
# wps.in: interval, string;
# wps.in: stat, string;
# wps.out: output, text;
library(WaterML)
library(xts)
library(lubridate)
#url <-'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location!CHMI-H:140~variable!CHMI-H:TEPLOTA~startDate!2015-07-01~endDate!2015-07-10~authToken!'
server <- gsub("!", "=", url)
server <- gsub("~", "&", server)
#TEST
#server <- 'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:140&variable=CHMI-H:TEPLOTA&startDate=2015-07-01&endDate=2015-07-10&authToken='
#server <- 'http://worldwater.byu.edu/app/index.php/byu_test_justin/services/cuahsi_1_1.asmx/GetValuesObject?location=byu_test_justin:B-Lw&variable=byu_test_justin:WATER&startDate=&endDate='
#interval <- "weekly"
#server <- 'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:841&variable=CHMI-H:SRAZKY&startDate=2015-07-01&endDate=2015-07-10&authToken='
#stat <- 'mean'
values <- GetValues(server)
#get time series object
ts <- xts(values$DataValue, order.by = values$time)
#convert to weekly

if (interval == "daily"){
  ts_daily <-apply.daily(ts,stat)
  date<- as.Date(as.POSIXlt(time(ts_daily)))
  value <- as.double(ts_daily)
  monthly_data <- data.frame(date,value)
  final_ts <- xts(monthly_data$value, order.by = date)
  
}
if (interval == "weekly")
{
  ts_weekly <- apply.weekly(ts,stat)
  final_ts <- ts_weekly
}
#convert to monthly
if (interval == "monthly")
{
  ts_monthly<- apply.monthly(ts, stat)
  #Converting the time so it displays as the first day of the month
  date<- as.Date(as.data.frame.Date(time(ts_monthly)))
  value <- as.double(ts_monthly)
  monthly_data <- data.frame(date,value)
  final_ts <- xts(monthly_data$value, order.by = date)
}

#plot(ts_weekly)
#plot(ts)
#plot(ts_monthly)
#plot(ts_daily)
#plot(final_ts)
#write the output
output <- "Weekly Values"
write.zoo(final_ts,output)
