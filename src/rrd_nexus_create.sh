rrdtool create temperature.rrd --step 60 \
DS:T_Buero:GAUGE:120:-40:80 \
DS:T_Aussen:GAUGE:120:-40:80 \
DS:T_Oben:GAUGE:120:-40:80 \
RRA:AVERAGE:0.5:1:1440 \
RRA:MIN:0.5:60:168 \
RRA:MAX:0.5:60:168 \
RRA:AVERAGE:0.5:60:168

#Interval 60 sec = 1 min
#Store raw data for 1440 min = 1 day
#MIN/MAX/AVERAGE over 60 min = 1 hour, store 168 hours = 1 week

