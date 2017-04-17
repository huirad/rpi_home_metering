#! /usr/bin/env python3 

#The program starts here
import sys, serial, time, datetime, argparse, struct

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
    clearInput(ser)
    req = bytes (b"<GETCPM>>")
    sendRequest(ser, req)
    reply = readReply(ser, 2)
    result = len(reply) == 2
    if result:
        cpm = reply[0]*256+reply[1]
        print("{0} CPM".format(cpm))
    else:
        print("Cannot read CPM")
    return result



##main()

parser = argparse.ArgumentParser(description='Read out the QG GMC-300 geiger counter')
parser.add_argument('-d', '--device', '--port', required=True, help='name of serial port device, e.g. /dev/ttyUSB0 for Linux or COM3 for Windows')
parser.add_argument('-v', '--verbose', action='count', help='synchronize time with local time of PC')
args = parser.parse_args()
if args.verbose:
    verbose = args.verbose


if args.device:	
    ser = openSerial(args.device)
    clearInput(ser)
    
    readCPM(ser)

    ser.close()


