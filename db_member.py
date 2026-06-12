"""
Access MemberDB.  After data is moved to PatrolDB, MemberDB will be abandoned
"""

import datetime
import logging

import common

DATE_FORMAT_MSACCESS = "#%m/%d/%Y#"
MAXINT_MSACCESS = 2147483647
MININT_MSACCESS = -2147483648


class MemberDB():
    """
    A class to manage the old MemberDB
    """
    # All functions and methods must return date time values as
    # datetime objects.  They must accept date time as datetime
    # objects and convert to the database native format.

    def __init__(self, cmn):
        logging.debug("Init db_member.MemberDB")
        self.cmn = cmn

    def get_active_members(self):
        """Return a dictionary with id:full_name"""

        sql_statement = """
            SELECT Members.MemberID, LastName, FirstName, PrefName
            FROM Members INNER JOIN Service
                ON (Members.MemberID = Service.MemberID)
            WHERE Service.DateDropped IS NULL
                OR (Service.DateRejoined IS NOT Null
                AND Service.DateRedropped IS NULL)"""
#       print(sql_statement)
#       print()
        self.curs_member.execute(sql_statement)
        name_dict = {}
        rows = self.curs_member.fetchall()
        for i in rows:
            name_dict[i.MemberID] = common.display_name(
                i.LastName, i.FirstName, i.PrefName)
        return name_dict

    def get_members(self):
        """Return a list of Member objects"""

        sql_statement = """
            SELECT MemberID, LastName, FirstName, PrefName, Birthday,
                `Deceased?`, DrLicenseNo, DLState, DrExpiryDate, CellPhone,
                HomePhone, `E-Mail`, MAddress, City, State, ZIP, AssociationNo,
                `Renter?`, LeaseExpDate, Notes, DHRdate
            FROM Members"""
#       print(sql_statement)
#       print()
        self.curs_member.execute(sql_statement)
        members = []
        rows = self.curs_member.fetchall()
        for i in rows:
            m = common.Member()
            m.member_id = i.MemberID
            m.surname = i.LastName
            m.given_name = i.FirstName
            m.nickname = i.PrefName
            m.birthdate = i.Birthday
            m.deceased = i[5] # Deceased?
            m.dl_number = i.DrLicenseNo
            m.dl_state_code = i.DLState
            m.dl_expiry_date = i.DrExpiryDate
#           if not isinstance(m.birthday, datetime.datetime):
#           if m.member_id > 780 or m.surname == "Scanlan":
#               print(f"{m.member_id}:  {m.surname}, {m.given_name}")
            m.telephone_number = []
            if i.CellPhone:
                cell = common.TelephoneNumber()
                cell.phone_type = 1 # Mobile/Cell
                cell.phone_number = i.CellPhone
                m.telephone_number.append(cell)
#               if m.member_id > 780 or m.surname == "Scanlan":
#                   print(f"        M:{cell.phone_number}{type(cell.phone_number)}")
            if i.HomePhone:
                home = common.TelephoneNumber()
                home.phone_type = 2 # Home
                home.phone_number = i.HomePhone
                m.telephone_number.append(home)
#               if m.member_id > 780 or m.surname == "Scanlan":
#                   print(f"        H:{home.phone_number}{type(home.phone_number)}")
            m.email_address = []
            if i[11]:	# E-mail
                home = common.EmailAddress()
                home.email_type = 2 # Home
                home.email_addr = i[11] # E-mail
                m.email_address.append(home)
            m.physical_address = []
            if i.MAddress or i.City or i.State or i.ZIP or i.AssociationNo:
                home = common.PhysicalAddress()
                home.phys_addr_type = 1 # SCSCAI address
                home.postal_code = i.ZIP
                home.state_code = i.State
                home.city_name = i.City
                if i.MAddress:
                    m_address = i.MAddress.split(maxsplit=1)
                    if m_address[0].isdigit():
                        home.street_number = m_address[0]
                        home.street_name = m_address[1]
                    else:
                        home.street_name = i.MAddress
                home.scscai_number = i.AssociationNo
                home.renter = i[17] # Renter?
                home.lease_expiry_date = i.LeaseExpDate
                m.physical_address.append(home)
            m.member_notes = []
            if i.Notes:
                n = common.MemberNotes()
                n.member_note = i.Notes
                m.member_notes.append(n)
            m.dl_history = []
            if i.DHRdate:
                n = common.DLHistory()
                n.dl_history_date = i.DHRdate
                n.dl_history_note = ""
                m.dl_history.append(n)

            members.append(m)
        return members

    def open_member_db(self):
        """Open Database used by Brian Dodd's applications"""

        try:
            import pyodbc
            conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=' + self.cmn.stns.get_pathname_member_db() + r';'
                r'Mode=Read;')
            logging.info("    connected to %s", conn_str)
            self.conn_member = pyodbc.connect(conn_str)
            self.curs_member = self.conn_member.cursor()
            return conn_str
        except:
            return None

if __name__ == '__main__':
    cmn = common.Common()
    d = MemberDB(cmn)

    d.open_member_db()
    print()
    print('Member DB')
    print('### Tables:')
    for i in d.curs_member.tables(tableType='TABLE'):
        print(i.table_name)
    print('### Views:')
    for i in d.curs_member.tables(tableType='VIEW'):
        print(i.table_name)
