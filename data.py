"""
A place to keep data
"""

import pyodbc

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


class TimeEntry():
    user_id = ""
    unit_id = ""
    service_date = None
    watch_number = 0
    shift_number = 0
    second_shift = False
    student = False
    instructor = False
    hours_rec = 0
    hours_calc = 0

    def __str__(self):
        return f"{self.user_id} {self.hours_calc}"


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

    def get_car_hours(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""
        # Table:  Car_Details
        # Match:  Watch_ID
        # Return fields:
        #     Watch_Number, Shift_Number, Car_Number, Driver1_ID,
        #     Driver1_Hours,  Driver2_ID, Driver2_Hours, Trainee_ID,
        #     Trainee_Hours, Observer, Observer_Hours

    def get_dispatch_hours(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""
        # Table:  Dispatcher_Log
        # Match:  Watch_ID
        # Return fields:
        #     Watch_Number, Shift_Number, Dispatcher1_ID,
        #     Dispatcher1_Hours,  Dispatcher2_ID, Dispatcher2_Hours

    def get_ic_hours(self, s_watch, e_watch):
        """Return list of TimeEntry for watches in range."""
        # Table:  IC_Details
        # Match:  Watch_ID
        # Return fields:
        #     Watch_Number, Shift_Number, IC_Number, Monitor_ID,
        #     Monitor_Hours,  Trainee_ID, Trainee_Hours

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
            WHERE Watch_Start between """ + s_date_st + """
                and """ + e_date_st
#       print(sql_statement)
#       print()
        self.curs_disp.execute(sql_statement)

        te_list = []
        rows = self.curs_disp.fetchall()
        for i in rows:
            if i.Watch_Commander_ID:
                te = TimeEntry()
                te.user_id = i.Watch_Commander_ID
                te.unit_id = ""
                te.service_date = i.Watch_Start
                te.watch_number = i.Watch_Number
                te.shift_number = 0
                te.second_shift = False
                te.student = False
                te.instructor = False
                if i.Watch_Commander_Trainee_ID:
                    te.instructor = True
                te.hours_rec = 12
                te.hours_calc = 12
                te_list.append(te)
            elif i.Watch_Commander_Trainee_ID:
                te = TimeEntry()
                te.user_id = i.Watch_Commander_Trainee_ID
                te.unit_id = ""
                te.service_date = i.Watch_Number
                te.watch_number = i.Watch_Start
                te.shift_number = 0
                te.second_shift = False
                te.student = True
                te.instructor = False
                te.hours_rec = 12
                te.hours_calc = 12
                te_list.append(te)
#       for i in te_list:
#           print(i)

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
