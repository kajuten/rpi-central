#!/usr/bin/python

import spidev
import RPi.GPIO as GPIO

# -------------------------
# spi setup
# -------------------------
spi = spidev.SpiDev()
# open spi port 0, device 0
spi.open(0, 0)
# -------------------------

# -------------------------
# GPIO setup
# -------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

NIRQ = 24
GPIO.setup(NIRQ, GPIO.IN)
# -------------------------

# free resources
def cleanup():
    '''Closes GPIO and SPI resources.'''
    GPIO.cleanup()
    spi.close()

#-----------------------------------------------------------------------------
# send function
def rf12_send(data=0):
    '''Send data via RF chip.

    Keyword arguments:
    data -- data to transmit, 1 Byte (default 0)
    '''
    while GPIO.input(NIRQ):
        time.sleep(0.01)
    spi_trans(0xB800 + data)

#-----------------------------------------------------------------------------
# low level function
def spi_trans(cmd):
    '''Write command via SPI to RF chip.

    Keyword arguments:
    cmd -- command as hex value, 2 Byte

    Return
    read -- received data as hex value, 2 Byte
    '''
    read = spi.xfer([cmd >> 8])[0] << 8
    read += spi.xfer([cmd])[0]

    return read
