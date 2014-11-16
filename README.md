Introduction
============
This is my home metering (Temperature, Humidity, ...) project connecting a TFA Nexus weather station with a a Raspberry Pi.

The following picture shows the main parts of the hardware setup
![hardware setup][hardware setup]
[hardware setup]: https://raw.githubusercontent.com/huirad/rpi_home_metering/master/doc/HW_Setup.png

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
The software architecture is shown in the following diagram
* The cron daemon 
  * reads its configuration data from the crontab
  * starts the python web server at reboot
  * calls the python script hm__update.py each 15min
* The python script [hm__update.py] (https://raw.githubusercontent.com/huirad/rpi_home_metering/master/src/hm__update.py)
  * reads out the temperature/humidity data from the Nexus weather station by calling the te923con program
  * updates the RRD database with the new data
  * creates a static web page from current data and a time series plot from RRD data
* The RRD database
  * is created at system setup by the shell script [hm__rrd_create.sh] (https://raw.githubusercontent.com/huirad/rpi_home_metering/master/src/hm__rrd_create.sh)
  * stores temperature/humidity data in a cyclic buffer
  * automatically calculates minimum/maximum values
* The python webserver
  * provides the static web page and the time series plot to the outer world

![software architecture][software architecture]
[software architecture]: https://raw.githubusercontent.com/huirad/rpi_home_metering/master/doc/SoftwareArchitecture.png


Installation and Setup of the Raspberry Pi
==========================================

Basic Raspberry Pi Setup:
* Install raspbian image (2014-09-09-wheezy-raspbian.img) on 4GB SD-Card using WinDiskImager
* Connect Raspberry Pi to the network
* Connect the Nexus weather station via USB to the Raspberry Pi
* Initial connect from Windows PC via putty-ssh (IP-adress assigned by router: 192.168.2.23)
  * `sudo raspi-config`
    * Timezone Berlin
    * limit GPU memory to smallest value (1MB)
    * Expand filesystem
  * `passwd`
    * change password
  * Optional: Verify that python and python3 are already installed
    * `python -V`
    * `python3 -V`

Compile the TE923 tool and configure USB HID access:
* Get the [te923] (http://te923.fukz.org/) tool and [compile] (http://www.mrbalky.com/tag/te923/)
  * `wget http://te923.fukz.org/downloads/te923tool-0.6.1.tgz`
  * `tar -xvf te923tool-0.6.1.tgz`
  * `cd te923tool-0.6.1`
  * `sudo apt-get install libusb-dev`
  * `make`
* Allow access to the USB HID device without root rights 
  * [create udev rule] (http://www.mrbalky.com/2010/05/09/weather-station-fixing-the-bugs/)
  * `sudo vi /etc/udev/rules.d/99-te923.rules`
  * enter `ATTRS{idVendor}=="1130", ATTRS{idProduct}=="6801", MODE="0660", GROUP="plugdev"`
  * `sudo reboot`
* Example output: `1416078280:21.90:51:8.00:86:U:U:U:U:U:U:7.70:83:956.8:U:3:0:U:U:U:U:0`
  * Colon-separated fields: timestamp, followed by temperature and humidity readings
  * Access individual fields by filtering with awk
    * `./te923con | awk -F: '{print $2}'`
  * Convert time from epoch to local time - see [epochconverter] (http://www.epochconverter.com/)
    * ``date -d @\`./te923con | awk -F: '{print $1}'` ``

Install rrdtool and the associated python package
* `sudo apt-get install rrdtool`
* `sudo apt-get install python-rrdtool`

Create the directory structure and deploy the scripts
* `mkdir weather`
* `cd weather`
  * copy the scripts `hm__update.py` and `hm__rrd_create.sh` here
  * create the RRD database by executing `./hm__rrd_create.sh`
* `mkdir www`
  * this directory is for the static web page and the time series plot

Configure the cron daemon to start the web server at reboot and to call the update script each 15min
* `crontab -e`
* enter
  * `*/15 * * * * cd $HOME/weather;python hm__update.py > www/index.htm`
  * `@reboot cd $HOME/weather/www;python3 -m http.server`
  * `@reboot cd $HOME/weather/www;python3 -m http.server`
* `sudo reboot`


Summary/Lessons Learned
=======================
Python
* Python is great.
* Python has a built-in webserver.
* Both Python2 and Python3 are pre-installed on the Raspberry Pi.
* The Python2/Python3 schism still exists, e.g. not all packages are available easily on Python3.

RRDTools
* RRDTool is great to store and graph log data.

GitHub
* GitHub provides a convenient way to share open source software including [markdown][github markdown] documentation

[github markdown]: https://help.github.com/articles/markdown-basics/


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
  * Use larger SD-Card to allow better wear leveling
  * See e.g. [here] (http://www.ideaheap.com/2013/07/stopping-sd-card-corruption-on-a-raspberry-pi/) or  [there](http://raspberrypi.stackexchange.com/questions/169/how-can-i-extend-the-life-of-my-sd-card)
* Stability of RF sensor connection:
  * Occasionally the connection between TFA Nexus and a remote sensor breaks for unknown reasons.
* Accuracy of humidity measurements: 
  * Humidity readings of different sensors at the same place can spread significantly
  * Recent example: One of the Nexus RF sensors measured 55% RH, the Conrad DL141TH measured 60% RH and the SHT 11 measured 65% RH.

  
References
==========
* Weather station:
    * [TFA Nexus](http://wiki.wetterstationen.info/index.php?title=TFA-Dostmann_Nexus)
	* [Hideki TE923](http://www.hidekielectronics.com/?m=6&p=2)
* The [te923] (http://te923.fukz.org/) tool to read out data from the Nexus weather station* RRDTool
  * http://oss.oetiker.ch/rrdtool/prog/rrdpython.en.html
  * http://oss.oetiker.ch/rrdtool/doc/rrdgraph_graph.en.html#GRAPH
  * http://kompf.de/weather/technik.html
* python  
  * web server
* The [AVR web server by Guido Socher](http://tuxgraphics.org/electronics/200709/avr-webserver-sensirion-humidity-temperature.shtml)
* Alternative approaches to record weather data - mostly more sophisticated
  * [fhem](http://fhem.de/fhem.html)
  * [wviewweather](http://www.wviewweather.com/)
  * [WeeWX](http://www.weewx.com/)


[power meter pulse counting]: http://openenergymonitor.org/emon/buildingblocks/introduction-to-pulse-counting  
  
  



01.11.2014
=============================

7.) Webserver, erster Gehversuch
./te923con > index.htm
python3 -m http.server
dann Abfrage http://192.168.2.23:8000/

TODO: Sinnvolle Aufbereitung und cronjob ==> http://www.kompf.de/weather/pionewire.html
TODO: Fritzbox Port forwarding und Webserver automatisch starten

8.) rrdtool installieren

http://www.kompf.de/weather/pionewire.html





10.) crontab  ===> TODO: Fehlerausgabe in Datei umleiten
http://www.kompf.de/weather/pionewiremini.html
http://raspberrywebserver.com/serveradmin/run-a-script-on-start-up.html
http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/4/?lang=de





















