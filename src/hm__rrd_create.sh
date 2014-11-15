rrdtool create home_metering.rrd --step 900 \
DS:T0:GAUGE:1800:-40:80 \
DS:H0:GAUGE:1800:0:100 \
DS:P0:GAUGE:1800:0:1500 \
DS:T1:GAUGE:1800:-40:80 \
DS:H1:GAUGE:1800:0:100 \
DS:T5:GAUGE:1800:-40:80 \
DS:H5:GAUGE:1800:0:100 \
DS:TK:GAUGE:1800:-40:80 \
DS:HK:GAUGE:1800:0:100 \
RRA:AVERAGE:0.5:1:2976 \
RRA:MIN:0.5:96:3650 \
RRA:MAX:0.5:96:3650 \
RRA:AVERAGE:0.5:96:3650 

#Interval 900 sec = 15 min
#Data source
#T0,H0,P0: Temperature, Humidity, Pressure from weather station
#T1,H1: Temperature, Humidity from remote sensor on channel 1
#T5,H5: Temperature, Humidity from remote sensor on channel 5
#TK,HK: Temperature, Humidity from remote sensor from cellar
#Store raw data for 2976*15min = 1 month
#MIN/MAX/AVERAGE over 96*15 min = 1 day, store 3650 days = 10 years
#===> resulting file size:  ca 1MB

