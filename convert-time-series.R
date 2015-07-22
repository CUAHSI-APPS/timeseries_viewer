# wps.des: timeSeriesConverter, title = Convert time series to weekly, 
# abstract = Convert time series to weekly; 
# wps.in: url, text;
# wps.in: interval, text;
# wps.in: stat, text;
# wps.out: output, text;
library(WaterML)
library(xts)

#server <- URLdecode(url1)
server <- "http://worldwater.byu.edu/app/index.php/byu_test_justin/services/cuahsi_1_1.asmx/GetValuesObject?location=byu_test_justin:B-Lw&variable=byu_test_justin:WATER&startDate=&endDate="
values <- GetValues(server)



#get time series object
ts <- xts(values$DataValue, order.by = values$time)

#convert to weekly
ts_weekly<- apply.monthly(ts, mean)
#Converting the time so it displays as the first day of the month
date<- as.Date(as.yearmon(time(ts_weekly)))
value <- as.double(ts_weekly)

weekly_data <- data.frame(date,value)

final_ts <- xts(weekly_data$value, order.by = date)
#plot(ts_weekly)
#plot(final_ts)



#write the output

output <- "Weekly Values"
write.zoo(final_ts,output)

