"""
xsdPatrol common classes and functions
"""

# These classes are mostly sacks of attributes
#pylint: disable=too-few-public-methods
#pylint: disable=too-many-arguments
#pylint: disable=too-many-boolean-expressions
#pylint: disable=too-many-branches
#pylint: disable=too-many-instance-attributes

import datetime
import logging
import os
import platform
import sys

import data
import settings

def calc_earned_hours(watch_num, shift_num, second_shift=False,
        student=False, instructor=False):
    """Returns earned hours for a shift
        This is very specific to Sun City Summerlin Security Patrol.
        Anyone else probably just wants to return the number of
        hours in a shift"""
    if student:
        return 4
    if watch_num == 0 and shift_num == 0:
        hours = 10
    elif watch_num == 0 and shift_num == 1:
        hours = 10
    elif watch_num == 0 and shift_num == 2:
        hours = 4
        if second_shift:
            hours += 2
    elif watch_num == 1 and shift_num == 0:
        hours = 4
        if second_shift:
            hours += 2
    elif watch_num == 1 and shift_num == 1:
        hours = 4
        if second_shift:
            hours += 2
    elif watch_num == 1 and shift_num == 2:
        hours = 7
        if second_shift:
            hours += 2
    else:
        # We should never get here but if we do,
        # give the user a funny looking number rather
        # than stopping the program
        logging.debug("""common.calc_earned_hours()
                unable to calculate hours correctly.
                Method returned 88 instead.""")
        return 88
    if instructor:
        hours += 4
    return hours


def get_console_name():
    """Return the console ID"""

    # The assumption here is that we have only one dispatcher
    # on a computer and can use the node name for a console ID
    fqd_name = platform.node()
    host_name = fqd_name.partition(".")[0]
    return host_name


def get_work_week_start_d(date_d):
    """Return a date object for the first day of the work for date"""
    first_day = 0       # Work week starts on Sunday
    earlier_td = datetime.timedelta(
        days=first_day + date_d.weekday() + 1)
    start_day_d = date_d - earlier_td
    return start_day_d


def init_logging():
    """Initialize logging

       Logging is what the program does to keep track of it's own
       progress.  Not to be confused with the log the program is
       intended to manage.  Dot those i's and cross those t's."""

    logging.basicConfig(format='%(levelname)s:%(message)s',
            filename=settings.LOGGING_FILE, encoding="utf-8",
            filemode="w", level=settings.LOGGING_LEVEL)
    logging.info("%s  %s", settings.ID_NAME, settings.ID_VER)
    logging.info(datetime.datetime.now().isoformat(" ", "seconds"))
    if os.name == "posix":
        logging.info(os.uname())
    elif os.name == "nt":
        logging.info(sys.getwindowsversion())
    else:
        logging.info("Running on %s", os.name)


class Common():
    """
    A collection of objects to pass around to various user interfaces
    (windows, etc.)
    """
    UNK = 0

    JOB_IDS = ["Unknown",
        "Dispatcher", "Disp. Trainee",
        "Driver", "Driver Trainee",
        "IC Officer", "IC Trainee",
        "Observer",
        "Watch Commander", "WC Trainee"]
    JOB_IDS_SHORT = ["UNK", "DI", "DIT", "DR", "DRT", "IC", "ICT",
        "OBS", "WC", "WCT"]
    DI = 1
    DIT = 2
    DR = 3
    DRT = 4
    IC = 5
    ICT = 6
    OBSERVER = 7
    WC = 8
    WCT = 9

    PLACE_MOBILITY = ["Unknown", "Fixed", "Portable", "Mobile"]
    FIXED = 1       # Does not move (i.e. a house)
    PORTABLE = 2    # Can be moved but is usually used from
                    # a single location (i.e. a travel trailer)
    MOBILE = 3      # Spends most of its service time moving (i.e. a car)

    RATINGS_1_5 = ["1 - Very Poor", "2", "3", "4", "5 - Very Good"]

    def __init__(self):
        logging.debug("Init common.Common")
        self.app_start_time_dt = datetime.datetime.now()
        self.app_start_time_dt = datetime.datetime(
            year=2024, month=3, day=20) #FIXME: Just for testing
        self.stns = settings.Settings()
        self.dat = data.Data(self)
