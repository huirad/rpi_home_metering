rpi_home_metering
=================

Home Metering (Temperature, Humidity, ...) with Raspberry Pi or other Linux boxes

Introduction
============


Requirements
============


System Architecture
===================


Software Architecture
=====================

Summary/Lessons Learned
=======================
* Python is great
* Python has a built-in webserver
* Both Python2 and Python3 are pre-installed on the Raspberry Pi
* The Python2/Python3 schism still exists. Not all packages are available easily on Python3

* RRDTool is great to store and graph log data

TO DO
=====
* Robustness against bad sensor data
* Dew point calculation


Open Issues
===========
* Internet Security: Is the python webserver vulnerable?
* SD-Card lifetime: Store data on ramdisk/tmpfs?



XXXXXXXXXXXXXXXXXXXXXXXX
========================

1.) 2014-09-09-wheezy-raspbian.img per WinDiskImager auf SD-Karte installiert.

2.) IP Adresse = 192.168.2.23
Login per putty-ssh (pi raspberry)
sudo raspi-config ==> Timezone Berlin, 1MB memory für GPU, Expand filesystem

3.) python3 (und python2) sind schon installiert
sudo apt-get install python3-numpy ==> numpy offenbar auch schon installiert


01.11.2014
=============================

4.) Passwort geändert
passwd

5.) te923 [1] compilieren [2]
wget http://te923.fukz.org/downloads/te923tool-0.6.1.tgz
tar -xvf te923tool-0.6.1.tgz
cd te923tool-0.6.1
sudo apt-get install libusb-dev
make
[5.1] http://te923.fukz.org/
[5.2] http://www.mrbalky.com/tag/te923/


6.) te923 aufrufen
#funktioniert, aber nur als root
sudo ./te923con 

#udev Regel für Zugriff ohne root [6.1]
sudo vi /etc/udev/rules.d/99-te923.rules
ATTRS{idVendor}=="1130", ATTRS{idProduct}=="6801", MODE="0660", GROUP="plugdev"
sudo udevadm control --reload-rules
#funktioniert aber erst nach reboot
#das explizite entladen des usb-hid scheint nicht nötig zu sein

#Zugriff auf einzelne Felder, z.B. per awk
./te923con | awk -F: '{print $2}'

#Uhrzeit im Klartext: [6.2] python3 -m http.server
date -d @`./te923con | awk -F: '{print $1}'`

[6.1] http://www.mrbalky.com/2010/05/09/weather-station-fixing-the-bugs/
[6.2] http://www.epochconverter.com/

7.) Webserver, erster Gehversuch
./te923con > index.htm
python3 -m http.server
#dann Abfrage http://192.168.2.23:8000/

TODO: Sinnvolle Aufbereitung und cronjob ==> http://www.kompf.de/weather/pionewire.html
TODO: Fritzbox Port forwarding und Webserver automatisch starten

8.) rrdtool installieren
sudo apt-get install rrdtool
sudo apt-get install python-rrdtool
#http://www.kompf.de/weather/pionewire.html

http://oss.oetiker.ch/rrdtool/prog/rrdpython.en.html
http://oss.oetiker.ch/rrdtool/doc/rrdgraph_graph.en.html#GRAPH




9.) te923con per python auslesen
#http://www.holzheizer-forum.de/wbb3/index.php?page=Thread&threadID=1053&pageNo=2


10.) crontab  ===> TODO: Fehlerausgabe in Datei umleiten
#http://www.kompf.de/weather/pionewiremini.html
#http://raspberrywebserver.com/serveradmin/run-a-script-on-start-up.html
http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/4/?lang=de

Jede Minute
echo '*/1 * * * * cd $HOME/weather;python nexus4912.py > index.htm' | crontab -

Bei StartUp
@reboot cd $HOME/weather;python3 -m http.server



















