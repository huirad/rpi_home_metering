rpi_home_metering
=================

Home Metering (Temperature, Humidity, ...) with Raspberry Pi or other Linux boxes

Introduction
============


Requirements
============

Functional Requirements
-----------------------
* Collect Temperature and Humidity readings from my home weather station
* Collect Temperature and Humidity readings from additional sensors
* Store Temperature and Humidity readings
* Make Temperature and Humidity available on the internet through a web server

Non-Functional Requirements
---------------------------
* Use already available Hardware: Raspberry Pi and the TFA Nexus weather station
* Re-use existing software: Have a bit fun in coding but do not re-invent the wheel

Personal Objectives
-------------------
* Improve my Python knowledge
* Improve my Raspberry Pi knowledge

System Architecture
===================
The system architecture is shown in the following deployment diagram.
* The Raspberry Pi collects Temperature and Humidity data from various sensors such as the TFA Nexus weather station
  * Sensor data are stored in a RRD archives
  * Sensor data are made available via a web server
* The Nexus TFA weather station 
  * has a built-in DCF77 time receiver,  a Temperature/Humidity sensor and a barometric pressure sensor
  * receives Temperature/Humidity data from up to 5 external sensors via 433MHz RF
* The DSL router 
  * makes the Raspberry Pi web server available to the internet via port forwarding
  * provides its internet IP address to a dynamic DNS service to ease accessibility

![system architecture deployment][system architecture deployment]


[system architecture deployment]: https://raw.githubusercontent.com/huirad/rpi_home_metering/master/doc/SystemArchitecture_Deployment.png

Software Architecture
=====================


Installation and Setup
======================

Raspberry Pi
------------
* Install raspbian image (2014-09-09-wheezy-raspbian.img) on 4GB SD-Card using WinDiskImager
* Initial connect from Windows PC via putty-ssh (IP-adress assigned by router: 192.168.2.23)
  * `sudo raspi-config`
    * Timezone Berlin
    * limit GPU memory to smallest value (1MB)
    * Expand filesystem
  * `passwd`
    * change password
  * get the [te923] (http://te923.fukz.org/) tool and [compile] (http://www.mrbalky.com/tag/te923/)
    * `wget http://te923.fukz.org/downloads/te923tool-0.6.1.tgz`
	* `tar -xvf te923tool-0.6.1.tgz`
	* `cd te923tool-0.6.1`
	* `sudo apt-get install libusb-dev`
	* `make`
	

Summary/Lessons Learned
=======================
<ul>
<li> Python is great.
<li> Python has a built-in webserver.
<li> Both Python2 and Python3 are pre-installed on the Raspberry Pi.
<li> The Python2/Python3 schism still exists. E.g. not all packages are available easily on Python3.
</ul>

<ul>
<li> RRDTool is great to store and graph log data.
</ul>

<ul>
<li> Github provides a convenient way to share open source software including [markdown][aaa] documentation
</ul>

[aaa]: https://help.github.com/articles/markdown-basics/


:construction: TO DO
=====
* Improve robustness against bad sensor data
  * te923con *-iU* to generate "unknown" values for rrdtool
* Add dew point calculation to the python script


:warning: Open Issues
===========
* Internet Security: Is the python webserver vulnerable?
  * Solution: Disable port forwarding at router. FTP push static website to external server (ftp -u URL file).
    * Only outgoing connection from Raspberry Pi. 
	* FTP password must be stored on Raspberry Pi. Is this the next security risk?
* SD-Card lifetime: 
  * Store static website data on ramdisk/tmpfs?
  * Separate code and data: store RRD database on USB flash drive instead on SD-Card with Raspbian OS.
  * Reduce log files written on SD-Card by OS and services
* Stability of RF sensor connection:
  * Occasionally the connection between TFA Nexus and a remote sensor breaks for unknown reasons.
* Accuracy of humidity measurements: 
  * Humidity readings of different sensors at the same place can spread significantly
  * Recent example: One of the Nexus RF sensors measured 55% RH, the Conrad DL141TH measured 60% RH and the SHT 11 measured 65% RH.

XXXXXXXXXXXXXXXXXXXXXXXX
========================





3.) python3 (und python2) sind schon installiert
sudo apt-get install python3-numpy ==> numpy offenbar auch schon installiert


01.11.2014
=============================




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




















