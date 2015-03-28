import collections
from sys import stdout
from os.path import isfile

__author__ = 'California Audio Visual Preservation Project'
__name__ = 'Audio_factory'
__version__ = '0.0.5'

from subprocess import Popen
from subprocess import PIPE
from time import sleep
import os
import re
from onesheet.AudioObject import *
import threading
import Queue


ENCODING = 'Encoding'
IDLE = 'Idle'
HALTING = 'Halting'
PERCENT_RE = re.compile("(([0-90]?[0-9])|(100))%")
ETA_RE = re.compile("[0-9]?[0-9]:[0-9]?[0-9](?=(\s))")

DEBUG = False


class AudioFactory(threading.Thread):
    """
    The audioFactory class is managing and implementing the converting of wav files to mp3.
     It has the ability add to queues and run as a standalone single thread.
    """
    data_lock = threading.Lock()
    def __init__(self, verbose=False):
        """

        :param verbose: setting this to True makes LAME's progress data print to the console.
        :return:
        """
        threading.Thread.__init__(self)

        self.verbose = verbose
        self._queue = Queue.Queue()
        self._jobs = []
        self.currentFile = ""
        self.current_status = IDLE
        self.status_part = 0
        self.status_total = 0
        self.status_percentage = 0



    @property
    def hasTasks(self):
        """

        :return: bool
        """
        return not self._queue.empty()

    @property
    def percent_done(self):
        """

        :return: int
        """
        return self.status_percentage

    @property
    def jobs(self):
        return self._jobs

    def set_status(self, export_name, status):

        temp = []
        for job in self._jobs:
            if job['destination'] == export_name:
                job['status'] = status
                temp.append(job)
            else:
                temp.append(job)
        self._jobs = temp

    def get_status(self, source_name):
        for job in self._jobs:
            if job['source'] == source_name:
                return job['status']

    def change_output_name(self, source, new_destination):
        if os.path.splitext(new_destination)[1] != ".mp3":
            raise ValueError("Not a file")
        with self.data_lock:
            replacement_q = Queue.Queue()
            while not self._queue.empty():
                temp = self._queue.get()
                if temp['source'] == source:
                    temp['destination'] = new_destination
                replacement_q.put(temp)
            self._queue = replacement_q

            replacement_jobs = []
            for job in self._jobs:
                if job['source'] == source:
                    job['destination'] = new_destination
                replacement_jobs.append(job)
            self._jobs = replacement_jobs
        for job in self._jobs:
            print job

    def add_audio_file(self, source_file, destination_file=None):
        """

        :param source_file:         A wav file path as a string.
        :param destination_file:    The desired name for the mp3.
        """
        if destination_file is None:
            base, exention = os.path.splitext(os.path.basename(source_file))

            # Checks and Prevents you from adding the same file with the same destination
            queues = self.preview_queues()
            for queue in queues:
                if queue[1]['source'] == source_file:
                    if queue[1]['destination'] == os.path.join(os.path.dirname(source_file), (base + ".mp3")):
                        raise RuntimeError("You cannot add a file already in the queue.")
            if DEBUG:
                destination_file = os.path.join("/Users/lpsdesk/PycharmProjects/audio_convert", (base + ".mp3"))
            else:
                destination_file = os.path.join(os.path.dirname(source_file), (base + ".mp3"))
        with self.data_lock:
            # print source_file
            new_queue = dict({'source': source_file, 'destination': destination_file, 'status': "Queued"})
            self._queue.put(new_queue)
            self._jobs.append(new_queue)
            self.status_total += 1

    def remove_audio_file(self, source_file):
        """

        :param source_file: The path of the file you wish to remove from the queue.
        :return:
        """
        with self.data_lock:
            replacement_q = Queue.Queue()
            while not self._queue.empty():
                temp = self._queue.get()
                if temp['source'] == source_file:
                    continue
                else:
                    replacement_q.put(temp)
            self._queue = replacement_q

            replacement_jobs = []
            for job in self._jobs:
                if job['source'] == source_file:
                    continue
                else:
                    replacement_jobs.append(job)
            self._jobs = replacement_jobs
            self.status_total -= 1

    def preview_queues(self):
        """

        :return: a list[queue number, dict({'source', 'destination'})
        """
        replacement_q = Queue.Queue()
        return_q = []
        i = 0
        with self.data_lock:
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
            with self.data_lock:
                self.status_part += 1

        else:
            raise IndexError("No more in the queue")
        pass

    def encode_file_from_queue(self, source_file):
        """

        :param source_file: The file name of a file in the queue you wish to start encoding
        :return:
        """
        with self.data_lock:
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
            self._encode(encode_me)
            with self.data_lock:
                self.status_part += 1
        else:
            raise ValueError(source_file + "not found in queue")


    def remove_from_queue(self, source_file):
        """
        NOT IMPLEMENTED YET
        :param source_file:
        :return:
        """
        pass

    def kill_encoding(self):
        # print "killing"
        with self.data_lock:
            self.current_status = HALTING
            self.lame.kill()
            while self.lame.poll() is None:
                sleep(1)

    def _encode(self, item):
        self.current_status = ENCODING
        source = item['source']
        self.currentFile = source
        destination = item['destination']

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
        with self.data_lock:
            self.set_status(item['destination'], "Encoding")
        # print item['destination']
        if self.verbose:
            self.lame = Popen(command)
        else:
            self.lame = Popen(command, stderr=PIPE, universal_newlines=True)
            self.lame.stderr.flush()
            lines = collections.deque(maxlen=1)
            t = threading.Thread(target=self.read_output, args=(self.lame, lines.append))
            t.daemon = True
            t.start()
            sleep(1)
            while self.lame.poll() == None:
                line = lines[0]
                # print "\r" + line.rstrip(),
                raw_percentage = re.findall(PERCENT_RE, line)
                if raw_percentage:
                    percentage = int(raw_percentage[0][0])
                    self.status_percentage = percentage
                    # print "\r" + str(self.status_percentage) + "%",
                    # print data
                    # print lame.poll()
                    # print "got here"
                sleep(.01)

            t.join()

        # force the program to wait until file is converted
        self.lame.communicate()
        if self.current_status != HALTING:
            with self.data_lock:
                self.set_status(item['destination'], "Done")
                self.currentFile = ""
                self.current_status = IDLE
        else:
            with self.data_lock:
                self.set_status(item['destination'], "Aborted")


    def read_output(self, process, append):
        while process.stderr.readline != "" and process.poll() is None:
            line = process.stderr.readline()
            append(line)

    def run(self):
        # print "staring thread"
        """
        For running as a thead only!
        :return:
        """
        while self.hasTasks:

            if self.current_status == HALTING:
                self.current_status = IDLE
                break
            else:
                self.encode_next()
