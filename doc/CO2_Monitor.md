# CO2 Monitor




## Hardware
The
[CO2-Monitor AIRCO2NTROL MINI](https://www.tfa-dostmann.de/produkt/co2-monitor-airco2ntrol-mini-31-5006/)
from TFA Dostmann seems to be a derivate of either the similar product by the US company
[CO2Meter](https://www.co2meter.com/products/co2mini-co2-indoor-air-quality-monitor)
or by the Taiwanese company 
[ZyAura](http://www.zyaura.com/products/ZGm05.asp).

The variant from CO2Meter has 2 push buttons on the back which are not accessible from outside the TFA variant.
But if you carefully open the lid at the back, then you see that those push buttons are also on the PCB of the TFA.
See [maker-tutorials.com](https://maker-tutorials.com/guenstiges-co2-messgeraet-airco2ntrol-im-test-1-raspberry-pi-fhem-usb/)
and [amazon](https://www.amazon.de/TFA-Dostmann-AirCO2ntrol-CO2-Monitor-Kunststoff/product-reviews/B00TH3OW4Q/ref=cm_cr_getr_d_paging_btm_next_3?ie=UTF8&reviewerType=all_reviews&pageNumber=3).

The device has a USB port for power supply. But it can also be used to reread out the data. See next section.

## Software / Communication Protocol

[Henyk Ploetz](https://github.com/henryk) made a great job of 
[re-engineering](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor)
the protcocol at the [USB interface](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor/log/17909-all-your-base-are-belong-to-us). 



Some further recipies using mainly python to access the USB - HID:

* [The original hack from Henryk Ploetz](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor/log/17909-all-your-base-are-belong-to-us)  - with Python Code!
* [henryk/co2mini-mqtt](https://github.com/henryk/co2mini-mqtt) - Python application from Henryk
* [heinemml/CO2Meter](https://github.com/heinemml/CO2Meter) - straighforward; udev rule in README
* [treitmayr/environment-monitor/co2-mini](https://gitlab.com/treitmayr/environment-monitor/tree/master/co2-mini) - very compact; udev-rule
* [wooga](https://github.com/wooga/office_weather) derived from the [original hack](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor/log/17909-all-your-base-are-belong-to-us)
* [nobodyinperson/co2monitor](https://gitlab.com/nobodyinperson/co2monitor) - [previously on github](https://github.com/nobodyinperson/co2monitor) - laaarge package
* [dmage/co2mon](https://github.com/dmage/co2mon) - C program ; references: [revspace.nl::CO2MeterHacking](https://revspace.nl), [ru](https://habr.com/en/company/masterkit/blog/248403/)


BACKSPACE, the Bamberg hacker space has in addition re-enigeered the internals

* [Project page](https://www.hackerspace-bamberg.de/Co2_Monitor)
* [Code](https://github.com/b4ckspace/esp8266-co2monitor)



## References

Documents/Datasheets on the CO2Mini

* TFA: [Manual](https://clientmedia.trade-server.net/1768_tfadost/media/8/00/1800.pdf)
* [Dostmann](https://dostmann-electronic.de/produkt/aircontrol-mini-co2-messgeraet.html?cid=6): [Manual](https://dostmann-electronic.de/produkt/aircontrol-mini-co2-messgeraet.html?cid=6)
* CO2Monitor: [Manual](http://co2meters.com/Documentation/Manuals/Manual-RAD-0301.pdf) [Protocol](http://co2meters.com/Documentation/Other/AN_RAD_0301_USB_Communications_Revised8.pdf) [Sensor Calibration procedure](http://www.co2meters.com/Documentation/AppNotes/AN131-Calibration.pdf)
* ZyAura: [ZGm05 Manual](http://www.zyaura.com/support/manual/pdf/ZyAura_CO2_Monitor_Carbon_Dioxide_ZGm053U%20English%20manual_1304.pdf) ; [ZyAura ZG01C Module Manual](http://www.zyaura.com/support/manual/pdf/ZyAura_CO2_Monitor_ZG01C_Module_ApplicationNote_141120.pdf)


Further Interesting Links :

* [DWD:Klimagase](https://www.dwd.de/DE/forschung/atmosphaerenbeob/zusammensetzung_atmosphaere/spurengase/inh_nav/klimagase_node.html)
* [ICOS Carbon Portal](https://www.icos-cp.eu/)
* ZyAura: [US: Air Code](http://www.zyaura.com/tutorial/regulation/Air%20Code.pdf)
* [SenseAir: Indoor Air Quality and Safety](https://senseair.com/applications/indoor-air-quality/indoor-air-quality-and-safety/)
* [SenseAir: CO2 Sensors](https://senseair.com/products?q=1331) - most are same as sold by [CO2Meter](https://www.co2meter.com/collections/co2-sensors) | [AN162](http://www.co2meters.com/Documentation/AppNotes/AN162-LP8-sensor-arduino-modbus-uart.pdf)
* [CO2Meter CozIR](https://www.co2meter.com/products/cozir-ambient-10000-ppm-co2-sensor?variant=840094613524)
* [Sensirion SCD30](https://www.sensirion.com/en/environmental-sensors/carbon-dioxide-sensors-co2/) 
* [Comparison between SenseAir and Sensirion Sensor](https://presentations.copernicus.org/EMS2018-497_presentation.pdf)