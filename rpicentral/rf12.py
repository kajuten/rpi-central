#!/usr/bin/env python2.7

import spidev
import RPi.GPIO as GPIO
import time
from flufl.enum import Enum


receive = list()
transmit = list()

index = 0

class TRX(Enum):
    IDLE = 0
    RECEIVE = 1
    TRANSMIT = 2

trx_state = TRX.IDLE

RF_LENGTH = 14


spi = None

# constants
NIRQ = 24


BAND_433MHZ = 1
BAND_868MHZ = 2
BAND_915MHZ = 3

RF_RECEIVER_ON = 0x82DD
RF_TRANSMITTER_ON = 0x823D


RF_RX_FIFO_READ = 0xB000
RF_TXREG_WRITE = 0xB800
RF_SLEEP_MODE = 0x8201 # dc = 1
RF_TXREG_FIFO_ENABLE = 0x80C8 # el = 1, ef = 1, band = 0, load capacitor = X
RF_RX_CTRL = 0x94A1 # VDI, FAST, 134kHz, 0dBm, -97dBm
RF_TX_CTRL = 0x9850 # mp = 0, 90kHz, 0dBm
RF_FREQUENCY = 0xA4B0 # f = 1200 -> fc = 433MHz
RF_DATA_RATE = 0xC623 # r = 35, cs = 0 -> data rate ~ 9600 kbit/s
RF_FIFO_CMD = 0xCA83 # FIFO 8 bit, 1-Sync Byte, ff = 0, dr = 1
RF_DATA_FILTER = 0xC2AD # al = 1, ml = 0, s = 0, DQD = 5
RF_SYNC_PATTERN = 0xCE2D # sync = 0x2D
RF_AFC = 0xC443 # a = 1, r = 0, st = 0, fi = 0, oe = 1, en = 1
RF_PLL = 0xCC77 # ob = 3, lpx = 1, ddy = 0, ddi = 1, bw0 = 1


RF_WAKE_UP = 0xE000 # not used
RF_LOW_DUTY_CYCLE = 0xC800 # not used
RF_LOW_BATTERY = 0xC000 # not used



def spi_initialize():
    '''Set up SPI.'''
    global spi
    spi = spidev.SpiDev()
    # open spi port 0, device 0
    spi.open(0, 0)


def gpio_initialize():
    '''Set up GPIO.

    Pin 24 is used as interrpt driven input
    '''
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(NIRQ, GPIO.IN)


def initialize(band=BAND_433MHZ):
    '''Set up RF12 chip.

    Keyword arguments:
    band -- specifies the used frequency band
            use these constants: BAND_433MHZ, BAND_868MHZ, BAND_915MHZ
    '''
    gpio_initialize()
    spi_initialize()

    spi_xfer() # initial SPI transfer added to avoid power-up problem
    spi_xfer(RF_SLEEP_MODE)

    # wait until RFM12B is out of power-up reset, this takes several *seconds*
    spi_xfer(RF_TXREG_WRITE) # in case we're still in OOK mode
    while not GPIO.input(NIRQ):
        spi_xfer(0x0000)

    spi_xfer(RF_TXREG_FIFO_ENABLE | (band < 4)) # el = 1, ef = 1, load capacitor = X
    spi_xfer(RF_FREQUENCY) # f = 1200 -> fc = 433MHz
    spi_xfer(RF_DATA_RATE) # r = 35, cs = 0 -> data rate ~ 9600 kbit/s
    spi_xfer(RF_RX_CTRL) # VDI, FAST, 134kHz, 0dBm, -97dBm
    spi_xfer(RF_DATA_FILTER) # al = 1, ml = 0, s = 0, DQD = 5

    spi_xfer(RF_FIFO_CMD) # FIFO 8 bit, 1-Sync Byte, ff = 0, dr = 1
    spi_xfer(RF_SYNC_PATTERN) # sync = 0x2D

    spi_xfer(RF_AFC) # a = 1, r = 0, st = 0, fi = 0, oe = 1, en = 1
    spi_xfer(RF_TX_CTRL) # mp = 0, 90kHz, 0dBm
    spi_xfer(RF_PLL) # ob = 3, lpx = 1, ddy = 0, ddi = 1, bw0 = 1

#    spi_xfer(RF_WAKE_UP) # not used
#    spi_xfer(RF_LOW_DUTY_CYCLE) # not used
#    spi_xfer(RF_LOW_BATTERY) # not used

    global trx_state
    trx_state = TRX.IDLE
    GPIO.add_event_detect(NIRQ, GPIO.FALLING, callback=transceive)


# free resources
def cleanup():
    '''Closes GPIO and SPI resources.'''
    if GPIO is not None:
        GPIO.cleanup()
    if spi is not None:
        spi.close()

#-----------------------------------------------------------------------------
# transceive function (interrupt driven)
def transceive(self):
    '''Send/receive data.

    Interrupt driven send and receive function.(Triggerd by falling Edge on
    NIRQ channel.

    Send:    to beginn call start_send()
    Receive: to beginn call start_receive()
    '''
    global trx_state
    global receive
    global transmit
    global index

    if(trx_state == TRX.RECEIVE):
        receive.append(spi_xfer(RF_RX_FIFO_READ))

        if len(receive) >= RF_LENGTH:
            spi_xfer(RF_SLEEP_MODE)
            trx_state = TRX.IDLE
            print receive

    elif(trx_state == TRX.TRANSMIT):
        spi_xfer(RF_TXREG_WRITE + transmit[index])
        print "Send: ", transmit[index] 
        if index >= len(transmit) -1:
            spi_xfer(RF_SLEEP_MODE)
            trx_state = TRX.IDLE
        index += 1


def get_status():
    return spi_xfer(0x0000)


def start_send(packet):
    global transmit
    global index
    global trx_state

    index = 0
    transmit = packet

    trx_state = TRX.TRANSMIT
    spi_xfer(RF_TRANSMITTER_ON)


def start_receive():
    global receive
    global trx_state

    receive = []

    trx_state = TRX.RECEIVE
    spi_xfer(RF_RECEIVER_ON)


#-----------------------------------------------------------------------------
# send function
def send(data=0):
    '''Send data via RF chip.

    Keyword arguments:
    data -- data to transmit, 1 Byte (default 0)
    '''
    while GPIO.input(NIRQ):
        time.sleep(0.01) # wait 10ms to let the cpu perform other tasks
    spi_xfer(RF_TXREG_WRITE + data)


#-----------------------------------------------------------------------------
# low level function
def spi_xfer(cmd=0):
    '''Write command via SPI to RF chip.

    Keyword arguments:
    cmd -- command as hex value, 2 Byte

    Return
    read -- received data as hex value, 2 Byte
    '''
    read = spi.xfer([cmd >> 8])[0] << 8
    read += spi.xfer([cmd])[0]

    return read
