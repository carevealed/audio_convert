from subprocess import PIPE, Popen
from os import walk, path
from sys import argv, stderr
from AudioObject import AudioObject

__author__ = 'Henry Borchers'
line = "--------------------------------------------------"

def convert_audio(fileName):
# convert_audio takes a file name as the argument and passes it to LAME.
# build the command for converting
    flags = "-s 44.1 --noreplaygain".split()
    file = AudioObject(fileName)
    # Mono
    if file.getAudioChannels() == 1:
        flags = flags + (("-b 160 ".split()))
    # Stereo
    if file.getAudioChannels() == 2:

        flags = flags + (("-b 320".split()))

    # flags = flags + (("-b 320".split()))
    program = ['lame']
    command = program
    command.append(fileName)
    command = command + flags

    lame = Popen(command, stdout=PIPE)

    # force the program to wait until file is converted
    lame.communicate()


def display_usage(errorMessage):
    if errorMessage:
        print line
        stderr.write("Error: " + errorMessage + "\n")
        print line
        # print "Error: " + errorMessage
    print "Usage: " + path.basename(__file__) + " directory"


def openingBanner():
    print"\n"
    print "Audio converter script for CAVPP. \n" \
          "Dependencies: \n" \
          "Python 2.7 \n" \
          "ffmpeg \n" \
          "\n" \
          "Programmed by Henry Borchers"


def main():
    openingBanner()
    try:
        input_argument = str(argv[1])
        if path.isdir(input_argument):
            for root, dir, files in walk(input_argument):
                for file in files:
                    if ".wav" in file:
                        print "Converting: " + path.join(root, file)
                        convert_audio(path.join(root, file))
        elif path.isfile(input_argument):
                if ".wav" in input_argument:
                    print "Converting: " + path.join(input_argument)
                    convert_audio(input_argument)
                else:
                    display_usage("This program only works with .wav files.")
        else:
            display_usage("Not a valid file or directory")

    except IndexError:
        display_usage("Missing directory or file")

if __name__ == '__main__':
    main()