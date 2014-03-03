#!/usr/bin/python

import time
import rf12

try:
    cmd = 0xff00
    print "sent:     " + hex(cmd)
    print "received: " + hex(rf12.spi_trans(cmd))
except Exception as e:
    print "Program halted"
    print type(e)
    print e.args
    print e
finally:
    # free resources
    rf12.cleanup()
