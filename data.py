"""
A place to keep data
"""

import datetime
import logging

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
#       self.con = sqlite3.connect(cmn.stns.db_pathname)
        logging.info("    connected to sqlite3 db \'%s\'",
            cmn.stns.db_pathname)
#       self.cur = self.con.cursor()

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

    def get_wc_date_range(self, s_date, e_date):
        """Return list of Watch Commanders who worked during a date range"""
        # Table: Watch_Commander_Log
        # Match:
        #     Watch_Start, Watch_end
        # Return fields:
        #     Watch_ID, Watch_Start, Watch_Commander_ID,
        #     Watch_Commander_Trainee_ID
