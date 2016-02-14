#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys
import opc
import RPi.GPIO as GPIO
import subprocess
import time
from PIL import Image

def setupSpiPins(clkPin, misoPin, mosiPin, csPin):
    ''' Set all pins as an output except MISO (Master Input, Slave Output)'''
    GPIO.setup(clkPin, GPIO.OUT)
    GPIO.setup(misoPin, GPIO.IN)
    GPIO.setup(mosiPin, GPIO.OUT)
    GPIO.setup(csPin, GPIO.OUT)

def transfer_byte(data, clkPin, misoPin, mosiPin):
    retVal = 0

    for bit in range(8):
        # Set RPi's output bit high or low depending on highest bit of data field
        if data & 0x80:
            GPIO.output(mosiPin, GPIO.HIGH)
        else:
            GPIO.output(mosiPin, GPIO.LOW)

        # Advance data to the next bit
        data <<= 1

        # Read 1 data bit in
        if GPIO.input(misoPin):
            retVal |= 0x1

        # Advance input to next bit
        retVal <<= 1

        # Pulse the clock pin HIGH then immediately low
        GPIO.output(clkPin, GPIO.HIGH)
        GPIO.output(clkPin, GPIO.LOW)

    return retVal/2

def transfer_bytes(bytes, clkPin, misoPin, mosiPin, csPin):

    received_bytes = [transfer_byte(byte, clkPin, misoPin, mosiPin) for byte in bytes]
    return received_bytes

def readADC(channel, clkPin, misoPin, mosiPin, csPin):
    if channel > 7 or channel < 0:
        return -1

    # Datasheet says chip select must be pulled high between conversions
    GPIO.output(csPin, GPIO.HIGH)

    # Start the read with both clock and chip select low
    GPIO.output(csPin, GPIO.LOW)
    GPIO.output(clkPin, GPIO.HIGH)

    reading = transfer_bytes([1, 8 + channel << 4, 0], clkPin, misoPin, mosiPin, csPin)

    GPIO.output(csPin, GPIO.HIGH)

    return float(((reading[1] & 3) << 8) + reading[2])/1023.0

RED_BUTTON = 17
BLUE_BUTTON = 18
YELLOW_BUTTON = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(YELLOW_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

numLEDs = 64

setupSpiPins(11, 9, 10, 8)

client = opc.Client('localhost:7890')

gif_im = Image.open('embers-2015-04-14.gif')

im = gif_im.convert('RGB')

(width, height) = im.size
spacing = width / numLEDs

pixels = [ (0,0,0) ] * numLEDs

iterations = 0

# hacky code to calculate average values of flickery flames image
#
#red = 0.0
#green = 0.0
#blue = 0.0

#for row in range(height):
#    for i in range(numLEDs):
#        r, g, b = im.getpixel((i * spacing, row))
#        red = red + float(r)
#        green = green + float(g)
#        blue = blue + float(b)

#print red/(height * numLEDs)
#print green/(height * numLEDs)
#print blue/(height * numLEDs)

while True:
    for row in range(height):

        hue_shift = readADC(0, 11, 9, 10, 8)
        brightness = readADC(1, 11, 9, 10, 8)
        duration = readADC(2, 11, 9, 10, 8)
        #print "duration: {0}".format(duration)
        for i in range(numLEDs):
            # Flicker if blue button pressed, or red pressed recently
            if((GPIO.input(BLUE_BUTTON) !=1) or (iterations > 0)):
                r, g, b = im.getpixel((i * spacing, row))
            else:
                r, g, b = (152, 48, 13) # assign average values of flames image
            # If red button pressed, start long period of flickering
            if(GPIO.input(RED_BUTTON) != 1):
                iterations = int(duration * 100)
            # If yellow button pressed, stop flickering, even if in long period
            if(GPIO.input(YELLOW_BUTTON) != 1):
                iterations = 0
                r, g, b = (152, 48, 13) # assign average values of flames image
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + hue_shift) % 1
            v = v * brightness
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            pixels[i] = r*255.0, g*255.0, b*255.0
        client.put_pixels(pixels)
        #print iterations
    iterations = iterations - 1
