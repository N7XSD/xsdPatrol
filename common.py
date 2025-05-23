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
import io
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


class DispatchDbReports():
    """Import form Dispatch DB and create reports"""

    def dispatch_db_hours(self, cmn, output, start_d, end_d):
        """Return a StringIO object conaining an HTML reports showing
           hours recoreded between dates in the dispatch DB"""

        time_dict = {}
        te_list = cmn.dat.get_wc_date_range(start_d, end_d)
        (watch_id_start, watch_id_end) = cmn.get_watch_range(te_list)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_dispatch_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_car_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        te_list = cmn.dat.get_ic_by_watch(watch_id_start, watch_id_end)
        cmn.add_time_entries(time_dict, te_list)

        output.write('<html>\n')
        output.write('<body>\n')
        output.write('<h1>Dispatch Log Hours Extract</h1>\n')
        output.write(f'<h2>From {start_d} to {end_d}</h2>\n')

        name_dict = cmn.dat.get_full_name(time_dict.keys())
        for i in sorted(name_dict, key=name_dict.get):
            output.write(f'<p>{name_dict[i]} ({i})</p>')
            total_rec = 0.0
            output.write('<table>')
            output.write(f'<tr><th>Hours</th>'
                + f'<th>Activity</th></tr>')
            for j in sorted(time_dict[i]):
                total_rec += j.hours_rec
                output.write(f'<tr><td style="text-align:right">'
                    + f'{j.hours_rec}</td>'
                    + f'<td>{j.unit_id}</td></tr>')
            output.write(f'<tr><td style="text-align:right">{total_rec}</td>'
                + f'<td>TOTAL</td></tr>')
            output.write('</table>')

        output.write('</body>\n')
        output.write('</html>')


class TimeEntry():
    user_id = ""
    unit_id = ""
    service_date = None
    watch_id = 0
    shift_number = 0
    second_shift = False
    student = False
    instructor = False
    hours_rec = 0.0
    hours_calc = 0.0

    def __str__(self, other):
        return (
            f"{self.user_id:12}"
            f" {self.watch_id}"
            f" {self.shift_number}"
            f" {self.hours_calc}")

    def __hash__(self):
        return hash(user_id, unit_id, service_date, watch_id,
            shift_number)

    def __eq__(self, other):
        return self.service_date == other.service_date

    def __lt__(self, other):
        return self.service_date < other.service_date


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

#       FIXME: Mess with the date just for testing
#       self.app_start_time_dt = datetime.datetime(
#           year=2024, month=3, day=20)
        self.app_start_time_dt -= datetime.timedelta(days=365)

        self.stns = settings.Settings()
        self.dat = data.Data(self)
        self.dat.open_dispatch_db()

    def add_time_entries(self, time_dict, te_list):
        """Add a time recored to a user.  A new user is created,
        if needed"""
        for i in te_list:
            if i.user_id in time_dict:
                time_dict[i.user_id].append(i)
            else:
                time_dict[i.user_id] = [i]

    def get_hours(self, start_d, end_d):
        """Return a list of TimeEntry objects for the date range"""
        self.dat.get_wc_date_range(start_d, end_d)

    def get_last_work_week(self, date_d):
        """Returns datetime.date objects for first day of @date_d work
        week and the first day of the following week"""

        start_d = get_work_week_start_d(date_d)
        end_d = start_d + datetime.timedelta(weeks=1)
        return (start_d, end_d)

    def get_watch_range(self, te_list):
        """Return smallest range of watches that includes all TimeEntry
        objects in te_list"""

        if te_list:
            max_watch = min_watch = te_list[0].watch_id
            for i in te_list:
                max_watch = max(max_watch, i.watch_id)
                min_watch = min(min_watch, i.watch_id)
            max_watch += 1      # It's a Python thing
        else:
            min_watch = max_watch = None
        return min_watch, max_watch
