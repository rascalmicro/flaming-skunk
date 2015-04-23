#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import colorsys, opc, subprocess, time
from PIL import Image

numLEDs = 64
client = opc.Client('localhost:7890')

#im = Image.open('flames.jpg')
gif_im = Image.open('embers-2015-04-14.gif')

im = gif_im.convert('RGB')

(width, height) = im.size
spacing = width / numLEDs

pixels = [ (0,0,0) ] * numLEDs

while True:
    for row in range(height):
        readings = subprocess.check_output('read-adc')
        shift = float(int(readings.split('\n')[4].split(' ')[2], 16))/65536.0
        for i in range(numLEDs):
            r, g, b = im.getpixel((i * spacing, row))
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + shift) % 1
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            pixels[i] = r*255.0, g*255.0, b*255.0
        client.put_pixels(pixels)
#        time.sleep(0.01)

#	for i in range(numLEDs):
#		pixels = [ (0,0,0) ] * numLEDs
#		pixels[i] = (255, 255, 255)
#		client.put_pixels(pixels)
#		time.sleep(0.01)
