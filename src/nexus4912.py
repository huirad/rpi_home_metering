#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import datetime
import time
import math
import rrdtool  


#python2 vs python3? ==> use python2
#- only the rrdtool package for python2 seeoms to be installed 
#   by sudo apt-get install python-rrdtool
#- python2 seems to understand also the python3 format strings 


#auslesen der Nexusdaten mit te923con und Aufbereitung der Daten zur Weiterverarbeitung
te923con = os.popen("./te923con")  
data = te923con.read()
data=data.strip()
fields=data.split(":")
#print(fields)

epoch = fields[0] #timestamp in seconds since 01-Jan-1970
T_Buero = fields[1]
RH_Buero = fields[2]
T_Aussen = fields[3]
RH_Aussen = fields[4]
T_Oben = fields[11]
RH_Oben = fields[12]
Luftdruck = fields[13]


DateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(epoch)))
Time = time.strftime("%H:%M:%S", time.localtime(float(epoch)))
print("<title>Nexus {0}</title>".format(Time))
print("{0}<BR>".format(DateTime))
print("Buero: {0}&deg;C {1}%<BR>".format(T_Buero, RH_Buero))
print("Aussen: {0}&deg;C {1}%<BR>".format(T_Aussen, RH_Aussen))
print("Oben: {0}&deg;C {1}%<BR>".format(T_Oben, RH_Oben))
print('<img src="temperatur.png">')

rrd_data = epoch+":"+T_Buero+":"+T_Aussen+":"+T_Oben
rrdtool.update("temperature.rrd" , rrd_data)
rrdtool.graph('temperatur.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 hour',
              '--end', 'now',
              '--vertical-label', 'Temperatur [°C]',
              '--title', 'Temperaturverlauf 49/12',
              'DEF:T_Buero=temperature.rrd:T_Buero:AVERAGE',
              'LINE2:T_Buero#00FF00:Buero',
              'VDEF:T_Buero_last=T_Buero,LAST',
              'GPRINT:T_Buero_last:%.1lf °C',
              'DEF:T_Aussen=temperature.rrd:T_Aussen:AVERAGE',
              'LINE2:T_Aussen#0000FF:Aussen',
              'VDEF:T_Aussen_last=T_Aussen,LAST',
              'GPRINT:T_Aussen_last:%.1lf °C')

 
