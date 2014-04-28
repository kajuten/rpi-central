#!/usr/bin/env python2.7

import time
import rf12

rf12.initialize(rf12.BAND_433MHZ)

try:
    cmd = 0xff00
    print "sent:     " + hex(cmd)
    print "received: " + hex(rf12.spi_xfer(cmd))
except KeyboardInterrupt:
    print "Programm stopped"
except Exception as e:
    print "Program halted"
    print type(e)
    print e.args
    print e
finally:
    # free resources
    rf12.cleanup()
