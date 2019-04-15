#!/usr/bin/env python2

'''
Read out the CO2-Monitor AIRCO2NTROL MINI       https://www.tfa-dostmann.de/produkt/co2-monitor-airco2ntrol-mini-31-5006/

This is a minimalistic script to read out the data and write them to a rrd database

References
- Reverse Engineering done by Henry Ploetz     https://hackaday.io/project/5301/logs?sort=oldest
- Derived Project from Michael Nosthoff        https://github.com/heinemml/CO2Meter
- Derived Project from Thomas Reitmayr         https://gitlab.com/treitmayr/environment-monitor/tree/master/co2-mini
'''

import sys, fcntl, time, datetime

#we can use any key so - lets choose the one for which phase2 simply collapses
key = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
shuffle = [2, 4, 0, 7, 1, 6, 5, 3]
ctmp = [0x84,  0x47,  0x56,  0xD6,  0x07,  0x93,  0x93,  0x56]


def decrypt(key, data):
    phase1 = [data[i] for i in shuffle]
    phase2 = phase1
    phase3 = [((phase2[i] >> 3) | (phase2[(i-1+8)%8] << 5)) & 0xff for i in range(8)]
    out = [(0x100 + phase3[i] - ctmp[i]) & 0xff for i in range(8)]
    return out


if __name__ == "__main__":

    fp = open(sys.argv[1], "a+b",  0)

    HIDIOCSFEATURE_9 = 0xC0094806
    set_report = "\x00" + "".join(chr(e) for e in key)      #different or Python3 - see https://github.com/heinemml/CO2Meter
    fcntl.ioctl(fp, HIDIOCSFEATURE_9, set_report)

    co2 = None
    temp = None
    rh = None

    while True:
        data = list(ord(e) for e in fp.read(8))             #different or Python3 - see https://github.com/heinemml/CO2Meter
        decrypted = decrypt(key, data)
        if decrypted[4] != 0x0d or (sum(decrypted[:3]) & 0xff) != decrypted[3]:
            print hd(data), " => ", hd(decrypted),  "Checksum error"
        else:
            op = decrypted[0]
            val = decrypted[1] << 8 | decrypted[2]
            #print "%s\t%02X\t%04X" % (datetime.datetime.now().isoformat(), op, val)
            #TODO CHECk RH reading? -> see http://www.zyaura.com/support/manual/pdf/ZyAura_CO2_Monitor_Carbon_Dioxide_ZG07%20series%20Module%20English%20user%20manual_1710.pdf
            if op == 0x41:
                rh = val/100.0
            if op == 0x42:
                temp = val/16.0-273.15
            if op == 0x50:
                co2 = val
            if co2 and temp and rh:
                print "%s\t%2.2f\t%4i\t%2.2f" % (datetime.datetime.now().isoformat(), temp, co2, rh)
                co2 = None
                temp = None
                rh = None

