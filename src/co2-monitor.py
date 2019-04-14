#!/usr/bin/env python2

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
    set_report = "\x00" + "".join(chr(e) for e in key)
    fcntl.ioctl(fp, HIDIOCSFEATURE_9, set_report)

    co2 = None
    temp = None

    while True:
        data = list(ord(e) for e in fp.read(8))
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
            if co2 and temp:
                print "%s\t%2.2f\t%4i" % (datetime.datetime.now().isoformat(), temp, co2)
                co2 = None
                temp = None

