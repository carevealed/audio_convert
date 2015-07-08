#!/usr/local/bin/python
import configparser
import sys
import subprocess

__title__ = 'Audio Convert'
__author__ = 'Henry Borchers'
__version__ = '0.1.1'
__license__ = 'GPL'

# import Queue
from os import walk
import os
import argparse
# sys.path.insert(0, os.path.abspath('..'))
from audio_convert.scripts.modules.Audio_factory import AudioFactory
settings_file = None
LAME_LOCATION = None


line = "--------------------------------------------------"





def openingBanner():
    print("\n")
    print("Audio converter script for CAVPP. \n" \
          "Dependencies: \n" \
          "Python 2.7 \n" \
          "OneSheet \n" \
          "ffmpeg \n" \
          "LAME \n" \
          "\n" \
          "Programmed by Henry Borchers\n")


def main(input_argument):
    global LAME_LOCATION
    derivative_maker = AudioFactory(LAME_LOCATION, verbose=True)
    # input_argument = str(argv[1])

    if os.path.isdir(input_argument):
        for root, dir, files in walk(input_argument):
            for file in files:
                if ".wav" in file:
                    # print("Adding \"" + path.join(root, file) + "\" to the queue."
                    derivative_maker.add_audio_file(os.path.join(root, file))
                    # print("found one"
    elif os.path.isfile(input_argument):
            if ".wav" in input_argument:
                print("Converting: " + os.path.join(input_argument))
                derivative_maker.add_audio_file(input_argument)
            else:
                # display_usage("This program only works with .wav files.")
                sys.stderr.write("This program only works with .wav files.")
    else:
        # display_usage("Not a valid file or directory")
        sys.stderr.write("Not a valid file or directory")

    # current_queue =         # display_usage("Missing directory or file")
    # for queue in derivative_maker.preview_queues():
    #     print(queue[0], queue[1]

    # print("\nencoding next\n"
    while derivative_maker.hasTasks:
        derivative_maker.encode_next()
        # encode_next
    # derivative_maker.daemon = True
    # derivative_maker.start()
    # derivative_maker.join()
    for queue in derivative_maker.preview_queues():
        print(queue[0], queue[1])



def setup_lame(settings_file):

    if not os.path.exists(settings_file):
        raise IOError(settings_file + " not found")

    # Look at the settings in ini file
    config = configparser.RawConfigParser()
    config.read([settings_file], encoding="utf-8")
    lame_location = config.get('EXTERNAL_PROGRAMS', 'lame_path')
    # print(lame_location)

    # test if they are valid
    try:
        subprocess.check_call([lame_location, "--license"])
    except FileNotFoundError:
        # if not, try to find it own.
        try:
            subprocess.check_call(['lame', "--license"])
            lame_location = 'lame'
        except FileNotFoundError:
            # sys.stderr.write("Unable to find lame mp3 encoder.\nExiting")
            raise FileNotFoundError("Unable to find lame")
    # if can't find return false
    return lame_location


def installed_start():
    # settings_file = os.path.abspath(os.path.join("audio_convert","AudioConvertSettings.ini"))
    settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../AudioConvertSEttings.ini')
    global LAME_LOCATION


    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="File or folder name", nargs='?', default="", type=str)
    parser.add_argument("-g", "--gui", help="EXPERIMENTAL: Loads the graphical user interface.", action='store_true')
    args = parser.parse_args()
    openingBanner()
    if args.gui:
        print("Starting graphical user interface!")
        # sys.path.insert(0, os.path.abspath('..'))
        from audio_convert.scripts.gui.gui import startup

        if args.input:
            startup(settings_file, args.input)
        else:
            startup(settings_file)

    elif args.input == "":
        parser.print_help()
    else:
        LAME_LOCATION = setup_lame(settings_file)
        main(args.input)
        # print(ars.input

if __name__ == '__main__':

   installed_start()
