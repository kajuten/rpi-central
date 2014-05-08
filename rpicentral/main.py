#!/usr/bin/env python2.7

import rpi
import rf12
import time

def main():
    print "Start..."

    rf12.initialize(rf12.BAND_433MHZ)

    print "Status: " + bin(rf12.get_status())


    msg = 'Hello'
    print "ID: " + bin(rpi.getID())
    print "\nSend \'" + msg + "\'"
    rpi.send(0, msg)
    rf12.start_receive()

    try:
        while True:
            rf12.get_status()
            time.sleep(10)
    except KeyboardInterrupt:
        print "Programm stopped"
    except Exception, e:
        print "Program halted"
        print type(e)
        print e
    finally:
        # free resources
        rf12.cleanup()

if __name__ == '__main__':
    main()
