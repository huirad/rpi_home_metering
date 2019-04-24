#!/usr/bin/env python2

'''
Read out the CO2-Monitor AIRCO2NTROL MINI       https://www.tfa-dostmann.de/produkt/co2-monitor-airco2ntrol-mini-31-5006/

This is a minimalistic script to read out the data and write them to a rrd database

References
- Reverse Engineering done by Henry Ploetz     https://hackaday.io/project/5301/logs?sort=oldest
- Derived Project from Michael Nosthoff        https://github.com/heinemml/CO2Meter
- Derived Project from Thomas Reitmayr         https://gitlab.com/treitmayr/environment-monitor/tree/master/co2-mini

Further References
[ZG07]  http://www.zyaura.com/support/manual/pdf/ZyAura_CO2_Monitor_Carbon_Dioxide_ZG07%20series%20Module%20English%20user%20manual_1710.pdf

'''

import sys, fcntl, time, datetime
import rrdtool

#we can use any key so - lets choose the one for which phase2 simply collapses
key = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
crot = [0x7C,  0xB9,  0xAA,  0x2A,  0xF9,  0x6D,  0x6D,  0xAA]


def decrypt(key, data):
    phase1 = [data[i] for i in shuffle]
    phase2 = phase1     #xor'ing with 0 is identity
    phase3 = [((phase2[i] >> 3) | (phase2[(i-1+8)%8] << 5)) & 0xff for i in range(8)]
    out = [(phase3[i] + crot[i]) & 0xff for i in range(8)]
    return out


if __name__ == "__main__":

    fp = open("/dev/co2mini1", "a+b",  0)

    HIDIOCSFEATURE_9 = 0xC0094806
    set_report = "\x00" + "".join(chr(e) for e in key)      #different or Python3 - see https://github.com/heinemml/CO2Meter
    fcntl.ioctl(fp, HIDIOCSFEATURE_9, set_report)

    co2 = None
    temp = None

    while co2 is None or temp is None:
        data = list(ord(e) for e in fp.read(8))             #different or Python3 - see https://github.com/heinemml/CO2Meter
        decrypted = decrypt(key, data)
        if decrypted[4] != 0x0d or (sum(decrypted[:3]) & 0xff) != decrypted[3]:
            print hd(data), " => ", hd(decrypted),  "Checksum error"
        else:
            op = decrypted[0]
            val = decrypted[1] << 8 | decrypted[2]
            #print "%s\t%02X\t%04X" % (datetime.datetime.now().isoformat(), op, val)
            if op == 0x42:
                temp = val/16.0-273.15
            if op == 0x50:
                co2 = val
            if co2 is not None and temp is not None:
                print "%s\t%2.2f\t%4i" % (datetime.datetime.now().isoformat(), temp, co2)
    epoch = time.time()
    rrd_data = "{0:d}:{1:d}".format(int(epoch), co2)
    print(rrd_data)
    rrdtool.update("co2_ppm.rrd" , rrd_data)
    rrdtool.graph('www/co2_day.png',
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', 'now -1 day',
                  '--end', 'now',
                  '--vertical-label', 'CO2 PPM',
                  '--title', 'CO2 PPM 24h',
                  'DEF:CO2=co2_ppm.rrd:CO2:AVERAGE',
                  'LINE2:CO2#00FF00:CO2',
                  'VDEF:CO2_last=CO2,LAST',
                  'GPRINT:CO2_last:%.1lf PPM',
                  )
    rrdtool.graph('www/co2_minmax.png',
                  '--imgformat', 'PNG',
                  '--width', '540',
                  '--height', '100',
                  '--start', 'now -1 month',
                  '--end', 'now',
                  '--vertical-label', 'CO2 PPM',
                  '--title', 'CO2 PPM 1 Monat',
                  'DEF:CO2MAX=co2_ppm.rrd:CO2:MAX',
                  'LINE2:CO2MAX#0000FF:CO2MAX',
                  'DEF:CO2MIN=co2_ppm.rrd:CO2:MIN',
                  'LINE2:CO2MIN#000080:CO2MIN',
                  )

