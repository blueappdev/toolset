#!/usr/bin/python

# mp3towav.py
# MP3 to WAV conversion using ffmpeg

import sys, getopt, glob, os.path

def process(mp3Filename):
    print "Process", mp3Filename
    baseFilename, extension = os.path.splitext(mp3Filename)
    assert extension.lower() == ".mp3", "only mp3 files are supported"
    wavFilename = baseFilename + ".wav"
    cmd = "ffmpeg -y -v 0 -i \"%s\" \"%s\"" % (mp3Filename, wavFilename)
    code = os.system(cmd)
    if code != 0:
         print "ffmpeg failed"
         sys.exit(2)

def usage():
    print "Usage:"
    print "       mp3towav file1.mp3 file2.mp3 file3.mp3"
    print "       mp3towav *.mp3"

if __name__ == "__main__":
    print "MP3 to WAV converter using ffmpeg"

    opts, args = getopt.getopt(sys.argv[1:],"h")

    if opts != [] or args == []:
        usage()
        sys.exit(2)
        
    counter = 0
    for each in args:
        for filename in glob.glob(each):
            counter = counter + 1
            process(filename)
    print counter, "mp3 files processed"
