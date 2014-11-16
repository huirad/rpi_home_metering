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

#Create HTML output
DateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(epoch)))
Time = time.strftime("%H:%M:%S", time.localtime(float(epoch)))
print("<title>{0}</title>".format(Time))
print("{0}<BR>".format(DateTime))
print("CH0: {0}&deg;C {1}%<BR>".format(T0, H0))
print("CH1: {0}&deg;C {1}%<BR>".format(T1, H1))
print("CH5: {0}&deg;C {1}%<BR>".format(T5, H5))
print("CHK: {0}&deg;C {1}%<BR>".format(TK, HK))
print('<img src="temp_day.png">')

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
              'LINE2:T5#FF0000:Oben',
              'VDEF:T5_last=T5,LAST',
              'GPRINT:T5_last:%.1lf °C',
              'DEF:TK=home_metering.rrd:TK:AVERAGE',
              'LINE2:TK#000000:Keller',
              'VDEF:TK_last=TK,LAST',
              'GPRINT:TK_last:%.1lf °C'              
              )
