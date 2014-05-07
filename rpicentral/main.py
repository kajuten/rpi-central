#!/usr/bin/env python2.7

import rpi
import rf12

def main():
    print "Start..."

    rf12.initialize(rf12.BAND_433MHZ)

    msg = 'Hello'

    try:
        print "Send \'" + msg + "\'"
        rpi.send(0, msg)
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

if __name__ == '__main__':
    main()
