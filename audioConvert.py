import Queue
import os
from subprocess import PIPE, Popen
from os import walk, path
from sys import argv, stderr
import threading
from time import sleep
from onesheet.AudioObject import *
import re

__author__ = 'Henry Borchers'
line = "--------------------------------------------------"
DEBUG = True


ENCODING = 'Encoding'
IDLE = 'Idle'

PERCENT_RE = re.compile("(([0-90]?[0-9])|(100))%")
ETA_RE = re.compile("[0-9]?[0-9]:[0-9]?[0-9](?=(\s))")

class AudioFactory(threading.Thread):
    def __init__(self, verbose=True):
        threading.Thread.__init__(self)
        self.verbose = verbose
        self._queue = Queue.Queue()
        self.currentFile = ""
        self.current_status = ""
        self.status_part = 0
        self.status_total = 0
        self.status_percentage = 0


    @property
    def hasTasks(self):
        return not self._queue.empty()

    def add_audio_file(self, source_file, destination_file=None):
        if destination_file is None:
            base, exention = os.path.splitext(os.path.basename(source_file))
            if DEBUG:
                destination_file = os.path.join("/Users/lpsdesk/PycharmProjects/audio_convert", (base + ".mp3"))
            else:
                destination_file = os.path.join(os.path.dirname(source_file), (base + ".mp3"))
        new_queue = dict({'source': source_file, 'destination': destination_file})
        self._queue.put(new_queue)
        self.status_total += 1

    def remove_audio_file(self, source_file):
        replacement_q = Queue.Queue()
        while not self._queue.empty():
            temp = self._queue.get()
            if temp['source'] == source_file:
                continue
            replacement_q.put(temp)
        self._queue = replacement_q
        self.status_total -= 1

    def preview_queues(self):
        replacement_q = Queue.Queue()
        return_q = []
        i = 0
        while not self._queue.empty():
            temp = self._queue.get()
            return_q.append((i, temp))
            replacement_q.put(temp)
            i += 1
        self._queue = replacement_q
        return return_q

    def encode_next(self):
        if not self._queue.empty():
            self._encode(self._queue.get())
            self.status_part -= 1

        else:
            raise IndexError("No more in the queue")
        pass

    def encode_file(self, source_file):
        replacement_q = Queue.Queue()
        encode_me = None
        while not self._queue.empty():
            temp = self._queue.get()
            if temp['source'] == source_file:
                encode_me = temp
                continue
            replacement_q.put(temp)
        self._queue = replacement_q
        if encode_me:
            self.status_part += 1
            self._encode(encode_me)
        else:
            raise ValueError(source_file + "not found in queue")


    def remove_from_queue(self, source_file):
        pass

    def _encode(self, item):
        self.current_status = ENCODING
        source = item['source']
        self.currentFile = source
        destination = item['destination']
        print "Encoding " + source + " as " + destination
        # convert_audio takes a file name as the argument and passes it to LAME.
        # build the command for converting
        flags = "-s 44.1 --noreplaygain".split()
        file = AudioObject(source)
        # Mono
        if file.audioChannels == 1:
            flags = flags + (("-b 160 ".split()))
        # Stereo
        if file.audioChannels == 2:

            flags = flags + (("-b 320".split()))

        # flags = flags + (("-b 320".split()))
        program = ['lame']
        command = program
        command.append(source)
        command = command + flags
        command.append(destination)

        if self.verbose:
            lame = Popen(command, stdout=PIPE)
        else:
            lame = Popen(command, stdout=PIPE, stderr=PIPE)
            while True:
                data = lame.stderr.readline()
                if data == "":
                    break

                raw_percentage = re.findall(PERCENT_RE, data)
                if raw_percentage:
                    percentage = int(raw_percentage[0][0])
                    self.status_percentage = percentage
                print "\r" + str(self.status_percentage) + "%",
                # print data
                # print lame.poll()
                sleep(.1)


        # force the program to wait until file is converted
        lame.communicate()
        self.currentFile = ""
        self.current_status = IDLE

    def run(self):
        print "staring thread"
        while self.hasTasks:
            self.encode_next()
#
#
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
    derivative_maker = AudioFactory(verbose=False)
    input_argument = str(argv[1])
    if path.isdir(input_argument):
        for root, dir, files in walk(input_argument):
            for file in files:
                if ".wav" in file:
                    print "Adding \"" + path.join(root, file) + "\" to the queue."
                    derivative_maker.add_audio_file(path.join(root, file))
    elif path.isfile(input_argument):
            if ".wav" in input_argument:
                print "Converting: " + path.join(input_argument)
                derivative_maker.add_audio_file(input_argument)
            else:
                # display_usage("This program only works with .wav files.")
                print("This program only works with .wav files.")
    else:
        # display_usage("Not a valid file or directory")
        print("Not a valid file or directory")

    # current_queue =         # display_usage("Missing directory or file")
    for queue in derivative_maker.preview_queues():
        print queue[0], queue[1]

    # print "\nencoding next\n"
    # while derivative_maker.hasTasks:
    #     derivative_maker.encode_next()
    derivative_maker.start()
    for queue in derivative_maker.preview_queues():
        print queue[0], queue[1]

if __name__ == '__main__':
    main()