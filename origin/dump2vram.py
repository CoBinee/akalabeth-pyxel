#!/usr/bin/env python
# coding: utf-8

# import
import sys
import numpy as np
from PIL import Image

# get color bit
def getcolorbit(data, x, y):
    return (data[(y // 0x40) * 0x0028 + ((y % 0x40) // 0x08) * 0x0080 + (y % 0x08) * 0x0400 + (x // 0x07)] >> 7) & 0x01 if 0 <= x and x < 280 else 0

# get pixel bit
def getpixelbit(data, x, y):
    return (data[(y // 0x40) * 0x0028 + ((y % 0x40) // 0x08) * 0x0080 + (y % 0x08) * 0x0400 + (x // 0x07)] >> (x % 0x07)) & 0x01 if 0 <= 0 and x < 280 else 0

# dump to apple2 vram
def dump2vram(inname, outname):

    # read input file
    inputarray = bytearray()
    with open(inname, 'r') as infile:
        for inline in infile:
            for hex in inline.split(' ', 16):
                if len(hex) == 2:
                    inputarray.append(int(hex, 16))
    
    # get vram array
    vramarray = inputarray[4:inputarray[2] + inputarray[3] * 0x0100]

    # color table
    colortable = {
        'black':  (0x00, 0x00, 0x00), # black
        'green':  (0x43, 0xC3, 0x00), # green
        'purple': (0xB6, 0x3D, 0xFF), # purple
        'orange': (0xEA, 0x5D, 0x15), # orange
        'blue':   (0x10, 0xA4, 0xE3), # blue
        'white':  (0xFF, 0xFF, 0xFF), # white
    }
    
    # make green array
    greenarray = np.array(Image.new('RGB', (280, 192), colortable['black']))
    for y in range(192):
        for x in range(280):
            if getpixelbit(vramarray, x, y) != 0:
                greenarray[y, x] = colortable['green']

    # make color array
    colorarray = np.array(Image.new('RGB', (280, 192), colortable['black']))
    for y in range(192):
        bit_last = 0
        for x in range(280):
            bit_0 = getpixelbit(vramarray, x + 0x00, y)
            bit_1 = getpixelbit(vramarray, x + 0x01, y)
            color = getcolorbit(vramarray, x, y)
            if bit_0 == bit_last or bit_0 == bit_1:
                palette = 'black' if bit_0 == 0 else 'white'
            else:
                if x % 2 == 0:
                    if color == 0:
                        palette = 'green' if bit_0 == 0 else 'purple'
                    else:
                        palette = 'orange' if bit_0 == 0 else 'blue'
                else:
                    if color == 0:
                        palette = 'green' if bit_last == 0 else 'purple'
                    else:
                        palette = 'orange' if bit_last == 0 else 'blue'
            colorarray[y, x] = colortable[palette]
            bit_last = bit_0

    # show green image
    greenimage = Image.fromarray(greenarray)
    greenimage.show()

    # show color image
    colorimage = Image.fromarray(colorarray)
    colorimage.save(outname)
    colorimage.show()

# main entry
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('./dump2vram.py <input dump file> <output binary file>')
    else:
        dump2vram(sys.argv[1], sys.argv[2])
