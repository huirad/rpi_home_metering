Introduction
============
This is my home metering (Temperature, Humidity, ...) project connecting a TFA Nexus weather station with a Raspberry Pi.

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
* The Raspberry Pi collects Temperature and Humidity data from various sensors, mainly from the TFA Nexus weather station
  * Sensor data are stored in RRD (round robin database) archives
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
* The python script [hm__update.py](https://raw.githubusercontent.com/huirad/rpi_home_metering/master/src/hm__update.py)
  * reads out the temperature/humidity data from the Nexus weather station by calling the te923con program
  * updates the RRD database with the new data
  * creates a static web page from current data and a time series plot from RRD data
* The RRD database
  * is created at system setup by the shell script [hm__rrd_create.sh](https://raw.githubusercontent.com/huirad/rpi_home_metering/master/src/hm__rrd_create.sh)
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
* Get the [te923](http://te923.fukz.org/) tool and [compile](http://www.mrbalky.com/tag/te923/)
  * `wget http://te923.fukz.org/downloads/te923tool-0.6.1.tgz`
  * `tar -xvf te923tool-0.6.1.tgz`
  * `cd te923tool-0.6.1`
  * `sudo apt-get install libusb-dev`
  * `make`
* Allow access to the USB HID device without root rights 
  * [create udev rule](http://www.mrbalky.com/2010/05/09/weather-station-fixing-the-bugs/)
  * `sudo vi /etc/udev/rules.d/99-te923.rules`
  * enter `ATTRS{idVendor}=="1130", ATTRS{idProduct}=="6801", MODE="0660", GROUP="plugdev"`
  * `sudo reboot`
* Example output: `1416078280:21.90:51:8.00:86:U:U:U:U:U:U:7.70:83:956.8:U:3:0:U:U:U:U:0`
  * Colon-separated fields: timestamp, followed by temperature and humidity readings
  * Access individual fields by filtering with awk
    * `./te923con | awk -F: '{print $2}'`
  * Convert time from epoch to local time - see [epochconverter](http://www.epochconverter.com/)
    * ``date -d @\`./te923con | awk -F: '{print $1}'` ``

Install rrdtool and the associated python package
* `sudo apt-get install rrdtool`
* `sudo apt-get install python-rrdtool`

Create the directory structure and deploy the scripts
* `mkdir weather`
* `cd weather`
  * copy the scripts `hm__update.py` and `hm__rrd_create.sh` here
  * copy the `te923con` exectuable here
  * create the RRD database by executing `./hm__rrd_create.sh`
* `mkdir www`
  * this directory is for the static web page and the time series plot

Configure the cron daemon to start the web server at reboot and to call the update script each 15min
* `crontab -e`
* enter
  * `*/15 * * * * cd $HOME/weather;python hm__update.py > www/index.htm`
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
[notepad++ markdown]: https://github.com/Edditoria/markdown_npp_zenburn


:construction: TO DO
=====
* Improve robustness against bad sensor data
  * te923con *-iU* to generate "unknown" values for rrdtool
* Add dew point calculation to the python script
* Redirect error output from programs run by cron 


:warning: Open Issues
===========
* Internet Security: Is the python webserver vulnerable?
  * Solution: Disable port forwarding at router. 
    * Push data to external server, e.g. [data.sparkfun.com](https://data.sparkfun.com/).
    * Create graps with [google charts](http://phant.io/graphing/google/2014/07/07/graphing-data/).
    * Only outgoing connection from Raspberry Pi. 
	* FTP password must be stored on Raspberry Pi. Is this the next security risk?
* Privacy
  * Can my life be spied out by analyzing those data?
* SD-Card lifetime: 
  * Store static website data on ramdisk/tmpfs?
  * Separate code and data: store RRD database on USB flash drive instead on SD-Card with Raspbian OS.
  * Reduce log files written on SD-Card by OS and services
  * Use larger SD-Card to allow better wear leveling
  * See e.g. [1](http://www.ideaheap.com/2013/07/stopping-sd-card-corruption-on-a-raspberry-pi/) or  [2](http://raspberrypi.stackexchange.com/questions/169/how-can-i-extend-the-life-of-my-sd-card) or [3](http://www.zdnet.com/raspberry-pi-extending-the-life-of-the-sd-card-7000025556/)
* Stability of RF sensor connection:
  * Occasionally the connection between TFA Nexus and a remote sensor breaks for unknown reasons.
* Accuracy of humidity measurements: 
  * Humidity readings of different sensors at the same place can spread significantly
  * Recent example: One of the Nexus RF sensors measured 55% RH, the Conrad DL141TH measured 60% RH and the SHT 11 measured 65% RH.

  
References
==========
* Weather station:
    * [TFA Nexus](http://wiki.wetterstationen.info/index.php?title=TFA-Dostmann_Nexus)
	* [All TFA weather stations](http://tfa-dostmann.de/index.php?id=62)
	* [Hideki TE923](http://www.hidekielectronics.com/?m=6&p=2)
* The [te923](http://te923.fukz.org/) tool to read out data from the Nexus weather station
* [RRDTool](http://oss.oetiker.ch/rrdtool/)
  * [... for beginners](http://oss.oetiker.ch/rrdtool/tut/rrd-beginners.en.html)
  * [... with python](http://oss.oetiker.ch/rrdtool/prog/rrdpython.en.html)
  * [rrdgraph](http://oss.oetiker.ch/rrdtool/doc/rrdgraph_graph.en.html#GRAPH)
  * [Intro by Martin Kompf](http://kompf.de/weather/technik.html)
* Python  
  * [web server](https://docs.python.org/3/library/http.server.html) `python3 -m http.server` 
* The [crontab](http://linux.die.net/man/1/crontab) command
  * Example 1: [run-a-script-on-start-up](http://raspberrywebserver.com/serveradmin/run-a-script-on-start-up.html)
  * Example 1: [Launch-Python-script-on-startup](http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/4/?lang=de)
* The [AVR web server by Guido Socher](http://tuxgraphics.org/electronics/200709/avr-webserver-sensirion-humidity-temperature.shtml)
* Similar projects
  * Martin Kompf: [DS1820 1-wire Temperature Sensor @ Raspberry Pi](http://www.kompf.de/weather/pionewiremini.html)
  * Charly Kuehnast: [DS1820 1-wire Temperature Sensor @ Raspberry Pi](http://kuehnast.com/s9y/archives/557-Raspberry-Pi-Temperaturfuehler-DS18B20-auslesen.html)

* Alternative approaches to record weather data - mostly more sophisticated
  * [fhem](http://fhem.de/fhem.html)
  * [wviewweather](http://www.wviewweather.com/)
  * [WeeWX](http://www.weewx.com/)


Connect a DS1820 1-wire tempeature sensor
=========================================
Connect the sensor using parasite power supply
* Connect the GND and! the VDD pin of the sensor to GND (these are the outer 2 pins)
* Connect the DQ pin (the middle one) to GPIO4 (pin7) of the RPi
* Add a 4.7kOhm resistor between 3.3V and GPIO4/DQ as pull-up
* `sudo modprobe w1-gpio pullup=1`
* `sudo modprobe w1-therm`
* `cd /sys/bus/w1/devices`
* `cd 10-00080*`
* `cat w1_slave` # the second line contains the temperature - with 3 decimal digits

You can automatically load the drivers by adding the to /etc/modules
* `w1-gpio pullup=1` 
* # or `w1-gpio pullup=1 gpiopin=17` to use GPIO17 instead of GPIO4
* `w1-therm`

Note: I have not been able to use I2C when w1 was configured with parasite power (`pullup=1`). If I use w1 with separate power supply (no `pullup`), then I2C works. In some posts
[1](https://github.com/raspberrypi/linux/issues/435)
[2](http://www.forum-raspberrypi.de/Thread-i2c-i2c-1wire-und-kamera-gleichzeitig)
[3](https://www.raspiprojekt.de/forum/sets-und-schaltungen/162-mpc23s17-mit-fhem-ansteuern-aber-wie.html?start=6)
, it was proposed to change the order of drivers in `/etc/modules`, but this did not help for me.
Probably this has been resolved with the latest Raspbian release, see [commit a827a5619e72983159a152fd4943d9618c7a81a3](https://github.com/raspberrypi/linux/commit/a827a5619e72983159a152fd4943d9618c7a81a3)??


References
* Martin Kompf: [DS1820 1-wire Temperature Sensor @ Raspberry Pi](http://www.kompf.de/weather/pionewiremini.html)
* [Explanation of the w1_slave field](http://thepiandi.blogspot.de/2013/06/a-raspberry-pi-thermometer-interpreting.html)
* Caution: newer Raspbian releases use the devicetree: See [1](https://www.raspiprojekt.de/anleitungen/schaltungen/9-1wire-mit-temperatursensor-ds18b20.html?showall=1&limitstart=), [2](http://www.raspberrypi.org/documentation/configuration/device-tree.md) or even better [2](http://www.fhemwiki.de/wiki/Raspberry_Pi_und_1-Wire#Software-Installation_ab_2015_bzw._Kernelversion_3.18.3)  [3](http://raspberrypi.stackexchange.com/questions/27073/firmware-3-18-x-breaks-i2c-spi-audio-lirc-1-wire-e-g-dev-i2c-1-no-such-f) [4](http://raspberry.tips/faq/raspberry-pi-device-tree-aenderung-mit-kernel-3-18-x-geraete-wieder-aktivieren/) [5](http://pi-buch.info/?p=344) [6](http://www.forum-raspberrypi.de/Thread-tutorial-geraetetreiber-und-device-tree-dt)
* List of 1-wire devices in [/sys/devices/w1_bus_master1/w1_master_slaves](http://www.gtkdb.de/index_31_2040.html)


[power meter pulse counting]: http://openenergymonitor.org/emon/buildingblocks/introduction-to-pulse-counting  
[Luftraumueberwachung1]: http://kuehnast.com/s9y/archives/571-Luftraumueberwachung.html  
[Luftraumueberwachung2]: http://www.raspberry-pi-geek.de/Magazin/2014/06/Luftraum-ueberwachen-mit-dem-Raspberry-Pi
[Recent news]: http://www.sueddeutsche.de/digital/sicherheit-von-smart-home-offen-wie-ein-scheunentor-1.2227389




















