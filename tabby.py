#!/usr/bin/env python
#
# requires python 2.7
#
# tabby.py - tabular listing of a table file
#

import sys, getopt, glob, string
import xml.etree.ElementTree

def exit(*args):
    if len(args):
        print "tabby.py:",
        for each in args:
            print  each,
        print 
    sys.exit(2)

class Workbook:
    def __init__(self):
        self.sheets = []

    def addSheet(self, aSheet):
        self.sheets.append(aSheet)

class Sheet:
    def __init__(self):
        self.records = []

    def addRecord(self, aRecord):
        self.records.append(aRecord)

class FileReaderInterface:
    def __init__(self, aFilename):
        self.filename = aFilename

    def getFileReaderClass(self):
        if self.isXMLFile():
            return XMLFileReader
        if self.isZipFile():
            exit("unsupported file format")
        return TextFileReader

    def isXMLFile(self):   
        stream = open(self.filename)
        # BOM should be handled
        contents = stream.read(10)
        stream.close()
        return contents.startswith("<")

    def isZipFile(self):   
        stream = open(self.filename)
        contents = stream.read(10)
        stream.close()
        return contents.startswith("PK")

    def getWorkbook(self):
        return self.getFileReaderClass()(self.filename).getWorkbook()
        
class FileReader:
    def __init__(self, aFilename):
        self.filename = aFilename

class TextFileReader(FileReader):
    def __init__(self, aFilename):
        FileReader.__init__(self, aFilename)

    #
    # Read a tab separated text file and store the records in self.sheets.
    # Text files have exactly one worksheet/table.
    #
    def getWorkbook(self):
        self.workbook = Workbook()
	self.workbook.addSheet(Sheet())
        stream = open(self.filename)
        for each in stream.readlines():
            self.currentSheet().addRecord(map(string.strip, each.split("\t")))
        stream.close()
        return self.workbook

    def currentSheet(self):
        return self.workbook.sheets[-1]

class XMLFileReader(FileReader):
    def __init__(self, aFilename):
        FileReader.__init__(self, aFilename)

    def getWorkbook(self):
        self.workbook = Workbook()
        tree = xml.etree.ElementTree.parse(self.filename)
        root = tree.getroot()
        for each in root:
            if self.hasTag(each, "Worksheet"):
                self.processWorksheet(each)
        return self.workbook

    def processWorksheet(self, anXMLElement):
        self.currentSheet = Sheet()
	self.workbook.addSheet(self.currentSheet)
        for each in anXMLElement:
            if self.hasTag(each, "Table"):
                self.processTable(each)

    def processTable(self, anXMLElement):
        for each in anXMLElement:
            if self.hasTag(each, "Row"):
                self.processRow(each)

    def processRow(self, anXMLElement):
        self.currentRecord = []
        self.currentSheet.addRecord(self.currentRecord)
        for each in anXMLElement:
            if self.hasTag(each, "Cell"):
                self.processCell(each)

    def processCell(self, anXMLElement):
        for each in anXMLElement:
            if self.hasTag(each, "Data"):
                self.processData(each)

    def processData(self, anElement):
        self.currentRecord.append(anElement.text)

    def hasTag(self, anElement, tagName):
        return self.extractTag(anElement) == tagName

    def extractTag(self, anElement):
        tokens = anElement.tag.split("}")
        assert(len(tokens) == 2)
        return tokens[-1]

class Formatter:
    def __init__(self, someArguments):
        self.indexesToExtract = None  # by default extract all
        options, arguments = getopt.getopt(someArguments, "s:h")

        for key, value in options:
             if key == "-h":
                  self.usage()
                  exit()
             elif key == "-s":
                 self.setWorksheetsToExtractFromOptionValue(value)    
             else:
                 exit("unsupported option")

        if arguments == []:
            exit("no arguments found")

        self.counter = 0
        for pattern in arguments:
            for file in glob.glob(pattern):
                self.processFile(file)
        if self.counter == 0:
            exit("no files found")

    def usage(self):
        print "tabby.py: extract excel data"
        print "usage: tabby.py [-h] -[s num] file [ file...]"
        print "  -h - help"
        print "  -s num (integer)"
        print "    extract worksheet with index num"

    def setWorksheetsToExtractFromOptionValue(self, optionValue):
        self.indexesToExtract = [ int(optionValue) ]

    def processFile(self, aFilename):
        self.workbook = FileReaderInterface(aFilename).getWorkbook()
        indexes = self.indexesToExtract
        if indexes is None:
            indexes = range(1, len(self.workbook.sheets) + 1)
        #print "indexes", indexes
        for each in indexes:
            sheet = self.getSheetWithIndex(each)
            if sheet is None:
                exit("worksheet", str(each), "not found")
            else:
                self.printSheet(sheet)
        self.counter += 1
    
    # The index is based on one and not on zero
    def getSheetWithIndex(self, index):
        sheets = self.workbook.sheets
        if 1 <= index <= len(sheets):
            return sheets[index-1]       
        else:
            return None

    #
    # A sheet is a list of records.
    #
    def printSheet(self, aSheet):
        maxRecordLength = 0
        for each in aSheet.records:
            maxRecordLength = max(maxRecordLength, len(each))
        widths = [0] * maxRecordLength      # array of zeros [0,0,0,0 ...]
        for each in aSheet.records:
            for index, value in enumerate(each):
                widths[index] = max(widths[index], len(value))
        for each in aSheet.records:
            for index, value in enumerate(each):
                alphabeticCharacters = filter(lambda ch: ch.isalpha(), value)
                if alphabeticCharacters == "":
                    print value.rjust(widths[index]),
                else:
                    print value.ljust(widths[index]),
            print

if __name__ == "__main__":
    Formatter(sys.argv[1:])

