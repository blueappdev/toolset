#!/usr/bin/env python
#
# requires python 2.7
#
# tabby.py - tabular listing of a table file
#

import sys, getopt, glob, string
from xml.etree import ElementTree

class Formatter:
    def __init__(self, someArguments):
        options, arguments = getopt.getopt(someArguments, "")

        for option in options:
             self.exit("tabby.py: no options supported yet")

        self.counter = 0
        for pattern in arguments:
            for file in glob.glob(pattern):
                self.processFile(file)
        if self.counter == 0:
            print "tabby.py: No file processed."

    def exit(self, message):
        print message
        sys.exit(2)

    def processFile(self, aFilename):
        self.readFile(aFilename)
        for each in self.sheets:
            self.printSheet(each)
        self.counter += 1

    #
    # A sheet is a list of records.
    #
    def printSheet(self, aSheet):
        maxRecordLength = 0
        for each in aSheet:
            maxRecordLength = max(maxRecordLength, len(each))
        widths = [0] * maxRecordLength      # array of zeros [0,0,0,0 ...]
        for each in aSheet:
            for index, value in enumerate(each):
                widths[index] = max(widths[index], len(value))
        for each in aSheet:
            for index, value in enumerate(each):
                alphabeticCharacters = filter(lambda ch: ch.isalpha(), value)
                if alphabeticCharacters == "":
                    print value.rjust(widths[index]),
                else:
                    print value.ljust(widths[index]),
            print

    def readFile(self, aFilename):
        # if file type is xml 
        self.readTextFile(aFilename)

    #
    # Read a tab separated text file and store the record in self.sheets.
    # A Text files have only one worksheet/table.
    #
    def readTextFile(self, aFilename):
        self.sheets = []
        records = []
        self.sheets.append(records)
        stream = open(aFilename)
        for each in stream.readlines():
            records.append(map(string.strip, each.split("\t")))
        stream.close()
        
      
if __name__ == "__main__":
    Formatter(sys.argv[1:])
