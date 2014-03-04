# RPi-central
-------------

Raspberry Pi is the interface between the internet and the low level hardware for a model railroad project

## Components
-------------

### MySQL database API

### RF12 chip API

- communication via SPI

- connected Pins: 

	Raspberry Pi  |     | RF12
------------: |:-----:| :---
3.3V		  | ----> | VDD
GPIO 24		  | <---- | NIRQ
MOSI 		  | ----> | SDI
GND			  | ----> | GND
MISO 		  | <---- | SDO
CLK  		  | ----> | SCK
CE0			  | ----> | nSEL

## Model Railroad description

**Goal:** a self-made model railroad which can be controlled via a PC

- Train components and casings are 3D printed
- PCB self-made
- Central Raspberry Pi connected to WIFI
- Communication from RPi-central to the signal-towers via RF12 chip [TRX433S][RF12]
- MySQL database hosted on Raspberry Pi
- Signal towers are controlled by an ATmega8 which is connected with a RF12 chip ([see signal-tower project][signal-tower])
- Another Raspberry Pi with a camera module is in every train which is connected via a 3G dongle to the internet ([see RPi-train project][RPi-train])

[RF12]: http://www.matrixmultimedia.com/resources/files/datasheets/RF%20Solutions%20Transciever.pdf
[signal-tower]: https://github.com/kajuten/
[RPi-train]: https://github.com/kajuten/