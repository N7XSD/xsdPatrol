"""
Access PatrolDB.
"""

import configparser
import datetime
import logging
import mariadb
import sys

import common


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

        # This is just a stub for reading the configuation.  It's safer
        # than hard coding password, etc.
        config = configparser.ConfigParser()
        config.read("my.ini")
        if "client-server" in config:
            sect = config["client-server"]
            self.db_host = sect["host"]
            self.db_port = int(sect["port"])
            self.db_user = sect["user"]
            self.db_user_passwd = sect["password"]
            self.db_database = sect["database"]

        try:
            print(f"Attempting connection to {self.db_database}")
            # Instantiate Connection
            conn = mariadb.connect(
                host=self.db_host,
                port=self.db_port,
                ssl_verify_cert=True, # FIXME
                user=self.db_user,
                passwd=self.db_user_passwd,
                db=self.db_database)
            print("Connected")
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
            print(f"### Tables:")
            curs.execute("SHOW TABLES")
            for i in curs:
                print(f"    {i[0]}")
            curs.close()
            conn.close()
        else:
            print("PatrolDB error: Cursor not defined")
    else:
        print("PatrolDB error: Connection not defined")

