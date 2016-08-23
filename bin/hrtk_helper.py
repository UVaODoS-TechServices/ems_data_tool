# -*- coding: utf-8 -*-

""" Utility for updating ems staging database. """

from ConfigParser import SafeConfigParser
from argparse import ArgumentParser

import pyodbc

from lib.tools import create_connmsg

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

    args = parser.parse_args()

    config = SafeConfigParser()
    config.optionxform(str())

    config.read(args.configfile)

    connmsg = create_connmsg(svr=config.get("DATABASE", "server"),
                             drv=config.get("DATABASE", "driver"),
                             db=config.get("DATABASE", "database"),
                             un=config.get("DATABASE", "username"),
                             pwd=config.get("DATABASE", "password"),
                             tc=config.get("DATABASE", "trusted_connection"))

    conn = pyodbc.connect(connmsg)
    cur = conn.cursor()

    cur.execute("USE EMS;")
    
    try:
        cur.execute("EXEC EMS.dbo.HRTK_Update_Group;")

        result = cur.fetchall()

        cur.commit()
        conn.commit()

        print "Update Successful!"

    except:
        print "An error occurred, could not update"

        raise

    print result


if __name__ == "__main__":
    main()
