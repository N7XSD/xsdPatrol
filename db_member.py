"""
Access MemberDB.  After data is moved to PatrolDB, MemberDB will be abandoned
"""

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
                `Renter?`, LeaseExpDate, Notes
            FROM Members"""
        print(sql_statement)
        print()
        self.curs_member.execute(sql_statement)
        members = []
        rows = self.curs_member.fetchall()
        for i in rows:
            m = common.Member()
            m.member_id = i.MemberID
            m.surname = i.LastName
            m.given_name = i.FirstName
            m.nickname = i.PrefName
            m.birthday = i.Birthday
            m.deceased = i[5]
            m.dl_number = i.DrLicenseNo
            m.dl_state_code = i.DLState	#FIXME: Compare to valid states
            m.dl_expiry_date = i.DrExpiryDate
            if i.CellPhone:
                cell = common.TelephoneNumber()
                cell.phone_type = 1
                cell.phone_number = i.CellPhone
                m.telephone_number.append(cell)
            if i.HomePhone:
                home = common.TelephoneNumber()
                home.phone_type = 2
                home.phone_number = i.HomePhone
                m.telephone_number.append(home)
            if i[11]:
                home = common.EmailAddress()
                home.phone_type = 2
                home.email_addr = i[11]
                m.email_address.append(home)
            if i.MAddress or i.City or i.State or i.ZIP or i.AssociationNo:
                home = common.PhysicalAddress()
                home.phys_addr_type = 1 # SCSCAI address
                home.postal_code = i.ZIP
                home.state_code = i.State
                home.city_name = i.City
#               FIXME: Parse MAddress to get street_*
                home.scscai_number = i.AssociationNo
                home.renter = i[17]
                home.lease_expiry_date = i.LeaseExpDate
                m.physical_address.append(home)
            if i.Notes:
                n = common.MemberNotes()
                n.member_note = i.Notes
                m.member_notes.append(n)
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
