#!/usr/bin/env python2.7

import crc16
import rf12

#----------------------------------------------------------------------------
GROUP_ID = 1
NODE_ID = 1



def checksum(data):
    '''Calculates CRC16 checksum of data.'''
    return crc16.crc16xmodem(data)

def getID():
    '''Generates ID in RF network.

    Depending on GROUP_ID and NODE_ID
    '''
    return (GROUP_ID << 13) + NODE_ID

#-----------------------------------------------------------------------------
# high level send function
def send(dest, data):
    '''Send data (64 Bytes).

    Byte 0-2:    PREAMBLE (3x 0xAA)
    Byte 3:      SYNC (0x2D)
    Byte 4,5:    TRANSMITTER ID
    Byte 6,7:    RECEIVER ID
    Byte 8-59:   DATA (52 Bytes)
    Byte 60,61:  CRC16 checksum
    Byte 62,63:  END (2x 0xAA)

    Keyword arguments:
    dest -- destination where data is sent to
    data -- data to transmit
    '''
    PREAMBLE = [0xAA, 0xAA, 0xAA]
    SYNC = 0x2D
    END = [0xAA, 0xAA]

    packet = PREAMBLE
    packet.append(SYNC)

    ID = getID()

    packet.append((ID >> 8) & 0xff)
    packet.append(ID & 0xff)

    packet.append((dest >> 8) & 0xff)
    packet.append(dest & 0xff)


    for c in data:
        packet.append(ord(c))

    cs = checksum(data)
    packet.append((cs >> 8) & 0xff)
    packet.append(cs & 0xff)

    packet.extend(END)

    rf12.start_send(packet)
