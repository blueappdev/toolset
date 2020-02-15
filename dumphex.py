#!/usr/bin/env python
#
# dumphex.py - dump hex representation of a binary file
#
# requires python 2.7
#

import getopt, glob, sys
import string

def usage():
    print "dumphex - dump hex representation of a binary file"

def represent(ch):
    return ch if 32 <= ord(ch) <= 127 else "."
    
def hexformat(n, len):
    return hex(n).upper()[2:].rjust(len, "0")
    
def processFile(file):
    stream = open(file,"rb")
    line = stream.read(16)
    counter = 0
    while len(line) > 0:
        print hexformat(counter, 4) + ":",
        for byte in line:
            byte = ord(byte)
            print hexformat(byte, 2), 
        for each in xrange(len(line), 16):
            print "  ", 
        print "", 
        print string.join(map(represent, line), "")
        counter = counter + len(line)
        line = stream.read(16)
    stream.close()
    
if __name__ == "__main__":
    options, arguments = getopt.getopt(sys.argv[1:], "") 
    if arguments == []:
        usage()
        sys.exit(2)

    for pattern in arguments:
        files = glob.glob(pattern)
        if files == []:
             print "No files found for", pattern
        for file in files:
            processFile(file)
             
