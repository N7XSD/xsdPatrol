"""
A place to keep data
"""

import pyodbc

import common
import datetime
import logging
import settings

DATE_FORMAT_MSACCESS = "#%m/%d/%Y#"


def display_name(surname, first_name, pref_name):
    """Return the full name as a string"""
    if not pref_name or pref_name == first_name:
        name = f"{first_name} {surname}"
    else:
        name = f'{first_name} "{pref_name}" {surname}'
    return name


def display_name_by_surname(surname, first_name, pref_name):
    """Return the full name, surname first, as a string"""
    if not pref_name or pref_name == first_name:
        name = f"{surname}, {first_name}"
    else:
        name = f'{surname}, {first_name} "{pref_name}"'
    return name


def parse_dispatch_name(disp_name):
    """Parse names in dispatch DB into surname, given name,
       and prefered name"""
    gname = ""
    pname = ""
    if not disp_name:
        surname = disp_name.strip()
    else:
        name_parts = disp_name.split()
        surname = name_parts[-1].strip()
        gname = ""
        for i in range(0, len(name_parts) - 1):
            gname += name_parts[i].strip() + " "
        gname = gname.strip()

    # Ugly hack to fix some names
    if disp_name == "Linda Van Horn":
        surname = "Van Horn"
        gname = "Linda"
    elif disp_name == "Maureen Mc Cartin":
        surname = "McCartin"
        gname = "Maureen"
    elif disp_name == "Marian De Sumrak":
        surname = "De Sumrak"
        gname = "Marian"
    elif disp_name == "De Ila Meyer":
        surname = "Meyer"
        gname = "De Ila"
    # Users with prefered names
    elif disp_name == "Geraldean Jeri Stephan":
        surname = "Stephan"
        gname = "Geraldean"
        pname = "Jerri"

    return (surname, gname, pname)

class Data():
    """
    A class to manage data
    """
    # All functions and methods must return date time values as
    # datetime objects.  They must accept date time as datetime
    # objects and convert to the database native format.  For SQLite
    # we use ISO date strings.

    def __init__(self, cmn):
        logging.debug("Init data.Data")
        self.cmn = cmn

    def get_car_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both satart and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT InService_DateTime, Car_Number, Watch_ID, Shift_Number,
                Driver1_ID, Driver1_Hours, Driver2_ID, Driver2_Hours,
                Trainee_ID, Trainee_Hours, Observer, Observer_Hours
            FROM Car_Details
            WHERE Watch_ID BETWEEN """ + s_watch_st + """
                AND """ + e_watch_st
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_dt = self.cmn.convert_watch_date(
                i.Watch_ID, i.Shift_Number)

            unit_st = "Car " + str(i.Car_Number)
            if i.Driver1_ID:
                te = common.TimeEntry()
                te.user_id = i.Driver1_ID
                te.unit_id = unit_st
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Driver1_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " WC"
                    te.hours_rec = 0.0
                te_list.append(te)
            elif i.Driver2_ID:
                te = common.TimeEntry()
                te.user_id = i.Driver2_ID
                te.unit_id = unit_st
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Driver2_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " WC"
                    te.hours_rec = 0.0
                te_list.append(te)
            elif i.Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Trainee_ID
                te.unit_id = unit_st + " Trainee"
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Trainee_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " WC"
                    te.hours_rec = 0.0
                te_list.append(te)
            elif i.Observer:
                te = common.TimeEntry()
                te.user_id = i.Observer
                te.unit_id = unit_st + " Observer"
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                te.hours_rec = float(i.Observer_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " WC"
                    te.hours_rec = 0.0
                te_list.append(te)
        return te_list

    def get_dispatch_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both satart and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT Shift_Start, Watch_ID, Shift_Number,
                Dispatcher1_ID, Dispatcher1_Hours,
                Dispatcher2_ID, Dispatcher2_Hours
            FROM Dispatcher_Log
            WHERE Watch_ID BETWEEN """ + s_watch_st + """
                AND """ + e_watch_st
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            if i.Dispatcher1_ID:
                te = common.TimeEntry()
                te.user_id = i.Dispatcher1_ID
                te.unit_id = "Dispatcher"
                te.service_date = i.Shift_Start
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                if i.Dispatcher2_ID:
                    te.unit_id = "Dispatcher Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Dispatcher1_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = "Dispatcher WC"
                    te.hours_rec = 0.0
                te_list.append(te)
            elif i.Dispatcher2_ID:
                te = common.TimeEntry()
                te.user_id = i.Dispatcher2_ID
                te.unit_id = "Dispatcher Trainee"
                te.service_date = i.Shift_Start
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Dispatcher2_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = "Dispatcher WC"
                    te.hours_rec = 0.0
                te_list.append(te)
        return te_list

    def get_ic_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both satart and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT InService_DateTime, IC_Number,
                Watch_ID, Shift_Number,
                Monitor_ID, Monitor_Hours,
                Trainee_ID, Trainee_Hours
            FROM IC_Details
            WHERE Watch_ID BETWEEN """ + s_watch_st + """
                AND """ + e_watch_st
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_dt = self.cmn.convert_watch_date(
                i.Watch_ID, i.Shift_Number)

            unit_st = "Unknown IC"
            if i.IC_Number == 1:
                unit_st = "Rampart IC"
            elif i.IC_Number == 2:
                unit_st = "Lake Meade IC"
            elif i.IC_Number == 3:
                unit_st = "Sun City IC"

            if i.Monitor_ID:
                te = common.TimeEntry()
                te.user_id = i.Monitor_ID
                te.unit_id = unit_st
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Monitor_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " WC"
                    te.hours_rec = 0.0
                te_list.append(te)
            elif i.Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Trainee_ID
                te.unit_id = unit_st + " Trainee"
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Trainee_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " WC"
                    te.hours_rec = 0.0
                te_list.append(te)
        return te_list

    def get_wc_date_range(self, s_date_d, e_date_d):
        """Return list of Watch Commanders who worked during a date range"""
        # Date range includes the start date and excludes the end date
        # (typical Python)

        # SQL between includes both satart and end dates so we addjust
        s_date_st = s_date_d.strftime(DATE_FORMAT_MSACCESS)
        e_date_st = (e_date_d - datetime.timedelta(days=1)).strftime(
            DATE_FORMAT_MSACCESS)

        sql_statement = """
            SELECT Watch_ID, Watch_Start, Watch_Number,
                Watch_Commander_ID, Watch_Commander_Trainee_ID
            FROM Watch_Commander_Log
            WHERE Watch_Start BETWEEN """ + s_date_st + """
                AND """ + e_date_st
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_dt = self.cmn.convert_watch_date(i.Watch_ID)

            if i.Watch_Commander_ID:
                te = common.TimeEntry()
                te.user_id = i.Watch_Commander_ID
                te.unit_id = "Watch Commander"
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = 0
                te.second_shift = False
                te.student = False
                te.instructor = False
                if i.Watch_Commander_Trainee_ID:
                    te.unit_id = "Watch Commander Trainer"
                    te.instructor = True
                te.hours_rec = 12.0
                te.hours_calc = 0.0
                te_list.append(te)
            elif i.Watch_Commander_Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Watch_Commander_Trainee_ID
                te.unit_id = "Watch Commander Trainee"
                te.service_date = start_dt
                te.watch_id = i.Watch_ID
                te.shift_number = 0
                te.second_shift = False
                te.student = True
                te.instructor = False
                te.hours_rec = 12.0
                te.hours_calc = 0.0
                te_list.append(te)

        return te_list

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
            name_dict[i.MemberID] = display_name(
                i.LastName, i.FirstName, i.PrefName)
        return name_dict

    def get_active_disp_users(self):
        """Return a dictionary with id:full_name"""

        sql_statement = """
            SELECT User_ID, User_Name
            FROM Users
            WHERE IsActive"""
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)
        name_dict = {}
        rows = self.curs_disp.fetchall()
        for i in rows:
#           (surname, givname, prefname) = parse_dispatch_name(i.User_Name)
#           name_dict[i.User_ID] = display_name_by_surname(
#               surname, givname, prefname)
            name_dict[i.User_ID] = i.User_Name
        return name_dict

    def get_full_name(self, user_ids):
        """Return a dictionary with id:full_name"""

        key_list = ""
        for i in user_ids:
            key_list += "'" + str(i) + "', "
        sql_statement = """
            SELECT User_ID, User_Name
            FROM Users
            WHERE User_ID IN (""" + key_list + ")"
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)
        name_dict = {}
        rows = self.curs_disp.fetchall()
        for i in rows:
            if not i.User_Name:
                full_Name = i.User_ID.strip()
            else:
                (sname, gname, pname
                    ) = parse_dispatch_name(i.User_Name)
                full_name = display_name_by_surname(
                    sname, gname, pname)
            name_dict[i.User_ID] = full_name
        return name_dict

    def open_dispatch_db(self):
        """Open Database used by Dispatch and WC logging applications"""

        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.cmn.stns.get_pathname_dispatch_db() + r';')
        logging.info("    connected to %s", conn_str)
        self.conn_disp = pyodbc.connect(conn_str)
        self.curs_disp = self.conn_disp.cursor()

    def open_member_db(self):
        """Open Database used by Dispatch and WC logging applications"""

        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.cmn.stns.get_pathname_member_db() + r';')
        logging.info("    connected to %s", conn_str)
        self.conn_member = pyodbc.connect(conn_str)
        self.curs_member = self.conn_member.cursor()


if __name__ == '__main__':
    cmn = common.Common()
    d = Data(cmn)

    d.open_dispatch_db()
    print()
    print('Dispatch DB')
    print('### Tables:')
    for i in d.curs_disp.tables(tableType='TABLE'):
        print(i.table_name)
    print('### Views:')
    for i in d.curs_disp.tables(tableType='VIEW'):
        print(i.table_name)

    d.open_member_db()
    print()
    print('Member DB')
    print('### Tables:')
    for i in d.curs_member.tables(tableType='TABLE'):
        print(i.table_name)
    print('### Views:')
    for i in d.curs_member.tables(tableType='VIEW'):
        print(i.table_name)
