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
















