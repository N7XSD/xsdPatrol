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
        email_lists = []
        phys_addr_lists = []
        note_lists = []
        for member in member_list:
            # Drop lists that are at the end of our list
            sql_values += member.values()[:-5]

            # Add the member_id to each list we dropped earlier and add
            # each of those lists to lists we'll use later
            for i in member.email_address:
                vl = i.values()
                vl.insert(0, member.member_id)
                email_lists.append(vl)
            for i in member.physical_address:
                vl = i.values()
                vl.insert(0, member.member_id)
                phys_addr_lists.append(vl)
            for i in member.member_note:
                vl = i.values()
                vl.insert(0, member.member_id)
                note_lists.append(vl)
        conn = None
        curs = None
        try:
            conn = self.db_connect()
            conn.begin()
            curs = self.db_cursor(conn)
#           curs.execute(sql_statement, sql_values)
#           self.add_member_email(email_lists, db_cursor=curs)
            self.add_member_phys_addr(phys_addr_lists, db_cursor=curs)
#           self.add_member_note(note_lists, db_cursor=curs)
            conn.commit()
            curs.close()
            curs = None
            conn.close()
            conn = None
        except mariadb.Error as e:
            print(type(e), e)
            ## FIXME: raise something or other
        if curs is not None:
            curs.close()
        if conn is not None:
            conn.close()

    def add_member_email(self, list_list, db_cursor=None):
        """Take a list of EmailAddress objects for a member and add them
           to the database"""

        curs = db_cursor
        sql_statement = """
            INSERT INTO email_address (member_id, active, email_type, email_addr)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
#       print(sql_statement)
#       print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
#       print(sql_values)
#       print()
        try:
            curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(type(e), e)
            ## FIXME: raise something or other

    def add_member_note(self, list_list, db_cursor=None):
        """Take a list of MemberNote objects for a member and add them
           to the database"""

        curs = db_cursor
        sql_statement = """
            INSERT INTO member_note (member_id, active, note_time,
                member_note)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
#       print(sql_statement)
#       print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
#       print(sql_values)
#       print()
        try:
            curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(type(e), e)
            ## FIXME: raise something or other

    def add_member_phys_addr(self, list_list, db_cursor=None):
        """Take a list of PhysicalAddress objects for a member and add
           them to the database"""

        curs = db_cursor
        sql_statement = """
            INSERT INTO physical_address (member_id, active,
                phys_addr_date, phys_addr_type, country_code,
                postal_code, state_code, city_name, unit_number,
                street_number, street_name, street_direction,
                scscai_number, renter, lease_exp_date)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
#       print(sql_statement)
#       print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
#       print(sql_values)
#       print()
        try:
            curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(type(e), e)
            ## FIXME: raise something or other

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
