# -*- coding: utf-8 -*-

""" Utility for fetching a list of departments. """

import json
import sys

from argparse import ArgumentParser
from ConfigParser import SafeConfigParser
from multiprocessing import Process, Queue

from ems_update import fetch_departments, prune_failed, WritingWorker
from lib.groups import process_departments
from lib.tools import unpack

def main():
    """ Where the magic happens. """

    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--configfile",
        nargs='?',
        help="filename that contains configuration data (i.e. somefile.ini)",
        required=True
        )
    parser.add_argument(
        "-o",
        "--outfile",
        nargs='?',
        help="filename to output data to (i.e. somefile.json)",
        required=True
        )

    args = parser.parse_args()

    config = SafeConfigParser()
    config.optionxform(str())
    config.read(args.configfile)

    worker = WritingWorker(args.outfile)
    queue = Queue()
    process = Process(target=worker.run, args=(queue,))
    process.isDaemon = True
    process.start()

    for department in prune_failed(list(fetch_departments(config))):
        queue.put(process_departments([department], config))
    
    queue.put("STOP")
    process.join()

    sys.exit(0)


if __name__ == "__main__":
    main()
