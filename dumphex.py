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

def getCharacterRepresentation(aCharacter):
    n = ord(aCharacter)
    if n < 32 or n > 127:
        return "."
    else:
        return aCharacter

def processFile(file):
    stream = open(file,"rb")
    line = stream.read(16)
    counter = 0
    while len(line) > 0:
        print hex(counter).upper()[2:].rjust(4,"0") + ":",
        for byte in line:
            byte = ord(byte)
            print hex(byte).upper()[2:].rjust(2,"0"), 
        for each in xrange(len(line),16):
            print "  ", 
        print "", 
        print string.join(map(getCharacterRepresentation, line), "")
        counter = counter + len(line)
        line = stream.read(16)
    stream.close()
    
if __name__ == "__main__":
    options, arguments = getopt.getopt(sys.argv[1:], "") 
    if arguments == []:
        usage()
        sys.exit(2)

    for eachFilePattern in arguments:
        files = glob.glob(eachFilePattern)
        if files == []:
             print "No files found for", eachFilePattern
        for each in files:
            processFile(each)
             
