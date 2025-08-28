"""
A place to keep data
"""

import pyodbc

import common
import datetime
import logging
import settings

DATE_FORMAT_MSACCESS = "#%m/%d/%Y#"
MAXINT_MSACCESS = 2147483647
MININT_MSACCESS = -2147483648


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

    def get_activity_codes(self):
        """Return list of Activity Codes and Descriptions."""

        sql_statement = """
            SELECT Code, Description, IsActive
            FROM Activity_Codes"""
        self.curs_disp.execute(sql_statement)

        code_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            code_list.append([bool(i.IsActive), int(i.Code),
                str(i.Description)])
        return(code_list)

    def get_car_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both start and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT InService_DateTime, Car_Number, Watch_Number, Shift_Number,
                Driver1_ID, Driver1_Hours, Driver2_ID, Driver2_Hours,
                Trainee_ID, Trainee_Hours, Observer, Observer_Hours
            FROM Car_Details
            WHERE Watch_ID BETWEEN ? AND ?"""
#       print(sql_statement)
#       print(s_watch_st, e_watch_st)
#       print()
        self.curs_disp.execute(sql_statement, (s_watch_st, e_watch_st))

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_d, _, _ = self.cmn.normalize_shift_date(
                i.InService_DateTime)

            unit_st = "Car " + str(i.Car_Number)
            if i.Driver1_ID:
                te = common.TimeEntry()
                te.user_id = i.Driver1_ID
                te.unit_id = unit_st
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Driver1_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)

            if i.Driver2_ID:
                te = common.TimeEntry()
                te.user_id = i.Driver2_ID
                te.unit_id = unit_st
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Driver2_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)

            if i.Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Trainee_ID
                te.unit_id = unit_st + " Trainee"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Trainee_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)

            if i.Observer:
                te = common.TimeEntry()
                te.user_id = i.Observer
                te.unit_id = unit_st + " Observer"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = False
                te.instructor = False
                te.hours_rec = float(i.Observer_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)
        return te_list

    def get_dispatch_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both start and end values so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT Shift_Start, Watch_Number, Shift_Number,
                Dispatcher1_ID, Dispatcher1_Hours,
                Dispatcher2_ID, Dispatcher2_Hours
            FROM Dispatcher_Log
            WHERE Watch_ID BETWEEN ? AND ?"""
#       print(sql_statement)
#       print(s_watch_st, e_watch_st)
#       print()
        self.curs_disp.execute(sql_statement, (s_watch_st, e_watch_st))

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_d, _, _ = self.cmn.normalize_shift_date(i.Shift_Start)

            if i.Dispatcher1_ID:
                te = common.TimeEntry()
                te.user_id = i.Dispatcher1_ID
                te.unit_id = "Dispatcher"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = False
                te.instructor = False
                if i.Dispatcher2_ID:
                    te.unit_id = "Dispatcher Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Dispatcher1_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = "Dispatcher (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)

            if i.Dispatcher2_ID:
                te = common.TimeEntry()
                te.user_id = i.Dispatcher2_ID
                te.unit_id = "Dispatcher Trainee"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Dispatcher2_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = "Dispatcher Trainee (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)
        return te_list

    def get_events_list(self, code_list, start_date=None):
        """Return a list of events"""
        start_date = datetime.datetime.now() - datetime.timedelta(days=5)
        event_list = []
        placeholders = ", ".join(["?"] * len(code_list))
        sql_statement = """
            SELECT Item_ID, Watch_ID, Shift_Number, Activity_DateTime,
                Ten_Code, Activity_Source, Location, Description
            FROM Activities
            WHERE IsActive AND Activity_DateTime > ?
                AND Ten_Code IN (""" + placeholders + ")"
#       print(sql_statement)
#       print(start_date, list(code_list))
#       print()
        self.curs_disp.execute(sql_statement, [start_date] + code_list)
        rows = self.curs_disp.fetchall()
        for i in rows:
            event = common.Event()
            event.item_id = i.Item_ID
            event.watch_id = i.Watch_ID
            event.shift_number = i.Shift_Number
            event.time_dt = i.Activity_DateTime
            event.code = i.Ten_Code
            event.source = "unknown"
            if i.Activity_Source == 1:
                event.source = "DISPATCH"
            elif i.Activity_Source == 2:
                event.source = "WATCHDMDR"
            event.location = i.Location
            event.description = i.Description
            event_list.append(event)
        return event_list

    def get_ic_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both start and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT InService_DateTime, IC_Number,
                Watch_Number, Shift_Number,
                Monitor_ID, Monitor_Hours,
                Trainee_ID, Trainee_Hours
            FROM IC_Details
            WHERE Watch_ID BETWEEN ? AND ?"""
#       print(sql_statement)
#       print(s_watch_st, e_watch_st)
#       print()
        self.curs_disp.execute(sql_statement, (s_watch_st, e_watch_st))

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_d, _, _ = self.cmn.normalize_shift_date(
                i.InService_DateTime)

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
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Monitor_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)

            if i.Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Trainee_ID
                te.unit_id = unit_st + " Trainee"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = i.Shift_Number - 1
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Trainee_Hours)
                if te.hours_rec == 99.0:
                    te.unit_id = unit_st + " (no hours earned)"
                    te.hours_rec = 0.0
                te_list.append(te)
        return te_list

    def get_wc_date_range(self, s_date_d, e_date_d):
        """Return list of Watch Commanders who worked during a date range"""
        # Date range includes the start date and excludes the end date
        # (typical Python).

        # Ask the DB for one day of data either side of the range so we
        # can do a little date/time munging later in the code.
        s_date1_d = s_date_d - datetime.timedelta(days=1)

        sql_statement = """
            SELECT Watch_ID, Watch_Start, Watch_Number,
                Watch_Commander_ID, Watch_Commander_Trainee_ID
            FROM Watch_Commander_Log
            WHERE Watch_Start BETWEEN ? AND ?"""
#       print(sql_statement)
#       print(s_date1_d, e_date_d)
#       print()
        self.curs_disp.execute(sql_statement, (s_date1_d, e_date_d))

        watch_id_first = MAXINT_MSACCESS
        watch_id_last = MININT_MSACCESS
        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            start_d, _ = self.cmn.normalize_watch_date(i.Watch_Start)
            if start_d < s_date_d or start_d >= e_date_d:
                continue

            if i.Watch_Commander_ID:
                watch_id_first = min(watch_id_first, i.Watch_ID)
                watch_id_last = max(watch_id_last, i.Watch_ID)
                te = common.TimeEntry()
                te.user_id = i.Watch_Commander_ID
                te.unit_id = "Watch Commander"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = -1
                te.second_shift = False
                te.student = False
                te.instructor = False
                if i.Watch_Commander_Trainee_ID:
                    te.instructor = True
                te.hours_rec = 12.0
                te.hours_calc = 0.0
                te_list.append(te)

            if i.Watch_Commander_Trainee_ID:
                watch_id_first = min(watch_id_first, i.Watch_ID)
                watch_id_last = max(watch_id_last, i.Watch_ID)
                te = common.TimeEntry()
                te.user_id = i.Watch_Commander_Trainee_ID
                te.unit_id = "Watch Commander Trainee"
                te.service_date = start_d
                te.watch_number = i.Watch_Number - 1
                te.shift_number = -1
                te.second_shift = False
                te.student = True
                te.instructor = False
                te.hours_rec = 4.0
                te.hours_calc = 0.0
                te_list.append(te)

        return te_list, watch_id_first, watch_id_last + 1

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
            name_dict[i.User_ID] = i.User_Name
        return name_dict

    def get_full_name(self, user_ids):
        """Return a dictionary with id:full_name"""

        # Every User_ID with hours found in the DB is added to the name
        # dictionary with a value intended to get attention.
        # Names later found in the Users table are changed to something
        # nicer.
        name_dict = {}
        for i in sorted(user_ids):
            name_dict[i] = f"### unexpected User_ID={i}"
        placeholders = ", ".join(["?"] * len(user_ids))
        sql_statement = """
            SELECT User_ID, User_Name
            FROM Users
            WHERE User_ID IN (""" + placeholders + ")"
#       print(sql_statement)
#       print(list(user_ids))
#       print()
        self.curs_disp.execute(sql_statement, list(user_ids))
        rows = self.curs_disp.fetchall()
#       print(f'Recoreds retrieved: {len(rows)}')
        for i in rows:
            if not i.User_Name:
                full_Name = i.User_ID.strip()
            else:
                (sname, gname, pname
                    ) = parse_dispatch_name(i.User_Name)
                full_name = display_name_by_surname(
                    sname, gname, pname)
            name_dict[i.User_ID] = full_name
#       for i, j in sorted(name_dict.items()):
#           print(f"{i}: {j}")
        return name_dict

    def get_responder_list(self):
        """Ugly stub that returns a responder list."""

        # FIXME: this should come from a DB table
        ugly_list = [
            "Watch Commander",
            "Driver",
            "Law Enforcement",
            "Fire + Rescue",
            "Ambulance"]
        resp_list = []
        for i, name in enumerate(ugly_list):
            resp = common.Responder()
            resp.resp_id = i
            resp.sort_index = i
            resp.name = str(name)
            resp_list.append(resp)
        return(resp_list)

    def open_dispatch_db(self):
        """Open Database used by Dispatch and WC logging applications"""

        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.cmn.stns.get_pathname_dispatch_db() + r';'
            r'Mode=Read;')
        logging.info("    connected to %s", conn_str)
        self.conn_disp = pyodbc.connect(conn_str)
        self.curs_disp = self.conn_disp.cursor()

    def open_member_db(self):
        """Open Database used by Brian Dodd's applications"""

        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.cmn.stns.get_pathname_member_db() + r';'
            r'Mode=Read;')
        logging.info("    connected to %s", conn_str)
        self.conn_member = pyodbc.connect(conn_str)
        self.curs_member = self.conn_member.cursor()

    def open_patrol_db(self):
        """Open Database used by xsdPatrol applications"""

        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.cmn.stns.get_pathname_patrol_db() + r';'
            r'Mode=Write;')
        logging.info("    connected to %s", conn_str)
        self.conn_patrol = pyodbc.connect(conn_str)
        self.curs_patrol = self.conn_patrol.cursor()

    def save_ticket(self, ticket):
        """This is where we put the ticket back in the DB.  This could
        be a new or existing record."""

        if ticket.ticket_id is None:
             sql_statement = """
                 INSERT INTO Ticket
                     (ID_Event, State, Open, Address, Cones_Used)
                 VALUES (?, ?, ?, ?, ?)"""
#            print(sql_statement)
#            print(ticket.initial_event.item_id, ticket.ticket_state,
#                ticket.open_dt, ticket.address, ticket.cones_used)
#            print()
             self.curs_patrol.execute(sql_statement,
                (ticket.initial_event.item_id, ticket.ticket_state,
                 ticket.open_dt, ticket.address, ticket.cones_used))
             self.conn_patrol.commit()
        else:
             sql_statement = """
                 UPDATE Ticket
                 SET State = ?, Open = ?, Address = ?, Cones_Used = ?)
                 WHERE ID = ?"""
             self.curs_patrol.execute(sql_statement,
                (ticket.ticket_state, ticket.open_dt, ticket.address,
                 ticket.cones_used, ticket.ticket_id))
#            print(sql_statement)
#            print(ticket.ticket_state, ticket.open_dt, ticket.address,
#                ticket.cones_used, ticket.ticket_id)
#            print()
             self.conn_patrol.commit()

#       print("SAVE TICKET")
#       print(f"ticket_id = {ticket.ticket_id}")
#       print(f"ticket_state = {ticket.ticket_state}")
#       print(f"open_dt = {ticket.open_dt}")
#       print(f"address = {ticket.address}")
#       print(f"responders = {ticket.responders}")
#       print(f"cones_used = {ticket.cones_used}")
#       print(f"initial_event.code = {ticket.initial_event.code}")
#       print(f"initial_event.description = {ticket.initial_event.description}")
#       print(f"folowup_events = {ticket.folowup_events}")
#       print()


if __name__ == '__main__':
    cmn = common.Common()
    d = Data(cmn)

#   d.open_dispatch_db()
#   print()
#   print('Dispatch DB')
#   print('### Tables:')
#   for i in d.curs_disp.tables(tableType='TABLE'):
#       print(i.table_name)
#   print('### Views:')
#   for i in d.curs_disp.tables(tableType='VIEW'):
#       print(i.table_name)

#   d.open_member_db()
#   print()
#   print('Member DB')
#   print('### Tables:')
#   for i in d.curs_member.tables(tableType='TABLE'):
#       print(i.table_name)
#   print('### Views:')
#   for i in d.curs_member.tables(tableType='VIEW'):
#       print(i.table_name)

    d.open_patrol_db()
    print()
    print('Patrol DB')
    print('### Tables:')
    for i in d.curs_patrol.tables(tableType='TABLE'):
        print(i.table_name)
    print('### Views:')
    for i in d.curs_patrol.tables(tableType='VIEW'):
        print(i.table_name)
