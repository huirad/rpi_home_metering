rrdtool create co2_ppm.rrd --step 900 \
DS:CO2:GAUGE:1800:0:10000 \
RRA:AVERAGE:0.5:1:2976 \
RRA:MIN:0.5:96:3650 \
RRA:MAX:0.5:96:3650 \
RRA:AVERAGE:0.5:96:3650 

#Interval 900 sec = 15 min
#Data source
#CO2: CO2 in ppm
#Store raw data for 2976*15min = 1 month
#MIN/MAX/AVERAGE over 96*15 min = 1 day, store 3650 days = 10 years
#===> resulting file size:  ca 112kB

