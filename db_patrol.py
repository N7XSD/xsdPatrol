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

    def add_member(self, member_list, replace=False):
        """Take a list of Member objects and add them to the database"""

        if replace:
            sql_statement = "REPLACE "
        else:
            sql_statement = "INSERT "
        sql_statement += """
            INTO member (member_id, user_name_logdb, surname,
                given_name, nickname, birthdate, deceased, dl_number,
                dl_state_code, dl_expiry_date)
            VALUES"""
        for i in range(len(member_list)):
            sql_statement += "\n(?, ?, ?, ?, ?, ?, ?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
#       print(sql_statement)
#       print()

        sql_values = []
        for member in member_list:
            sql_values += member.values()[:-5]
        conn = None
        curs = None
        try:
            conn = self.db_connect()
            conn.begin()
            curs = self.db_cursor(conn)
            curs.execute(sql_statement, sql_values)
            conn.commit()
            curs.close()
            curs = None
            conn.close()
            conn = None
        except Exception as e:
            print(type(e), e)
        if curs is not None:
            curs.close()
        if conn is not None:
            conn.close()
        ## raise something or other

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
            logging.info(f"Attempting connection to {self.db_database}")
            # Instantiate Connection
            conn = mariadb.connect(
                host=self.db_host,
                port=self.db_port,
                ssl_verify_cert=True, # FIXME
                user=self.db_user,
                passwd=self.db_user_passwd,
                db=self.db_database)
            logging.info("Connected")
        except mariadb.Error as e:
            logging.info(f"Error connecting to the database: {e}")
            conn = None
        return conn

    def db_cursor(self, conn):
        if conn:
            try:
                curs = conn.cursor(named_tuple=True)
            except mariadb.Error as e:
                logging.info(f"MariaDB Error creating database curesor: {e}")
                curs = None
            except:
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
