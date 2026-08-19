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
        self.conn = None
        self.curs = None

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
##      print(sql_statement)
##      print()

        sql_values = []
        telephone_lists = []
        email_lists = []
        phys_addr_lists = []
        note_lists = []
        for member in member_list:
            # Drop lists that are at the end of our list
            sql_values += member.values()[:-5]

            # Add the member_id to each list we dropped earlier and add
            # each of those lists to lists we'll use later
            for i in member.telephone_number:
                vl = i.values()
                vl.insert(0, member.member_id)
                telephone_lists.append(vl)
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
        try:
            self.db_connect()
            self.conn.begin()
            self.db_cursor()
            print("Um... adding data to tables disabled right now")
# The following lines are commented out for development
#           self.curs.execute(sql_statement, sql_values)
#           self.add_member_telephone(telephone_lists)
#           self.add_member_email(email_lists)
#           self.add_member_phys_addr(phys_addr_lists)
#           self.add_member_note(note_lists)
            self.conn.commit()
            self.curs.close()
            self.curs = None
            self.conn.close()
            self.conn = None
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other
        if self.curs is not None:
            self.curs.close()
        if self.conn is not None:
            self.conn.close()

    def add_member_email(self, list_list):
        """Take a list of EmailAddress objects for a member and add them
           to the database"""

        sql_statement = """
            INSERT INTO email_address (member_id, active, email_date,
                email_type, email_addr)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
##      print(sql_statement)
##      print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
##      print(sql_values)
##      print()
        try:
            self.curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other

    def add_member_note(self, list_list):
        """Take a list of MemberNote objects for a member and add them
           to the database"""

        sql_statement = """
            INSERT INTO member_note (member_id, active, note_time,
                member_note)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
##      print(sql_statement)
##      print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
##      print(sql_values)
##      print()
        try:
            self.curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other

    def add_member_phys_addr(self, list_list):
        """Take a list of PhysicalAddress objects for a member and add
           them to the database"""

        sql_statement = """
            INSERT INTO physical_address (member_id, active,
                phys_addr_date, phys_addr_type, country_code,
                postal_code, state_code, city_name, unit_number,
                street_number, street_name, street_direction,
                scscai_number, renter, lease_exp_date)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?, ?, ?, ?, ?,"\
                + " ?, ?, ?, ?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
##      print(sql_statement)
##      print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
##      print(sql_values)
##      print()
        try:
            self.curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other

    def add_member_telephone(self, list_list):
        """Take a list of TelephoneNumber objects for a member and add
           them to the database"""

        sql_statement = """
            INSERT INTO telephone_number (member_id, active, phone_date,
                phone_type, phone_country_code, phone_number, phone_ext)
            VALUES"""
        for i in range(len(list_list)):
            sql_statement += "\n(?, ?, ?, ?, ?, ?, ?),"
        sql_statement = sql_statement[:-1] + ";"
##      print(sql_statement)
##      print()

        sql_values = []
        for item_list in list_list:
            sql_values += item_list
##      print(sql_values)
##      print()
        try:
            self.curs.execute(sql_statement, sql_values)
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
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
            self.conn = mariadb.connect(
                host=self.db_host,
                port=self.db_port,
                ssl_verify_cert=True, # FIXME
                user=self.db_user,
                passwd=self.db_user_passwd,
                db=self.db_database)
            logging.info("Connected")
        except mariadb.Error as e:
            logging.info(f"Error connecting to the database: {e}")
            self.conn = None

    def db_cursor(self):
        if self.conn:
            try:
                self.curs = self.conn.cursor(named_tuple=True)
            except mariadb.Error as e:
                logging.info(f"MariaDB Error creating database curesor: {e}")
                self.curs = None
            except:
                logging.info(f"Error creating database curesor: {e}")
                self.curs = None

    def db_table_list(self):
        """Return a list of table names"""

        self.db_connect()
        items = []
        if self.conn:
            self.db_cursor()
            if self.curs:
                self.curs.execute("SHOW TABLES")
                for i in self.curs:
                    items.append(i)
                self.curs.close()
                self.conn.close()
        self.conn = None
        return items

    def get_members(self):
        """Return a list of member objects pulled from the database"""

        sql_statement = """
            SELECT member_id, user_name_logdb, surname, given_name,
                nickname, birthdate, deceased, dl_number, dl_state_code,
                dl_expiry_date
            FROM member"""
##      print(sql_statement)
##      print()

        members = []
        try:
            self.db_connect()
            self.conn.begin()
            self.db_cursor()
            self.curs.execute(sql_statement)
            rows = self.curs.fetchall()
            for i in rows:
                members.append(i)
            self.curs.close()
            self.curs = None
            self.conn.close()
            self.conn = None
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other
        return members

    def get_member_address(self, member_id):
        """Return a list of address rows for member_id"""

        sql_statement = """
            SELECT member_id, active, phys_addr_type, country_code,
                postal_code, state_code, city_name, unit_number,
                street_number, street_name, street_direction,
                scscai_number, renter, lease_exp_date
            FROM physical_address
            WHERE active and (member_id=?)
            ORDER BY phys_addr_type"""
##      print(sql_statement)
##      print()

        items = []
        try:
            self.db_connect()
            self.conn.begin()
            self.db_cursor()
            self.curs.execute(sql_statement, [member_id])
            rows = self.curs.fetchall()
            for i in rows:
                items.append(i)
            self.curs.close()
            self.curs = None
            self.conn.close()
            self.conn = None
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other
        return items

    def get_member_email(self, member_id):
        """Return a list of email rows for member_id"""

        sql_statement = """
            SELECT member_id, active, email_type, email_addr
            FROM email_address
            WHERE active and (member_id=?)
            ORDER BY email_type"""
##      print(sql_statement)
##      print()

        items = []
        try:
            self.db_connect()
            self.conn.begin()
            self.db_cursor()
            self.curs.execute(sql_statement, [member_id])
            rows = self.curs.fetchall()
            for i in rows:
                items.append(i)
            self.curs.close()
            self.curs = None
            self.conn.close()
            self.conn = None
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other
        return items

    def get_member_telephone(self, member_id):
        """Return a list of email rows for member_id"""

        sql_statement = """
            SELECT member_id, active, phone_type, phone_country_code,
                phone_number, phone_ext
            FROM telephone_number
            WHERE active and (member_id=?)
            ORDER BY phone_type"""
##      print(sql_statement)
##      print()

        items = []
        try:
            self.db_connect()
            self.conn.begin()
            self.db_cursor()
            self.curs.execute(sql_statement, [member_id])
            rows = self.curs.fetchall()
            for i in rows:
                items.append(i)
            self.curs.close()
            self.curs = None
            self.conn.close()
            self.conn = None
        except mariadb.Error as e:
            print(sys._getframe().f_code.co_name, " ", type(e), e)
            ## FIXME: raise something or other
        return items

if __name__ == '__main__':
    cmn = common.Common()
    pdb = PatrolDB(cmn)
    tables = pdb.db_table_list()
    if tables:
        print(f"### Tables:")
        for i in tables:
            print(f"    {i[0]}")
    else:
       print("No table names found")
