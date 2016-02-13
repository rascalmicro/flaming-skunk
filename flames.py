#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys
import opc
import RPi.GPIO as GPIO
import spidev
import subprocess
import time
from PIL import Image

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def setupSpiPins(clkPin, misoPin, mosiPin, csPin):
    ''' Set all pins as an output except MISO (Master Input, Slave Output)'''
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(misoPin, GPIO.IN)
    GPIO.setup(mosiPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)

numLEDs = 64

def readADC(channel):
    if channel > 7 or channel < 0:
        return -1
    # spi.xfer2 sends three bytes and returns three bytes:
    # byte 1: the start bit (always 0x01)
    # byte 2: configure bits, see MCP3008 datasheet table 5-2
    # byte 3: don't care
    r = spi.xfer2([1, 8 + channel << 4, 0])
    # Three bytes are returned; the data (0-1023) is in the
    # lower 3 bits of byte 2, and byte 3 (datasheet figure 6-1)
    v = ((r[1] & 3) << 8) + r[2]
    return float(v)/1023.0

setupSpiPins(11, 9, 10, 8)
spi = spidev.SpiDev()
spi.open(0, 0)

client = opc.Client('localhost:7890')

gif_im = Image.open('embers-2015-04-14.gif')

im = gif_im.convert('RGB')

(width, height) = im.size
spacing = width / numLEDs

pixels = [ (0,0,0) ] * numLEDs

while True:
    for row in range(height):

        if(GPIO.input(17) !=1):
            print("Button 1 pressed")
        else:
            print("nothing")

        # data should be in the format: shift, fire/nofire
        hue_shift = readADC(0)
#        print('Shift is {0}'.format(shift))
        brightness = readADC(1)
        for i in range(numLEDs):
            r, g, b = im.getpixel((i * spacing, row))
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + hue_shift) % 1
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            pixels[i] = r*255.0, g*255.0, b*255.0
        client.put_pixels(pixels)
