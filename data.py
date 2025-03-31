"""
A place to keep data
"""

import pyodbc

import common
import datetime
import logging
import settings

DATE_FORMAT_MSACCESS = "#%m/%d/%Y#"


def display_name(last_name, first_name, pref_name):
    """Return the full name as a string"""
    if not pref_name or pref_name == first_name:
        name = f"{first_name} {last_name}"
    else:
        name = f'{first_name} "{pref_name}" {last_name}'
    return name


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
        logging.info("    connected to dispatch db \'%s\'",
            cmn.stns.pathname_dispatch_db)

    def get_car_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both satart and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT
                InService_Date, Car_Number, Watch_ID, Shift_Number,
                Driver1_ID,Driver1_Hours, Driver2_ID,Driver2_Hours,
                Trainee_ID, Trainee_Hours, Observer, Observer_Hours
            FROM
                Car_Details
            WHERE Watch_ID BETWEEN """ + s_watch_st + """
                and """ + e_watch_st
        print(sql_statement)
        print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            unit_st = "Car " + str(i.Car_Number)
            if i.Monitor_ID:
                te = common.TimeEntry()
                te.user_id = i.Monitor_ID
                te.unit_id = unit_st
                te.service_date = i.InService_Date
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Monitor_Hours)
                te_list.append(te)
            elif i.Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Trainee_ID
                te.unit_id = unit_st + " Trainee"
                te.service_date = i.InService_Date
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Trainee_Hours)
                te_list.append(te)
        return te_list

    def get_dispatch_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both satart and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT
                Shift_Start, Watch_ID, Shift_Number,
                Dispatcher1_ID,Dispatcher1_Hours,
                Dispatcher2_ID,Dispatcher2_Hours
            FROM
                Dispatcher_Log
            WHERE Watch_ID BETWEEN """ + s_watch_st + """
                and """ + e_watch_st
        print(sql_statement)
        print()
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
                te_list.append(te)
        return te_list

    def get_ic_by_watch(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""

        # SQL BETWEEN includes both satart and end dates so we addjust
        s_watch_st = str(s_watch)
        e_watch_st = str(e_watch - 1)

        sql_statement = """
            SELECT
                InService_Date, IC_Number,
                Watch_ID, Shift_Number,
                Monitor_ID,Monitor_Hours,
                Trainee_ID, Trainee_Hours
            FROM
                IC_Details
            WHERE Watch_ID BETWEEN """ + s_watch_st + """
                and """ + e_watch_st
        print(sql_statement)
        print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            unit_st = "Unknown IC"
            if IC_Number == 1:
                unit_st = "Rampart IC"
            elif IC_Number == 2:
                unit_st = "Lake Meade IC"
            elif IC_Number == 3:
                unit_st = "Sun City IC"

            if i.Monitor_ID:
                te = common.TimeEntry()
                te.user_id = i.Monitor_ID
                te.unit_id = unit_st
                te.service_date = i.InService_Date
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = False
                te.instructor = False
                if i.Trainee_ID:
                    te.unit_id = unit_st + " Trainer"
                    te.instructor = True
                te.hours_rec = float(i.Monitor_Hours)
                te_list.append(te)
            elif i.Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Trainee_ID
                te.unit_id = unit_st + " Trainee"
                te.service_date = i.InService_Date
                te.watch_id = i.Watch_ID
                te.shift_number = i.Shift_Number
                te.student = True
                te.instructor = False
                te.hours_rec = float(i.Trainee_Hours)
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
            SELECT
                Watch_ID, Watch_Start, Watch_Number,
                Watch_Commander_ID, Watch_Commander_Trainee_ID
            FROM
                Watch_Commander_Log
            WHERE Watch_Start BETWEEN """ + s_date_st + """
                and """ + e_date_st
        print(sql_statement)
        print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            if i.Watch_Commander_ID:
                te = common.TimeEntry()
                te.user_id = i.Watch_Commander_ID
                te.unit_id = "Watch Commander"
                te.service_date = i.Watch_Start
                te.watch_id = i.Watch_ID
                te.shift_number = 0
                te.second_shift = False
                te.student = False
                te.instructor = False
                if i.Watch_Commander_Trainee_ID:
                    te.unit_id = "Watch Commander Trainer"
                    te.instructor = True
                te.hours_rec = 12.0
                te.hours_calc = 12.0
                te_list.append(te)
            elif i.Watch_Commander_Trainee_ID:
                te = common.TimeEntry()
                te.user_id = i.Watch_Commander_Trainee_ID
                te.unit_id = "Watch Commander Trainee"
                te.service_date = i.Watch_Start
                te.watch_id = i.Watch_ID
                te.shift_number = 0
                te.second_shift = False
                te.student = True
                te.instructor = False
                te.hours_rec = 12.0
                te.hours_calc = 12.0
                te_list.append(te)

        return te_list

    def open_dispatch_db(self):
        """Open Database used by Dispatch and WC logging applications"""

        conn_str = (r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=' + self.cmn.stns.pathname_dispatch_db + r';')
        logging.info("    connected to %s", conn_str)
        self.conn_disp = pyodbc.connect(conn_str)
        self.curs_disp = self.conn_disp.cursor()
#       print('### Tables:')
#       for i in self.curs_disp.tables(tableType='TABLE'):
#           print(i.table_name)
#       print('### Views:')
#       for i in self.curs_disp.tables(tableType='VIEW'):
#           print(i.table_name)
