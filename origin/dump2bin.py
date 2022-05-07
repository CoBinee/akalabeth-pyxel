#!/usr/bin/env python
# coding: utf-8

# import
import sys

# dump to binary
def dump2bin(inname, outname):

    # output array
    outbytes = bytearray()

    # read input file
    with open(inname, 'r') as infile:
        for inline in infile:
            for hex in inline.split(' ', 16):
                if len(hex) == 2:
                    outbytes.append(int(hex, 16))

    # write output file
    with open(outname, 'wb') as outfile:
        outfile.write(outbytes)

# main entry
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('./dump2bin.py <input dump file> <output binary file>')
    else:
        dump2bin(sys.argv[1], sys.argv[2])
