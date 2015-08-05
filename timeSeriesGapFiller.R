# wps.des: timeSeriesGapFiller, title = Fills in gaps in a time series, 
# abstract = Fills data gaps in time series; 
# wps.in: url, string;
# wps.out: output, text;
library(WaterML)
library(xts)
#url <- 'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:140&variable=CHMI-H:TEPLOTA&startDate=2015-07-01&endDate=2015-07-10&authToken='
#url<- 'http://hydrodata.info/chmi-h/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-H:140&variable=CHMI-H:TEPLOTA&startDate=2015-07-01&endDate=2015-07-10&authToken='
#url <-'http://hydrodata.info/chmi-d/cuahsi_1_1.asmx/GetValuesObject?location=CHMI-D:171~variable!CHMI-D:PRUTOK~startDate!2014-07-01~endDate!2015-07-30~authToken!'
server <- gsub("!", "=", url)
server <- gsub("~", "&", server)
values <- GetValues(server)
#get time series object
ts <- xts(values$DataValue, order.by = values$time)
#convert to weekly

date<- as.Date(as.POSIXlt(time(ts)))
value <- as.double(ts)
data <- data.frame(date,value)
final <- xts(data$value, order.by = date)
final_ts<-na.approx(final)
output <- "Modified Values"
write.zoo(final_ts,output)
#plot(final_ts)
