"""
Access PatrolDB.
"""

import datetime
import logging
import sys

import common

# To be imported later
mariadb = None


class PatrolDB():
    """
    A class to manage PatrolDB
    """
    # All functions and methods must return date time values as
    # datetime objects.  They must accept date time as datetime
    # objects and convert to the database native format.

    def __init__(self, cmn):
        logging.debug("Init db_patrol.PatrolDB")
        self.cmn = cmn

    def db_connect(self):
        """Connect to the Patrol database"""

        db_host = "serverless-northeurope.sysp0000.db3.skysql.com"
        db_port = 4007
        db_user = "dbpbf14211271"
        db_user_pass = "ws1c6y7F:4FgGJq90qeKkl3" # FIXME
        db_database = "patrol"
        try:
            import mariadb
            # Instantiate Connection
            conn = mariadb.connect(
                host=db_host,
                port=db_port,
                ssl_verify_cert=True, # FIXME
                user=db_user,
                passwd=db_user_pass,
                db=db_database)
#           logging.info("    connected to %s", conn_str)
        except mariadb.Error as e:
            print(f"Error connecting to the database: {e}")
            logging.info(f"Error connecting to the database: {e}")
            conn = None
        return conn

    def db_cursor(self, conn):
        if conn:
            try:
                curs = conn.cursor(named_tuple=True)
            except mariadb.Error as e:
                print(f"MariaDB Error creating database curesor: {e}")
                logging.info(f"MariaDB Error creating database curesor: {e}")
                curs = None
            except:
                print(f"Error creating database curesor: {e}")
                logging.info(f"Error creating database curesor: {e}")
                curs = None
        return curs

if __name__ == '__main__':
    cmn = common.Common()
    pdb = PatrolDB(cmn)
    conn = pdb.db_connect()
    if conn:
        curs = pdb.db_cursor(conn)
        if curs:
            print('PatrolDB Tables:')
            curs.execute("SHOW TABLES")
            for i in curs:
                print(f"    {i[0]}")
            curs.close()
            conn.close()
        else:
            print("PatrolDB error: Cursor not defined")
    else:
        print("PatrolDB error: Connection not defined")

