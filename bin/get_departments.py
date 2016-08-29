# -*- coding: utf-8 -*-

""" Utility for fetching a list of departments. """

import json

from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

from ems_update import fetch_departments, prune_failed
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

    departments = list(fetch_departments(config))
    departments = prune_failed(departments)
    groups = unpack(process_departments(departments, config))

    with open(args.outfile, 'w') as fout:
        for group in groups:
            fout.write(json.dumps(group) + '\n')


if __name__ == "__main__":
    main()
