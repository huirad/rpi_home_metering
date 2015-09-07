#!/usr/bin/python
# -*- coding: latin-1 -*-

#python2 has to be used because only the rrdtool package for python2 is available
#   by sudo apt-get install python-rrdtool
#the coding has to be set to latin to allow use of the ° character


import os
import datetime
import time
import math
import rrdtool  
from urllib import urlopen
import re

def dewpoint(t, rh):
    """Calculate the dew point of water in air at normal pressure.

    The dew point is calculated using the Magnus formula as
    described in the english Wikipedia article or the Sensirion 
    application notes. 
    The Magnus parameter set from D. Sonntag is used.
    
    Parameters
    ----------
    t: float
        Temperature in °C
    rh: float
        Relative Humidity in %
        
    Returns
    -------
    float
        The dew point temperature in °C
    """
    h = (math.log10(rh)-2)/0.4343 + (17.62*t)/(243.12+t); 
    dp    = 243.12*h/(17.62-h); # this is the dew point in °Celsius
    return dp


#Read current data from Nexus weather station 
#  the option -iU ensures that invalid data are set to "U" as requried by rrdtool
te923con = os.popen("./te923con -iU")  
data = te923con.read()
#expected output looks like "1416078280:21.90:51:8.00:86:U:U:U:U:U:U:7.70:83:956.8:U:3:0:U:U:U:U:0"
data=data.strip()
fields=data.split(":")
epoch = fields[0]    #Timestamp in seconds since 01-Jan-1970 UTC
T0 = fields[1]       #Temperature from weather station
H0 = fields[2]       #Humidity from weather station
T1 = fields[3]       #Temperature from remote sensor channel 1
H1 = fields[4]       #Humidity from  remote sensor channel 1
T5 = fields[11]      #Temperature from remote sensor channel 5
H5 = fields[12]      #Humidity from  remote sensor channel 5
P0 = fields[13]      #Barometric pressure in mbar
FC = fields[15]      #Weather forecast

#Read Temperature/Humidity data from the AVR webserver
TK = "U"
HK = "U"
""" temporarily disable
try:
    for line in urlopen('http://192.168.2.150/'):
        line = line.decode('latin_1').rstrip()  # Decoding the binary data to text.
        if 'Temperatur' in line: #expected output looks like "Temperatur   : 18.9°C"
            t = re.findall("([+-]?\d+.?\d+)",line)
            if len(t) > 0:
                TK = t[0].encode('latin_1')
        if 'Feuchte ' in line: #expected output looks like "Rel. Feuchte : 66%"
            t = re.findall("([+-]?\d+.?\d+)",line)
            if len(t) > 0:
                HK = t[0].encode('latin_1')
except:
    pass
"""    

#Create HTML output
DateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(epoch)))
Time = time.strftime("%H:%M:%S", time.localtime(float(epoch)))
try: 
    DP0 = dewpoint(float(T0), float(H0))
except:    
    DP0 = 0.0
try:
    DP1 = dewpoint(float(T1), float(H1))
except:
    DP1 = 0.0
try:
    DP5 = dewpoint(float(T5), float(H5))
except:
    DP5 = 0.0
try:
    DPK = dewpoint(float(TK), float(HK))
except:
    DPK = 0.0

    
print("<title>{0}</title>".format(Time))
print("{0}<BR>".format(DateTime))
print("CH0: {0}&deg;C {1}% [DP: {2:.1f}&deg;C]<BR>".format(T0, H0, DP0))
print("FC:  {0}  | {1}mbar<BR>".format(FC, P0))
print("CH1: {0}&deg;C {1}% [DP: {2:.1f}&deg;C]<BR>".format(T1, H1, DP1))
print("CH5: {0}&deg;C {1}% [DP: {2:.1f}&deg;C]<BR>".format(T5, H5, DP5))
print("CHK: {0}&deg;C {1}% [DP: {2:.1f}&deg;C]<BR>".format(TK, HK, DPK))
print('<BR><img src="temp_day.png">')
print('<BR><img src="humi_day.png">')
print('<BR><img src="t1t51_minmax.png">')

#TODO: decode forecast
#0 - heavy snow
#1 - little snow
#2 - heavy rain
#3 - little rain
#4 - cloudy
#5 - some clouds
#6 - sunny


#push data to data.sparkfun.com
try:
    with open ('sparkfun_keys', 'r') as f:
        public_key = f.readline().strip()
        private_key = f.readline().strip()
        url = 'http://data.sparkfun.com/input/'+public_key+'?private_key='+private_key
        url = url + '&h0='+H0
        url = url + '&t0='+T0
        url = url + '&p0='+P0
        url = url + '&h1='+H1
        url = url + '&t1='+T1
        url = url + '&h5='+H5
        url = url + '&t5='+T5        
        #print(url)
        urlopen(url)
except:
    print('except')
    pass




#Update the RRD database and create graphs from the RRD data
rrd_data = epoch+":"+T0+":"+H0+":"+P0+":"+T1+":"+H1+":"+T5+":"+H5+":"+TK+":"+HK
#print(rrd_data)
#print(type(rrd_data))
rrdtool.update("home_metering.rrd" , rrd_data)
rrdtool.graph('www/temp_day.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 day',
              '--end', 'now',
              '--vertical-label', 'Temperatur [°C]',
              '--title', 'Temperatur 24h',
              'DEF:T0=home_metering.rrd:T0:AVERAGE',
              'LINE2:T0#00FF00:Innen',
              'VDEF:T0_last=T0,LAST',
              'GPRINT:T0_last:%.1lf °C',
              'DEF:T1=home_metering.rrd:T1:AVERAGE',
              'LINE2:T1#0000FF:Aussen',
              'VDEF:T1_last=T1,LAST',
              'GPRINT:T1_last:%.1lf °C',
              'DEF:T5=home_metering.rrd:T5:AVERAGE',
              'LINE2:T5#FF0000:Mal hier mal da',
              'VDEF:T5_last=T5,LAST',
              'GPRINT:T5_last:%.1lf °C',
              'DEF:TK=home_metering.rrd:TK:AVERAGE',
              'LINE2:TK#000000:Keller',
              'VDEF:TK_last=TK,LAST',
              'GPRINT:TK_last:%.1lf °C'
              )
rrdtool.graph('www/humi_day.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 day',
              '--end', 'now',
              '--vertical-label', 'Rel. Feuchte [%]',
              '--title', 'Luftfeuchtigkeit 24h',
              'DEF:H0=home_metering.rrd:H0:AVERAGE',
              'LINE2:H0#00FF00:Innen',
              'VDEF:H0_last=H0,LAST',
              'GPRINT:H0_last:%.0lf %%',
              'DEF:H1=home_metering.rrd:H1:AVERAGE',
              'LINE2:H1#0000FF:Aussen',
              'VDEF:H1_last=H1,LAST',
              'GPRINT:H1_last:%.0lf %%',
              'DEF:H5=home_metering.rrd:H5:AVERAGE',
              'LINE2:H5#FF0000:Mal hier mal da',
              'VDEF:H5_last=H5,LAST',
              'GPRINT:H5_last:%.0lf %%',
              'DEF:HK=home_metering.rrd:HK:AVERAGE',
              'LINE2:HK#000000:Keller',
              'VDEF:HK_last=HK,LAST',
              'GPRINT:HK_last:%.0lf %%'
              )
rrdtool.graph('www/t1t51_minmax.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 month',
              '--end', 'now',
              '--vertical-label', 'Temperatur [°C]',
              '--title', 'Temperatur 1 Monat',
              'DEF:T1MAX=home_metering.rrd:T1:MAX',
              'LINE2:T1MAX#0000FF:T1MAX',
              'DEF:T1MIN=home_metering.rrd:T1:MIN',
              'LINE2:T1MIN#000080:T1MIN',
              'DEF:T5MAX=home_metering.rrd:T5:MAX',
              'LINE2:T5MAX#FF0000:T5MAX',
              'DEF:T5MIN=home_metering.rrd:T5:MIN',
              'LINE2:T5MIN#800000:T5MIN'
              )              
