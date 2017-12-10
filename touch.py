#!/usr/bin/env python
#
# touch.py - remove files
#
# python 2.7 required
#

import sys, getopt, glob
import os, os.path 

def usage():
    print "touch.py - remove files"
    print "    -a not supported change only the access time"
    print "    -c not supported do not create any file"
    print "    -d not supported (ignored)"
    print "    -f not supported"
    print "    -h not supported"
    print "    -m not supported change only the modification time"
    print "    -t not supported"
    print "    -t not supported"
            
if __name__ == "__main__":
    options, arguments = getopt.getopt(sys.argv[1:], "acdfhmrt")
        
    if arguments == []:
        usage()
        sys.exit(2)
    
    for key, value in options:
        print "options not supported yet", key
        sys.exit(2)

    for filename in arguments:
        if not os.path.exists(filename):
            stream = open(filename,"w")
            stream.close()
               

   
    
    
