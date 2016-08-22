#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyodbc

from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

def main():
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

    connstr = "SERVER=%s;DRIVER=%s;DATABASE=%s;UID=%s;PWD=%s;Trusted_Connection=%s;" 
    connstr = connstr % (
                         config.get("DATABASE", "server"),
                         config.get("DATABASE", "driver"),
                         config.get("DATABASE", "database"),
                         config.get("DATABASE", "username"),
                         config.get("DATABASE", "password"),
                         config.get("DATABASE", "trusted_connection"),
                        )

    conn = pyodbc.connect(connstr)
    cur = conn.cursor()

    cur.execute("USE EMS;")
    try:
        cur.execute("EXEC EMS.dbo.HRTK_Update_Group;")

        result = cur.fetchall()

        cur.commit()
        conn.commit()

        print "Update Successful!"

    except Exception:
        print "An error occurred, could not update"

        raise

    print result


if __name__ == "__main__":
    main()
