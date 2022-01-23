#! /usr/bin/env python

#python2 has to be used because only the rrdtool package for python2 is available
#   by sudo apt-get install python-rrdtool
#   TODO CHECK installation of rrdtool for python3 via pip3:
#      sudo pip3 install rrdtool
#

#The program starts here
import sys, serial, time, datetime, struct
import rrdtool  

#global variables
verbose = 0     #debug level

def openSerial(device):
    #For reading 654 bytes at 9600 baud, less than 1 second should be sufficient
    #But on Windows 7, I observed data loss, so I had to increase the timeout to 2 seconds.
    #Maybe this is a USB-serial issue.
    ser = serial.Serial(device, 57600, timeout=2)
    return ser

def clearInput(ser):
    time.sleep(0.1)
    while ser.inWaiting():
        if verbose>=2:
            print("{0} bytes inWaiting".format(ser.inWaiting()))
        ser.flushInput()
        time.sleep(0.1)

def sendRequest(ser, request):
    n = ser.write(request)
    if verbose>=2:
        print("{0} bytes written".format(n))
    return n

def readReply(ser, n_expected_bytes):
    result=ser.read(n_expected_bytes)
    result=struct.unpack('BB', result) #needed for python2!
    if verbose>=2:
        print("{0} bytes read".format(len(result)))
        if len(result):
            print("{0:2X}".format(result[0]))
    if len(result) < n_expected_bytes:
        print("{0} bytes received, but {1} expected!!!\n".format(len(result), n_expected_bytes));
    return result


def readCPM(ser):
    cpm = None
    clearInput(ser)
    req = bytes (b"<GETCPM>>")
    sendRequest(ser, req)
    reply = readReply(ser, 2)
    if (len(reply) == 2):
        cpm = reply[0]*256+reply[1]
        #print("{0} CPM".format(cpm))
    else:
        pass
        #print("Cannot read CPM")
    return cpm



##main()
epoch = time.time()
ser = openSerial("/dev/ttyUSB0")
clearInput(ser)
cpm = readCPM(ser)
ser.close()

#Update the RRD database and create graphs from the RRD data
rrd_data = "{0:d}:{1:d}".format(int(epoch), cpm)
print(rrd_data)
#print(type(rrd_data))
rrdtool.update("geiger_count.rrd" , rrd_data)
rrdtool.graph('www/gc_day.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 day',
              '--end', 'now',
              '--vertical-label', 'Geiger CPM',
              '--title', 'Geiger CPM 24h',
              'DEF:GC=geiger_count.rrd:GC:AVERAGE',
              'LINE2:GC#00FF00:Geiger',
              'VDEF:GC_last=GC,LAST',
              'GPRINT:GC_last:%.1lf CPM',
              )
rrdtool.graph('www/gc_minmax.png',
              '--imgformat', 'PNG',
              '--width', '540',
              '--height', '100',
              '--start', 'now -1 month',
              '--end', 'now',
              '--step', '86400',
              '--vertical-label', 'Geiger CPM',
              '--title', 'Geiger CPM 1 Monat',
              'DEF:GCMAX=geiger_count.rrd:GC:MAX',
              'LINE2:GCMAX#0000FF:GCMAX',
              'DEF:GCMIN=geiger_count.rrd:GC:MIN',
              'LINE2:GCMIN#000080:GCMIN',
              )   
