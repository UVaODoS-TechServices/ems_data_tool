#! /usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

from ems_update import verify_database

def main():
    parser = ArgumentParser()
    parser.add_argument(
                        "-c",
                        "--configfile",
                        nargs='?',
                        help="filename that contains configuration data (i.e. somefile.ini)",
                        required=True
                       )
    parser.add_argument(
                        "-f",
                        "--filenames",
                        nargs='*',
                        help="script files to check the database (i.e. somefile.sql)",
                        required=True
                       )
    
    args = parser.parse_args()
    
    config = SafeConfigParser()
    config.optionxform(str())
    config.read(args.configfile)
    result = verify_database(config, args.filenames)
    
    if result:
        print "passed!"
    
    else:
        print "failed!", result


if __name__ == "__main__":
    main()
