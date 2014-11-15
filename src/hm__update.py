#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import datetime
import time
import math
import rrdtool  


#python2 vs python3? ==> use python2
#- only the rrdtool package for python2 seeos to be installed 
#   by sudo apt-get install python-rrdtool
#- python2 seems to understand also the python3 format strings 


#Read current data from Nexus weather station 
#  the option -iU ensures that invalid data are set to "U" as requried by rrdtool
te923con = os.popen("./te923con -iU")  
data = te923con.read()
#expected output:
#1416078280:21.90:51:8.00:86:U:U:U:U:U:U:7.70:83:956.8:U:3:0:U:U:U:U:0
data=data.strip()
fields=data.split(":")
#print(fields)

epoch = fields[0]    #Timestamp in seconds since 01-Jan-1970 UTC
T0 = fields[1]       #Temperature from weather station
H0 = fields[2]       #Humidity from weather station
T1 = fields[3]       #Temperature from remote sensor channel 1
H1 = fields[4]       #Humidity from  remote sensor channel 1
T5 = fields[11]      #Temperature from remote sensor channel 5
H5 = fields[12]      #Humidity from  remote sensor channel 5
P0 = fields[13]      #Barometric pressure in mbar
FC = fields[15]      #Weather forecast


TK="U"
HK="U"


DateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(epoch)))
Time = time.strftime("%H:%M:%S", time.localtime(float(epoch)))
print("<title>HM {0}</title>".format(Time))
print("{0}<BR>".format(DateTime))
print("CH0: {0}&deg;C {1}%<BR>".format(T0, H0))
print("CH1: {0}&deg;C {1}%<BR>".format(T1, H1))
print("CH5: {0}&deg;C {1}%<BR>".format(T5, H5))
print('<img src="temperatur.png">')

rrd_data = epoch+":"+T0+":"+H0+":"+P0+":"+T1+":"+H1+":"+T5+":"+H5+":"+TK+":"+HK
print(rrd_data)
rrdtool.update("home_metering.rrd" , rrd_data)
'''
rrdtool.graph('temperatur.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 hour',
              '--end', 'now',
              '--vertical-label', 'Temperatur [°C]',
              '--title', 'Temperaturverlauf 49/12',
              'DEF:T0=home_metering.rrd:T_Buero:AVERAGE',
              'LINE2:T_Buero#00FF00:Buero',
              'VDEF:T_Buero_last=T_Buero,LAST',
              'GPRINT:T_Buero_last:%.1lf °C',
              'DEF:T_Aussen=temperature.rrd:T_Aussen:AVERAGE',
              'LINE2:T_Aussen#0000FF:Aussen',
              'VDEF:T_Aussen_last=T_Aussen,LAST',
              'GPRINT:T_Aussen_last:%.1lf °C')
'''
 
